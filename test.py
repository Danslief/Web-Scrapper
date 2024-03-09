from selenium import webdriver
import time
from bs4 import BeautifulSoup
import pandas as pd

# Function to extract all text from specified BeautifulSoup elements
def extract_text(element):
    # Specify the tags to extract text from
    tags = ['p', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'span', 'div']
    texts = []

    # Extract text from specified tags
    for tag in tags:
        elements = element.find_all(tag)
        for el in elements:
            texts.append(el.get_text())

    return texts

# Function to scrape content from a given URL
def scrape_content(url, scroll_limit):
    # Initialize Chrome WebDriver
    options = webdriver.ChromeOptions()
    options.add_argument('headless')  # To run Chrome in headless mode
    driver = webdriver.Chrome(options=options)
    driver.get(url)

    # Scroll to the bottom of the page a fixed number of times
    for _ in range(scroll_limit):
        # Scroll down to the bottom of the page
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)  # Wait for 2 seconds for content to load

    # Get the page source after scrolling
    page_source = driver.page_source

    # Close the WebDriver
    driver.quit()

    # Create a BeautifulSoup object to parse the HTML content
    soup = BeautifulSoup(page_source, 'html.parser')

    # Initialize empty lists to store different types of content
    images = []
    videos = []
    audio = []
    text = []

    # Extracting images
    for img in soup.find_all('img'):
        if 'src' in img.attrs:  # Check if 'src' attribute exists
            images.append(img['src'])

    # Extracting videos
    for video in soup.find_all('video', {'src': True}):
        videos.append(video['src'])

    # Extracting audio files
    for audio_tag in soup.find_all('audio', {'src': True}):
        audio.append(audio_tag['src'])

    # Extracting text content
    text.append(extract_text(soup))

    # Determine the maximum length among images, videos, and audio lists
    max_length = max(len(images), len(videos), len(audio), len(text))

    # Fill the lists with empty strings to ensure they have the same length
    images += [''] * (max_length - len(images))
    videos += [''] * (max_length - len(videos))
    audio += [''] * (max_length - len(audio))
    text += [''] * (max_length - len(text))

    # Return a dictionary containing all extracted content
    return {'images': images, 'videos': videos, 'audio': audio, 'text': text}


# URLs to scrape
urls = [
    'https://www.upwork.com'
]

# Scraping content from each URL and storing it in a list
scraped_data = []
for url in urls:
    print(f"Scraping content from {url}")
    data = scrape_content(url, scroll_limit=10)  # Specify scroll limit as 2
    if data:
        scraped_data.append(data)

# Saving data to separate files
for i, item in enumerate(scraped_data):
    # Create a DataFrame from the scraped data
    df = pd.DataFrame(item)
    # Save the DataFrame to a CSV file
    df.to_csv(f'data_{i}.csv', index=False)

print("Data scraping and categorization completed.")
