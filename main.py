"""
This module contains the main code for the news scraper.
"""

import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
from dotenv import load_dotenv
from database.database import save_article_to_db, article_exists

# Load environment variables
load_dotenv()
CHROMEDRIVER_PATH = os.getenv("CHROMEDRIVER_PATH")
BASE_URL_NEWS = os.getenv("BASE_URL_NEWS")
BASE_URL = os.getenv("BASE_URL")


def setup_webdriver():
    """Sets up Selenium WebDriver with Chrome options."""
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    service = Service(executable_path=CHROMEDRIVER_PATH or "chromedriver")
    driver = webdriver.Chrome(service=service, options=chrome_options)
    return driver


def get_page_content(url):
    """Fetches page content for the given URL."""
    driver = setup_webdriver()
    driver.get(url)
    soup = BeautifulSoup(driver.page_source, "html.parser")
    driver.quit()
    return soup


def parse_article(article):
    """Extracts and returns details from a single article."""
    date_tag = article.find(class_="date_part")
    date = date_tag.get_text(strip=True) if date_tag else "No date found"

    title_tag = article.find(class_="title")
    title = title_tag.get_text(strip=True) if title_tag else "No title found"

    body_tag = article.find(class_="body multiline")
    body = body_tag.get_text(strip=True) if body_tag else "No body found"

    categories_tag = article.find(class_="categories")
    categories = (
        categories_tag.get_text(strip=True) if categories_tag else "No categories found"
    )

    permalink = article.get("ta_permalink")

    image_container = article.find(class_="feature_image_container")
    img_src = get_image_source(image_container)

    return date, title, body, categories, permalink, img_src


def get_image_source(image_container):
    """Extracts the highest resolution image URL from the image container,
    with enhanced error handling."""
    if not image_container:
        return "No image found"

    img_tag = image_container.find("img")
    if not img_tag:
        return "No image found"

    img_src = img_tag.get("src", "")
    if img_src.startswith("http"):
        return img_src

    img_srcset = img_tag.get("srcset", "")
    if img_srcset:
        try:
            # Extract URLs and their widths, filtering out any malformed entries
            srcset_entries = [entry.split(" ") for entry in img_srcset.split(",")]
            srcset_entries = [
                entry
                for entry in srcset_entries
                if len(entry) == 2 and entry[1].endswith("w")
            ]
            # If no valid entries are found, return a generic message
            if not srcset_entries:
                return "No valid entries in srcset"

            # Convert widths to integers, select the entry with the maximum width
            highest_res_entry = max(
                srcset_entries, key=lambda entry: int(entry[1][:-1])
            )
            highest_res_url = highest_res_entry[0]
            # If the URL is relative, prepend the base URL
            if highest_res_url.startswith("/"):
                highest_res_url = f"{BASE_URL}{highest_res_url}"
            return highest_res_url
        except ValueError:
            # In case of conversion error, log the issue and return a generic message
            print("Error parsing srcset widths.")
            return "Error in srcset parsing"

    return "No direct image link available"


def should_display_article(date, body, img_src):
    """Determines if the article should be displayed based on its content."""
    return not (
        date == "No date found"
        or body == "No body found"
        or img_src == "No image found"
    )


def scrape_jamaica_observer(show_all=True):
    """Main function to scrape articles, with graceful handling of KeyboardInterrupt."""
    base_url = BASE_URL_NEWS
    pagination_suffix = os.getenv("PAGINATION_SUFFIX")
    page_number = 1
    has_content = True
    page_num = 1

    try:
        while has_content:
            page_url = (
                f"{base_url}page/{page_number}/{pagination_suffix}"
                if page_number > 1
                else f"{base_url}{pagination_suffix}"
            )
            print(f"Scraping Page: {page_number} - {page_url}")
            soup = get_page_content(page_url)

            articles = soup.find_all("article")
            if not articles:
                print("No articles found. Ending scrape.")
                break

            for article in articles:
                date, title, body, categories, permalink, img_src = parse_article(
                    article
                )
                # Skip articles that already exist in the database
                if article_exists(permalink):
                    print(f"Article already exists: {title}")
                    continue
                #
                if show_all or should_display_article(date, body, img_src):
                    save_article_to_db(
                        date, title, body, categories, permalink, img_src, page_num
                    )
                    # Extract page number from the URL
                    page_num = int(page_url.split("/")[-2]) if page_number > 1 else 1
                    print(f"Saved: {title}")
                else:
                    print(f"Omitted (incomplete information): {title}")

            page_number += 1  # Next page
    except KeyboardInterrupt:
        print("\nScraping interrupted by user. Exiting cleanly...")


if __name__ == "__main__":
    scrape_jamaica_observer(show_all=False)  # Set to True to display all articles
