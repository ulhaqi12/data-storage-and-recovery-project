import requests
from bs4 import BeautifulSoup


def scrape_title(url):
    try:
        # Send a request to the URL without following robots.txt rules
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"}
        response = requests.get(url, headers=headers, allow_redirects=True)

        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            # Parse the HTML content with BeautifulSoup
            soup = BeautifulSoup(response.content, "html.parser")

            # Extract the title
            title = soup.title.string.strip() if soup.title else "Title not found"

            return title
        else:
            return f"Failed to retrieve content. Status code: {response.status_code}"

    except Exception as e:
        return f"Error: {e}"
