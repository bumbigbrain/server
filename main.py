
from fastapi import FastAPI
from minio import Minio
from dotenv import load_dotenv
import subprocess
import psycopg2
import os
import uvicorn

load_dotenv()

primary_endpoint = os.getenv("PRIMARY_DB_ENDPOINT")
primary_db_user = os.getenv("PRIMARY_DB_USER", "postgres")
primary_db_password = os.getenv("PRIMARY_DB_PASSWORD", "postgres")
primary_db_name = os.getenv("PRIMARY_DB_NAME")

secondary_endpoint = os.getenv("SECONDARY_DB_ENDPOINT")
secondary_db_user = os.getenv("SECONDARY_DB_USER", "postgres")
secondary_db_password = os.getenv("SECONDARY_DB_PASSWORD", "postgres")
secondary_db_name = os.getenv("SECONDARY_DB_NAME")


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

def create_connection_and_table(host, user, password, dbname):

    try:
        conn = psycopg2.connect(
            host=host,
            user=user,
            password=password,
            dbname=dbname,
            connect_timeout=5
        )

        print(f"connected to {host}")
    except:
        print(f"error while connecting to {host}")

    return conn


# Connect and create table in primary database
primary_conn = create_connection_and_table(
    primary_endpoint, primary_db_user, primary_db_password, primary_db_name
)

# Connect and create table in secondary database
secondary_conn = create_connection_and_table(
    secondary_endpoint, secondary_db_user, secondary_db_password, secondary_db_name
)




def is_connected_to_db(db: str = None):
    conn = primary_conn if db == "primary" else secondary_conn
    try:
        res = ""
        with conn.cursor() as cur:
            cur.execute("SELECT 1;")
            res = cur.fetchone()

        if res[0] != 1:
            return False
    except:
        return False
    
    return True


app = FastAPI()

@app.get("/hello-world")
async def helloWorld(student_id: str = None):

    if student_id is None:
        return {"message": "Please identify your student_id"}
        
    
    file_path = f"{student_id}_server-connection_1"
    # Create the file
    with open(file_path, 'w') as f:
        pass  # just create an empty file

    print(f"{file_path} created successfully!")

    client.fput_object(
        bucket_name,
        f"check_dir/{file_path}",
        file_path,
    )

    print("File uploaded successfully!")
    
    return {"message":"Hello World!!"}


@app.get("/test-primary")
async def testPrimary(student_id: str = None):
    
    if student_id is None:
        return {"message": "Please identify your student_id"}
    
    if is_connected_to_db("primary"):
        file_path = f"{student_id}_primary-connection_1"
        # Create the file
        with open(file_path, 'w') as f:
            pass  # just create an empty file

        print(f"{file_path} created successfully!")

        client.fput_object(
            bucket_name,
            f"check_dir/{file_path}",
            file_path,
        )

        print("File uploaded successfully!")
        
        return {"message": "Ping Primary DB Successfully."}
    else:
        return {"message":"Can not connect to Primary DB."}
    

@app.get("/test-secondary")
async def testSecondary(student_id: str = None):
    
    if student_id is None:
        return {"message": "Please identify your student_id"}
    
    if is_connected_to_db("secondary"):
        file_path = f"{student_id}_secondary-connection_1"
        # Create the file
        with open(file_path, 'w') as f:
            pass  # just create an empty file

        print(f"{file_path} created successfully!")

        client.fput_object(
            bucket_name,
            f"check_dir/{file_path}",
            file_path,
        )

        print("File uploaded successfully!")
        
        return {"message": "Ping Secondary DB Successfully."}
    else:
        return {"message": "Cannot connect to Secondary DB."}
    


@app.get("/test-load")
async def testLoad(time_out_min: str = 1):
    # Basic stress-ng command

    time_out_sec = int(time_out_min * 60)
    command = [
        "stress-ng",
        "--cpu", "4",         # 4 CPU workers
        "--cpu-load", "80",    # 80% load
        "--timeout", f"{time_out_sec}s"     # Run for 60 seconds
    ]

    # Run the command
    try:
        subprocess.run(command, check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error running stress-ng: {e}")


@app.get("/check-autoscaling")
async def checkAutoscaling(student_id: str = None):
    
    if student_id is None:
        return {"message": "Please identify your student_id"}
    
    bucket_name = "my-bucket"

    # List and count objects
    count = 0
    for obj in client.list_objects(bucket_name, recursive=True):
        splited_object_name = obj.object_name.split("/")
        dir = splited_object_name[0]  
        if dir != "test_dir":
            continue
        count += 1
    
    if count > 1:
        file_path = f"{student_id}_auto-scaling_1"
        # Create the file
        with open(file_path, 'w') as f:
            pass  # just create an empty file

        print(f"{file_path} created successfully!")

        client.fput_object(
            bucket_name,
            f"check_dir/{file_path}",
            file_path,
        )

        print("File uploaded successfully!")
        

@app.get("/scores")
async def checkScore(student_id: str = None):
    
    if student_id is None:
        return {"message": "Please identify your student_id"}
    
    bucket_name = "my-bucket"

    res = {
        f"{student_id}": {
            "server-connection": 0,
            "primary-connection": 0,
            "secondary-connection": 0,
            "auto-scaling": 0
        }
    }
     
    # List objects
    for obj in client.list_objects(bucket_name, recursive=True):
        splited_object_name = obj.object_name.split("/")
        dir = splited_object_name[0]  
        if dir != "check_dir":
            continue
        
        object_name = splited_object_name[1].split("_")
        topic = object_name[1]
        res[student_id][topic] = 1
        
            
    return res

