# ==========================================================
# WEB SCRAPING PROJECT (STUDENT FRIENDLY VERSION)
# ==========================================================
# Website      : https://quotes.toscrape.com
# Purpose      : Extract quotes from multiple pages
# Output       : CSV file
# Level        : Beginner → Intermediate
# ==========================================================

# ----------------------------------------------------------
# STEP 0: IMPORT REQUIRED LIBRARIES
# ----------------------------------------------------------
# requests       → Used to send request to website
# BeautifulSoup  → Used to read and extract HTML content
# pandas         → Used to store data and save it as CSV
# time           → Used to add delay (avoid blocking)
# ----------------------------------------------------------

import requests
from bs4 import BeautifulSoup
import pandas as pd
import time

# ----------------------------------------------------------
# STEP 1: DEFINE BASE URL
# ----------------------------------------------------------
# {} will be replaced by page number
# Example:
# https://quotes.toscrape.com/page/1/
# https://quotes.toscrape.com/page/2/
# ----------------------------------------------------------

BASE_URL = "https://quotes.toscrape.com/page/{}/"

# ----------------------------------------------------------
# STEP 2: USER CONTROLS (STUDENT CAN CHANGE THESE)
# ----------------------------------------------------------
# START_PAGE → from which page scraping should start
# END_PAGE   → till which page scraping should continue
# ----------------------------------------------------------

START_PAGE = 1
END_PAGE = 200   # You can change this value

# ----------------------------------------------------------
# STEP 3: CREATE EMPTY LIST TO STORE DATA
# ----------------------------------------------------------
# All scraped data will be stored here
# ----------------------------------------------------------

all_quotes_data = []

# ----------------------------------------------------------
# STEP 4: LOOP THROUGH PAGES
# ----------------------------------------------------------
# range(START_PAGE, END_PAGE + 1)
# Example: 1 to 200
# ----------------------------------------------------------

for page in range(START_PAGE, END_PAGE + 1):

    # Create full URL for current page
    url = BASE_URL.format(page)
    print(f"Scraping page {page}: {url}")

    # ------------------------------------------------------
    # STEP 4.1: SEND REQUEST TO WEBSITE
    # ------------------------------------------------------
    response = requests.get(url)

    # If page does not exist, stop scraping
    if response.status_code != 200:
        print(f"Page {page} not found. Stopping scraping.")
        break

    # ------------------------------------------------------
    # STEP 4.2: PARSE HTML CONTENT
    # ------------------------------------------------------
    soup = BeautifulSoup(response.text, "html.parser")

    # ------------------------------------------------------
    # STEP 4.3: FIND ALL QUOTE BLOCKS
    # ------------------------------------------------------
    quotes = soup.find_all("div", class_="quote")

    # If no quotes found, stop scraping
    if not quotes:
        print("No data found on this page. Stopping.")
        break

    # ------------------------------------------------------
    # STEP 4.4: EXTRACT DATA FROM EACH QUOTE
    # ------------------------------------------------------
    for quote in quotes:

        # Extract quote text
        text = quote.find("span", class_="text").text

        # Extract author name
        author = quote.find("small", class_="author").text

        # Extract tags related to quote
        tags = [tag.text for tag in quote.find_all("a", class_="tag")]

        # Store extracted data in dictionary
        all_quotes_data.append({
            "Page_Number": page,
            "Quote": text,
            "Author": author,
            "Tags": ", ".join(tags),
            "Quote_Length": len(text)
        })

    # ------------------------------------------------------
    # STEP 4.5: ADD DELAY (VERY IMPORTANT)
    # ------------------------------------------------------
    # This avoids sending too many requests quickly
    # Helps to prevent IP blocking
    # ------------------------------------------------------
    time.sleep(1)

# ----------------------------------------------------------
# STEP 5: CONVERT LIST TO DATAFRAME
# ----------------------------------------------------------
df = pd.DataFrame(all_quotes_data)

# ----------------------------------------------------------
# STEP 6: SAVE DATA TO CSV FILE
# ----------------------------------------------------------
df.to_csv("quotes_page_range_data.csv", index=False)

# ----------------------------------------------------------
# STEP 7: SUCCESS MESSAGE
# ----------------------------------------------------------
print("Scraping completed successfully!")
print(f"Total records collected: {len(df)}")