import requests
import os
from pathlib import Path
from urllib.parse import urlparse
import csv


# Sample data in the format: ("sound type", "sound pack", "url")
# In a real application, you would load this from a CSV, database, or API.

data_array = []
with open("auxylib.csv", 'r', newline='', encoding='utf-8') as file:
    # Create a CSV reader object
    reader = csv.reader(file)
    # Skip the header row if present (optional)
    # next(reader, None) 
    # Iterate over each row and append it to the data list
    for row in reader:
        data_array.append(row)

print(data_array)

for sound_type, sound_pack, url in data_array:
    print(sound_type)
    print(sound_pack)
    print(url)

    # 1. Extract the filename from the URL
    
    parsed_url = urlparse(url)
    filename = Path(parsed_url.path).name

    print(parsed_url)
    print(filename)
        
    if not filename:
        print(f"Skipping URL: {url} - could not determine filename.")
        continue
        
    local_dir = Path("./" + sound_type + "/" + sound_pack)
    local_path = str(local_dir) + "/" + filename

    print(local_dir)
    print(local_path)
        
    # print("-" * 30)
    # print(f"Processing: Type='{sound_type}', Pack='{sound_pack}'")
    # print(f"URL: {url}")
        
    # 3. Download the file

    with requests.get(url, stream=True, timeout=10) as r:
        r.raise_for_status()  # Raise an exception for bad status codes (4xx or 5xx)
        
        # Create the directory if it doesn't exist
        local_dir.mkdir(parents=True, exist_ok=True)
        print(f"-> Downloading to: {local_path}")
        # Write the file content to the local file path
        with open(local_path, 'wb') as f:
            for chunk in r.iter_content(chunk_size=8192):
                f.write(chunk)