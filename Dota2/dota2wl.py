#coding=utf8
import json
import urllib.request
import matplotlib.pyplot as plt
import math
import matplotlib

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

def Score(peer1,allwl1,steamid2):
    #peer1 = json.loads(get_json_peer(steamid1))
    #allwl1 = json.loads(get_json_allwl(steamid1))
    peer2 = json.loads(get_json_peer(steamid2))
    allwl2 = json.loads(get_json_allwl(steamid2))
    winrate = -1
    for player in peer1:
        if player['account_id'] == steamid2:
            winrate = player['with_win']/player['with_games']
            with_win = player['with_win']
            with_games = player['with_games']
            break
    if winrate == -1:
        return (-1, -1)
    winrate1 = (allwl1['win']-with_win)/(allwl1['win']+allwl1['lose']-with_games)
    winrate2 = (allwl2['win']-with_win)/(allwl2['win']+allwl2['lose']-with_games)
    return [winrate/winrate1, winrate/winrate2]

def describe_player(steamid):
    peer = json.loads(get_json_peer(steamid))
    allwl = json.loads(get_json_allwl(steamid))
    peerlist = []
    score_pos_x = []
    score_pos_y = []
    for player in peer:
        '''
        score = Score(peer, allwl, player['account_id'])
        peerlist.append([player['personaname'],score[0],score[1]])
        score_pos_x.append(score[0]-1)
        score_pos_y.append(score[1]-1)
        
        '''
        try:
            score = Score(peer, allwl, player['account_id'])
            peerlist.append([player['personaname'],score[0],score[1]])
            score_pos_y.append((score[0]-score[1])/abs(score[0]-score[1])*math.sqrt(2*abs(score[0]-score[1])))
            print ((score[0]-score[1])/abs(score[0]-score[1])*math.sqrt(2*abs(score[0]-score[1])))
            score_pos_x.append(score[0]-1)
            print (score[0]-1)
        except:
            next
    #画出图
    #print (score)
    myfont = matplotlib.font_manager.FontProperties(fname="Light.ttc")
    matplotlib.rcParams['font.sans-serif'] = ['SimHei']
    plt.scatter(score_pos_x,score_pos_y)
    plt.plot([-1,1],[0,0])
    plt.plot([0,0],[-1,1])
    plt.text(0.5, 1, u'灵魂队友')
    plt.text(-1, 1, u'炸弹人')
    plt.text(0.5, -1, u'老司机')
    plt.text(-1, -1, u'猪队友')
    plt.savefig('dota2score_'+str(steamid)+'.jpg')
    #列出玩家列表
    for x in peerlist:
        print (x)
    return 0

if __name__ == '__main__':
    steamid = 144358325
    describe_player(steamid)
