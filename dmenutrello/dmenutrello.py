import jsonpickle
import json
import functools
import dmenu
import configparser
from os.path import expanduser
from trello import TrelloClient
import sys, tempfile, os
from subprocess import call

#constants
BOARDS = 0
LISTS = 1
CARDS = 2
COMMENTS = 3

#EDITOR = os.environ.get('EDITOR','vim')
EDITOR = None
TERMINAL = None
TERMINALARG = None
dmenu_show = None

cache = './dmenutrellocache.json'

def writeCache(cache, data):
    with open(cache, 'w') as cachefile:
        cachefile.write(jsonpickle.encode(data))

def openCache(cache):
    with open(cache, 'r') as cachefile:
        return jsonpickle.decode(cachefile.read())

def readJson(jsonfile):
    with open(jsonfile, 'r') as read_file:
        data = json.load(read_file)
    return data

def writeJson(jsonfile, data):
    with open(jsonfile, 'w') as write_file:
                    json.dump(data,
                            write_file,
                            ensure_ascii = False,
                            sort_keys = True,
                            indent = 4 )

def toJson(client):
    output = {}
    output['/_obj'] = client
    output['/'] = {}
    for board in client.list_boards():
        #if board.name == 'Chaos':
        output['/'][board.name+'_obj'] = board
        output['/'][board.name] = {}
        for singlelist in board.list_lists():
            output['/'][board.name][singlelist.name + '_obj'] = singlelist
            output['/'][board.name][singlelist.name] = {}
            for card in singlelist.list_cards():
                i = 0
                output['/'][board.name][singlelist.name][card.name + '_obj'] = card
                output['/'][board.name][singlelist.name][card.name] = {}
                for comment in card.get_comments():
                    output['/'][board.name][singlelist.name][card.name][str(i)] = comment['data']['text']
                    i+=1
    return output

def listIt(client):
    formatData(toJson(client),0)

def show(mode, data, parent, prompt):
    menuItems= []
    if mode != BOARDS:
        menuItems.append('..')
    menuItems.extend(data.keys())
    out = dmenu_show(menuItems, prompt=prompt)
    #check for match
    if out == '..':
        return data, parent
    if out in data:
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
                data[out][d['data']['text']] = d
        elif mode == COMMENTS:
            data[out] = this
            #insert the comment text to a tmp file and edit it in vim
            initial_message = out.encode('utf-8')
            with tempfile.NamedTemporaryFile(suffix=".tmp") as tf:
                tf.write(initial_message)
                tf.flush()
                #open new terminal and open vim
                call([TERMINAL, TERMINALARG, EDITOR, tf.name])

                # do the parsing with `tf` using regular File operations.
                # for instance:
                tf.seek(0)
                edited_message = tf.read().decode('utf-8').replace('\n','')
                #update comment by id
                if edited_message != '':
                    parent.update_comment(data[out]['id'], edited_message)
                    data[edited_message] = data[out]
                    del data[out]
                    return show(mode, data, parent, "ok")
                else:
                    return show(mode, data, parent, "not allowed")

        return data[out], this
    elif out is not None:
        #no match, add new and call this function again with another prompt
        if mode == BOARDS:
            data[out] = parent.add_board(out)
        elif mode == LISTS:
            data[out] = parent.add_list(out)
        elif mode == CARDS:
            data[out] = parent.add_card(out)
        elif mode == COMMENTS:
            data[out] = parent.comment(out)
        return show(mode, data, parent, "ok")

def show2(mode, data, parent, prompt):
    menuItems= []
    if mode != BOARDS:
        menuItems.append('..')
    for key in data.keys():
        if '_obj' not in key:
            menuItems.append(key)
    out = dmenu_show(menuItems, prompt=prompt)

    if out == '..':
        show2(mode - 1, parent, parent, '')
    else:
        show2(mode + 1, data[out], data, '')
    #for key, value in data.items():
    #    print(value)

def main2():
    global dmenu_show, TERMINAL, TERMINALARG, EDITOR
    config = configparser.ConfigParser()
    data = openCache(cache)

    config.read(expanduser('~/.dmenutrello'))

    dmenu_show = functools.partial(dmenu.show,
            font=config.get('DMENU', 'font'),
            background_selected=config.get('DMENU','background_selected'),
            foreground_selected=config.get('DMENU','foreground_selected'),
            foreground=config.get('DMENU','foreground'),
            background=config.get('DMENU','background'))

    TERMINAL = config.get('TERMINAL','terminal')
    TERMINALARG = config.get('TERMINAL','terminal_argument')
    EDITOR = config.get('TERMINAL', 'editor')
    show2(0, data['/'], data['/'],'')

def main():
    global dmenu_show, TERMINAL, TERMINALARG, EDITOR
    config = configparser.ConfigParser()
    parent = [None] * 5
    data = [None] * 5
    data[0] = {}

    config.read(expanduser('~/.dmenutrello'))

    dmenu_show = functools.partial(dmenu.show,
            font=config.get('DMENU', 'font'),
            background_selected=config.get('DMENU','background_selected'),
            foreground_selected=config.get('DMENU','foreground_selected'),
            foreground=config.get('DMENU','foreground'),
            background=config.get('DMENU','background'))

    TERMINAL = config.get('TERMINAL','terminal')
    TERMINALARG = config.get('TERMINAL','terminal_argument')
    EDITOR = config.get('TERMINAL', 'editor')
    key = config.get('TRELLO', 'key')
    token = config.get('TRELLO', 'token')
    parent[0] = TrelloClient(
        api_key = key,
        api_secret = token
        )

    writeCache(cache, toJson(parent[0]))
    for board in parent[0].list_boards():
        data[0][board.name] = board

    # itreate through the levels
    i = 0
    while i != 4:
        data[i+1], parent[i+1] = show(i, data[i], parent[i], '')
        # if the same element returns its a back(..) move
        if data[i+1] == data[i]:
            #because show function replaces the trello object with a dict of the sub object
            # I have to find it and replace it with the trello object
            for key,value in data[i-1].items():
                if type(value) is dict:
                    data[i-1][key] = parent[i]
            i -= 1
        else:
             i += 1

if __name__ == '__main__':
    try:
        main2()
    except KeyboardInterrupt:
        pass

