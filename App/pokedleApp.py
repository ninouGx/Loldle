import math
import csv
import numpy as np
import os
from tqdm import tqdm
import curses
#import readline
import time
import re

############################################################################################################
#  Constants
############################################################################################################

EXACT = np.uint8(0)
ATLEAST = np.uint8(1)
WRONG = np.uint8(2)
BEFORE = np.uint8(3)
AFTER = np.uint8(4)

DATA_DIR = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "Data"
)
POKE_LIST = os.path.join(DATA_DIR, "pokemon_data.csv")

############################################################################################################
#   Data functions
############################################################################################################

class Pokemon:
    Name = ""
    Type1 = ""
    Type2 = ""
    Habitat = ""
    Colors = []
    EvolutionStage = 0
    Height = 0.0
    Weight = 0.0

        
def get_pokemon_list():
    result = []
    with open(POKE_LIST, newline="") as csvfile:
        reader = csv.DictReader(csvfile, delimiter=";")
        for row in reader:
            result.append(row["Pokemon Name"])
    return result

def get_pokemon_list_with_data():
    result = []
    with open(POKE_LIST, newline="") as csvfile:
        reader = csv.DictReader(csvfile, delimiter=";")
        for row in reader:
            poke = Pokemon()
            # row : Pokemon;Type 1;Type 2;Habitat;Color(s);Evolution Stage;Height;Weight
            poke.Name = row["Pokemon"]
            poke.Type1 = row["Type 1"]
            poke.Type2 = row["Type 2"]
            poke.Habitat = row["Habitat"]
            poke.Colors = row["Color(s)"].split(",")
            poke.EvolutionStage = int(row["Evolution Stage"])
            poke.Height = float(row["Height"])
            poke.Weight = float(row["Weight"])
            
            result.append(poke)
    return result

def get_random_poke(poke_list):
    return poke_list[np.random.randint(0, len(poke_list))]

def get_comparaison_with_poke(try_poke: Pokemon() , choosen_poke: Pokemon()):
    result = [4] * 7
    if try_poke == choosen_poke:
        result = [EXACT] * 7 
    else:
        result[0] = EXACT if try_poke.Type1 == choosen_poke.Type1 else WRONG
        result[1] = EXACT if try_poke.Type2 == choosen_poke.Type2 else WRONG
        result[2] = EXACT if try_poke.Habitat == choosen_poke.Habitat else WRONG
        result[3] = ATLEAST if len(set(try_poke.Colors).intersection(choosen_poke.Colors)) > 0 else WRONG
        result[3] = EXACT if sorted(try_poke.Colors) == sorted(choosen_poke.Colors) else result[3]
        result[4] = AFTER if try_poke.EvolutionStage < choosen_poke.EvolutionStage else BEFORE
        result[4] = EXACT if try_poke.EvolutionStage == choosen_poke.EvolutionStage else result[4]
        result[5] = AFTER if try_poke.Height < choosen_poke.Height else BEFORE
        result[5] = EXACT if try_poke.Height == choosen_poke.Height else result[5]
        result[6] = AFTER if try_poke.Weight < choosen_poke.Weight else BEFORE
        result[6] = EXACT if try_poke.Weight == choosen_poke.Weight else result[6]        
    return int("".join(map(str, result)), 5)

def base_10_to_5(n: int, size: int = 7):
    result = []
    while n > 0:
        result.insert(0, n % 5)
        n //= 5
    while len(result) < size:
        result.insert(0, 0)
    return result[-size:]
            
def find_poke_with_name(poke_name, poke_list):
    for poke in poke_list:
        if poke.Name == poke_name:
            return poke
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
        elif elem == BEFORE:
            result += "⬇️"
        elif elem == AFTER:
            result += "⬆️"
        else:
            result += "❓"
    return result

def convert_visual_to_combinaison(visual):
    result = []
    for elem in visual:
        if elem == "🟩":
            result.append(EXACT)
        elif elem == "🟧":
            result.append(ATLEAST)
        elif elem == "🟥":
            result.append(WRONG)
        elif elem == "⬇️" or elem == "⬇":
            result.append(BEFORE)
        elif elem == "⬆️" or elem == "⬆":
            result.append(AFTER)
        else:
            result.append(WRONG)
    return result

def convert_string_to_combinaison(string):
    result = []
    for elem in string:
        if elem == "0":
            result.append(EXACT)
        elif elem == "1":
            result.append(ATLEAST)
        elif elem == "2":
            result.append(WRONG)
        elif elem == "3":
            result.append(BEFORE)
        elif elem == "4":
            result.append(AFTER)
        else:
            result.append(WRONG)
    return result

