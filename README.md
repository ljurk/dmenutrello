# dmenutrello

## trello for dmenu

### Installation

    pip install dmenutrello --user

### Usage

create a file called .dmenutrello in your home directory with the folowing content

	[TRELLO]
	key = YOUR_TRELLO_KEY
	token = YOUR_TRELLO_TOKEN


to use this script with your trello, pass your key and token to dmenutrello

    dmenutrello

example for i3

    bindkey $mod+t dmenutrello

you can navigate throug your boards, lists, cards and comments, by typing in a new name the corresponding element will be added


### todo

- open comments in vim and save them
- open links in webbrowser
- mark cards as checked
