import os
import requests
from pathlib import Path

# Create breeds folder if it doesn't exist
breeds_folder = "static/images/breeds"
Path(breeds_folder).mkdir(parents=True, exist_ok=True)

# Dog breed images with URLs and filenames (using different CDN)
dog_breeds = {
    "beagle.jpg": "https://dog.ceo/api/breed/beagle/images/random",
    "pug.jpg": "https://dog.ceo/api/breed/pug/images/random",
    "golden_retriever.jpg": "https://dog.ceo/api/breed/retriever/golden/images/random",
    "labrador.jpg": "https://dog.ceo/api/breed/labrador/images/random",
    "german_shepherd.jpg": "https://dog.ceo/api/breed/germanshepherd/images/random",
    "bulldog.jpg": "https://dog.ceo/api/breed/bulldog/english/images/random",
    "rottweiler.jpg": "https://dog.ceo/api/breed/rottweiler/images/random",
    "doberman.jpg": "https://dog.ceo/api/breed/doberman/images/random",
    "husky.jpg": "https://dog.ceo/api/breed/husky/images/random",
}

print("Downloading dog breed images from dog.ceo API...")

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
}

for filename, url in dog_breeds.items():
    try:
        # Get the JSON response to get the image URL
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code == 200:
            data = response.json()
            if data.get('status') == 'success':
                image_url = data.get('message')
                # Download the actual image
                img_response = requests.get(image_url, headers=headers, timeout=10)
                if img_response.status_code == 200:
                    filepath = os.path.join(breeds_folder, filename)
                    with open(filepath, 'wb') as f:
                        f.write(img_response.content)
                    print(f"✅ Downloaded: {filename}")
                else:
                    print(f"❌ Failed to download image for {filename}")
            else:
                print(f"❌ API error for {filename}")
        else:
            print(f"❌ Failed to fetch {filename} (Status: {response.status_code})")
    except Exception as e:
        print(f"❌ Error downloading {filename}: {str(e)}")

print("\n✅ Done! All images have been downloaded to static/images/breeds/")

