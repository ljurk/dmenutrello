[![PyPI version](https://badge.fury.io/py/dmenutrello.svg)](https://badge.fury.io/py/dmenutrello)

# dmenutrello

## trello for dmenu

### Installation

Install dmenu
for Arch-based distros:

	pacman -S dmenu

for Debian-based distros:

	apt-get install dmenu

to install my package simply type

    pip install dmenutrello --user

### Usage

create a file called `.dmenutrello` in your home directory with this content:

- your Trello key & token
- your dmenu appearance settings
- the terminal in which vim will be opened
- the dmenu command (if you want to use rofi you have to place a script with the content `rofi -dmenu` somewhere and put the path to it to command config value)

like this:
```
[TRELLO]
key = YOUR_TRELLO_KEY
token = YOUR_TRELLO_TOKEN

[DMENU]
font = DejaVu Sans Mono for Powerline-14
background_selected = #2aa198
foreground_selected = #191919
foreground = #2aa198
background = #191919
command = dmenu

[TERMINAL]
terminal = urxvt
terminal_argument = -e

```

to use this script call

    dmenutrello

example i3 key binding

    bindsym $mod+t exec $HOME/.local/bin/dmenutrello



you can navigate through your boards, lists, cards and comments

by typing in a new name the corresponding element will be added


### todo

- [x] basic navigation
- [x] add a .. option to go up one level
- [x] add objects(board, lists, cards, comments)
- [x] open comments in vim and save them
- open links in webbrowser
- mark cards as checked
