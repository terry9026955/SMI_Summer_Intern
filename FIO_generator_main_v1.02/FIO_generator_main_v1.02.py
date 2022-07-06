import csv
import numpy as np
import pandas as pd
import threading
import queue
import matplotlib.pyplot as plt

def dragfun(filepath):
    if filepath[0] == '"':
        filepath = filepath.split('"')
        filepath = filepath[1]
        print(filepath)
    else:
        filepath = filepath
    return filepath

def sclFormat1(filename, nummode, latency):
    sec = []
    IOps = []
    readsec = []
    total_read = []
    tw = []
    i = 0
    with open(filename, 'r') as f:
        RRcsv = csv.reader(f)
        for row in RRcsv:
            sec = np.append(sec, row[0])
            IOps = np.append(IOps, row[1])
            if latency == 1:
                tw = np.array(np.append(tw, row[1]), dtype='float_')
            else:
                i = i + 1 
                sec = np.array(sec, dtype='float_')
                IOps = np.array(IOps, dtype='float_')
                print("Found IOps, Number of {}" .format(i))
        if latency == 0:
            for i in range(len(IOps)):
                if i == 0:
                    readsec = np.append(readsec, IOps[i]*nummode*(sec[i]/10**3)/1024**2)
                else:
                    readsec = np.append(readsec, IOps[i]*nummode*((sec[i]-sec[i-1])/10**3)/1024**2)
            
            tw = np.append(tw, readsec)

            for i in range(len(readsec)):
                if i == 0:
                    total_read = np.append(total_read, readsec[i])
                else:
                    readsec[i] += readsec[i-1]
                    total_read = np.append(total_read, readsec[i])
            if nummode == 1:
                IOps = IOps / 1024
            
    return total_read, IOps, tw
        
 
def namesplit(name):
    name = name.split('-')
    for _ in name:
        if 'RRQD128' in _:
            figname = 'RND Read Q128T1'
        elif 'RWQD128' in _:
            figname = 'RND Write Q128T1'
        elif 'SRQD128' in _:
            figname = 'SEQ Read Q128T1'
        elif 'SWQD128' in _:
            figname = 'SEQ Write Q128T1'
        
        elif 'RRQD1' in _:
            figname = '4K RND Read'
        elif 'RWQD1' in _:
            figname = '4K RND Write'
        elif 'SRQD1' in _:
            figname = '128K SEQ Read'
        elif 'SWQD1' in _:
            figname = '128K SEQ Write'

    return figname

def dataappend(q):
    data = []
    arr = np.array(list(q.queue), dtype='float_')
    data = np.append(data, arr)
    return data
        
def plotfig(mode, qlist, stage, y_scale):
    plt.figure()
    plt.plot(qlist[stage][0][0], qlist[stage][0][1], label = 'stage'+str(stage+1))
    plt.title('SLC Cache Test - '+mode, fontsize=15, fontweight='bold')
    plt.ylim(bottom=0, top=max(qlist[stage][0][1])+50000)
    plt.xlabel('Host '+mode.split(' ')[1]+'(GB)')
    plt.ylabel(y_scale)
    plt.legend(loc=1)
    plt.grid(True, linestyle = "-", color = 'gray' , linewidth = '0.5', axis='y')
    plt.show()

