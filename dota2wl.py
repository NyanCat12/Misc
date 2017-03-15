#coding=utf8
import json
import urllib.request

def alignment(str1, space, align = 'left'):
    length = len(str1.encode('gb2312'))
    space = space - length if space >=length else 0
    if align == 'left':
        str1 = str1 + ' ' * space
    elif align == 'right':
        str1 = ' '* space +str1
    elif align == 'center':
        str1 = ' ' * (space //2) +str1 + ' '* (space - space // 2)
    return str1

def get_json_peer(steamid):
    url = 'https://api.opendota.com/api/players/'+str(steamid)+'/peers'
    response = urllib.request.urlopen(url)
    code = response.getcode()
    html = response.read()
    mystr = html.decode("utf8")
    response.close()
    return mystr

def get_json_allwl(steamid):
    url = 'https://api.opendota.com/api/players/'+str(steamid)+'/wl'
    response = urllib.request.urlopen(url)
    code = response.getcode()
    html = response.read()
    mystr = html.decode("utf8")
    response.close()
    return mystr

def read_json(steamid):
    data = json.loads(get_json_peer(steamid))
    allwl = json.loads(get_json_allwl(steamid))
    print ('Total win rate: {:<5.1f}%'.format(allwl['win']/(allwl['win']+allwl['lose'])*100))
    for player in data:
        try:
            print ('Name: '+alignment(str(player['personaname']),40),'Games: '+alignment(str(player['games']),10),'Win rate: {win_rate:<5.1f}%'.format(win_rate=player['win']/player['games']*100))
        except:
            next
    return 0

def score(steamid):
    

if __name__ == '__main__':
    steamid = 120710320
    read_json(steamid)
