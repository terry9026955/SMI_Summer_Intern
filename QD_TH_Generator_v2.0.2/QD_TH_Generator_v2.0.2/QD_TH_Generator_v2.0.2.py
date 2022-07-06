#from mpl_toolkits.mplot3d import Axes3D
import numpy as np
import csv
import pandas as pd
import queue
#import matplotlib.pyplot as plt

def readName(filepath):
    if filepath[0] == '"':
        filepath = filepath.split('"')
        filepath = filepath[1]
        print(filepath)
    else:
        filepath = filepath
    return filepath

def GtorTH1(file):
    istep = 0
    andWrite = []
    andRead = []
    andMix = []
    with open(file, 'r') as f:
        rawwork = csv.reader(f)
        for row in rawwork:
            if "'Target Type" in row:
                istep += 1
                if istep == 1:
                    ind = row.index('IOps')
                    indMB = row.index('MBps (Decimal)')
                    target = row.index('Access Specification Name')
                    #print(target)
            elif 'WORKER' in row:
                if row[target] == '4K RND WRITE':
                    andWrite = np.append(andWrite, row[ind])
                if row[target] == '4K RND READ':
                    andRead = np.append(andRead, row[ind])
                if row[target] == '4K RND 70R/30W':
                    andMix = np.append(andMix, row[ind])
                if row[target] == '128K SEQ WRITE':
                    andWrite = np.append(andWrite, row[indMB])
                if row[target] == '128K SEQ READ':
                    andRead = np.append(andRead, row[indMB])
                if row[target] == '128K SEQ 70R/30W':
                    andMix = np.append(andMix, row[indMB])
        #print(andWrite)
        #print(andRead)
        #print(andMix)
    return andWrite, andRead, andMix

def GtormultiTH(file):
    istep = 0
    andWrite = []
    andRead = []
    andMix = []
    q1 = queue.Queue()
    with open(file, 'r') as f:
        rawwork = csv.reader(f)
        for row in rawwork:
            if "'Target Type" in row:
                istep += 1
                if istep == 1:
                    ind = row.index('IOps')
                    indMB = row.index('MBps (Decimal)')
                    target = row.index('Access Specification Name')
                    ind_name = row.index('Target Name')
                    #print(target)
            elif 'WORKER' in row:
                q1.put(row)
    type = len(np.unique(np.array(list(q1.queue))[:,ind_name]))
    #print(type)
    for row in list(q1.queue):
        if row[target] == '4K RND WRITE':
            andWrite = np.append(andWrite, row[ind])
        if row[target] == '4K RND READ':
            andRead = np.append(andRead, row[ind])
        if row[target] == '4K RND 70R/30W':
            andMix = np.append(andMix, row[ind])
        if row[target] == '128K SEQ WRITE':
            andWrite = np.append(andWrite, row[indMB])
        if row[target] == '128K SEQ READ':
            andRead = np.append(andRead, row[indMB])
        if row[target] == '128K SEQ 70R/30W':
            andMix = np.append(andMix, row[indMB])
    with q1.mutex:
        q1.queue.clear()
    print(q1.empty())
    for i in range(int(len(andWrite)/type)):
        #a = np.sum(np.array(andWrite[i*type:i*type+type], dtype='float_'))
        q1.put(np.sum(np.array(andWrite[i*type:i*type+type], dtype='float_')))
    andWrite = list(q1.queue)
    with q1.mutex:
        q1.queue.clear()
    for i in range(int(len(andRead)/type)):
        q1.put(np.sum(np.array(andRead[i*type:i*type+type], dtype='float_')))
    andRead = list(q1.queue)
    with q1.mutex:
        q1.queue.clear()
    for i in range(int(len(andMix)/type)):
        q1.put(np.sum(np.array(andMix[i*type:i*type+type], dtype='float_')))
    andMix = list(q1.queue)
    with q1.mutex:
        q1.queue.clear()
    #print(andWrite)
    #print(andRead)
    #print(andMix)
    return andWrite, andRead, andMix