def count_arrow_in_string(string):
    result = 0
    for elem in string:
        if elem == "⬇" or elem == "⬆":
            if string[string.index(elem) + 1] == "️":
                result += 1
    return result

############################################################################################################
#   Entropy functions
############################################################################################################

def calculate_each_combinaison(poke_to_test: Pokemon(), poke_list: [Pokemon()]):
    result = []
    for poke in poke_list:
        result.append(get_comparaison_with_poke(poke_to_test, poke))
    return result

# Return the list of champs that can be the choosen champ regarding their compatibility with the combinaison
# Example: with alistar, if combinaison is [0, 2, 1, 0, 2, 2, 5]  (🟩🟥🟧🟩🟥🟥⬆️) 
# the champ have to be a male, not a support, be a minotaur with other species, have mana, not a melee, not from runeterra and be released strictly after 2009 (>= 2010)
def find_compatibles_pokes_with_combinaison(pokemon : Pokemon(), combinaison: [int], poke_list: [Pokemon()]):
    result = []
    for poke in poke_list:
        comparaison = base_10_to_5(get_comparaison_with_poke(pokemon, poke))
        for i in range(len(comparaison)):
            if not (combinaison[i] == comparaison[i] or combinaison[i] == ATLEAST and comparaison[i] == EXACT):
                break
            if i == len(comparaison) - 1:
                result.append(poke)
    return result

def compute_entropy_for_a_poke(poke: Pokemon(), possible_pokes: [Pokemon()]):
    #besoin solutions possibles, du champion, 
    entropy = 0
    for poke_to_test in possible_pokes:
        combinaison = base_10_to_5(get_comparaison_with_poke(poke, poke_to_test))
        compatibles_pokes = find_compatibles_pokes_with_combinaison(poke, combinaison, possible_pokes)
        p = len(compatibles_pokes) / len(possible_pokes)
        if p > 0:
            entropy += - p * math.log(p, 2)
    return entropy

def max_entropy(poke_list: [Pokemon()], verbose: bool = False):
    max_entropy = -1
    max_poke = None
    for poke in poke_list:
        entropy = compute_entropy_for_a_poke(poke, poke_list)
        if verbose:
            print(f"Evaluating {poke.Name}: \tentropy = {entropy}")
        if entropy > max_entropy:
            max_entropy = entropy
            max_poke = poke
            if verbose:
                print(f"New max found: {max_poke.Name} with entropy = {max_entropy}")
    if verbose:
        print(f"Maximum entropy is {max_entropy} with {max_poke.Name}") if not max_poke == None else print("")
    return max_poke, max_entropy

############################################################################################################
#   Statistics functions
############################################################################################################

def test_average_attempts_with_entropy():
    number_of_games = 100
    poke_list = get_pokemon_list_with_data()
    total_attempts = 0
    for i in tqdm(range(number_of_games)):
        last_remaining_pokes_size = 0
        game = GameState()
        while not game.is_poke_found:
            last_remaining_pokes_size = len(game.remaining_pokes)
            if len(game.remaining_pokes) == len(game.poke_list):
                game.last_tested_poke = find_poke_with_name("Onix", game.remaining_pokes)
            elif len(game.remaining_pokes) < len(game.poke_list):
                game.last_tested_poke = max_entropy(game.remaining_pokes)[0]
            game.tested_pokes.insert(0, game.last_tested_poke)
            game.combinaison.insert(0,get_comparaison_with_poke(game.last_tested_poke, game.choosen_poke))
            game.remaining_pokes.remove(game.last_tested_poke)
            game.remaining_pokes = find_compatibles_pokes_with_combinaison(game.last_tested_poke, base_10_to_5(game.combinaison[0]), game.remaining_pokes)
            #game.reduction_history_poke_list_size.append(last_remaining_pokes_size - len(game.remaining_pokes))

            if game.last_tested_poke == game.choosen_poke:
                print(f"Score: {len(game.tested_pokes)}")
                print(f"Poke found: {game.last_tested_poke.Name}")
                print("Guesses: ", [poke.Name for poke in game.tested_pokes])
                #print("Reductions: ", game.reduction_history_poke_list_size)
                game.display_combi_and_poke()
                game.is_poke_found = True
                total_attempts += len(game.tested_pokes)
    print(f"Average attempts: {total_attempts / number_of_games}")
    
    
