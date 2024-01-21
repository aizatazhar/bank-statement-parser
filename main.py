import subprocess
import json

if __name__ == "__main__":
    subprocess.call(["python", "parse.py"])
    with open("config.json", "r") as config_file:
        config = json.load(config_file)
    if "google sheets id" in config:
        subprocess.call(["python", "google_sheets.py"])