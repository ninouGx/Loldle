from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import time
import json
import csv

# Set up the Firefox WebDriver
firefox_driver_path = '/home/ninou/Downloads/operadriver_linux64/geckodriver'  # Replace with the actual path
firefox_options = webdriver.FirefoxOptions()
# You can set preferences and options here if needed

driver = webdriver.Firefox(options=firefox_options)

# URL of the page with the champion data (replace with the actual URL)
url = "https://loldle.net/classic"  # Replace with the actual URL
driver.get(url)


time.sleep(0.5)

try:
    consent_button = driver.find_element(By.XPATH, '//p[@class="fc-button-label" and text()="Consent"]')
    consent_button.click()
except:
    pass

# Replace with the champion's name you want to retrieve data for
with open('champions.json') as json_file:
    champion_data = json.load(json_file)
    
champion_name_to_guess = input("Enter guess champion's name: ")

for i in range(0,len(champion_data)):
#for i in range(0,29):
    # Locate the input field and type the champion's name
    if champion_data[i] != champion_name_to_guess:
        input_field = driver.find_element(By.CSS_SELECTOR, 'input[placeholder="Type champion name ..."]')
        input_field.send_keys(champion_data[i])

        # Simulate pressing Enter
        input_field.send_keys(Keys.ENTER)
        time.sleep(0.05)
#Finally enter the guesses champ and retrieve his data
input_field.send_keys(champion_name_to_guess)
input_field.send_keys(Keys.ENTER)

# Wait for the page to load (you might need to adjust the time depending on the page)
time.sleep(2)

# Get the page source after submitting the form
html_content = driver.page_source

#save html content to file
with open('data.html', 'w') as f:
    f.write(html_content)
    

# Parse the HTML content using BeautifulSoup
soup = BeautifulSoup(html_content, 'html.parser')

champion_elements = soup.find_all('div', class_='square-content')

if champion_elements:
    # Create or open a CSV file to write the data
    with open('champions_data.csv', 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['Champion Name', 'Gender', 'Position(s)', 'Species', 'Resource', 'Range type', 'Region(s)', 'Release year']  # Add other column names as needed
        writer = csv.writer(csvfile, delimiter=';', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        
        # Write the header row
        writer.writerow(fieldnames)

        # Loop through champion elements and extract data
        for i in range(8, len(champion_elements), 8):
            champion_name_element = champion_elements[i].find_next('div', class_='champion-icon-name', style='display: none;')
            champion_name = champion_name_element.get_text().strip() if champion_name_element else ""

            gender_element = champion_elements[i + 1].find('span')
            gender = gender_element.get_text().strip() if gender_element else ""

            positions_element = champion_elements[i + 2].find('div')
            positions = positions_element.get_text().strip().replace(" ", "") if positions_element else ""

            species_element = champion_elements[i + 3].find('div')
            species = species_element.get_text().strip().replace(" ", "") if species_element else ""

            resource_element = champion_elements[i + 4].find('span')
            resource = resource_element.get_text().strip() if resource_element else ""

            range_type_element = champion_elements[i + 5].find('div')
            range_type = range_type_element.get_text().strip().replace(" ", "") if range_type_element else ""

            regions_element = champion_elements[i + 6].find('div')
            regions = regions_element.get_text().strip().replace(" ", "") if range_type_element else ""

            release_year_element = champion_elements[i + 7].find('span')
            release_year = release_year_element.get_text().strip() if release_year_element else ""

            # Write the champion data to the CSV file
            writer.writerow([
                champion_name,
                gender,
                positions,
                species,
                resource,
                range_type,
                regions,
                release_year
            ])
else:
    print("Champion name element not found.")

# Close the browser window
driver.quit()