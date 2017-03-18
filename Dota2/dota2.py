#coding=utf8
import json
import urllib.request
import matplotlib.pyplot as plt
import math
import matplotlib

#英雄id和英雄名
def Hero_Group(hero_id):
    url = 'https://api.opendota.com/api/heroStats'
    Hero_Name = 'hero'
    return Hero_Name

#英雄表现百分位
def Hero_Percentile(hero_id):
    url = 'https://api.opendota.com/api/benchmarks/?hero_id='+str(hero_id)
    mystr = urllib.request.urlopen(url).read().decode('utf8')
    Hero = json.loads(mystr)['result']
    x = []
    y = []
    for percentile in Hero['gold_per_min']:
        x.append(percentile['percentile'])
        y.append(percentile['value'])
    plt.plot(y,x)
    plt.xlabel('gold_per_min')
    plt.ylabel('percentile')
    plt.title('Percentile of GPM')
    plt.show()
    
    return Hero

if __name__ == '__main__':
    Hero_Percentile(4)
    
