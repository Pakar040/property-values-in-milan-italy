import re
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec


def geocode(address):
    # Set up Chrome options
    options = Options()
    options.add_argument("--headless")  # Enables headless mode
    options.add_argument("--disable-gpu")  # Disables GPU hardware acceleration
    options.add_argument("--window-size=1920x1080")  # Specifies the window size

    # Set up the Selenium WebDriver. This example uses Chrome.
    chrome_driver = webdriver.Chrome(options=options)

    # Update address for url
    address = address.replace(" ", "+")

    # URL of the page you want to scrape
    initial_url = f'https://www.google.com/maps/search/{address}'

    # Go to the Google Maps URL
    chrome_driver.get(initial_url)
    # print("Initial URL:", initial_url)

    try:
        # Wait for an element that reliably indicates the map has loaded;
        WebDriverWait(chrome_driver, 20).until(
            # this could be the zoom controls or other map features
            ec.visibility_of_element_located((By.CSS_SELECTOR, ".m6QErb.DxyBCb"))
            # Example: CSS selector for zoom-in button
        )

        # Additional delay to ensure the URL updates if necessary
        WebDriverWait(chrome_driver, 10).until(lambda driver: "@" in driver.current_url)

    finally:
        # Get and print the current URL
        updated_url = chrome_driver.current_url
        # print("Updated URL:", updated_url)

        # Clean up by closing the browser
        chrome_driver.quit()

        # Regular expression to match the latitude and longitude
        match = re.search(r'@([-\d.]+),([-\d.]+)', updated_url)

        latitude = "LatitudeNotFound"
        longitude = "LongitudeNotFound"
        if match:
            latitude = match.group(1)
            longitude = match.group(2)
            # print("Latitude:", latitude)
            # print("Longitude:", longitude)
        else:
            print("Coordinates not found in the URL.")

        return f"{latitude}:{longitude}"
