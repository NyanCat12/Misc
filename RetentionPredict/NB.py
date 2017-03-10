import numpy as np
from sklearn.naive_bayes import GaussianNB
from sklearn.decomposition import PCA
from sklearn.metrics import accuracy_score

TrainFile = open('Train.csv', 'r')
Sample = []
Label = []
i = 1
length = len(TrainFile.readlines())
TrainFile.seek(0)
#样本维度:
#ID，游戏时长，最高等级，是否加入公会，获取元宝，消耗元宝，手动打副本次数，获取铜钱，消耗铜钱，消耗体力，登录次数，完成成就数，最高战力，副本失败数，商城购买次数，商城购买消耗元宝，商城购买道具数
while i < (length+1):
    test = TrainFile.readline()[:-1]
    a = test.split(';')
    b = []
    for x in a[1:-1]:
        if x == 'NULL':
            x = 0.0#Replace all 'NULL's
        b.append(float(x))
    Sample.append(b)
    if int(a[-1]) == 0:
        Label.append(1)#Oh we lost this player!
    else:
        Label.append(0)#Yes they logged in the next day!
    i += 1
TrainFile.close()
SampleNum = len(Sample)

#Load the test dataset
TestFile = open('Test.csv', 'r')
Player = []
Retension = []
i = 1
length = len(TestFile.readlines())
TestFile.seek(0)
while i < (length+1):
    test = TestFile.readline()[:-1]
    a = test.split(';')
    b = []
    for x in a[1:-1]:
        if x == 'NULL':
            x = 0.0
        b.append(float(x))
    Player.append(b)
    if int(a[-1]) == 0:
        Retension.append(1)
    else:
        Retension.append(0)
    i += 1
TestFile.close()

#PCA
pca = PCA()
pca.fit(Sample)
ratio = pca.explained_variance_ratio_
sum_ratio = 0
i = 1
for x in ratio:
    sum_ratio += x
    if sum_ratio >= 0.99:
        break
    else:
        i += 1
pca = PCA(n_components = i)
pca.fit(Sample)
Sample = pca.transform(Sample)
Player = pca.transform(Player)

#Building a model
X = Sample
y = Label
Predict = Player

model = GaussianNB()
model.fit(X,y)

#Predict
Z = model.predict(Predict)

print (accuracy_score(Retension, Z))
