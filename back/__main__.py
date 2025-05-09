import subprocess
import os

if not os.path.exists("apollo"):
    print("Creating apollo directory...")
    os.makedirs("apollo")
else:
    print("Apollo directory already exists.")

if not os.path.exists("apollo/people"):
    print("Creating apollo/people directory...")
    os.makedirs("apollo/people")
else:
    print("Apollo/people directory already exists.")

if not os.path.exists("apollo/organizations"):
    print("Creating apollo/organizations directory...")
    os.makedirs("apollo/organizations")
else:
    print("Apollo/organizations directory already exists.")

subprocess.run(["fastapi", "run", "./back/api.py", "--port", "8000"])