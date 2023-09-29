import math
import csv
import numpy as np
import os
from tqdm import tqdm
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
CHAMP_LIST = os.path.join(DATA_DIR, "champions_data.csv")

############################################################################################################
#   Data functions
############################################################################################################

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
        result[6] = AFTER if try_champ.ReleaseYear < choosen_champ.ReleaseYear else BEFORE
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

############################################################################################################
#   Entropy functions
############################################################################################################

def calculate_each_combinaison(champ_to_test: Champion(), champ_list: [Champion()]):
    result = []
    for champ in champ_list:
        result.append(get_comparaison_with_champ(champ_to_test, champ))
    return result

# Return the list of champs that can be the choosen champ regarding their compatibility with the combinaison
# Example: with alistar, if combinaison is [0, 2, 1, 0, 2, 2, 5]  (🟩🟥🟧🟩🟥🟥⬆️) 
# the champ have to be a male, not a support, be a minotaur with other species, have mana, not a melee, not from runeterra and be released strictly after 2009 (>= 2010)
def find_compatibles_champs_with_combinaison(champion : Champion(), combinaison: [int], champ_list: [Champion()]):
    result = []
    for champ in champ_list:
        comparaison = base_10_to_5(get_comparaison_with_champ(champion, champ))
        for i in range(len(comparaison)):
            if not (combinaison[i] == comparaison[i] or combinaison[i] == ATLEAST and comparaison[i] == EXACT):
                break
            if i == len(comparaison) - 1:
                result.append(champ)
    return result

def compute_entropy_for_a_champ(champ: Champion(), possible_champs: [Champion()]):
    #besoin solutions possibles, du champion, 
    entropy = 0
    for champ_to_test in possible_champs:
        combinaison = base_10_to_5(get_comparaison_with_champ(champ, champ_to_test))
        compatibles_champs = find_compatibles_champs_with_combinaison(champ, combinaison, possible_champs)
        p = len(compatibles_champs) / len(possible_champs)
        if p > 0:
            entropy += - p * math.log(p, 2)
    return entropy

def max_entropy(champ_list: [Champion()], verbose: bool = False):
    max_entropy = -1
    max_champ = None
    for champ in champ_list:
        entropy = compute_entropy_for_a_champ(champ, champ_list)
        if verbose:
            print(f"Evaluating {champ.Name}: \tentropy = {entropy}")
        if entropy > max_entropy:
            max_entropy = entropy
            max_champ = champ
            if verbose:
                print(f"New max found: {max_champ.Name} with entropy = {max_entropy}")
    if verbose:
        print(f"Maximum entropy is {max_entropy} with {max_champ.Name}") if not max_champ == None else print("")
    return max_champ, max_entropy

############################################################################################################
#   Statistics functions
############################################################################################################

def test_average_attempts_with_entropy():
    number_of_games = 100
    champ_list = get_champ_list_with_data()
    total_attempts = 0
    for i in tqdm(range(number_of_games)):
        last_remaining_champs_size = 0
        game = GameState()
        while not game.is_champ_found:
            last_remaining_champs_size = len(game.remaining_champs)
            if len(game.remaining_champs) == len(game.champ_list):
                game.last_tested_champ = find_champ_with_name("Bel'Veth", game.remaining_champs)
            elif len(game.remaining_champs) < len(game.champ_list):
                game.last_tested_champ = max_entropy(game.remaining_champs)[0]
            game.tested_champs.insert(0, game.last_tested_champ)
            game.combinaison.insert(0,get_comparaison_with_champ(game.last_tested_champ, game.choosen_champ))
            game.remaining_champs.remove(game.last_tested_champ)
            game.remaining_champs = find_compatibles_champs_with_combinaison(game.last_tested_champ, base_10_to_5(game.combinaison[0]), game.remaining_champs)
            #game.reduction_history_champ_list_size.append(last_remaining_champs_size - len(game.remaining_champs))

            if game.last_tested_champ == game.choosen_champ:
                print(f"Score: {len(game.tested_champs)}")
                print(f"Champ found: {game.last_tested_champ.Name}")
                print("Guesses: ", [champ.Name for champ in game.tested_champs])
                #print("Reductions: ", game.reduction_history_champ_list_size)
                game.display_combi_and_champ()
                game.is_champ_found = True
                total_attempts += len(game.tested_champs)
    print(f"Average attempts: {total_attempts / number_of_games}")
    
    
