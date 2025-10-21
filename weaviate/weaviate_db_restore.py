import weaviate
from weaviate.classes.backup import BackupStorage

client = weaviate.connect_to_local()
BACKUP_ID = "my_nvidia_rag_export_20251021" # Must match the ID used for creation

print(f"Starting restore for ID: {BACKUP_ID}...")

result = client.backup.restore(
    backup_id=BACKUP_ID,
    backend="filesystem",
    wait_for_completion=True
)

if result.status == "SUCCESS":
    print(f"✅ Restore successful! Data is now available.")
else:
    print(f"❌ Restore failed. Status: {result.status}")
    
client.close()