def getlog(filepath):
    nstep = 0
    getfile = readName(filepath)
    getmode = getfile.split('_')
    for item in getmode:
        if '4K' in item:
            mode = '4K'
        elif '128K' in item:
            mode = '128K'
        item = item.split('-')
        try:
            if 'TH1' in item:
                mode = mode+'_TH1'
                w, r, m = GtorTH1(getfile)
            else:
                if nstep == 0:
                    if 'TH2' in item:
                        mode = mode+'_TH2'
                        nstep += 1
                    elif 'TH4' in item:
                        mode = mode+'_TH4'
                        nstep += 1
                    elif 'TH8' in item:
                        mode = mode+'_TH8'
                        nstep += 1
                    elif 'TH16' in item:
                        mode = mode+'_TH16'
                        nstep += 1
                    if nstep == 1:
                        w, r, m = GtormultiTH(getfile)
        except:
            print('Ignore rule...')
    return w, r, m, mode

def main():
    while 0==0:
        try:
            product_name = input('Please enter your product name: ')
            Qindex = ['QD1','QD2','QD4','QD8','QD16','QD32','QD64','QD128','QD256','QD512','QD1024','QD2048']
            TH = ['TH1', 'TH2', 'TH4', 'TH8', 'TH16']
            qtype = queue.Queue()
            qmode = queue.Queue()
            for i in range(5):
                #print('Please enter the file path of your csvfile, 5 of {}:'.format(i+1))
                filepath = input('Please enter the file path of your csvfile, {} of 5:'.format(i+1))
                locals()['file'+str(i)] = getlog(filepath)
                print(locals()['file'+str(i)])
                qmode.put(locals()['file'+str(i)][len(locals()['file'+str(i)])-1].split('_')[0])
                qtype.put(locals()['file'+str(i)][len(locals()['file'+str(i)])-1].split('_')[1])
                
                locals()[str(list(qtype.queue)[i])] = {
                    "Write" : locals()['file'+str(i)][0], "Read" : locals()['file'+str(i)][1], "Mix" : locals()['file'+str(i)][2]
                }
                #print(locals()[str(list(qtype.queue)[i])])
                
                locals()['df_'+str(TH.index(str(list(qtype.queue)[i])))] = pd.concat({k: pd.Series(v, index=Qindex, name=str(list(qtype.queue)[i])) for k, v in locals()[str(list(qtype.queue)[i])].items()})
                print(locals()['df_'+str(TH.index(str(list(qtype.queue)[i])))])
                if i == 4:
                    for j in range(4):
                        if j == 0:
                            try:
                                t = pd.concat([locals().get(('df_'+str(j))), locals().get(('df_'+str(j+1)))], axis=1)
                            except:
                                print('Please inspect your file and guarantee all of them are in different thread.')
                        else:
                            t = pd.concat([t, locals().get(('df_'+str(j+1)))], axis=1, join='outer')
            print(t)
            check_li = np.array(np.unique(list(qtype.queue)))
            if len(np.unique(list(qmode.queue))) != 1:
                print('Please chek your file name all in the same mode(4K or 128K)!!')
            else:
                #print((TH == check_li).any())
                if (len(check_li)) == len(TH):
                    print('pass')
                    t.to_csv(product_name + '_' + np.array(np.unique(list(qmode.queue)))[0] +'_QDvsTH_list.csv')
                    #nmp = np.array(t.to_numpy(), dtype='float_')
                    #print(nmp)
                    
                    with qtype.mutex:
                        qtype.queue.clear()
                    with qmode.mutex:
                        qmode.queue.clear()
                    
                else:
                    print('Error: Please ensure all your files are in different theard.')
        except:
            print('Unknow Fail...')
        
            

if __name__ == '__main__':
    main()
