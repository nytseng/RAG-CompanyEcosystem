import time
from langchain_core.callbacks import BaseCallbackHandler
from langchain_core.outputs import LLMResult
from langchain_core.messages import BaseMessage

class MetricsHandler(BaseCallbackHandler):
    def __init__(self):
        self.total_input_tokens = 0
        self.total_output_tokens = 0
        self.successful_requests = 0
        self.total_latency = 0.0
        self.start_time = 0.0

    def on_llm_start(self, serialized, prompts, **kwargs):
        self.start_time = time.perf_counter()

    def on_llm_end(self, response: LLMResult, **kwargs):
        end_time = time.perf_counter()
        self.total_latency += (end_time - self.start_time)
        self.successful_requests += 1

        # 1. Try Standard LangChain Usage Metadata (Preferred for 0.2+)
        # Structure: response.generations[0][0].message.usage_metadata
        try:
            if response.generations:
                first_gen = response.generations[0][0]
                # Check if it's a ChatGeneration with a message attribute
                if hasattr(first_gen, 'message') and hasattr(first_gen.message, 'usage_metadata'):
                    usage = first_gen.message.usage_metadata
                    # Usage might be None if the model didn't return it
                    if usage:
                        self.total_input_tokens += usage.get("input_tokens", 0)
                        self.total_output_tokens += usage.get("output_tokens", 0)
                        return # Found it, exit early
        except Exception as e:
            pass # Fallback if structure differs

        # 2. Fallback: Check global llm_output (Older versions/Ollama raw)
        if response.llm_output:
            # Ollama specific keys
            self.total_input_tokens += response.llm_output.get("prompt_eval_count", 0)
            self.total_output_tokens += response.llm_output.get("eval_count", 0)
            
            # OpenAI specific keys (sometimes mapped here)
            if "token_usage" in response.llm_output:
                usage = response.llm_output["token_usage"]
                self.total_input_tokens += usage.get("prompt_tokens", 0)
                self.total_output_tokens += usage.get("completion_tokens", 0)

    def report(self):
        print(f"\n--- 📊 PERFORMANCE METRICS ---")
        print(f"Total LLM Calls:      {self.successful_requests}")
        print(f"Total LLM Latency:    {self.total_latency:.2f}s")
        print(f"Total Input Tokens:   {self.total_input_tokens}")
        print(f"Total Output Tokens:  {self.total_output_tokens}")
        print(f"------------------------------\n")