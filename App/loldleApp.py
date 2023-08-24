import math
import csv
import numpy as np
import os


EXACT = np.uint8(0)
ATLEAST = np.uint8(1)
WRONG = np.uint8(2)
YOUNGER = np.uint8(3)
OLDER = np.uint8(4)

DATA_DIR = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "Data"
)
CHAMP_LIST = os.path.join(DATA_DIR, "champions_data.csv")

class Champion:
    Name = ""
    Gender = ""
    Positions = []
    Species = []
    Resource = ""
    RangeType = []
    Regions = []
    ReleaseYear = 0
    
    def __str__(self):
            positions_str = ", ".join(self.Positions)
            species_str = ", ".join(self.Species)
            range_type_str = ", ".join(self.RangeType)
            regions_str = ", ".join(self.Regions)

            champ_info = (
                f"Name: {self.Name}\n"
                f"Gender: {self.Gender}\n"
                f"Positions: {positions_str}\n"
                f"Species: {species_str}\n"
                f"Resource: {self.Resource}\n"
                f"Range Type: {range_type_str}\n"
                f"Regions: {regions_str}\n"
                f"Release Year: {self.ReleaseYear}"
            )
            return champ_info
        
def get_champ_list():
    result = []
    with open(CHAMP_LIST, newline="") as csvfile:
        reader = csv.DictReader(csvfile, delimiter=";")
        for row in reader:
            result.append(row["Champion Name"])
    return result

def get_champ_list_with_data():
    result = []
    with open(CHAMP_LIST, newline="") as csvfile:
        reader = csv.DictReader(csvfile, delimiter=";")
        for row in reader:
            champ = Champion()
            champ.Name = row["Champion Name"]
            champ.Gender = row["Gender"]
            champ.Positions = row["Position(s)"].split(",")
            champ.Species = row["Species"].split(",")
            champ.Resource = row["Resource"]
            champ.RangeType = row['Range type'].split(",")
            champ.Regions = row["Region(s)"].split(",")
            champ.ReleaseYear = int(row['Release year'])
            result.append(champ)
    return result

def get_random_champ(champ_list):
    return champ_list[np.random.randint(0, len(champ_list))]

def get_comparaison_with_champ(try_champ: Champion() , choosen_champ: Champion()):
    result = [4] * 7
    if try_champ == choosen_champ:
        result = [EXACT] * 7 
    else:
        result[0] = EXACT if try_champ.Gender == choosen_champ.Gender else WRONG
        result[1] = ATLEAST if len(set(try_champ.Positions).intersection(choosen_champ.Positions)) > 0 else WRONG
        result[1] = EXACT if sorted(try_champ.Positions) == sorted(choosen_champ.Positions) else result[1]
        result[2] = ATLEAST if len(set(try_champ.Species).intersection(choosen_champ.Species)) > 0 else WRONG
        result[2] = EXACT if sorted(try_champ.Species) == sorted(choosen_champ.Species) else result[2]
        result[3] = EXACT if try_champ.Resource == choosen_champ.Resource else WRONG
        result[4] = ATLEAST if len(set(try_champ.RangeType).intersection(choosen_champ.RangeType)) > 0 else WRONG
        result[4] = EXACT if sorted(try_champ.RangeType) == sorted(choosen_champ.RangeType) else result[4]
        result[5] = ATLEAST if len(set(try_champ.Regions).intersection(choosen_champ.Regions)) > 0 else WRONG
        result[5] = EXACT if sorted(try_champ.Regions) == sorted(choosen_champ.Regions) else result[5]
        result[6] = OLDER if try_champ.ReleaseYear < choosen_champ.ReleaseYear else YOUNGER
        result[6] = EXACT if try_champ.ReleaseYear == choosen_champ.ReleaseYear else result[6]
        
    return int("".join(map(str, result)), 5)

def base_10_to_5(n: int, size: int = 7):
    result = []
    while n > 0:
        result.insert(0, n % 5)
        n //= 5
    while len(result) < size:
        result.insert(0, 0)
    return result[-size:]
            
def find_champ_with_name(champ_name, champ_list):
    for champ in champ_list:
        if champ.Name == champ_name:
            return champ
    return None

def convert_combinaison_to_visual(combinaison):
    result = ""
    for elem in combinaison:
        if elem == EXACT:
            result += "🟩"
        elif elem == ATLEAST:
            result += "🟧"
        elif elem == WRONG:
            result += "🟥"
        elif elem == YOUNGER:
            result += "🟪"
        elif elem == OLDER:
            result += "🟦"
        else:
            result += "❓"
    return result
    

class GameState:
    choosen_champ: Champion()
    champ_list: [Champion()]
    tested_champs: [Champion()]
    combinaison: [int]
    last_tested_champ: Champion()
    is_champ_found = False
    
    def __init__(self):
        self.champ_list = get_champ_list_with_data()
        self.choosen_champ = get_random_champ(self.champ_list)
        self.tested_champs = []
        self.combinaison = [WRONG*7]
        
    def display_combinaison(self):
        print(convert_combinaison_to_visual(base_10_to_5(self.combinaison[0])))
    
    def display_combi_and_champ(self):
        print("🚹📍🦄⭐️🗡️ 🌎🕰️")
        for i in range(len(self.tested_champs)-1, -1, -1):
            champ = self.tested_champs[i]
            combi = self.combinaison[i]
            print(convert_combinaison_to_visual(base_10_to_5(combi)), " ", champ.Name)

def play_game():
    game = GameState()
    os.system('cls' if os.name == 'nt' else 'clear')
    while not game.is_champ_found:
        #clear screen
        
        #print(game.choosen_champ)
        print("Choose a champion")
        input_champ = input().lower()
        available_champs = [champ.Name for champ in game.champ_list if champ.Name.lower().startswith(input_champ) and champ not in game.tested_champs]
        if len(available_champs) == 0:
            print("No champions found with that name. Try again.")
            continue
        elif len(available_champs) == 1:
            game.last_tested_champ = find_champ_with_name(available_champs[0], game.champ_list)
        else:
            print("Available champions:")
            for champ in available_champs:
                print(champ)
            continue
        game.tested_champs.insert(0, game.last_tested_champ)
        game.combinaison.insert(0,get_comparaison_with_champ(game.last_tested_champ, game.choosen_champ))
        os.system('cls' if os.name == 'nt' else 'clear')
        #game.display_combinaison()
        game.display_combi_and_champ()
        if game.last_tested_champ == game.choosen_champ:
            game.is_champ_found = True
            print("You found the champion!")
        
        
    

def main():
    # Possible Colors:
    # Gender - two colors: red or green
    # Position(s) - three colors: red, orange, green  
    # Species -  three colors: red, orange, green
    # Resource - two colors: red or green
    # Range type - three colors: red, orange, green
    # Region(s) - three colors: red, orange, green
    # Release year - three colors: green, blue or purple
    # 0 🟩 green right one, 
    # 1 🟧 orange have atleast one part of it, 
    # 2 🟥 red not part of it, 
    # 3 🟦 blue younger, 
    # 🟩🟥🟧🟩🟥🟥🟪
    # 0 2 1 0 2 2 4
    # 0*5^0 + 2*5^1 + 1*5^2 + 0*5^3 + 2*5^4 + 2*5^5 + 4*5^6 = 70035
    # total possible 78124 car base 5 avec 7 emplacement possibles
    
    play_game()
    
if __name__ == "__main__":
    main()