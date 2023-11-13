import os
import requests
import csv
import json
import time
from bs4 import BeautifulSoup
from urllib.parse import urlparse
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

# Function to fetch pages using Selenium and save them to a directory
def fetch_pages(input_file, output_dir):
    chrome_options = Options()
    chrome_options.add_experimental_option("excludeSwitches", ["enable-logging"])  # Suppress DevTools/USB logging

    # Initialize the Chrome WebDriver with options
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

    # Create a directory for page sources if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)

    urls = extract_urls_from_html(input_file)

    for index, url in enumerate(urls):
        driver.get(url)
        time.sleep(1)  # Wait for the page to load

        output_filename = os.path.join(output_dir, f'page_source_{index}.html')
        with open(output_filename, 'w', encoding='utf-8') as output_file:
            output_file.write(driver.page_source)

    driver.quit()

# Function to extract post URLs from an HTML file
def extract_urls_from_html(html_file):
    with open(html_file, 'r', encoding='utf-8') as file:
        soup = BeautifulSoup(file, 'html.parser')

    urls = []
    uploads_table = soup.find('h3', string='Uploads').find_next('table')
    for link in uploads_table.find_all('a'):
        urls.append(link.get('href'))

    return urls

# Function to fetch and process post details from an HTML file
def fetch_post_details(file_path, images_folder, videos_folder):
    post_id = "unknown"  # Initialize post_id with a default value
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            soup = BeautifulSoup(file, 'html.parser')

        json_data = json.loads(soup.find('script', {'type': 'application/ld+json'}).string)
        post_id = urlparse(json_data.get("@id", "")).path.split('/')[-1]  # Extract post_id

        title = json_data.get("headline", "No title found")
        date = json_data.get("datePublished", "No date found")
        image_url = json_data.get("image", None)
        video_url = json_data.get("video", {}).get("contentUrl", None)
        image_path = download_media(image_url, images_folder) if image_url else None
        video_path = download_media(video_url, videos_folder) if video_url else None

        interaction_stats = json_data.get("interactionStatistic", [])
        upvotes = downvotes = comments = "0"
        for stat in interaction_stats:
            interaction_type = stat.get("interactionType", "")
            count = str(stat.get("userInteractionCount", 0))
            if "LikeAction" in interaction_type:
                upvotes = count
            elif "DislikeAction" in interaction_type:
                downvotes = count
            elif "CommentAction" in interaction_type:
                comments = count

        return post_id, title, date, upvotes, downvotes, comments, image_url, video_url, image_path, video_path
    except Exception as e:
        return post_id, 'Error fetching post details', 'Error', '0', '0', '0', None, None, None, None

# Function to download media files (images or videos)
def download_media(media_url, folder):
    if not media_url:
        return None
    response = requests.get(media_url, stream=True)
    if response.status_code == 200:
        post_id = urlparse(media_url).path.split('/')[-1]
        file_path = os.path.join(folder, post_id)
        with open(file_path, 'wb') as file:
            for chunk in response.iter_content(1024):
                file.write(chunk)
        return file_path
    return None

# Function to process HTML files in a directory and write data to a CSV file
def process_files_in_directory(directory, csv_file, images_folder, videos_folder):
    with open(csv_file, 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['Post ID', 'Title', 'Date', 'Upvotes', 'Downvotes', 'Comments', 'Image URL', 'Video URL', 'Local Image Path', 'Local Video Path'])

        for filename in os.listdir(directory):
            if filename.endswith(".html"):
                file_path = os.path.join(directory, filename)
                post_details = fetch_post_details(file_path, images_folder, videos_folder)
                writer.writerow(post_details)

# Directory and file setup
pages_directory = 'pages'
output_csv = 'output_data.csv'
images_folder = 'images'
videos_folder = 'videos'
os.makedirs(images_folder, exist_ok=True)
os.makedirs(videos_folder, exist_ok=True)

# Fetch pages and process them
fetch_pages('Your 9GAG data.html', pages_directory)
process_files_in_directory(pages_directory, output_csv, images_folder, videos_folder)