def plotGC(fn, qlist, productname, y_scale):
    f1 = plt.figure(namesplit(fn[0])+'1rd')
    plt.plot(qlist[0][0][0], qlist[0][0][1], label = productname)
    plt.title('GC Policy Test - '+namesplit(fn[0])+' 1st Run', fontsize=15, fontweight='bold')
    plt.ylim(bottom=0)
    plt.xlabel('Host write(GB)')
    plt.ylabel(y_scale)
    plt.legend(loc=1)
    plt.grid(True, linestyle = "-", color = 'gray' , linewidth = '0.5', axis='y')
    f2 = plt.figure(namesplit(fn[1])+'2nd')
    plt.plot(qlist[1][0][0], qlist[1][0][1], label = productname)
    plt.title('GC Policy Test - '+namesplit(fn[1])+' 2nd Run', fontsize=15, fontweight='bold')
    plt.ylim(bottom=0)
    plt.xlabel('Host write(GB)')
    plt.ylabel(y_scale)
    plt.legend(loc=1)
    plt.grid(True, linestyle = "-", color = 'gray' , linewidth = '0.5', axis='y')
    f3 = plt.figure(namesplit(fn[2])+'3rd')
    plt.plot(qlist[2][0][0], qlist[2][0][1], label = productname)
    plt.title('GC Policy Test - '+namesplit(fn[2])+' 3rd Run', fontsize=15, fontweight='bold')
    plt.ylim(bottom=0)
    plt.xlabel('Host write(GB)')
    plt.ylabel(y_scale)
    plt.legend(loc=1)
    plt.grid(True, linestyle = "-", color = 'gray' , linewidth = '0.5', axis='y')
    f4 = plt.figure(namesplit(fn[3])+'1st')
    plt.plot(qlist[3][0][0], qlist[3][0][1], label = productname)
    plt.title('GC Policy Test - '+namesplit(fn[3])+' 1st Run', fontsize=15, fontweight='bold')
    plt.ylim(bottom=0)
    plt.xlabel('Host Read(GB)')
    plt.ylabel(y_scale)
    plt.legend(loc=1)
    plt.grid(True, linestyle = "-", color = 'gray' , linewidth = '0.5', axis='y')
    f5 = plt.figure(namesplit(fn[4])+'2nd')
    plt.plot(qlist[4][0][0], qlist[4][0][1], label = productname)
    plt.title('GC Policy Test - '+namesplit(fn[4])+' 2nd Run', fontsize=15, fontweight='bold')
    plt.ylim(bottom=0)
    plt.xlabel('Host Read(GB)')
    plt.ylabel(y_scale)
    plt.legend(loc=1)
    plt.grid(True, linestyle = "-", color = 'gray' , linewidth = '0.5', axis='y')
    f6 = plt.figure(namesplit(fn[5])+'3rd')
    plt.plot(qlist[5][0][0], qlist[5][0][1], label = productname)
    plt.title('GC Policy Test - '+namesplit(fn[5])+' 3rd Run', fontsize=15, fontweight='bold')
    plt.ylim(bottom=0)
    plt.xlabel('Host Read(GB)')
    plt.ylabel(y_scale)
    plt.legend(loc=1)
    plt.grid(True, linestyle = "-", color = 'gray' , linewidth = '0.5', axis='y')
    f7 = plt.figure('1st compare')
    plt.plot(qlist[0][0][0], qlist[0][0][1], label = productname+' write', color='darkred')
    plt.plot(qlist[3][0][0], qlist[3][0][1], label = productname+' Read')
    plt.title('GC Policy Test -Write/Read Q128T1 1st Run compare', fontsize=15, fontweight='bold')
    plt.ylim(bottom=0)
    plt.xlabel('Throughput(GB)')
    plt.ylabel(y_scale)
    plt.legend(loc=1)
    plt.grid(True, linestyle = "-", color = 'gray' , linewidth = '0.5', axis='y')
    f8 = plt.figure('2nd compare')
    plt.plot(qlist[1][0][0], qlist[1][0][1], label = productname+' write', color='darkred')
    plt.plot(qlist[4][0][0], qlist[4][0][1], label = productname+' Read')
    plt.title('GC Policy Test -Write/Read Q128T1 2nd Run compare', fontsize=15, fontweight='bold')
    plt.ylim(bottom=0)
    plt.xlabel('Throughput(GB)')
    plt.ylabel(y_scale)
    plt.legend(loc=1)
    plt.grid(True, linestyle = "-", color = 'gray' , linewidth = '0.5', axis='y')
    f9 = plt.figure('3rd compare')
    plt.plot(qlist[2][0][0], qlist[2][0][1], label = productname+' write', color='darkred')
    plt.plot(qlist[5][0][0], qlist[5][0][1], label = productname+' Read')
    plt.title('GC Policy Test -Write/Read Q128T1 3rd Run compare', fontsize=15, fontweight='bold')
    plt.ylim(bottom=0)
    plt.xlabel('Throughput(GB)')
    plt.ylabel(y_scale)
    plt.legend(loc=1)
    plt.grid(True, linestyle = "-", color = 'gray' , linewidth = '0.5', axis='y')
    plt.show()

