#!/bin/bash

#!/bin/bash
set -e  # Exit on any error

# Create and activate virtual environment
python3 -m venv venv
source venv/bin/activate

# Install requirements
pip install -r requirements.txt

