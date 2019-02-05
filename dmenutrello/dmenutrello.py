import functools
import dmenu
import configparser
from os.path import expanduser
from trello import TrelloClient


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
        temp = data[out]
        board=temp
        data[out] = {}
        if mode == BOARDS:
            for d in temp.list_lists():
                data[out][d.name] = d
        elif mode == LISTS:
            for d in temp.list_cards():
                data[out][d.name] = d
        elif mode == CARDS:
            for d in temp.get_comments():
                data[out][d.name] = d

        return data[out]
    elif out is not None:
        #no match, add new
        data[out] = parent.add_board(out)
        return show(mode, data, prompt, "ok")

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
    ### BOARD
    #fill data dict
    for board in client.list_boards():
        data[board.name] = board

    matchedData = show(BOARDS, data, client, '')

    data = matchedData
    listData = show(LISTS, matchedData, data, '')
    show(CARDS, listData, matchedData, '')
    #out=dmenu_show(matchedData.keys())



def main():
    config = configparser.ConfigParser()
    config.read(expanduser('~/.dmenutrello'))

    key = config.get('TRELLO', 'key')
    token = config.get('TRELLO', 'token')

    menu(key, token)

if __name__ == '__main__':
    main()

