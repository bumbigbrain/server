## How the Application Starts

1. When the EC2 instance starts, `cloud-init` automatically runs the `user-data.sh` script.
2. The `user-data.sh` script performs the following:
   - Downloads and installs the required OS-level dependencies for the application.
   - Sets environment variables (ENV) necessary for accessing **MinIO** and **RDS PostgreSQL**.
3. The `user-data.sh` script then calls `setup.sh`, which handles downloading and installing the application-specific libraries.
4. Finally, `user-data.sh` runs:
   - `onstart.py` to test the connection to **MinIO**.
   - `main.py` to start the **FastAPI server**.

---

## What You Are Allowed to Modify

- You are allowed to modify `user-data.sh`, particularly to update ENV variables.
- You are allowed to pass `user-data.sh` as a user-data to launch EC2.




