import matplotlib.pyplot as plt
from ZhihuCrawler import *

# 解决乱码
plt.rcParams['font.sans-serif'] = ['KaiTi']
plt.rcParams['axes.unicode_minus'] = False

#----------------------------------- 统计词频-----------------------------#
Fre = { }
for item in stringForAuthor:
    if item not in Fre:
        Fre[item] = 1
    else:
        Fre[item] +=1
# 根据词频排序到列表
prices_sorted = sorted(zip(Fre.values(), Fre.keys()))
authorLable = []
lableFre = []
for i in range(0,len(prices_sorted)):
    authorLable.append(prices_sorted[i][1])
    lableFre.append(prices_sorted[i][0])

plt.bar(authorLable[1039:], lableFre[1039:])
plt.savefig("./image/lable.png",dpi=180)

#----------------------------------- 统计词频-----------------------------#
Fre = { }
for item in stringForComment:
    if item not in Fre:
        Fre[item] = 1
    else:
        Fre[item] +=1
# 根据词频排序到列表
prices_sorted = sorted(zip(Fre.values(), Fre.keys()))
commentLable = []
lableFre = []
for i in range(0,len(prices_sorted)):
    commentLable.append(prices_sorted[i][1])
    lableFre.append(prices_sorted[i][0])
# print(len(commentLable))
plt.bar(commentLable[5572:], lableFre[5572:])
plt.savefig("./image/comment.png",dpi=180,fontsize=10)