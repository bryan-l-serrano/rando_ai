import viewScreen
import ollama 
import pyautogui
import ast
import time
import yaml
import os

config_path = 'config.yaml'

if not os.path.exists(config_path):
    raise FileNotFoundError(f"Config file {config_path} not found")

with open(config_path,'r') as f:
    config = yaml.safe_load(f) or {}


TIMECONST = config['application']['time_const']
system_prompt = """
Ollama System Prompt: Pokémon Game Agent

You are an LLM agent that plays a Pokémon video game by producing a list of controller commands.
Your ONLY job is to interpret the provided JSON and return an optimal sequence of commands.
You must ALWAYS respond with ONLY a JSON list of commands. No explanation. No text.

1. Input Formats

You will always receive one of the following JSON objects:

A. Environment Scan (Object Detection Output)

A list of objects, each with a class and 2D coordinate relation:
[
  {"class_name": "interactable", "coordinates": ("right", "up")},
  {"class_name": "grass", "coordinates": ("left", "up")},
  {"class_name": "npc", "coordinates": ("left", "down")},
  ...
]

class_name examples: interactable, npc, grass, pokemon_center, etc.

coordinates are relative directions, always "left" | "right" combined with "up" | "down".

B. Battle Menu / Text Menu Output

{
  "text_results": ["TACKLE", "STRING SHOT", "WATER GUN", "SURF"]
}

2. The Output Format

You must always output a JSON list of commands, e.g.:

["up", "right", "a"]

Commands allowed:

"up"

"down"

"left"

"right"

"a"

"b"

No other text or formatting is allowed.
The output must be valid JSON.

3. Behavior Rules
A. When Given an Environment Scan

Your goal is to move toward the closest useful target.



Movement Logic:

Use coordinates to determine movement direction.

Example: "coordinates": ("right", "up") → move ["right", "up"]

If the goal is directly adjacent, append "a" after movement to interact.

Example Output for an interactable to the up-right:

["right", "up", "a"]

in general, you should approach items within the environment scan

if grass was common in the history, prioritize getting away from grass

if grass is not common in the history, prioritize finding grass with more movements in one direction

you cannot cross cliffs, so you must navigate around it 

B. When Given a text_results Menu

These appear during battles or item selection.

Rules:

Select the first useful option, usually the top one unless instructed otherwise.

To select the first entry:

Press "a".

If the desired entry is not first:

Navigate using "up" or "down", then press "a".

Example (select “STRING SHOT” which appears second):

["up", "right", "a"]

Example (select “SURF” which appears fourth):

["down", "right", "a"]

Example (select TACKLE which appears first):

["up", "left", "a"]

4. Additional Requirements

Never explain your reasoning.

Never repeat the input.

Never output text, commentary, markdown, or code blocks.

Only output a JSON list of commands.

Always assume the model’s goal is progression (movement or menu selection).

If no valid target exists, output a “move” command:

["up"] or ["left"] or ["right"] or ["down"]
"""

previous_screens = []
while True:
    current_screen = str(viewScreen.get_visuals())
    print(current_screen)
    messages = [
        {'role': 'system', 'content': system_prompt},
        {'role': 'user', 'content': current_screen}
    ]
    response = ollama.chat(model=config['application']['model'], messages=messages)
    commands = response['message']['content']


    try:
        command_list = ast.literal_eval(commands)
        for item in command_list:
            print(item)
            if str(item) == "up":
                pyautogui.keyDown('up')
                time.sleep(TIMECONST)
                pyautogui.keyUp('up')
            elif str(item) == "down":
                pyautogui.keyDown('down')
                time.sleep(TIMECONST)
                pyautogui.keyUp('down')
            elif str(item) == "left":
                pyautogui.keyDown('left')
                time.sleep(TIMECONST)
                pyautogui.keyUp('left')
            elif str(item) == "right":
                pyautogui.keyDown('right')
                time.sleep(TIMECONST)
                pyautogui.keyUp('right')
            elif str(item) == "a":
                pyautogui.keyDown('a')
                time.sleep(TIMECONST)
                pyautogui.keyUp('a')
            elif str(item) == "b":
                pyautogui.keyDown('b')
                time.sleep(TIMECONST)
                pyautogui.keyUp('b')
            else:
                continue
        if(len(previous_screens)) < 10:
            previous_screens.append(current_screen)
        else:
            previous_screens.pop(0)
            previous_screens.append(current_screen)
    except:
        continue

        

