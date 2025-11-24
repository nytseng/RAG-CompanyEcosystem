# Source - https://stackoverflow.com/a
# Posted by datawookie
# Retrieved 2025-11-23, License - CC BY-SA 4.0

#!/bin/bash

# Start Ollama in the background.
/bin/ollama serve &
# Record Process ID.
pid=$!

# Pause for Ollama to start.
sleep 5

echo "🔴 Retrieve Gemma3 model..."
ollama pull gemma3
echo "🟢 Done!"

# Wait for Ollama process to finish.
wait $pid
