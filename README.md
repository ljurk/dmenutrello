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

create a file called .dmenutrello in your home directory with the following content

	[TRELLO]
	key = YOUR_TRELLO_KEY
	token = YOUR_TRELLO_TOKEN


to use this script call 

    dmenutrello

example i3 key binding

    bindsym $mod+t exec $HOME/.local/bin/dmenutrello



you can navigate through your boards, lists, cards and comments

by typing in a new name the corresponding element will be added


### todo

- add a .. option to go up one level
- open comments in vim and save them
- open links in webbrowser
- mark cards as checked
