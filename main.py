import numpy as np
import matplotlib.pyplot as plt

from utils.data import *
from utils.util import *

base_score = [0, 0, 0, 0, 70001, 0, 100100, 100100, 0, 30001]

print("词条编号：")
for i in range(len(attr)):
    print(str(i) + " " + attr[i])

# main = int(tmp) if (tmp := input("选择主词条：（默认小生命）") != '') else 1 
main = 1

attrs = (6, 7, 5)
upgrades = (3, 2, 2, 1)

artitype = 0
artiprob = [0.2, 1/3, 1]
base = dict()


    
def init(maina:int = main):
    global base
    base = {}
    for i in range(9999):
        id = sorted([i//1000, (i//100)%10, (i//10)%10, i%10])
        id = id[0]*1000 + id[1]*100 + id[2]*10 + id[3]
        p = prob(maina, i//1000, (i//100)%10, (i//10)%10, i%10)
        if p > 0:
            if id in base.keys():
                base[id] += p
            else:
                base[id] = p

upgrade = np.zeros((6, 6, 6, 6), dtype=float)
upgrade[0, 0, 0, 0] = 1

for i in range(1, 5):
    for index in np.ndindex((i, i, i, i)):
        a, b, c, d = [i - 1 - j for j in index]
        upgrade[a+1, b, c, d] += upgrade[a, b, c, d] / 4
        upgrade[a, b+1, c, d] += upgrade[a, b, c, d] / 4
        upgrade[a, b, c+1, d] += upgrade[a, b, c, d] / 4
        upgrade[a, b, c, d+1] += upgrade[a, b, c, d] / 4
        upgrade[a, b, c, d] = 0

uu = upgrade.copy()

for index in np.ndindex((5, 5, 5, 5)):
    a, b, c, d = [4 - i for i in index]
    upgrade[a+1, b, c, d] += upgrade[a, b, c, d] / 4
    upgrade[a, b+1, c, d] += upgrade[a, b, c, d] / 4
    upgrade[a, b, c+1, d] += upgrade[a, b, c, d] / 4
    upgrade[a, b, c, d+1] += upgrade[a, b, c, d] / 4
    upgrade[a, b, c, d] = 0

for j in np.ndindex((6, 6, 6, 6)):
    upgrade[j] = upgrade[j] * artiprob[artitype] + uu[j] * (1-artiprob[artitype])


def sump(a, b=-1, c=-1, d=-1):
    pp = 0
    for i in base.keys():
        if str(a) in str(i) and (str(b) in str(i) or b == -1) and (c == -1 or str(c) in str(i)) and (d == -1 or str(d) in str(i)):
            pp = pp + base[i]
    return pp

def get_upgrade(mainn, mainc=1, subn=0, subc=0):
    pp = 0
    if mainn + subn > 5 or mainc + subc > 4:
        raise ValueError("Bad upgrade")
    if mainc < 1 and subc < 1:
        return 1

    for i in np.ndindex((6, 6, 6, 6)):
        if (((mainc == 0) or (sum(i[:mainc]) >= mainn)) and
        ((subc == 0) or (sum(i[-subc:]) >= subn))):
            pp += upgrade[i]
    return pp

# init(main)
# print("胚子概率为：%.6f(1/%d~)" % (x:=sump(*attrs), 1+1/x))
# print("升级概率为：%.6f(1/%d~)" % (y:=get_upgrade(*upgrades), 1+1/y))
# print("总概率为：%.6f" % (x * y))
# print("部位、套装概率为：%.6f" % (z := 0.1*pmain[main]))
# print("锁定部位、套装时期望为：%.2f把" % (1/2.13/x/y/z))

def get_score():
    global score
    score = dict()
    for key, val in base.items():
        a = (key//1000, (key//100)%10, (key//10)%10, key%10)
        if val == 0:
            continue
        for index in np.ndindex((6, 6, 6, 6)):
            if upgrade[index] <= 0:
                continue
            res = sum([(base_score[a[i]] * (1+index[i])) for i in range(4)])
            if res not in score.keys():
                score[res] = 0
            score[res] += val * upgrade[index]
    return score

# s = get_score()

# print([(i[0], round(i[1], 6)) for i in sorted(s.items(), key=lambda x: x[0])])
# print([(i[0], "%.6f" % (10/2.13/i[1]/pmain[main])) for i in sorted(s.items(), key=lambda x: x[0])])


N = 200
res = {0:1.0}


for i in range(5):
    init(main_list[i])
    s = get_score()
    s = dict_pow(s, round(N*0.1*1.065*main_weight[i][main_list[i]]))
    s = dict_mul(s, base_dict[i])
    # print([(i[0], round(i[1], 6)) for i in sorted(s.items(), key=lambda x: x[0])])
    res = dict_add(res, s)

# [print(f'{i[0]:>8} : {i[1]:.8e}') for i in sorted(res.items(), key=lambda x: x[0], reverse=True)]


sorted_key = sorted(res.keys())
sorted_res = [res[key] for key in sorted_key]
cumulative = [res[sorted_key[0]]]

[cumulative.append(cumulative[-1] + res[key]) for key in sorted_key[1:]]

[print(f'{sorted_key[i]//10000:>4}({(sorted_key[i]//100)%100:>2}+{sorted_key[i]%100:>2}): {cumulative[i]:>.4f}, {res[sorted_key[i]]:>.5f}') for i in filter(lambda x: res[sorted_key[x]] > 1/len(sorted_key), range(len(sorted_key)))]

print(f'{sorted_key[-1]//10000:>4}({(sorted_key[-1]//100)%100:>2}+{sorted_key[-1]%100:>2}): {res[sorted_key[-1]]:>.5e}')

plt.plot(sorted_key, cumulative)
# plt.plot(sorted_key, sorted_res)
plt.show()