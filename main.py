import requests
from bs4 import BeautifulSoup
import random
from urllib.parse import urljoin  # Import urljoin for safer URL construction

# Step 1: Start with the first page
base_url = "http://quotes.toscrape.com/"
url = base_url

# Step 2: Initialize an empty list to hold all the quotes
all_quotes = []

while url:  # Keep scraping until there are no more "Next" pages
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    # Step 3: Extract the quotes on the current page
    quotes = soup.select('div.quote')
    
    for quote in quotes:
        text_elem = quote.find('span', class_='text')
        author_elem = quote.find('small', class_='author')

        # Only store valid quotes
        if text_elem and author_elem:
            text = text_elem.get_text()
            author = author_elem.get_text()
            all_quotes.append((text, author))

    # Step 4: Find the "Next" button and update the URL using urljoin
    next_btn = soup.select_one('li.next > a')
    if next_btn:
        next_url = next_btn.get('href')
        if isinstance(next_url, str):  # Ensure next_url is a string
            url = urljoin(base_url, next_url)  # Use urljoin to concatenate URLs safely
        else:
            url = None
    else:
        # If there's no "Next" button, stop the loop
        url = None

# Step 5: Randomly select a few quotes
num_quotes_to_display = 5  # Change this to the number of quotes you want
if len(all_quotes) > num_quotes_to_display:
    random_quotes = random.sample(all_quotes, num_quotes_to_display)
else:
    random_quotes = all_quotes  # If there aren't enough quotes, show all

# Step 6: Print the random quotes
for text, author in random_quotes:
    print(f'"{text}" - {author}')
