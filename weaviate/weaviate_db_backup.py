import weaviate
from weaviate.classes.backup import BackupStorage
from weaviate.classes.backup import BackupLocation
from weaviate.classes.init import Auth, AdditionalConfig, Timeout


# 1. Connect to your local client
client = weaviate.connect_to_local(host="localhost", port=8080, grpc_port=50051,
    additional_config=AdditionalConfig(
        timeout=Timeout(init=30, query=60, insert=120)  # Values in seconds
    ))

# 2. Define a unique ID for your backup
BACKUP_ID = "nvidia_final"

# 3. Start the backup process
print(f"Starting backup with ID: {BACKUP_ID}...")

try:
    result = client.backup.create(
        backup_id=BACKUP_ID,
        backend="filesystem", # Use the 'filesystem' backend
        include_collections=["ChunkedNvidiaTranscripts", "ChunkedNvidiaPublications", "ChunkedNvidiaArticles", "NvidiaTranscripts", "NvidiaPublications", "NvidiaArticles", "NvidiaInfo"], # Specify the collection(s) to back up
        wait_for_completion=True, # Wait until the process finishes before continuing
        backup_location=BackupLocation.FileSystem(path="/var/lib/weaviate/backups")
    )
    
    # Check the result status
    if result.status == "SUCCESS":
        print(f"✅ Backup successful! Status: {result}")
    else:
        print(f"❌ Backup failed or finished with status: {result.status}")

except Exception as e:
    print(f"An error occurred during backup: {e}")

client.close()