############################################################################################################
#   Game functions
############################################################################################################

class GameState:
    choosen_poke: Pokemon()
    poke_list: [Pokemon()]
    tested_pokes: [Pokemon()]
    combinaison: [int]
    reduction_history_poke_list_size: [int] = []
    last_tested_poke: Pokemon()
    remaining_pokes: [Pokemon()]
    is_poke_found = False
    
    def __init__(self):
        self.poke_list = get_pokemon_list_with_data()
        self.choosen_poke = get_random_poke(self.poke_list)
        self.tested_pokes = []
        self.combinaison = [WRONG*7]
        self.remaining_pokes = self.poke_list.copy()
        
    def display_combinaison(self):
        print(convert_combinaison_to_visual(base_10_to_5(self.combinaison[0])))
    
    def display_combi_and_poke(self):
        print("1️⃣2️⃣🏞️🌈🔄📏⚖️")
        for i in range(len(self.tested_pokes)-1, -1, -1):
            poke = self.tested_pokes[i]
            combi = self.combinaison[i]
            print(convert_combinaison_to_visual(base_10_to_5(combi)), " ", poke.Name)

    def ask_for_combinaison(self):
        isValid = False
        while not isValid:
            # A valid combinaison is 7 characters long, each character is a number between 0 and 4 or each character is an emoji (🟩🟥🟧⬇️⬆️)
            input_combinaison = input(f"Give the result combinaison for {self.last_tested_poke.Name} (7 characters, 0 to 4 or 🟩🟥🟧⬇️⬆️):\n")
            input_combinaison.replace(" ","").replace('️',"")
            if (len(input_combinaison) - count_arrow_in_string(input_combinaison)) != 7 and (not re.match("^[0-4]*$", input_combinaison) or not re.match("^[🟩🟥🟧⬇️⬆️⬆⬇]*$", input_combinaison)):
                    print("Invalid combinaison. Try again.")
                    continue
            isValid = True
        if re.match("^[0-4]*$", input_combinaison):
            return input_combinaison
        else:
            # Transform string emoji to an int combinaison, example: 🟩🟥🟧🟩🟥🟥⬆️ -> 0220014
            listStr = [char for char in input_combinaison]
            for i in range(listStr.count('️')):
                listStr.pop(listStr.index('️'))
            return "".join(map(str, convert_visual_to_combinaison(listStr)))     

def ask_for_poke(poke_list: [Pokemon()]):
    isValid = False
    while not isValid:
        input_poke = input("Choose a Pokemon you want to try\n").lower()
        available_pokes = [poke.Name for poke in poke_list if poke.Name.lower().startswith(input_poke)]
        if len(available_pokes) == 0:
            print("No pokemons found with that name. Try again.")
            continue
        elif len(available_pokes) == 1:
            print(f"You chose {available_pokes[0]}")
            return find_poke_with_name(available_pokes[0], poke_list)
        else:
            print("Available pokemons:")
            for poke in available_pokes:
                print(poke)
            continue       
        
def print_comparaison_between_poke(poke1: Pokemon(), poke2: Pokemon()):
    print(poke1.Name, " ", poke2.Name)
    comparaison = base_10_to_5(get_comparaison_with_poke(poke1, poke2))
    print(comparaison)
    print(convert_combinaison_to_visual(comparaison))
    
def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')
        
def play_game():
    game = GameState()
    clear_screen()
    while not game.is_poke_found:
        game.last_tested_poke = ask_for_poke(set(game.poke_list).symmetric_difference(game.tested_pokes))
        game.tested_pokes.insert(0, game.last_tested_poke)
        game.combinaison.insert(0,get_comparaison_with_poke(game.last_tested_poke, game.choosen_poke))
        clear_screen()
        game.display_combi_and_poke()
        if game.last_tested_poke == game.choosen_poke:
            game.is_poke_found = True
            print("You found the pokemon!")
            
def play_assisted_game():
    game = GameState()
    clear_screen()
    while not game.is_poke_found:
        #if it's not the first poke tested, calculate entropy because the best initial poke is Bel'Veth
        if len(game.remaining_pokes) < len(game.poke_list):
            #calculate entropy
            max_entropy(game.remaining_pokes, verbose =True)      
        if len(game.remaining_pokes) <= 5:
            for poke in game.remaining_pokes:
                print(poke.Name)
        game.last_tested_poke = ask_for_poke(set(game.poke_list).symmetric_difference(game.tested_pokes))
        game.tested_pokes.insert(0, game.last_tested_poke)
        game.combinaison.insert(0,get_comparaison_with_poke(game.last_tested_poke, game.choosen_poke))
        game.remaining_pokes.remove(game.last_tested_poke)
        game.remaining_pokes = find_compatibles_pokes_with_combinaison(game.last_tested_poke, base_10_to_5(game.combinaison[0]), game.remaining_pokes)
        clear_screen()
        game.display_combi_and_poke()
        if game.last_tested_poke == game.choosen_poke:
            game.is_poke_found = True
            print("You found the pokemon!")
            for poke in game.remaining_pokes:
                print(poke.Name)
                
