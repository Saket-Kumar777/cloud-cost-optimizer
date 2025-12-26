import json
import os

# Define the data directory relative to this file
# This ensures it finds 'data' even if you run the script from a different folder
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "data")

def ensure_data_dir():
    """Creates the data directory if it doesn't exist."""
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR)

def save_json(filename, data):
    """Saves a dictionary as a JSON file."""
    ensure_data_dir()
    filepath = os.path.join(DATA_DIR, filename)
    try:
        with open(filepath, 'w') as f:
            json.dump(data, f, indent=4)
        print(f"Saved: {filename}")
    except Exception as e:
        print(f"Error saving {filename}: {e}")

def load_json(filename):
    """Loads a JSON file and returns a dictionary."""
    filepath = os.path.join(DATA_DIR, filename)
    if os.path.exists(filepath):
        try:
            with open(filepath, 'r') as f:
                return json.load(f)
        except json.JSONDecodeError:
            print(f"Error: {filename} is not valid JSON.")
            return None
    print(f"File not found: {filename}")
    return None

def save_text(filename, text):
    """Saves a string to a text file."""
    ensure_data_dir()
    filepath = os.path.join(DATA_DIR, filename)
    try:
        with open(filepath, 'w') as f:
            f.write(text)
        print(f"Saved: {filename}")
    except Exception as e:
        print(f"Error saving {filename}: {e}")

def load_text(filename):
    """Loads a text file and returns a string."""
    filepath = os.path.join(DATA_DIR, filename)
    if os.path.exists(filepath):
        with open(filepath, 'r') as f:
            return f.read()
    return None