def main():
    while True:
        try:
            print('Please select mode: \n1.SLCCache 2.Latency 3.WR3cycle 4.GCPolicy')
            option = input()
        except:
            print('ERROR: Please enter the correct number.')
        if option == '1':
            print('You select FIO-SLCCache')
            t_list = []
            q1 = queue.Queue()
            q2 = queue.Queue()
            q3 = queue.Queue()
            q4 = queue.Queue()
            q5 = queue.Queue()
            productname = input('Please enter the product what you want to report:')
            filepath_1 = dragfun(input('Please enter your file path of stage 1: '))
            filepath_2 = dragfun(input('Please enter your file path of stage 2: '))
            filepath_3 = dragfun(input('Please enter your file path of stage 3: '))
            filepath_4 = dragfun(input('Please enter your file path of stage 4: '))
            filepath_5 = dragfun(input('Please enter your file path of stage 5: '))
            fn = [filepath_1, filepath_2, filepath_3, filepath_4, filepath_5]
            capacity_str = []
            for i  in range(len(fn)):
                try:
                    n = fn[i].split("\\")
                    getn = n[len(n)-1]
                    getCapacity = getn.split("_")[0].split("-")
                except:
                    getCapacity = fn[i].split("_")[0].split("-")
                capacity_str = np.append(capacity_str, getCapacity[len(getCapacity)-2])
            capacity = []
            for i in range(len(capacity_str)):
                capacity = np.append(capacity, int(''.join(filter(str.isdigit, capacity_str[i]))))
            print(capacity)
            nm = namesplit(fn[1]).split(' ')
            for n_item in nm:
                if n_item == 'SEQ':
                    nummode = 1
                    y_scale = 'MB/s'
                elif n_item == 'RND':
                    nummode = 4
                    y_scale = 'IOPs'
            t1 = threading.Thread(target=lambda q, arg1, arg2, arg3: q.put(sclFormat1(arg1, arg2, arg3)), args=(q1, filepath_1, nummode, 0))
            t_list.append(t1)
            t2 = threading.Thread(target=lambda q, arg1, arg2, arg3: q.put(sclFormat1(arg1, arg2, arg3)), args=(q2, filepath_2, nummode, 0))
            t_list.append(t2)
            t3 = threading.Thread(target=lambda q, arg1, arg2, arg3: q.put(sclFormat1(arg1, arg2, arg3)), args=(q3, filepath_3, nummode, 0))
            t_list.append(t3)
            t4 = threading.Thread(target=lambda q, arg1, arg2, arg3: q.put(sclFormat1(arg1, arg2, arg3)), args=(q4, filepath_4, nummode, 0))
            t_list.append(t4)
            t5 = threading.Thread(target=lambda q, arg1, arg2, arg3: q.put(sclFormat1(arg1, arg2, arg3)), args=(q5, filepath_5, nummode, 0))
            t_list.append(t5)

            for t in t_list:
                t.start()
            for t in t_list:
                t.join()
            qlist = [list(q1.queue), list(q2.queue), list(q3.queue), list(q4.queue), list(q5.queue)]
            pattern_dict = {
                "Total Read stage1" : qlist[0][0][0], "stage1" : qlist[0][0][1],
                "Total Read stage2" : qlist[1][0][0], "stage2" : qlist[1][0][1],
                "Total Read stage3" : qlist[2][0][0], "stage3" : qlist[2][0][1],
                "Total Read stage4" : qlist[3][0][0], "stage4" : qlist[3][0][1],
                "Total Read stage5" : qlist[4][0][0], "stage5" : qlist[4][0][1]
            }
            df = pd.DataFrame.from_dict(pattern_dict, orient='index')
            df = df.transpose()
            
            stage_read = []
            Total_read_format2 = []
            all_write = []
            for i in range(len(qlist)):
                stage_read = np.append(stage_read, qlist[i][0][2])
                all_write = np.append(all_write, qlist[i][0][1])
            
            for _ in range(len(stage_read)):
                if _ == 0:
                        Total_read_format2 = np.append(Total_read_format2, stage_read[_])
                else:
                    stage_read[_] += stage_read[_-1]
                    Total_read_format2 = np.append(Total_read_format2, stage_read[_])
            totaldict = {
                "Total_read_format2": Total_read_format2, "all_write": all_write
            }
            df_total = pd.DataFrame.from_dict(totaldict, orient='index')
            df_total = df_total.transpose()
            print(df_total)
            df_total.to_csv(productname+"_Total_Read_format.csv")
            # Plot figure for format2
            mode = namesplit(fn[0])
            plt.figure()
            plt.plot(Total_read_format2, all_write, label = productname)
            for i in range(len(capacity)):
                plt.axvline(x=sum(capacity[:i+1]), color='black', linewidth=2, linestyle='--')
            plt.title('SLC Cache Test - '+mode, fontsize=15, fontweight='bold')
            plt.ylim(bottom=0)
            plt.xlabel('Host '+mode.split(' ')[1]+'(GB)')
            plt.ylabel(y_scale)
            plt.legend(loc=1)
            plt.grid(True, linestyle = "-", color = 'gray' , linewidth = '0.5', axis='y')
            plt.show()
            for i in range(len(fn)+1):
                if i == (len(fn)):
                    plt.figure()
                    for j in range(len(fn)):
                        plt.plot(qlist[j][0][0], qlist[j][0][1], label = 'stage'+str(j+1))
                    plt.title('SLC Cache Test - '+mode, fontsize=15, fontweight='bold')
                    plt.ylim(bottom=0)
                    plt.xlabel('Host '+mode.split(' ')[1]+'(GB)')
                    plt.ylabel(y_scale)
                    plt.legend(loc=1)
                    plt.grid(True, linestyle = "-", color = 'gray' , linewidth = '0.5', axis='y')
                    plt.show()
                else:
                    mode = namesplit(fn[i])
                    plotfig(mode, qlist, i, y_scale)
            df.to_csv(productname+'_'+mode+'_test_pattern.csv', index=False)
            

        elif option == '2':
            print('You select FIO-Latency.')
            t_list = []
            q1 = queue.Queue()
            q2 = queue.Queue()
            productname = input('Please enter the product what you want to report:')
            filepath_3time = dragfun(input('Please enter your file path of 3 times: '))
            filepath_laten = dragfun(input('Please enter your file path of Latency: '))
            fn = [filepath_3time, filepath_laten]
            nm = namesplit(fn[1]).split(' ')
            for n_item in nm:
                if n_item == 'SEQ':
                    nummode = 1
                    y_scale = 'MB/s'
                elif n_item == 'RND':
                    nummode = 4
                    y_scale = 'IOPs'
            mode = namesplit(fn[0])
            if namesplit(fn[0]).split(' ')[2] != namesplit(fn[1]).split(' ')[2]:
                print('ERROR: Please check the file and make sure there are in the same mode.')
                break
            else:
                print('Starting to generate the data...')
                t1 = threading.Thread(target=lambda q, arg1, arg2, arg3: q.put(sclFormat1(arg1, arg2, arg3)), args=(q1, filepath_3time, nummode, 0))
                t_list.append(t1)
                t2 = threading.Thread(target=lambda q, arg1, arg2, arg3: q.put(sclFormat1(arg1, arg2, arg3)), args=(q2, filepath_laten, nummode, 1))
                t_list.append(t2)

                for t in t_list:
                    t.start()
                for t in t_list:
                    t.join()
                    
                qlist = [list(q1.queue), list(q2.queue)]
                pattern_dict = {
                    "Total" : qlist[0][0][0], productname+y_scale : qlist[0][0][1], productname+"Latency" : qlist[1][0][2],
                }
                df = pd.DataFrame.from_dict(pattern_dict, orient='index')
                df = df.transpose()
                print(df)
                df.to_csv(productname+'_'+mode+'_Latency.csv', index=False)
                if len(qlist[0][0][0]) != len(qlist[1][0][2]):
                    latency = qlist[1][0][2][:len(qlist[0][0][0])]
                
                #Plot layout
                #import matplotlib.ticker as mticker
                # = 10 # y軸密集度
                nm_mode = namesplit(fn[0]).split(' ')[2]
                fig, ax1 = plt.subplots()
                plt.title('FIO - '+ mode+' Latency', fontsize=15, fontweight='bold')
                plt.xlabel('Host '+ nm_mode+'(GB)')
                ax2 = ax1.twinx()
                ax1.set_ylabel(y_scale)
                l1 = ax1.plot(qlist[0][0][0], qlist[0][0][1], color='lightsteelblue', label=productname+y_scale)
                ax1.set_ylim(top=max(qlist[0][0][1])+10000)
                ax1.axvline(x=int(max(qlist[0][0][0])/3), color='black', linewidth=2, linestyle='--')
                ax1.axvline(x=int(max(qlist[0][0][0])*2/3), color='black', linewidth=2, linestyle='--')
                ax1.grid(True, linestyle = "-", color = 'gray' , linewidth = '0.5', axis='y')
                ax1.tick_params(axis='y',  color='lightsteelblue')
                ax2.set_ylabel('usec', color='red')
                #ax2.yaxis.set_major_locator(mticker.MultipleLocator(tick_spacing))
                l2 = ax2.plot(qlist[0][0][0], latency, color='darkred', alpha=1, label=productname+'Latency')
                ax2.tick_params(axis='y', color='darkred')
                lns = l1+l2
                labs = [l.get_label() for l in lns]
                fig.tight_layout()
                plt.legend(lns, labs, loc=1)
                plt.show()

        elif option == '3':
            print('You select FIO-WR3cycle.')
            t_list = []
            q1 = queue.Queue()
            q2 = queue.Queue()
            productname = input('Please enter the product what you want to report:')
            filepath_1 = dragfun(input('Please enter your file path of Write: '))
            filepath_2 = dragfun(input('Please enter your file path of Read: '))
            fn = [filepath_1, filepath_2]
            nm = namesplit(fn[1]).split(' ')
            for n_item in nm:
                if n_item == 'SEQ':
                    nummode = 1
                    y_scale = 'MB/s'
                elif n_item == 'RND':
                    nummode = 4
                    y_scale = 'IOPs'
            t1 = threading.Thread(target=lambda q, arg1, arg2, arg3: q.put(sclFormat1(arg1, arg2, arg3)), args=(q1, filepath_1, nummode, 0))
            t_list.append(t1)
            t2 = threading.Thread(target=lambda q, arg1, arg2, arg3: q.put(sclFormat1(arg1, arg2, arg3)), args=(q2, filepath_2, nummode, 0))
            t_list.append(t2)
            for t in t_list:
                t.start()
            for t in t_list:
                t.join()
            
            if namesplit(fn[0]).split(' ')[1] == namesplit(fn[1]).split(' ')[1]:
                print('ERROR: Please check the file and make sure there are in different mode.')
                break
            else:
                qlist = [list(q1.queue), list(q2.queue)]
                pattern_dict = {
                    "Total Write" : qlist[0][0][0], productname+" Write IOps" : qlist[0][0][1],
                    "Total Read" : qlist[1][0][0], productname+" Read IOps" : qlist[1][0][1],
                }
                df = pd.DataFrame.from_dict(pattern_dict, orient='index')
                df = df.transpose()
                print(df)
                df.to_csv(productname+'_WriteRead3Cycle.csv', index=False)
                f1 = plt.figure(namesplit(fn[0]))
                plt.plot(qlist[0][0][0], qlist[0][0][1], label = productname)
                plt.title('FIO - '+namesplit(fn[0])+' - 3cycles', fontsize=15, fontweight='bold')
                plt.axvline(x=int(max(qlist[0][0][0])/3), color='black', linewidth=2, linestyle='--')
                plt.axvline(x=int(max(qlist[0][0][0])*2/3), color='black', linewidth=2, linestyle='--')
                plt.ylim(bottom=0)
                plt.xlabel('Host write(GB)')
                plt.ylabel(y_scale)
                plt.legend(loc=1)
                plt.grid(True, linestyle = "-", color = 'gray' , linewidth = '0.5', axis='y')
                f2 = plt.figure(namesplit(fn[1]))
                plt.plot(qlist[1][0][0], qlist[1][0][1], label = productname)
                plt.title('FIO - '+namesplit(fn[1])+' - 3cycles', fontsize=15, fontweight='bold')
                plt.axvline(x=int(max(qlist[1][0][0])/3), color='black', linewidth=2, linestyle='--')
                plt.axvline(x=int(max(qlist[1][0][0])*2/3), color='black', linewidth=2, linestyle='--')
                plt.ylim(bottom=0)
                plt.xlabel('Host Read(GB)')
                plt.ylabel(y_scale)
                plt.legend(loc=1)
                plt.grid(True, linestyle = "-", color = 'gray' , linewidth = '0.5', axis='y')
                plt.show()

        elif option =='4':
            print('You select FIO-GCPolicy.')
            t_list = []
            q1 = queue.Queue()
            q2 = queue.Queue()
            q3 = queue.Queue()
            q4 = queue.Queue()
            q5 = queue.Queue()
            q6 = queue.Queue()
            productname = input('Please enter the product what you want to report:')
            filepath_1 = dragfun(input('Please enter your file path of 1st Write: '))
            filepath_2 = dragfun(input('Please enter your file path of 2nd Write: '))
            filepath_3 = dragfun(input('Please enter your file path of 3rd Write: '))
            filepath_4 = dragfun(input('Please enter your file path of 1st Read: '))
            filepath_5 = dragfun(input('Please enter your file path of 2nd Read: '))
            filepath_6 = dragfun(input('Please enter your file path of 3rd Read: '))
            fn = [filepath_1, filepath_2, filepath_3, filepath_4, filepath_5, filepath_6]
            nm = namesplit(fn[1]).split(' ')
            for n_item in nm:
                if n_item == 'SEQ':
                    nummode = 1
                    y_scale = 'MB/s'
                elif n_item == 'RND':
                    nummode = 4
                    y_scale = 'IOPs'
            t1 = threading.Thread(target=lambda q, arg1, arg2, arg3: q.put(sclFormat1(arg1, arg2, arg3)), args=(q1, filepath_1, nummode, 0))
            t_list.append(t1)
            t2 = threading.Thread(target=lambda q, arg1, arg2, arg3: q.put(sclFormat1(arg1, arg2, arg3)), args=(q2, filepath_2, nummode, 0))
            t_list.append(t2)
            t3 = threading.Thread(target=lambda q, arg1, arg2, arg3: q.put(sclFormat1(arg1, arg2, arg3)), args=(q3, filepath_3, nummode, 0))
            t_list.append(t3)
            t4 = threading.Thread(target=lambda q, arg1, arg2, arg3: q.put(sclFormat1(arg1, arg2, arg3)), args=(q4, filepath_4, nummode, 0))
            t_list.append(t4)
            t5 = threading.Thread(target=lambda q, arg1, arg2, arg3: q.put(sclFormat1(arg1, arg2, arg3)), args=(q5, filepath_5, nummode, 0))
            t_list.append(t5)
            t6 = threading.Thread(target=lambda q, arg1, arg2, arg3: q.put(sclFormat1(arg1, arg2, arg3)), args=(q6, filepath_6, nummode, 0))
            t_list.append(t6)

            for t in t_list:
                t.start()
            for t in t_list:
                t.join()

            qlist = [list(q1.queue), list(q2.queue), list(q3.queue), list(q4.queue), list(q5.queue), list(q6.queue)]
            pattern_dict = {
                    "1st Total Write" : qlist[0][0][0], productname+"1st Write" : qlist[0][0][1],
                    "1st Total Read" : qlist[3][0][0], productname+"1st Read" : qlist[3][0][1],
                    "2nd Total Write" : qlist[1][0][0], productname+"2nd Write" : qlist[1][0][1],
                    "2nd Total Read" : qlist[4][0][0], productname+"2nd Read" : qlist[4][0][1],
                    "3rd Total Write" : qlist[2][0][0], productname+"3rd Write" : qlist[2][0][1],
                    "3rd Total Read" : qlist[5][0][0], productname+"3rd Read" : qlist[5][0][1]
            }
            df = pd.DataFrame.from_dict(pattern_dict, orient='index')
            df = df.transpose()
            print(df)
            df.to_csv(productname+'_GCPolicy.csv', index=False)
            plotGC(fn, qlist, productname, y_scale)
            f1 = plt.figure('Write compare')
            for i in range(int(len(qlist)/2)):
                plt.plot(qlist[i][0][0], qlist[i][0][1], label = productname+'_'+str(i+1)+'_round_write')
            plt.title('GC Policy Test - Write Q128T1', fontsize=15, fontweight='bold')
            plt.ylim(bottom=0)
            plt.xlabel('Host Write(GB)')
            plt.ylabel(y_scale)
            plt.legend(loc=1)
            plt.grid(True, linestyle = "-", color = 'gray' , linewidth = '0.5', axis='y')
            f2 = plt.figure('Read compare')
            for i in range(int(len(qlist)/2)):
                plt.plot(qlist[i+3][0][0], qlist[i+3][0][1], label = productname+'_'+str(int(i+1))+'_round_Read')
            plt.title('GC Policy Test - Read Q128T1', fontsize=15, fontweight='bold')
            plt.ylim(bottom=0)
            plt.xlabel('Host Read(GB)')
            plt.ylabel(y_scale)
            plt.legend(loc=1)
            plt.grid(True, linestyle = "-", color = 'gray' , linewidth = '0.5', axis='y')
            plt.show()
        else:
            print('ERROR: Please enter the correct number.')


if __name__ == '__main__':
    main()