# 9gagMyContentDownloader

## Overview

The `9gagMyContentDownloader.py` script allows you to download content from 9gag. You can use it to scrape and save posts, images, and videos from 9gag for later use or analysis.

## Usage

0. pip install requirements.txt

1. Clone this repository to your local machine.

2. Replace the Your 9gag data.html file in the project folder with your own HTML data file from 9gag. This file contains the web pages you want to scrape content from.

3. Run the script with the following command:

   python 9gagMyContentDownloader.py

The script will process the HTML data file, extract post details, and download images and videos as necessary. The downloaded content will be saved in the `images` and `videos` folders.

4. You can also find the extracted data in a CSV file named `output_data.csv`. This file contains information about each post, including the post ID, title, date, upvotes, downvotes, comments, image URL, video URL, and local paths to downloaded images and videos. You can use this data for further analysis or processing.

## CSV Data

The `output_data.csv` file contains the following columns:

- `Post ID`: The unique identifier for each post.
- `Title`: The title of the post, if available.
- `Date`: The date the post was published.
- `Upvotes`: The number of upvotes received by the post.
- `Downvotes`: The number of downvotes received by the post.
- `Comments`: The number of comments on the post.
- `Image URL`: The URL of the post's image, if available.
- `Video URL`: The URL of the post's video, if available.
- `Local Image Path`: The local path to the downloaded image file, if an image was downloaded.
- `Local Video Path`: The local path to the downloaded video file, if a video was downloaded.

You can use this CSV data for various purposes, such as analysis, reporting, or further processing of the downloaded content.

## Notes

- The script includes a random delay between processing different URLs to mimic human-like behavior and avoid overloading the website's servers. This helps prevent detection as a web scraper and ensures successful data retrieval.

- In case of SSL errors (handshake failures), the script will retry accessing the URL after a short delay (5 seconds). This is done to handle temporary network issues that can occur during web scraping.

- The script can be configured to access a Chrome instance where the user is logged in by making use of Selenium WebDriver. This allows for interactions with the website as if you were using a web browser while being logged in. 

Enjoy using `9gagMyContentDownloader` to download and manage your 9gag content!

---

**Author: MPWrbk
**Date:13-Nov-2023

This project is licensed under the [MIT License](LICENSE).