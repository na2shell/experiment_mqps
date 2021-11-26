import time
from matplotlib import pyplot
from statistics import mean, median,variance,stdev

f = open("log.txt","r")

ans_dict = {}
for data in f:
    arr = data.split(" ")
    if(arr[-4] == "MQPs"):
        continue
    #print(arr)
    p = arr[-2]
    dif_time = float(arr[0])-float(arr[-3])
    if(p in ans_dict):
        ans_dict[p].append(dif_time)
    else:
        ans_dict[p] = [dif_time]

x = [i+1 for i in range(5)]
y = [0 for _ in range(5)]
st = [0 for _ in range(5)]
for key in ans_dict:
    arr = ans_dict[key]
    av = sum(arr)/len(arr)
    y[int(key)-1] = av
    st[int(key)-1] = stdev(arr)

print([x,y])

fig = pyplot.figure()
ax = fig.add_subplot(1, 1, 1)

ax.plot(x,y)
ax.errorbar(x, y, yerr=st)
pyplot.show()

