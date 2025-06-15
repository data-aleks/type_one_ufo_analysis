from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, WebDriverException, NoSuchElementException, ElementClickInterceptedException, StaleElementReferenceException

from warnings import warn
from time import sleep
from random import randint
import pandas as pd
from datetime import datetime

# --- WebDriver Setup ---
# Configure Chrome options
chrome_options = Options()
# Optional: Run in headless mode (browser UI won't be shown)
# Uncomment the line below to run headless
chrome_options.add_argument("--headless")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--log-level=3")  # Suppress logs
# Add a user-agent to mimic a real browser more closely
chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.88 Safari/537.36")

try:
    # Initialize the WebDriver. Ensure chromedriver is in your system's PATH.
    driver = webdriver.Chrome(options=chrome_options)
except WebDriverException as e:
    print(f"Error initializing WebDriver: {e}")
    print("Please ensure you have Chrome installed and ChromeDriver is in your system's PATH or its path is specified.")
    print("You can download ChromeDriver from: https://chromedriver.chromium.org/downloads")
    exit()  # Exit if driver can't be initialized

# --- Data Storage Initialization ---
# Lists to hold the scraped data for each column
all_sighting_data = []

# --- Progress Tracking Setup ---
start_time = datetime.now()
print(f"Scraping started at: {start_time.strftime('%Y-%m-%d %H:%M:%S')}")
print("-" * 50)

# --- BASE URL FOR SCRAPING ---
BASE_URL = "https://nuforc.org/subndx/?id=highlights"

# Define the CSS selectors for each data column
COLUMN_SELECTORS = {
    "occurred": 'td[class*="column-occurred"]',
    "city": 'td[class*="column-city"]',
    "state": 'td[class*="column-state"]',
    "country": 'td[class*="column-country"]',
    "shape": 'td[class*="column-shape"]',
    "summary": 'td[class*="column-summary"]'
}

current_page = 0
MAX_PAGES_TO_SCRAPE = 15 # Scrape up to 15 pages (user mentioned ~12 pages)

# --- Load the initial page ---
try:
    driver.get(BASE_URL)
    # Wait for the main data table to be present
    # Assuming the table itself will contain a specific ID or class
    # For nuforc.org/subndx, the table is usually within a div with id="sighting_data" or similar
    # Let's wait for the table rows to appear.
    WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, 'table.display')) # Or a more specific table selector if available
    )
    print(f"Loaded initial page: {BASE_URL}")
    sleep(randint(3, 5)) # Small pause after initial load
except TimeoutException:
    print(f'Timeout: No data table found on {BASE_URL} after 20 seconds. Exiting.')
    driver.quit()
    exit()
except WebDriverException as e:
    print(f'WebDriver Error loading initial page {BASE_URL}: {e}. Exiting.')
    driver.quit()
    exit()

