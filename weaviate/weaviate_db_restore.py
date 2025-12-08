import weaviate
from weaviate.classes.backup import BackupStorage\
from weaviate.classes.init import Auth, AdditionalConfig, Timeout

client = weaviate.connect_to_local(host="weaviate", port=8080, grpc_port=50051,
    additional_config=AdditionalConfig(
        timeout=Timeout(init=30, query=60, insert=120)  # Values in seconds
    ))
BACKUP_ID = "nvidia_split_1" # Must match the ID used for creation

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