import functools
import dmenu
import configparser
from os.path import expanduser
from trello import TrelloClient

#constants
BOARDS = 0
LISTS = 1
CARDS = 2
COMMENTS = 3

dmenu_show= functools.partial(dmenu.show, font='DejaVu Sans Mono for Powerline-14', background_selected='#2aa198',foreground_selected='#191919', foreground='#2aa198', background='#191919')

def show(mode, data, parent, prompt):
    out = dmenu_show(data.keys(), prompt=prompt)
    board = None
    #check for match
    if out in data:
        match = True
        #save object for return, 'this' is the parent of the underlying object
        this = data[out]
        #override match with new dictionary and fill it
        data[out] = {}
        if mode == BOARDS:
            for d in this.list_lists():
                data[out][d.name] = d
        elif mode == LISTS:
            for d in this.list_cards():
                data[out][d.name] = d
        elif mode == CARDS:
            for d in this.get_comments():
                data[out][d.name] = d

        return data[out], this
    elif out is not None:
        #no match, add new and call this function again with another prompt
        if mode == BOARDS:
            data[out] = parent.add_board(out)
        elif mode == LISTS:
            data[out] = parent.add_list(out)
        elif mode == CARDS:
            data[out] = parent.add_card(out)
        return show(mode, data, parent, "ok")

def menu(key, token):
    client = TrelloClient(
        api_key = key,
        api_secret = token
        )
    match = False

    #client.list_boards()
    #client.add_board()
    #board.list_lists()
    #board.add_list()
    #list.list_cards()
    #list.add_card()
    #card.get_comments()
    #names.append(board.name+ " #" + str(len(board.list_lists())))

    data = {}
    matchedData = None
    #initial filling
    for board in client.list_boards():
        data[board.name] = board

    #matchedData = show(BOARDS, data, client, '')
    data, parent = show(BOARDS, data, client, '')
    print(data)
    print(parent)
    data, parent  = show(LISTS, data, parent, '')
    print(data)
    print(parent)
    data, parent  = show(CARDS, data, parent, '')
    print(data)
    print(parent)

def main():
    config = configparser.ConfigParser()
    config.read(expanduser('~/.dmenutrello'))

    key = config.get('TRELLO', 'key')
    token = config.get('TRELLO', 'token')

    menu(key, token)

if __name__ == '__main__':
    main()