def play_cheat_online_game():
    game = GameState()
    clear_screen()
    while not game.is_poke_found:
        if len(game.remaining_pokes) < len(game.poke_list):
            max_entropy(game.remaining_pokes, verbose =True)
        if len(game.remaining_pokes) == 0:
            print("Your combinaison is wrong, there is no possible pokemon left")
            break
        if len(game.remaining_pokes) <= 5:
            for poke in game.remaining_pokes:
                print(poke.Name)
        game.last_tested_poke = ask_for_poke(set(game.poke_list).symmetric_difference(game.tested_pokes))
        print("Now enter this pokemon on the website")
        game.tested_pokes.insert(0, game.last_tested_poke)
        combi = game.ask_for_combinaison()
        game.combinaison.insert(0,int(combi, 5))
        game.remaining_pokes = find_compatibles_pokes_with_combinaison(game.last_tested_poke, base_10_to_5(game.combinaison[0]), game.remaining_pokes)
        clear_screen()
        game.display_combi_and_poke()
        if game.combinaison[0] == EXACT*7:
            game.is_poke_found = True
            print("You found the pokemon!")
        
        

############################################################################################################
#   Test functions
############################################################################################################
    
def test_aspects():
    while True:
        poke_list = get_pokemon_list_with_data()
        poke1 = ask_for_poke(poke_list)
        poke2 = ask_for_poke(poke_list)
        
        print_comparaison_between_poke(poke1, poke2)
        
def test_compatibles_pokes():
    poke_list = get_pokemon_list_with_data()
    poke = ask_for_poke(poke_list)
    combi = input("Give a combinaison\n")
    combi = convert_string_to_combinaison(combi)

    compatibles_pokes = find_compatibles_pokes_with_combinaison(poke, combi, poke_list)
    for poke in compatibles_pokes:
        print(poke.Name)
        
def test_maximum_entropy():
    poke_list = get_pokemon_list_with_data()
    max_poke, max_entrop = max_entropy(poke_list, verbose=True)
    print(f"Maximum entropy is {max_entrop} with {max_poke.Name}")
            
def update_with_static_progress_bar():
    static_text = "Static Text: "
    dynamic_text = "Dynamic Data: {}%"

    for progress in range(101):
        terminal_content = static_text + dynamic_text.format(progress)
        print(terminal_content, end="\r", flush=True)
        time.sleep(0.1)  # Simulate some work being done

    print("\nTask completed!")

############################################################################################################
#   Main
############################################################################################################

def display_choice_menu(stdscr):
    valid_inputs = {
        "up": [ord("w"), ord("z"), curses.KEY_UP],
        "down": [ord("s"), curses.KEY_DOWN],
    }
    modes = ["Play", "Play with help", "Play interactive for online"]
    index = 0

    while True:
        stdscr.clear()

        # Display menu options with arrow logo
        stdscr.addstr("Choose a mode: (up ^ / down v / enter)")
        for i in range(len(modes)):
            if i == index:
                stdscr.addstr(f"\n[X] {modes[i]}", curses.COLOR_CYAN)
            else:
                stdscr.addstr(f"\n[ ] {modes[i]}")

        # Get user input
        key = stdscr.getch()

        # Update selection based on user input
        if key in valid_inputs["up"]:
            index = (index - 1) % len(modes)
        elif key in valid_inputs["down"]:
            index = (index + 1) % len(modes)
        elif key == ord('\n'):
            return str(index + 1)

        stdscr.refresh()
        
def play_menu():
    clear_screen()

    choice = curses.wrapper(display_choice_menu)
    
    if choice == "1":
        play_game()
    elif choice == "2":
        play_assisted_game()
    elif choice == "3":
        play_cheat_online_game()
    
def main():    
    #test_aspects()
    #test_compatibles_pokes()
    #test_maximum_entropy()    
    #test_average_attempts_with_entropy()

    play_menu()
        
if __name__ == "__main__":
    main()