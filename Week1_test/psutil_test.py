#使用psutil來獲取分割槽資訊

import psutil

disk = psutil.disk_partitions()
print(psutil.disk_usage)
print("-------------------------------------------------------")

for i in disk:
    print("磁碟：%s   分割槽格式:%s" % (i.device, i.fstype)) # 碟符  分割槽格式
    disk_use = psutil.disk_usage(i.device) 

    print("使用了：%.1f GB,\n空閒：%.1f GB,\n總共：%.1f GB,\n使用率%.1f%%,\n" % (
        disk_use.used / 1024 / 1024 / 1024, disk_use.free / 1024 / 1024 / 1024, disk_use.total / 1024 / 1024 / 1024,
        disk_use.percent))

print("-------------------------------------------------------")

#Memory Situation
memory = psutil.virtual_memory()
# memory.used  使用的
# memory.total  總共
ab = float(memory.used) / float(memory.total) * 100
print("記憶體使用率為:%.2f%%" % ab)




#法二: 用Python來操作CMD指令

#import os
#os.system('cmd /k "diskpart&&list disk"') 




# Get disk serial number
# import win32api

# path = "C:/"
# info = win32api.GetVolumeInformation(path)
# print( "disk serial number = %d" % info[1] )


# Get Disk Information
# import os 
# os.system('cmd /k "wmic logicaldisk list brief')


