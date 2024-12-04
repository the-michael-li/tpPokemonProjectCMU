# ChatGPT taught me how to webscrape lololol
# All the Move Info is webscraped from https://pokemondb.net/move/all

import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

# URL of the page to scrape
url = "https://pokemondb.net/move/all"

# Send a GET request to fetch the page content
response = requests.get(url)

# Parse the HTML content
soup = BeautifulSoup(response.text, "html.parser")

# Find the table that contains the move data
table = soup.find("table")  # Assuming the first table is the one you need

# Extract the rows of the table
rows = table.find_all("tr")

# Extract the first column (e.g., move names) from each row
moveInfo = { }


for row in rows:
    # Find all cells in the row
    cells = row.find_all("td")  # `td` is for table data cells
    if cells:  # Skip header rows that don't have `td`
        moveName = cells[0].get_text(strip=True).replace(' ', '-').lower()
        moveDescription = cells[6].get_text(strip=True)
        movePower = cells[3].get_text(strip=True) if cells[3].get_text(strip=True) != '—' else 0
        cells[2].get_text(strip=True)
        img_tags = row.find_all("img")
        image_urls = [urljoin(url, img.get("src")) for img in img_tags if img.get("src")]
        moveCategory = None
        if len(image_urls) >= 1:
            if 'move-physical' in image_urls[0]: 
                moveCategory = 0
            elif 'move-special' in image_urls[0]: 
                moveCategory = 1
            elif 'move-status' in image_urls[0]: 
                moveCategory = 2
        if not ('Z-Move' in moveDescription or 'G-Max' in moveDescription or 'Dynamax' in moveDescription):
            moveInfo[moveName] = [movePower, cells[1].get_text(strip=True).lower(), moveCategory]


# Print the first column
for move in moveInfo: 
    print(f'"{move}": {moveInfo[move]}, ')