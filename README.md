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

create a file called `.dmenutrello` in your home directory with your Trello key & token and your dmenu appearance settings

	[TRELLO]
	key = YOUR_TRELLO_KEY
	token = YOUR_TRELLO_TOKEN

        [DMENU]
        font = DejaVu Sans Mono for Powerline-14
        background_selected = #2aa198
        foreground_selected = #191919
        foreground = #2aa198
        background = #191919


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
- open comments in vim and save them
- open links in webbrowser
- mark cards as checked
