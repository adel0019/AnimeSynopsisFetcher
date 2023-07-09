## Anime Synopsis Fetcher

The Anime Synopsis Fetcher is a Python script that automates the process of fetching anime synopses from the AniList API and saving them into a `description.txt` file for each anime in your local anime collection. It helps you organize and keep track of the synopsis information for your favorite anime series.

### Features

- Fetches anime synopses using the AniList API.
- Creates a `description.txt` file with the anime name, category, and synopsis.
- Skips anime folders that already have a `description.txt` file.
- Excludes anime folders with the name "OVA" or "OVAS" from the process.
- Works with various anime categories such as Action, Airing, Comedy, Fantasy, Isekai, Kids, Mystery, Romance, Shonen, Slice of Life, Sports, and Uncategorized.

### How It Works

1. The script scans the specified root directory for anime folders categorized by different genres.
2. For each anime folder, it checks if there are video files present and skips the folder if there are none.
3. It also skips anime folders with the name "OVA" or "OVAS" to avoid processing unrelated content.
4. If a `description.txt` file already exists in the anime folder and follows the expected structure, the script skips that folder.
5. For the remaining anime folders, it searches for the corresponding anime information using the AniList API based on the folder name.
6. If the anime is found, it retrieves the anime name and synopsis, removes any HTML tags from the synopsis, and formats the information.
7. Finally, it creates a `description.txt` file in the anime folder and saves the anime name, category, and synopsis.

### Usage

1. Install the required dependencies by running `pip install -r requirements.txt`.
2. Set the root directory of your anime collection in the `root_dir` variable.
3. Run the script using `python main.py`.
4. The script will automatically fetch and save the anime synopses for each anime folder.

### Missing Synopsis Files

After running the script, a file named "missing_synopsis_files.txt" will be created in the root directory of your anime collection. This file contains the paths of the anime folders that do not have a `description.txt` file. You can refer to this file to identify the anime folders that need to be processed manually or have missing synopses.
