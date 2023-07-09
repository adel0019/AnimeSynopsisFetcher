import os
import requests
from bs4 import BeautifulSoup
import time

# AniList API endpoint for anime search
ANILIST_API_URL = 'https://graphql.anilist.co'

# Specify the root directory where the anime folders are located
root_dir = r"E:\Anime"

# List of anime categories
categories = [
    "Action",
    "Airing",
    "Comedy",
    "Fantasy",
    "Isekai",
    "Kids",
    "Mystery",
    "Romance",
    "Shonen",
    "Slice of Life",
    "Sports",
    "Uncategorized"
]


def search_anime(anime_name):
    # GraphQL query for anime search
    query = '''
    query ($search: String) {
      Media (search: $search, type: ANIME) {
        id
        title {
          romaji
        }
        description
      }
    }
    '''

    # Variables for the GraphQL query
    variables = {
        'search': anime_name
    }

    try:
        # Send the GraphQL request to AniList API
        response = requests.post(ANILIST_API_URL, json={'query': query, 'variables': variables})
        response.raise_for_status()
        data = response.json()

        if data and 'data' in data and 'Media' in data['data'] and data['data']['Media'] is not None:
            anime_data = data['data']['Media']
            return anime_data
        else:
            return None
    except requests.RequestException as e:
        print(f"An error occurred during the API request: {e}")
        return None
    finally:
        # Introduce a delay of 2 seconds between API requests to avoid rate limit issues
        time.sleep(2)



def process_anime_folder(folder_path, category):
    video_files = get_video_files(folder_path)

    if len(video_files) == 0:
        print(f"No video files found in folder '{os.path.basename(folder_path)}'. Skipping.")
        return

    if "OVA" in os.path.basename(folder_path).upper() or "OVAS" in os.path.basename(folder_path).upper():
        print(f"Skipping folder '{os.path.basename(folder_path)}'. Contains 'OVA' or 'OVAS' in the name.")
        return

    description_file = os.path.join(folder_path, 'description.txt')

    # Check if description.txt already exists and follows the expected structure
    if os.path.exists(description_file):
        with open(description_file, 'r', encoding='utf-8') as f:
            content = f.read()

        # Check if the file contains the expected structure
        if validate_description_file(content):
            print(f"Skipping folder '{os.path.basename(folder_path)}'. Description file already exists.")
            return

    anime_folder_name = os.path.basename(folder_path)
    anime_data = search_anime(anime_folder_name)

    if anime_data:
        anime_name = anime_data['title']['romaji']
        anime_synopsis = anime_data['description']

        # Remove <br>, <i>, and </i> tags from synopsis
        soup = BeautifulSoup(anime_synopsis, 'html.parser')
        synopsis_text = soup.get_text()

        # Format the description file path
        description_file = os.path.join(folder_path, 'description.txt')

        # Write anime name, category, and synopsis to the description file
        with open(description_file, 'w', encoding='utf-8') as f:
            f.write(f"Anime Name: {anime_name}\n")
            f.write(f"Category: {category}\n\n")
            f.write(f"Synopsis:\n{synopsis_text}\n")
    else:
        print(f"Anime '{anime_folder_name}' not found on AniList")


def validate_description_file(content):
    # Split the content by lines
    lines = content.strip().split('\n')

    # Check if the content follows the expected structure
    if len(lines) == 3 and lines[0].startswith("Anime Name:") and lines[1].startswith("Category:") and lines[
        2].startswith("Synopsis:"):
        return True
    else:
        return False


def get_video_files(folder_path):
    video_extensions = ['.mp4', '.mkv', '.avi', '.mov']

    video_files = []
    for item in os.listdir(folder_path):
        item_path = os.path.join(folder_path, item)
        if os.path.isfile(item_path) and os.path.splitext(item)[1].lower() in video_extensions:
            video_files.append(item)
    return video_files


def process_category(category):
    print(f"Processing category: {category}")
    category_folder = os.path.join(root_dir, category)

    anime_folders = []
    for root, dirs, files in os.walk(category_folder):
        for dir in dirs:
            anime_folder = os.path.join(root, dir)
            if os.path.isdir(anime_folder):
                anime_folders.append(anime_folder)

    if not anime_folders:
        print(f"No anime folders found in category '{category}'.")
        return

    for anime_folder in anime_folders:
        print(f"Working on folder: {anime_folder}")
        process_anime_folder(anime_folder, category)


# def scan_anime_folders():
#     for category in categories:
#         process_category(category)
#
#
# scan_anime_folders()
