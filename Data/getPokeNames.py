import json
import requests

# Make a request to the PokéAPI for the first 151 Pokémon which correspond to the first generation.
response = requests.get('https://pokeapi.co/api/v2/pokemon?limit=151')

# Check if the request was successful
if response.status_code == 200:
    # Parse the JSON response to get the list of Pokémon names
    pokemon_data = response.json()
    pokemon_names = [pokemon['name'] for pokemon in pokemon_data['results']]
    with open('pokemon.json', 'w') as f:
        f.write(json.dumps(pokemon_names, indent=4))
else:
    pokemon_names_json = "An error occurred while fetching the data."

