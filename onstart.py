from minio import Minio
from dotenv import load_dotenv
import socket
import os

load_dotenv()

minio_endpoint = os.getenv("MINIO_ENDPOINT")
minio_port = os.getenv("MINIO_PORT", "9001")
minio_access_key = os.getenv("MINIO_ACCESS_KEY")
minio_secret_key = os.getenv("MINIO_SECRET_KEY")


# Initialize the client
try:
    client = Minio(
        f"{minio_endpoint}:{minio_port}",       # MinIO server URL
        access_key=minio_access_key, # Your access key
        secret_key=minio_secret_key, # Your secret key
        secure=False             # True if using HTTPS
    )
    print("Connected to minio server.")
except:
    print("Cannot connect to minio server.")


# Check if a bucket exists
bucket_name = "my-bucket"
if not client.bucket_exists(bucket_name):
    client.make_bucket(bucket_name)


print(f"Bucket '{bucket_name}' is ready!")

hostname = socket.gethostname()
local_ip = socket.gethostbyname(hostname)

print(f"Local IP address: {local_ip}")

file_path = f"{local_ip}"

# Create the file
with open(file_path, 'w') as f:
    pass  # just create an empty file

print(f"{file_path} created successfully!")

client.fput_object(
    bucket_name,
    f"test_dir/{file_path}",
    file_path,
)

print("File uploaded successfully!")