# --- Main scraping loop: Iterate through pages ---
while current_page < MAX_PAGES_TO_SCRAPE:
    current_page += 1
    print(f"\n--- Scraping Page {current_page} ---")

    # Wait for the table body to be loaded or re-loaded after navigation
    try:
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'table.display tbody'))
        )
        # Give a small buffer for all elements to fully render
        sleep(2)
    except TimeoutException:
        print(f"Timeout waiting for table body on page {current_page}. It might be the last page or an error occurred.")
        break

    # Get all rows from the current page's table body
    try:
        # Assuming the rows containing data are directly under tbody
        sighting_rows = driver.find_elements(By.CSS_SELECTOR, 'table.display tbody tr')
        print(f"Found {len(sighting_rows)} sighting records on page {current_page}.")
    except NoSuchElementException:
        print(f"No sighting rows found on page {current_page}. End of data or error.")
        break
    except StaleElementReferenceException:
        warn("Stale element reference when finding rows. Retrying current page.")
        sleep(5)
        continue # Try to re-find elements on the current page

    if not sighting_rows:
        print(f"No records found on page {current_page}. Likely reached the end.")
        break

    # --- Scrape data from current page's rows ---
    for i, row in enumerate(sighting_rows):
        sighting = {}
        for col_name, css_selector in COLUMN_SELECTORS.items():
            try:
                # Find the specific td element within the current row
                element = row.find_element(By.CSS_SELECTOR, css_selector)
                sighting[col_name] = element.text.strip()
            except NoSuchElementException:
                sighting[col_name] = "N/A" # Set to N/A if element not found
                warn(f"Column '{col_name}' not found for row {i+1} on page {current_page}.")
            except Exception as e:
                sighting[col_name] = "Error"
                warn(f"Error scraping '{col_name}' for row {i+1} on page {current_page}: {e}")
        all_sighting_data.append(sighting)

        # Print a sample of scraped data
        if (i + 1) % 50 == 0 or i == 0: # Print first and every 50th record
            print(f"  Sample Record {len(all_sighting_data)}: Occurred: {sighting.get('occurred', '')} | City: {sighting.get('city', '')} | Shape: {sighting.get('shape', '')}")

    # --- Find and click the "Next" button for pagination ---
    next_button = None
    try:
        # Wait for the 'next' pagination button to be clickable
        next_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, 'a.paginate_button.next'))
        )
        if "disabled" in next_button.get_attribute("class"):
            print("Next button is disabled. Reached the last page.")
            break # Exit loop if next button is disabled

        # Scroll to the button to ensure it's in view and clickable
        driver.execute_script("arguments[0].scrollIntoView(true);", next_button)
        sleep(randint(1, 2)) # Small pause after scroll

        # Use JavaScript to click the button to bypass potential interception issues
        driver.execute_script("arguments[0].click();", next_button)
        print(f"Clicked 'Next' button. Waiting for next page to load...")
        sleep(randint(5, 8)) # Give time for the new content to load

        # Wait for any element from the next page to confirm navigation
        WebDriverWait(driver, 10).until(
            EC.staleness_of(sighting_rows[0]) # Wait for the old rows to become stale
        )
        print("Page navigation successful.")

    except TimeoutException:
        print("Timeout: 'Next' button not found or not clickable within the time limit. Assuming end of results.")
        break # Exit loop if button not found or new content not loaded
    except NoSuchElementException:
        print("No 'Next' button found. Assuming all records are loaded.")
        break # Exit loop if button is not present
    except ElementClickInterceptedException:
        warn("Element click intercepted (even with JS) for 'Next' button. Retrying current page (might skip).")
        sleep(5) # Wait and try again
        # If it's intercepted, it might be a temporary overlay. The next loop iteration will try again.
        # For a pagination loop, it's safer to break if multiple retries fail.
        break # Breaking to prevent infinite loop on persistent interception
    except StaleElementReferenceException:
        warn("Stale element reference for 'Next' button. Re-locating and trying again.")
        sleep(2)
        continue # Try finding and clicking the button again for the current page
    except Exception as e:
        warn(f"An unexpected error occurred while clicking 'Next': {e}. Stopping.")
        break # Exit for other unexpected errors

# --- ALWAYS REMEMBER TO CLOSE THE BROWSER ---
driver.quit()
print("-" * 50)
print("WebDriver closed.")
print(f"Scraping complete! Total records scraped: {len(all_sighting_data)}")

# --- Create DataFrame and Save to CSV ---
if all_sighting_data:
    ufo_data = pd.DataFrame(all_sighting_data)

    print("\n--- Scraped Data Preview (from DataFrame) ---")
    print(ufo_data.head())

    print("\n--- DataFrame Info ---")
    ufo_data.info()

    csv_filename = "ufo_sighting_data.csv"
    ufo_data.to_csv(csv_filename, index=False)

    print(f"\nData successfully saved to {csv_filename}")
else:
    print("No data was scraped.")
