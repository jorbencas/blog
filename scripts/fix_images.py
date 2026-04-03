import os
import requests
from urllib.parse import urlparse

def validate_url(url):
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except Exception as e:
        print(f"URL validation error: {e}")
        return False


def process_file(file_path):
    if not os.path.isfile(file_path):
        print(f"File not found: {file_path}")
        return
    try:
        with open(file_path, 'r') as file:
            content = file.readlines()
            for line in content:
                url = line.strip()
                if validate_url(url):
                    response = requests.get(url)
                    if response.status_code == 200:
                        # Process the image or URL
                        print(f"Successfully processed: {url}")
                    else:
                        print(f"Failed to retrieve {url}: {response.status_code}")
                else:
                    print(f"Invalid URL: {url}")
    except Exception as e:
        print(f"Error processing file: {e}")


# Example usage:
# process_file('path_to_your_file.txt')