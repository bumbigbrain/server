
from fastapi import FastAPI
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

app = FastAPI()

@app.get("/hello-world")
async def helloWorld():
    return {"message":"Hello World!!"}



@app.get("/test-primary")
async def testPrimary():
    try:
        res = ""
        with primary_conn.cursor() as cur:
            cur.execute("SELECT 1;")
            res = cur.fetchone()

        if res[0] != 1:
            return "Cannot ping primary db"
    except:
        return "Cannot ping primary db"

    return "Ping primary db successfully"


@app.get("/test-secondary")
async def testSecondary():
    try:
        res = ""
        with secondary_conn.cursor() as cur:
            cur.execute("SELECT 1;")
            res = cur.fetchone()

        if res[0] != 1:
            return "Cannot ping secondary db"
    except:
        return "Cannot ping secondary db"

    return "Ping secondary db successfully"



@app.get("/test-load")
async def testLoad():
    # Basic stress-ng command
    command = [
        "stress-ng",
        "--cpu", "4",         # 4 CPU workers
        "--cpu-load", "80",    # 80% load
        "--timeout", "60s"     # Run for 60 seconds
    ]

    # Run the command
    try:
        subprocess.run(command, check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error running stress-ng: {e}")


