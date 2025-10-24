# Weaviate RAG Demo Setup Guide

This guide outlines the steps to set up the Weaviate vector database, ingest the NVIDIA article data (using Hugging Face's `all-MiniLM-L6-v2` embeddings), and run similarity searches using LangChain.

## Prerequisites

Before starting, ensure you have the following installed and running:

1. **Docker:** Required to run the Weaviate instance.

2. **Python 3.8+:** With a virtual environment recommended.

3. **Dependencies:** Install the required Python packages (weaviate-client, langchain-weaviate, langchain-community, etc.).

```bash 
pip install weaviate-client langchain-weaviate langchain-community langchain-core langchain-text-splitters
```

4. **Data:** Ensure your scraped article data is available in the `nvidia_articles/` directory.

## Step 1: Start the Weaviate Database

You must start the Weaviate container before attempting to connect to it. The ingestion and query scripts are configured to connect to `http://localhost:8080`.

To start the database in the background:

```bash 
docker compose up -d
```

> **Note:** Wait a few moments for the container to fully initialize and become ready after running this command. Also make sure the volume is properly mounted so that you can create a backup.

## Step 2: Build the Database and Ingest Data

This step loads the articles, splits them into chunks, calculates the `all-MiniLM-L6-v2` embeddings, creates the Weaviate collection (`NvidiaNewsArticleHF`), and uploads the vectors.

Run your data ingestion script:

```bash 
python weaviate_db.py
```
or back up the current database (make sure the volume is mounted for weaviate_backups)

```bash
python weaviate_db_backup.py
```

or restore the previously built database

```bash
python weaviate_db_restore.py
```


## Step 3: Query the Vector Database

Once the ingestion is complete, you can use the retrieval script (`weaviate_query.py`) to perform vector similarity searches against your newly indexed data.

Run the query script:

```bash 
python weaviate_query.py
```
