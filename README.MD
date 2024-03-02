# Jamaica Observer News Scraper

This project is a web scraper that fetches articles from the Jamaica Observer news website. It uses FastAPI for the web server and Selenium for the web scraping.

## Project Structure

```
.
├── .dockerignore
├── .DS_Store
├── .envexample
├── .gitignore
├── api
│   └── app
│       ├── __pycache__
│       ├── db_utils.py
│       ├── main.py
│       └── robots.txt
├── database
│   ├── __init__.py
│   ├── __pycache__
│   └── database.py
├── docker-compose.yml
├── Dockerfile
├── main.py
├── requirements.txt
├── start.sh
└── storage
```
## Setup

1. Clone the repository.
2. Install the dependencies by running `pip install -r requirements.txt`.
3. Set up your environment variables in a `.env` file. You'll need to set `CHROMEDRIVER_PATH`, `BASE_URL_NEWS`, and `BASE_URL`.
4. Build the Docker image by running `docker build -t jamaica-observer-scraper .`.
5. Run the Docker container by running `docker run -p 1876:1876 jamaica-observer-scraper`.

## Usage

The scraper is started by running `main.py`. By default, it only displays articles that have a date, body, and image. To display all articles, set the `show_all` parameter to `True` when calling `scrape_jamaica_observer()`.

## Warning

Web scraping should be done responsibly. As of the time of writing, the Jamaica Observer's `robots.txt` file does not disallow scraping. However, always check the website's `robots.txt` file and terms of service to ensure that you're allowed to scrape it. Be respectful of the website's resources and don't overload their servers with too many requests at once. This scraper is intended for educational purposes and should not be used to violate any laws or terms of service.
```