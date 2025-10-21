import weaviate
from weaviate.classes.backup import BackupStorage
from weaviate.classes.backup import BackupLocation


# 1. Connect to your local client
client = weaviate.connect_to_local()

# 2. Define a unique ID for your backup
BACKUP_ID = "my_nvidia_rag_export_20251021"

# 3. Start the backup process
print(f"Starting backup with ID: {BACKUP_ID}...")

try:
    result = client.backup.create(
        backup_id=BACKUP_ID,
        backend="filesystem", # Use the 'filesystem' backend
        include_collections=["NvidiaNewsArticleHF"], # Specify the collection(s) to back up
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