############################################################################################################
#   Game functions
############################################################################################################

class GameState:
    choosen_champ: Champion()
    champ_list: [Champion()]
    tested_champs: [Champion()]
    combinaison: [int]
    reduction_history_champ_list_size: [int] = []
    last_tested_champ: Champion()
    remaining_champs: [Champion()]
    is_champ_found = False
    
    def __init__(self):
        self.champ_list = get_champ_list_with_data()
        self.choosen_champ = get_random_champ(self.champ_list)
        self.tested_champs = []
        self.combinaison = [WRONG*7]
        self.remaining_champs = self.champ_list.copy()
        
    def display_combinaison(self):
        print(convert_combinaison_to_visual(base_10_to_5(self.combinaison[0])))
    
    def display_combi_and_champ(self):
        print("🚹📍🦄⭐️🗡️ 🌎🕰️")
        for i in range(len(self.tested_champs)-1, -1, -1):
            champ = self.tested_champs[i]
            combi = self.combinaison[i]
            print(convert_combinaison_to_visual(base_10_to_5(combi)), " ", champ.Name)


def ask_for_champ(champ_list: [Champion()]):
    isValid = False
    while not isValid:
        input_champ = input("Choose a champion\n").lower()
        available_champs = [champ.Name for champ in champ_list if champ.Name.lower().startswith(input_champ)]
        if len(available_champs) == 0:
            print("No champions found with that name. Try again.")
            continue
        elif len(available_champs) == 1:
            print(f"You chose {available_champs[0]}")
            return find_champ_with_name(available_champs[0], champ_list)
        else:
            print("Available champions:")
            for champ in available_champs:
                print(champ)
            continue

def ask_for_combinaison():
    isValid = False
    while not isValid:
        # A valid combinaison is 7 characters long, each character is a number between 0 and 4 or each character is an emoji (🟩🟥🟧⬇️⬆️)
        input_combinaison = input("Give the combinaison (7 characters, 0 to 4 or 🟩🟥🟧⬇️ ⬆️\n")
        if len(input_combinaison) != 7:
            if not re.match("^[0-4]*$", input_combinaison) and not re.match("^[🟩🟥🟧⬇️⬆️]*$", input_combinaison):
                print("Invalid combinaison. Try again.")
                continue
        isValid = True
    if re.match("^[0-4]*$", input_combinaison):
        return input_combinaison
    else:
        # Transform string emoji to an int combinaison, example: 🟩🟥🟧🟩🟥🟥⬆️ -> 0220014
        print("You chose: ",convert_visual_to_combinaison(input_combinaison))
        print("test", EXACT, ATLEAST, WRONG, BEFORE, AFTER)
        listStr = [char for char in input_combinaison]
        listStr.pop() # To remove the null character at the end
        return "".join(map(str, convert_visual_to_combinaison(listStr)))     
        
        
def print_comparaison_between_champ(champ1: Champion(), champ2: Champion()):
    print(champ1.Name, " ", champ2.Name)
    comparaison = base_10_to_5(get_comparaison_with_champ(champ1, champ2))
    print(comparaison)
    print(convert_combinaison_to_visual(comparaison))
    
def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')
        
def play_game():
    game = GameState()
    clear_screen()
    while not game.is_champ_found:
        game.last_tested_champ = ask_for_champ(set(game.champ_list).symmetric_difference(game.tested_champs))
        game.tested_champs.insert(0, game.last_tested_champ)
        game.combinaison.insert(0,get_comparaison_with_champ(game.last_tested_champ, game.choosen_champ))
        clear_screen()
        #game.display_combinaison()
        game.display_combi_and_champ()
        if game.last_tested_champ == game.choosen_champ:
            game.is_champ_found = True
            print("You found the champion!")
            
