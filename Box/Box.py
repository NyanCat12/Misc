import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl

mpl.rcParams['font.family'] = 'sans-serif'
mpl.rcParams['font.sans-serif'] = [u'SimHei']

File1 = open('sample1.txt','r')
sample1 = File1.readlines()
data1 = []
for x in sample1:
    data1.append(float(x[:-1]))

File2 = open('sample2.txt','r')
sample2 = File2.readlines()
data2 = []
for x in sample2:
    data2.append(float(x[:-1]))

File3 = open('sample3.txt','r')
sample3 = File3.readlines()
data3 = []
for x in sample3:
    data3.append(float(x[:-1]))

File4 = open('sample4.txt','r')
sample4 = File4.readlines()
data4 = []
for x in sample4:
    data4.append(float(x[:-1]))

File5 = open('sample5.txt','r')
sample5 = File5.readlines()
data5 = []
for x in sample5:
    data5.append(float(x[:-1]))

File6 = open('sample6.txt','r')
sample6 = File6.readlines()
data6 = []
for x in sample6:
    data6.append(float(x[:-1]))

File7 = open('sample7.txt','r')
sample7 = File7.readlines()
data7 = []
for x in sample7:
    data7.append(float(x[:-1]))

data = [data1, data2, data3, data4, data5, data6, data7]
labels = [ '1','2','3','4','5','6','7']

#并列作图
#fig, (ax1, ax2) = plt.subplots(1, 2, figsize = (8, 4))

#柱状分布
#ax1.hist(data)
#ax2.boxplot(data2)

plt.boxplot(data, labels = labels, widths = 0.4)

plt.savefig('hist_boxplot')
plt.show()
