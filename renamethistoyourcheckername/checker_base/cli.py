from array import array
import asyncio
import os

def print_title():
    clear()
    print("""
███╗   ██╗███████╗██╗  ██╗██╗   ██╗███████╗    ██████╗  ██████╗ 
████╗  ██║██╔════╝╚██╗██╔╝██║   ██║██╔════╝   ██╔════╝ ██╔════╝ 
██╔██╗ ██║█████╗   ╚███╔╝ ██║   ██║███████╗   ██║  ███╗██║  ███╗
██║╚██╗██║██╔══╝   ██╔██╗ ██║   ██║╚════██║   ██║   ██║██║   ██║
██║ ╚████║███████╗██╔╝ ██╗╚██████╔╝███████║██╗╚██████╔╝╚██████╔╝
╚═╝  ╚═══╝╚══════╝╚═╝  ╚═╝ ╚═════╝ ╚══════╝╚═╝ ╚═════╝  ╚═════╝ """)
    print()


def query_option(name: str, options: list) -> int:
    print_title()
    print(f'[{name}]\n')
    for i, option in enumerate(options,1):
        print(f'[{i}] {option}')
        
    print()
    
    option = pretty_input('Select an option')
    return int(option) if option else None

def pretty_input(name: str) -> str:
    try:
        value = input(f'==> {name}: ')
        return value
    except ValueError:
        return None

def clear(): 
    os.system('cls' if os.name == 'nt' else 'clear') 
    # pass

        
def print_box(lines: list[str], indent=2):
    length = 0
    for line in lines:
        if len(line) > length:
            length = len(line)
    """Print message-box with optional title."""
    # space = " " * (indent*2)

    box = f'╔{"".ljust(length + indent, "═")}╗\n'
    for line in lines:
        print(length - len(line))
        add = length - len(line)
        box += f'║ {line}{"".ljust(add, " ")} ║\n'

    box += f'╚{"".ljust(length + indent, "═")}╝'

    print(box)