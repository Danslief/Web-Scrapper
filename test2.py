from selenium import webdriver
from bs4 import BeautifulSoup
import time
import pandas as pd

# Function to scrape content from a given URL
def scrape_content(url, scroll_limit=2):
    # Initialize Chrome WebDriver
    options = webdriver.ChromeOptions()
    options.add_argument('headless')
    driver = webdriver.Chrome(options=options)
    driver.get(url)

    # Scroll to the bottom of the page a fixed number of times
    for _ in range(scroll_limit):
        # Scroll down to the bottom of the page
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        # Wait for a short while to let the content load
        time.sleep(2)

    # Get the page source after scrolling
    page_source = driver.page_source

    # Close the WebDriver
    driver.quit()

    # Create a BeautifulSoup object to parse the HTML content
    soup = BeautifulSoup(page_source, 'html.parser')

    return soup


# Function to extract relevant data from parsed HTML
def extract_data(soup):
    # Example: Extracting titles of articles
    titles = [title.text.strip() for title in soup.find_all('h2', class_='article-title')]
    return titles


# URLs to scrape
urls = [
    'https://www.politifact.com',
    'https://www.altnews.in',
    'https://mastodon.social/explore'
]

# Scraping content from each URL and storing it in a list
scraped_data = []
for url in urls:
    print(f"Scraping content from {url}")
    soup = scrape_content(url, scroll_limit=5)  # Specify scroll limit as 5
    scraped_data.append(soup)

# Extracting relevant data
extracted_data = []
for soup in scraped_data:
    data = extract_data(soup)
    extracted_data.append(data)

# Saving data to Excel file
for i, data in enumerate(extracted_data):
    df = pd.DataFrame({'Titles': data})
    df.to_excel(f'data_{i}.xlsx', index=False)

print("Data scraping, parsing, and saving to Excel completed.")
