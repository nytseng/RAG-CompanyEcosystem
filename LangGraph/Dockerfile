FROM python:3.11-slim

ENV PYTHONUNBUFFERED=1

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container at /app
COPY requirements.txt .

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install torch --index-url https://download.pytorch.org/whl/cpu
RUN pip install sentence-transformers

# Copy the rest of the application's code
# Assumes your script is named 'main.py'
COPY weaviate_agent.py .

# Define the command to run your app
CMD ["python", "weaviate_agent.py"]