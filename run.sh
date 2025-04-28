#!/bin/bash

source venv/bin/activate

python3 onstart.py && uvicorn main:app --host 0.0.0.0
