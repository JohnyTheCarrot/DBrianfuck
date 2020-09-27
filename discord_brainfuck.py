import sys
import re
help = "python3 discord_brainfuck.py [dbf_code_file_here] [bot token file]"

if len(sys.argv) != 3:
    print(help)
    exit(0)

f = open(sys.argv[1], 'r')
all_code = f.read()
f.close()

cells = [0]
current_cell = 0

def match_bracket(text: str,left_br: str,right_br: str,start: int):
  top = 0
  pos = start
  pattern = f"[{left_br}{right_br}]"
  remaining_string = text[start:len(text)]
  next_match = re.search(pattern,remaining_string)
  while next_match:
    pos+=next_match.span()[1]
    if re.search(left_br,next_match.group()):
      top+=1
    elif re.search(right_br,next_match.group()):
      top-=1
    if top==0:
      break
    remaining_string = remaining_string[next_match.span()[1]:len(remaining_string)+1]
    next_match = re.search(pattern,remaining_string)
  if next_match:
    return pos-1
  else:
    raise Exception(f"No closing bracket found for bracket at {start}")

def insert_to_cell(cell: int, value: int):
    if cell > len(cells):
        for c in range(len(cells)-cell):
            cells.append(0)
    try:
        cells[cell] = value
    except:
        cells.append(value)

def get_from_cell(cell: int):
    try:
        return cells[cell]
    except IndexError:
        return 0

def increment_cell_value(cell: int):
    cur_cell = get_from_cell(cell)
    if cur_cell > 255:
        insert_to_cell(cell, 0)
    else:
        insert_to_cell(cell, cur_cell+1)

def decrement_cell_value(cell: int):
    cur_cell = get_from_cell(cell)
    if cur_cell > 255:
        insert_to_cell(cell, 0)
    else:
        insert_to_cell(cell, cur_cell-1)

def print_cells():
    to_print = ""
    for cell in cells:
        to_print += f"[{cell}]"
    print(to_print)

commands = []

index = 0
def interpret(code: str, index: int):
    global current_cell
    while index+1 != len(code):
        char = code[index]
        if char == ">":
            current_cell+=1
        elif char == "<":
            current_cell-=1
        elif char == "+":
            increment_cell_value(current_cell)
        elif char == "-":
            decrement_cell_value(current_cell)
        elif char == "[":
            current_cell_value = get_from_cell(current_cell)
            if current_cell_value == 0:
                index = match_bracket(code,"\[","\]",index)
        elif char == "]":
            current_cell_value = get_from_cell(current_cell)
            if current_cell_value != 0:
                reversed_code = code[::-1]
                #this looks disgusting only due to weird inversion tricks and off by one errors
                index = len(code)-(match_bracket(reversed_code,"\]","\[",len(code)-index-1)+1)
        elif char == ",":
            insert_to_cell(current_cell, ord(input("")[0]))
        elif char == "$":
            commands.append({"trigger": "", "response": ""})
        elif char == "*":
            commands[len(commands)-1]["trigger"] += chr(get_from_cell(current_cell))
        elif char == "!":
            commands[len(commands)-1]["response"] += chr(get_from_cell(current_cell))
        elif char == ".":
            print(chr(get_from_cell(current_cell)), end = "")
        index+=1

interpret(all_code, 0)
#print(commands)
for command in commands:
    print(f"Added command {command['trigger']}")

# Discord Bot

import discord

client = discord.Client()

@client.event
async def on_message(message):
    for command in commands:
        if message.content == command["trigger"]:
            await message.channel.send(command["response"])
            return

client.run(open(sys.argv[2], "r").read())
