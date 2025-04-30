import os
import requests
from urllib.parse import quote

# Configuration
CATEGORIES = {
    "clothing": "Traditional clothing of Bangladesh",
    "festival": "Festivals in Bangladesh",
    "rural_life": "Rural life in Bangladesh",
    "food": "Bangladeshi cuisine",
    "folk_art": "Bangladeshi folk art",
    "architecture": "Architecture of Bangladesh"
}
IMAGES_PER_CATEGORY = 50
OUTPUT_DIR = "gen-cv-dataset/images"
USER_AGENT = "GenCVProjectBot/1.0 (your_email@example.com)"

def fetch_image_urls(category_name, max_images):
    search_url = "https://commons.wikimedia.org/w/api.php"
    params = {
        "action": "query",
        "generator": "search",
        "gsrsearch": category_name,
        "gsrlimit": max_images,
        "prop": "imageinfo",
        "iiprop": "url",
        "format": "json"
    }
    headers = {"User-Agent": USER_AGENT}
    response = requests.get(search_url, params=params, headers=headers)
    data = response.json()
    image_urls = []
    pages = data.get("query", {}).get("pages", {})
    for page in pages.values():
        image_info = page.get("imageinfo", [])
        if image_info:
            image_urls.append(image_info[0]["url"])
    return image_urls

def download_images(category, urls):
    category_path = os.path.join(OUTPUT_DIR, category)
    os.makedirs(category_path, exist_ok=True)
    for idx, url in enumerate(urls):
        try:
            response = requests.get(url, headers={"User-Agent": USER_AGENT})
            if response.status_code == 200:
                file_extension = os.path.splitext(url)[1]
                file_name = f"{category}_{idx+1}{file_extension}"
                file_path = os.path.join(category_path, file_name)
                with open(file_path, "wb") as f:
                    f.write(response.content)
                print(f"Downloaded: {file_path}")
        except Exception as e:
            print(f"Failed to download {url}: {e}")

def main():
    for category, search_term in CATEGORIES.items():
        print(f"Processing category: {category}")
        urls = fetch_image_urls(search_term, IMAGES_PER_CATEGORY)
        download_images(category, urls)

if __name__ == "__main__":
    main()
