from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import time
import json
import csv

# Loop through champion elements and extract data
def extract_lol_data(character_elements, writer):
    for i in range(8, len(character_elements), 8):
                champion_name_element = character_elements[i].find_next('div', class_='champion-icon-name', style='display: none;')
                champion_name = champion_name_element.get_text().strip() if champion_name_element else ""

                gender_element = character_elements[i + 1].find('span')
                gender = gender_element.get_text().strip() if gender_element else ""

                positions_element = character_elements[i + 2].find('div')
                positions = positions_element.get_text().strip().replace(" ", "") if positions_element else ""

                species_element = character_elements[i + 3].find('div')
                species = species_element.get_text().strip().replace(" ", "") if species_element else ""

                resource_element = character_elements[i + 4].find('span')
                resource = resource_element.get_text().strip() if resource_element else ""

                range_type_element = character_elements[i + 5].find('div')
                range_type = range_type_element.get_text().strip().replace(" ", "") if range_type_element else ""

                regions_element = character_elements[i + 6].find('div')
                regions = regions_element.get_text().strip().replace(" ", "") if range_type_element else ""

                release_year_element = character_elements[i + 7].find('span')
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

# Get the height in meters in float format. From 70cm to 0.7 or 1m70 to 1.7 or 1m to 1.0
def transform_height_to_meters(height) -> float:
    if 'cm' in height:
        return float(height.replace('cm', '')) / 100
    elif 'm' in height:
        if len(height) == 2:
            return float(height.replace('m', ''))
        return float(height.replace('m', '')) / 100

                
def extract_pokemon_data(character_elements, writer):
    for i in range(8, len(character_elements), 8):
                pokemon_name_element = character_elements[i].find_next('div', class_='champion-icon-name', style='display: none;')
                pokemon_name = pokemon_name_element.get_text().strip() if pokemon_name_element else ""

                type_1_element = character_elements[i + 1].find('span')
                type_1 = type_1_element.get_text().strip() if type_1_element else ""

                type_2_element = character_elements[i + 2].find('div')
                type_2 = type_2_element.get_text().strip().replace(" ", "") if type_2_element else ""

                habitat_element = character_elements[i + 3].find('div')
                habitat = habitat_element.get_text().strip().replace(" ", "") if habitat_element else ""

                color_element = character_elements[i + 4].find('div')
                color = color_element.get_text().strip().replace(" ", "") if color_element else ""

                evolution_stage_element = character_elements[i + 5].find('div')
                evolution_stage = evolution_stage_element.get_text().strip().replace(" ", "") if evolution_stage_element else ""

                height_element = character_elements[i + 6].find('div')
                height = transform_height_to_meters(height_element.get_text().strip().replace(" ", "")) if height_element else ""

                weight_element = character_elements[i + 7].find('span')
                weight = weight_element.get_text().strip().replace(" ", "").replace("kg", "").replace("g", "") if weight_element else ""

                # Write the champion data to the CSV file
                writer.writerow([
                    pokemon_name,
                    type_1,
                    type_2,
                    habitat,
                    color,
                    evolution_stage,
                    height,
                    weight
                ])

def main(url, character_to_find, field_list, file_name, json_file_name, place_holder, extract_function):
    # Set up the Firefox WebDriver
    firefox_driver_path = '/home/ninou/Downloads/operadriver_linux64/geckodriver'  # Replace with the actual path
    firefox_options = webdriver.FirefoxOptions()
    # You can set preferences and options here if needed

    driver = webdriver.Firefox(options=firefox_options)

    driver.get(url)

    time.sleep(0.5)

    try:
        consent_button = driver.find_element(By.XPATH, '//p[@class="fc-button-label" and text()="Consent"]')
        consent_button.click()
    except:
        pass

    # Replace with the champion's name you want to retrieve data for
    with open(json_file_name) as json_file:
        character_data = json.load(json_file)
        
    # Locate the input field
    input_field = driver.find_element(By.CSS_SELECTOR, 'input[placeholder="' + place_holder + '"]')
    for i in range(0,len(character_data)):
    #for i in range(0,29):
        # type the champion's name
        if character_data[i].lower() != character_to_find.lower():
            input_field.send_keys(character_data[i])

            # Simulate pressing Enter
            input_field.send_keys(Keys.ENTER)
            time.sleep(0.03)
    #Finally enter the guesses champ and retrieve his data
    input_field.send_keys(character_to_find)
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

    character_elements = soup.find_all('div', class_='square-content')

    if character_elements:
        # Create or open a CSV file to write the data
        with open(file_name, 'w', newline='', encoding='utf-8') as csvfile:
            fieldnames = field_list
            writer = csv.writer(csvfile, delimiter=';', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            
            # Write the header row
            writer.writerow(fieldnames)

            # Loop through champion elements and extract data
            extract_function(character_elements, writer)
            
    else:
        print("Character name element not found.")

    # Close the browser window
    driver.quit()
    
def retrieve_lol_var():
    url = "https://loldle.net/classic"
    character_to_find = input("Enter guess character's name: ")
    field_list = ['Champion Name', 'Gender', 'Position(s)', 'Species', 'Resource', 'Range type', 'Region(s)', 'Release year']
    file_name = 'champions_data_test.csv'
    json_file_name = 'champions.json'
    place_holder = 'Type champion name ...'
    extract_function = extract_lol_data
    
    return url, character_to_find, field_list, file_name, json_file_name, place_holder, extract_function

def retrieve_pokemon_var():
    url = "https://pokedle.net/classic"
    character_to_find = input("Enter guess character's name: ")
    field_list = ['Pokemon', 'Type 1', 'Type 2', 'Habitat', 'Color(s)', 'Evolution Stage', 'Height', 'Weight']
    file_name = 'pokemon_data.csv'
    json_file_name = 'pokemon.json'
    place_holder = 'Type pokémon name ...'
    extract_function = extract_pokemon_data
    
    return url, character_to_find, field_list, file_name, json_file_name, place_holder, extract_function

def lol():
    url, character_to_find, field_list, file_name, json_file_name, place_holder, extract_function = retrieve_lol_var()
    main(url, character_to_find, field_list, file_name, json_file_name, place_holder, extract_function)

def pokemon():
    url, character_to_find, field_list, file_name, json_file_name, place_holder, extract_function = retrieve_pokemon_var()
    main(url, character_to_find, field_list, file_name, json_file_name, place_holder, extract_function)

if __name__ == '__main__':
    #pokemon()
    lol()