def play_assisted_game():
    game = GameState()
    clear_screen()
    while not game.is_champ_found:
        #if it's not the first champ tested, calculate entropy because the best initial champ is Bel'Veth
        if len(game.remaining_champs) < len(game.champ_list):
            #calculate entropy
            max_entropy(game.remaining_champs, verbose =True)      
        if len(game.remaining_champs) <= 5:
            for champ in game.remaining_champs:
                print(champ.Name)
        game.last_tested_champ = ask_for_champ(set(game.champ_list).symmetric_difference(game.tested_champs))
        game.tested_champs.insert(0, game.last_tested_champ)
        game.combinaison.insert(0,get_comparaison_with_champ(game.last_tested_champ, game.choosen_champ))
        game.remaining_champs.remove(game.last_tested_champ)
        game.remaining_champs = find_compatibles_champs_with_combinaison(game.last_tested_champ, base_10_to_5(game.combinaison[0]), game.remaining_champs)
        clear_screen()
        #game.display_combinaison()
        game.display_combi_and_champ()
        if game.last_tested_champ == game.choosen_champ:
            game.is_champ_found = True
            print("You found the champion!")
            for champ in game.remaining_champs:
                print(champ.Name)
def play_cheat_online_game():
    game = GameState()
    clear_screen()
    while not game.is_champ_found:
        if len(game.remaining_champs) < len(game.champ_list):
            max_entropy(game.remaining_champs, verbose =True)
        if len(game.remaining_champs) == 0:
            print("Your combinaison is wrong, there is no possible champion left")
            break
        if len(game.remaining_champs) <= 5:
            for champ in game.remaining_champs:
                print(champ.Name)
        game.last_tested_champ = ask_for_champ(set(game.champ_list).symmetric_difference(game.tested_champs))
        game.tested_champs.insert(0, game.last_tested_champ)
        combi = ask_for_combinaison()
        game.combinaison.insert(0,int(combi, 5))
        game.remaining_champs = find_compatibles_champs_with_combinaison(game.last_tested_champ, base_10_to_5(game.combinaison[0]), game.remaining_champs)
        clear_screen()
        game.display_combi_and_champ()
        if game.combinaison[0] == EXACT*7:
            game.is_champ_found = True
            print("You found the champion!")
        
        

############################################################################################################
#   Test functions
############################################################################################################
    
def test_aspects():
    while True:
        champ_list = get_champ_list_with_data()
        champ1 = ask_for_champ(champ_list)
        champ2 = ask_for_champ(champ_list)
        
        print_comparaison_between_champ(champ1, champ2)
        
def test_compatibles_champs():
    champ_list = get_champ_list_with_data()
    champ = ask_for_champ(champ_list)
    combi = input("Give a combinaison\n")
    combi = convert_string_to_combinaison(combi)

    compatibles_champs = find_compatibles_champs_with_combinaison(champ, combi, champ_list)
    for champ in compatibles_champs:
        print(champ.Name)
        
def test_maximum_entropy():
    champ_list = get_champ_list_with_data()
    max_champ, max_entrop = max_entropy(champ_list)
    print(f"Maximum entropy is {max_entrop} with {max_champ.Name}")
          
import curses

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

            
def update_with_static_progress_bar():
    static_text = "Static Text: "
    dynamic_text = "Dynamic Data: {}%"

    for progress in range(101):
        terminal_content = static_text + dynamic_text.format(progress)
        print(terminal_content, end="\r", flush=True)
        time.sleep(0.1)  # Simulate some work being done

    print("\nTask completed!")
    
def main():    
    #test_aspects()
    #test_compatibles_champs()
    #test_maximum_entropy()
    
    #test_average_attempts_with_entropy()
    
    #play_cheat_online_game()
    #play_assisted_game()
    #play_game() /home/ninou/Documents/Dev/Lolidle/App

    clear_screen()

    choice = curses.wrapper(display_choice_menu)
    

    if choice == "1":
        play_game()
    elif choice == "2":
        play_assisted_game()
    elif choice == "3":
        play_cheat_online_game()
        
if __name__ == "__main__":
    main()