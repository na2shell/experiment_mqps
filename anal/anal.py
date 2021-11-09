import sys
from statistics import mean, median,variance,stdev

def main():
    file_path = "./log.txt"
    file_w_path = "for_draw.txt"
    f = open(file_path,"r")
    times = []
    
    for data in f:
        data = data.rstrip("\n")
        data_list = data.split()
        #print(float(data_list[0]))
        p = data_list[4].replace("\'", "")
        #print(p)
        ans = float(data_list[0]) - float(data_list[3])
        times.append([p,ans])
    
    #print(times)
    
    fw = open(file_w_path,"w")

    
    for i in range(1,6):
        smp = []
        for time in times:
            #print(time[0])
            if (time[0] == "message-pr"+str(i)):
                p#rint("hoge")
                smp.append(time[1])
        
        ans = [str(i),mean(smp), mean(smp) - variance(smp), mean(smp) + variance(smp)]
        ans = [str(s) for s in ans]
        print(len(smp),ans)
        fw.write(" ".join(ans))
        fw.write("\n")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("trap!")
        sys.exit(1)