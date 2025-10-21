import requests
import uuid
from sentence_transformers import SentenceTransformer
from qdrant_client import QdrantClient
from qdrant_client.http import models

# --- transcript_txt_to_vector functions ---

def get_all_txt_files_from_repo(owner, repo, start_path=""):
    txt_file_urls = []
    directories_to_visit = [start_path]
    while directories_to_visit:
        current_path = directories_to_visit.pop()
        api_url = f"https://api.github.com/repos/{owner}/{repo}/contents/{current_path}"
        try:
            response = requests.get(api_url)
            response.raise_for_status()
            for item in response.json():
                if item['type'] == 'dir':
                    directories_to_visit.append(item['path'])
                elif item['type'] == 'file' and item['name'].lower().endswith('.txt'):
                    txt_file_urls.append(item['download_url'])
        except requests.exceptions.RequestException as e:
            print(f"Error fetching contents from {api_url}: {e}")
    return txt_file_urls

def get_all_md_files_from_repo(owner, repo, start_path=""):
    md_file_urls = []
    directories_to_visit = [start_path]
    while directories_to_visit:
        current_path = directories_to_visit.pop()
        api_url = f"https://api.github.com/repos/{owner}/{repo}/contents/{current_path}"
        try:
            response = requests.get(api_url)
            response.raise_for_status()
            for item in response.json():
                if item['type'] == 'dir':
                    directories_to_visit.append(item['path'])
                elif item['type'] == 'file' and item['name'].lower().endswith('.md') and item['name'].lower() != "readme.md":
                    md_file_urls.append(item['download_url'])
        except requests.exceptions.RequestException as e:
            print(f"Error fetching contents from {api_url}: {e}")
    return md_file_urls

def extract_text_from_txt_url(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.text
    except requests.exceptions.RequestException as e:
        print(f"Error fetching TXT from {url}: {e}")
        return None

# --- NEW: Function to get already processed URLs from Qdrant ---
def get_processed_urls_from_qdrant(client, collection_name):
    """Fetches the 'source_url' from the payload of all existing points."""
    processed_urls = set()
    # Scroll through all points in the collection
    scrolled_points = client.scroll(
        collection_name=collection_name,
        with_payload=["source_url"], # Only fetch the source_url field
        limit=100 # Fetch in batches of 100
    )[0]
    
    for point in scrolled_points:
        if point.payload and 'source_url' in point.payload:
            processed_urls.add(point.payload['source_url'])
            
    return processed_urls

# --- 1. Initialize and ensure collection exists ---
print("Initializing model and Qdrant client...")
model = SentenceTransformer('all-MiniLM-L6-v2')
# Use a persistent local database
client = QdrantClient(path="./qdrant_db_COSINE") 

collection_name = "github_all_txt_documents"
vector_size = 384

# Use the new, safer method to create the collection if it doesn't exist
if not client.collection_exists(collection_name=collection_name):
    print(f"Collection '{collection_name}' does not exist. Creating now...")
    client.create_collection(
        collection_name=collection_name,
        vectors_config=models.VectorParams(size=vector_size, distance=models.Distance.COSINE),
    )
else:
    print(f"Collection '{collection_name}' already exists.")

# --- 2. LOGIC: Find which files are new ---
owner = "nytseng"
repo = "RAG-CompanyEcosystem"
start_path = "data"

# Get all files from the source (GitHub) change the helper function later
print("\nFetching all file URLs from GitHub...")
txt_source_urls = set(get_all_txt_files_from_repo(owner, repo, start_path))
md_source_urls = set(get_all_md_files_from_repo(owner, repo, start_path))
all_source_urls = txt_source_urls | md_source_urls
print(f"Found {len(all_source_urls)} total files in repo.")

############ test total files #############
# i = 1
# for x in sorted([x for x in all_source_urls]):
    
#     print(i ," : ", x)
#     i+=1
############ test total files #############

# Step 2b: Get all files already in our database (Qdrant)
print("Fetching processed file URLs from Qdrant...")
processed_urls = get_processed_urls_from_qdrant(client, collection_name)
print(f"Found {len(processed_urls)} files already in the database.")


urls_to_process = all_source_urls - processed_urls
print(f"Found {len(urls_to_process)} new file(s) to process.")

# Step 2c: Determine which files to process

# checked all the contentis correct for transcript txt file


# for i, url in enumerate(urls_to_process): 
#     text = extract_text_from_txt_url(url)
#     print("Processing: ", i, url)
#     print("Text: ", text)


# --- 3. PROCESSING: Ingest only the new files ---
if not urls_to_process:
    print("\nNo new files to add. Database is up to date! ✅")
else:
    print("\nStarting ingestion of new files...")
    for file_url in urls_to_process:
        print(f"Processing: {file_url.split('/')[-1]}")
        text = extract_text_from_txt_url(file_url)

        if text:
            vector = model.encode(text).tolist()
            client.upsert(
                collection_name=collection_name,
                points=[
                    models.PointStruct(
                        id=str(uuid.uuid4()),
                        vector=vector,
                        payload={"source_url": file_url}
                    )
                ],
                wait=True,
            )
            print(f"✅ Successfully added to collection.")
    print("\nIngestion complete!")