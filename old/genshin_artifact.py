import random

attr = ['元素伤害','小生命','大生命','小攻击','大攻击','小防御','大防御','暴击','爆伤','精通','充能']
prob = [0, 150, 100, 150, 100, 150, 100, 75, 75, 100, 100, 0, 0, 0]
posstr = ['生之花','死之羽','时之沙','空之杯','理之冠']
meta = [[0.0583, 0.0583, 0.0729], [298.75, 19.45, 23.15], [13160.4, 709.916, 770.63]]
score = [0, 0, 0, 0, 2.29565, 0, 0, [1525, 9999], 6.6, [22, 104], [1, 0.5]]
for i in [1, 3, 5]:
    score[i] = score[i+1]*meta[1][(i-1)//2]/meta[0][(i-1)//2]/meta[2][(i-1)//2]
main = [1, 3, 9, 11, 7]
# limit = [30,50,100,150,200,300,500,1000,1500,2000,3000,5000,10000]
limit = [200, 500, 1000, 3000]
maxtime = 1000000

def getsub(main, sub1 = 0, sub2 = 0, sub3 = 0):
    weight = 1100-prob[main]-prob[sub1]-prob[sub2]-prob[sub3] # 总权重
    rnd = random.randint(1,weight)
    for i in range(1,11):
        if i == main or i == sub1 or i == sub2 or i == sub3:
            continue;
        if rnd <= prob[i]:
            return i
        rnd = rnd - prob[i]

def sigmoid(cnt, param1, param2):
    return (param2*cnt)/(param1+cnt)

class artifact:
    def __init__(self):
        
        # 生成位置和初始词条数
        self.sub = [0, 0, 0, 0, 0]
        self.data = [0, 0, 0, 0, 0]
        self.pos = random.randint(0,4)
        self.max = 4+(random.randint(1,5)>4)
        self.score = 0
        
        # 生成主词条
        match self.pos:
            case 0:
                self.main = 1
            case 1:
                self.main = 3
            case 2:
                rnd = random.randint(1,5000)
                if(rnd<=1334):
                    self.main = 2
                elif(rnd<=2667):
                    self.main = 4
                elif(rnd<=4000):
                    self.main = 6
                elif(rnd<=4500):
                    self.main = 9
                else:
                    self.main = 10
            case 3:
                rnd = random.randint(1,4000)
                if(rnd<=767):
                    self.main = 2
                elif(rnd<=1534):
                    self.main = 4
                elif(rnd<=2300):
                    self.main = 6
                elif(rnd<=2400):
                    self.main = 9
                elif(rnd<=2600):
                    self.main = 0
                elif(rnd<=3000):
                    self.main = 11 # 用于计算双套装用杯子
                else:
                    self.main = 13 # 其他属性空之杯
            case 4:
                rnd = random.randint(1,5000)
                if(rnd<=1100):
                    self.main = 2
                elif(rnd<=2200):
                    self.main = 4
                elif(rnd<=3300):
                    self.main = 6
                elif(rnd<=3500):
                    self.main = 9
                elif(rnd<=4000):
                    self.main = 7
                elif(rnd<=4500):
                    self.main = 8
                else:
                    self.main = 12 # 治疗
        
        if self.main != main[self.pos]:
            return

        # 生成副词条
        self.sub[1] = getsub(self.main)
        self.sub[2] = getsub(self.main, self.sub[1])
        self.sub[3] = getsub(self.main, self.sub[1], self.sub[2])
        self.sub[4] = getsub(self.main, self.sub[1], self.sub[2], self.sub[3])
        for i in range(1,5):
            self.data[i] = random.randint(1,4)+6
        
        # 强化副词条
        for i in range(0,self.max):
            rnd = random.randint(1,4)
            self.data[rnd] = self.data[rnd] + random.randint(1,4)+6
        
        # 评分
        for i in range(1,5):
            if(self.sub[i] in [7, 9, 10]):
                self.score += sigmoid(self.data[i]/8.5, score[self.sub[i]][0], score[self.sub[i]][1])
            else:
                self.score += score[self.sub[i]] * self.data[i]/8.5
        self.score = round(self.score,1)
    
    def info(self):
        ret = [0]*11
        for i in range(1,5):
            ret[self.sub[i]] = self.data[i]
        ret[0] = self.score
        return ret

    def __str__(self):
        ret = posstr[self.pos] + ' ' + attr[self.main] + '\n'
        for i in range(1,5):
            ret = ret + attr[self.sub[i]] + ' ' + str(round(self.data[i]/8.5,1)) + '条' + '\n'
        ret = ret + '总分 ' + str(self.score) + '\n'
        return ret

    def __eq__(self, s):
        return self.score == s.score
    
    def __gt__(self, s):
        return self.score > s.score

tmpbest = [[0 for i in range(0,11)] for i in range(0,5)]
avgbest = [[[0 for i in range(0,11)] for i in range(0,5)] for i in range(0, len(limit))]
bestarti = [[[0 for i in range(0,11)] for i in range(0,5)] for i in range(0, len(limit))]
cnt = [[0 for i in range(0,5)] for i in range(0, len(limit))]

for i in range(1, 1+maxtime): # 模拟
    
    a = artifact()
    
    if a.main == main[a.pos]:
        for j in range(0, len(limit)):
            if a.score > bestarti[j][a.pos][0]:
                bestarti[j][a.pos] = a.info()
            else:
                break
    
    for j in range(0, len(limit)):
        if i % limit[j] == 0:
            for k in range(0,5):
                getarti = 0
                for l in range(0,11):
                    avgbest[j][k][l] += bestarti[j][k][l]
                    if bestarti[j][k][l] > 0:
                        getarti = 1
                if getarti:
                    cnt[j][k] += 1
            bestarti[j] = tmpbest[:]
    
    if i % max(10000,maxtime//100) == 0:
        print(i//(maxtime//100),end='%\n')

for i in range(0,len(limit)): # 输出
    print(limit[i])
    sum = [0 for i in range(0,11)]
    for j in range(0,5):
        print(posstr[j] + '(' + str(round(cnt[i][j]/(maxtime//limit[i]), 2)) + ')', end='：')
        for k in range(1,11):
            ans = avgbest[i][j][k]/(maxtime//limit[i])/8.5
            sum[k] += ans
            print(attr[k], end=' ')
            print(round(ans,2), end=',')
        print('')
    print("总计：",end='')
    for k in range(1,11):
        if(k in [1, 3, 5]):
            sum[k+1] += sum[k]*meta[1][(k-1)//2]/meta[0][(k-1)//2]/meta[2][(k-1)//2]
            continue
        print(attr[k], end=' ')
        print(round(sum[k],2), end=',')
    print('\n')