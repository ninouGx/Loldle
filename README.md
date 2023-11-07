# Loldle - Python Terminal Edition (not official)

**Loldle** brings the classic Loldle game to your terminal! 
Experimental use to try some statistical optimization strategies while reliving the essence of the original game.

## Features

- Classic Loldle gameplay in your terminal.
- Assisted mode (use the algorithm and give champions with best entropy).
- Online version helper (give you the best entropy champions when playing the official game).
- Chromium Extension to retrieve the champions combinations easier by copying it in the terminal.
- Test optimization techniques.

## Get Started
1. `git clone https://github.com/ninouGx/Loldle`
2. `cd Loldle`
3. `python App/loldleApp.py`

### Use the Extension
On a chromium browser:
1. Go to `chrome://extensions/`
2. Enable `Developer mode`
3. Click on `Load unpacked`
4. Select the `Extension` folder of the project
5. Go to [https://loldle.net/classic](https://loldle.net/classic)
6. Click on the extension icon
7. Copy the champions combination in the terminal

### To Scrap Data
1. `cd Loldle`
2. `source loldle/bin/activate`
3. `python Data/retreieveCharacter.py` *you need to find the character of the day*

## Informations (number to input for each category)
- 🟩 Exact match -> **0**
  
  🟧 Partial match (atleast one correct element) -> **1**
  
  🟥 No corresponding with the champion -> **2**
  
  ⬇️ The champion has been release before (ex: yours in 2022 and 2016 for the one to find) -> **3**
  
  ⬆️ The champion has been release after -> **4**
  #

- 🚹 Gender
  
  📍 Roles
  
  🦄 Species
  
  ⭐️ Ressource (like mana or energy)
  
  🗡️ Range Type
  
  🌎 Region(s) (like Ionia or Shurima)
  
  🕰️ Release Date
  #

Source videos:
  
  - [ScienceEtonnante - JE CRAQUE WORDLE !](https://www.youtube.com/watch?v=iw4_7ioHWF4&pp=ygUXd29yZGxlIHNjaWVuY2VldG9ubmFudGU%3D)
  
  - [3Blue1Brown - Solving Wordle using information theory](https://www.youtube.com/watch?v=v68zYyaEmEA&t=0s)
  #

Official Game Source: [https://loldle.net/classic](https://loldle.net/classic)
