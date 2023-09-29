import os
import requests
import hashlib
import json
import difflib

# Function to download a file and save it to the 'db/' folder
def download_file(url):
    response = requests.get(url)
    if response.status_code == 200:
        file_name = os.path.join('db', os.path.basename(url))
        with open(file_name, 'wb') as file:
            file.write(response.content)
        return file_name
    else:
        return None

# Function to calculate the SHA-256 hash of a file
def calculate_hash(file_name):
    hasher = hashlib.sha256()
    with open(file_name, 'rb') as file:
        while True:
            data = file.read(65536)  # Read in 64k chunks
            if not data:
                break
            hasher.update(data)
    return hasher.hexdigest()

# Function to compare file sizes and update the JSON file
def update_json(file_info):
    json_file = 'db/files_info.json'
    if os.path.exists(json_file):
        with open(json_file, 'r') as f:
            data = json.load(f)
    else:
        data = {}

    for url, size in file_info.items():
        if url in data and data[url] != size:
            print(f"File '{url}' has changed in size!")
        data[url] = size

    with open(json_file, 'w') as f:
        json.dump(data, f, indent=4)

# List of URLs to process
urls = [
    "https://jacob2020baklas.github.io/test/testjsmon.js",
    "https://jacob2020baklas.github.io/test/",
    "https://example.com/",
]

file_info = {}

for url in urls:
    if url.endswith('.js'):
        file_name = download_file(url)
        if file_name:
            file_info[url] = os.path.getsize(file_name)
    else:
        response_file = download_file(url)
        if response_file:
            file_info[url] = os.path.getsize(response_file)

update_json(file_info)