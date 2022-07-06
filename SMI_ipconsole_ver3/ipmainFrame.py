from PyQt5 import QtWidgets, QtCore
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import smi_ipconsole_v3_ui as ui
import sys
import wmi
import numpy as np
import logging
import os
import time
import queue

class Main(QMainWindow, ui.Ui_MainWindow):
    # UI 初始化
    def initiaztion(self, booling):
        self.lineEdit.setDisabled(booling)
        self.lineEdit_2.setDisabled(booling)
        self.lineEdit_4.setDisabled(booling)
        self.lineEdit_5.setDisabled(booling)

    def initialAct(self):
        wmiService = wmi.WMI()
        colNicConfigs = wmiService.Win32_NetworkAdapterConfiguration(IPEnabled = True)
        objNicConfig = colNicConfigs[0]
        return objNicConfig

    def getMBInfo(self):
        wmiService = wmi.WMI()
        os_info = wmiService.Win32_OperatingSystem()[0]
        BIOSInfo = wmiService.Win32_BIOS()[0]
        Processor = wmiService.Win32_Processor()[0]
        wmi_object_memory = wmiService.Win32_PhysicalMemory()
        RAMCapacity = []
        for i in range(len(wmi_object_memory)):
            RAMInfo = wmi_object_memory[i]
            RAMCapacity = np.array(np.append(RAMCapacity, RAMInfo.Capacity), dtype="float_")
            #print(RAMInfo.Capacity)
        # 1 Bytes = 9.313225746154785×10-10 Gigabytes 
        Capacity = sum(RAMCapacity)*(9.313225746154785)*10**(-10)
        return os_info, BIOSInfo, Processor, Capacity

    def showInfo(self):
        # Switch to tab of Info(second page)
        self.tabWidget.setCurrentIndex(1)
        self.textBrowser.clear()
        # Get NetworkAdapterConfiguration and os information
        objNicConfig= self.initialAct()
        os_info, BIOSInfo, Processor, Capacity = self.getMBInfo()
        self.textBrowser.append("NetworkAdapter: "+str(objNicConfig.Description)+"\nIP(IPV4, IPV6): "+str(objNicConfig.IPAddress)+"\nIPGateway: "+str(objNicConfig.DefaultIPGateway)
                                                +"\nDNSServer: "+str(objNicConfig.DNSServerSearchOrder)+"\nSubnetMasks: "+str(objNicConfig.IPSubnet[0]))
        self.textBrowser.append("OS Name: "+str(os_info.Caption)+"\nBuild Number: "+str(os_info.BuildNumber))
        self.textBrowser.append("CPU Name: "+str(Processor.Name)+"\nManufacturer: "+str(BIOSInfo.Manufacturer)+"\nBIOS version: "+str(BIOSInfo.SMBIOSBIOSVersion)+"\nRAM Capacity: "+str(Capacity)+"GB")
        return True

    def setConfig(self):
        try:
            # Set static Ip
            if self.radioButton_2.isChecked():
                # Switch to tab of Info(second page)
                self.tabWidget.setCurrentIndex(1)
                self.textBrowser.append('Start setting static Ip configuration...')
                istep = 1
                objNicConfig= self.initialAct()
                IPaddress_str = str(self.lineEdit_3.text())
                ipline = IPaddress_str.split(".")
                inDefaultGateways = [str(ipline[0])+'.'+str(ipline[1])+'.'+str(ipline[2])+'.254']
                inSubnetMasks = [str(objNicConfig.IPSubnet[0])]
                inGatewayCostMetrics = [1]
                #inDNSServers = [str(objNicConfig.DNSServerSearchOrder[0]),str(objNicConfig.DNSServerSearchOrder[1])]
                inIPaddress = [IPaddress_str]
                # Start to setting static Ip
                returnValue = objNicConfig.EnableStatic(IPAddress = inIPaddress, SubnetMask = inSubnetMasks)
                if returnValue[0] == 0 or returnValue[0] == 1:
                    self.textBrowser.append('Successfully setting IP')
                    istep += istep
                else:
                    self.textBrowser.append('ERROR: IP or SubnetMask setting error')
                    return
                returnValue = objNicConfig.SetGateways(DefaultIPGateway = inDefaultGateways, GatewayCostMetric = inGatewayCostMetrics)
                if returnValue[0] == 0 or returnValue[0] == 1:
                    self.textBrowser.append('Successfully setting Gateways')  
                    istep += istep          
                else:
                    self.textBrowser.append('ERROR: Gateways Setting error')
                    return
                returnValue = objNicConfig.SetDNSServerSearchOrder()
                if returnValue[0] == 0 or returnValue[0] == 1:
                    self.textBrowser.append('Successfully setting AutoDNS')
                    istep += istep
                else:
                    self.textBrowser.append(str(returnValue)+'ERROR: DNS Setting error')
                    return
            #Set DHCP
            if self.radioButton.isChecked():
                self.textBrowser.append('Start setting DHCP configuration...')
                #Initial DHCP
                objNicConfig= self.initialAct()
                # Enable DHCP
                returnValue = objNicConfig.EnableDHCP()
                if returnValue[0] == 0 or returnValue[0] == 1:
                    self.textBrowser.append('Successfully setting DHCP')
                else:
                    self.textBrowser.append('Fail to set DHCP')
                    return
                returnValue = objNicConfig.SetDNSServerSearchOrder()
                if returnValue[0] == 0 or returnValue[0] == 1:
                    self.textBrowser.append('Successfully setting AutoDNS')
                else:
                    self.textBrowser.append('Fail to set AutoDNS')
                    return
                self.textBrowser.append('DHCP Enable!')
        except:
            # record log file for error code
            realtime = time.strftime("%Y%m%d_%H%M%S", time.localtime())
            FORMAT = '%(asctime)s %(levelname)s: %(message)s'
            Filepath = os.path.dirname(os.path.realpath(__file__))+"\\log\\"+str(realtime)+"_errorcode.log"
            logging.basicConfig(level=logging.DEBUG, filename=Filepath, filemode='w', format=FORMAT)
            logging.error("Catch an exception.", exc_info=True)
            QtWidgets.QMessageBox.information(self, 'ERROR', 'Please check log file', QtWidgets.QMessageBox.Cancel)
            self.textBrowser.setText('Architecture ERROR...')

    #Checkbox 觸發訊號
    def checkToggled(self):
        if self.checkBox.isChecked():
            self.initiaztion(False)
        else:
            self.initiaztion(True)

    def itemClicked_event(self, item):
        # checkState = 0(No select), = 2(select)
        if item.checkState() == 2:
            print(item.text())
        return True
    
    def selectAll_item(self, item):
        for i in range(self.listWidget.count()):
            print(item.text())
        return True
    
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.initiaztion(True)
        self.pushButton.clicked.connect(self.showInfo)
        self.pushButton_2.clicked.connect(self.setConfig)
        self.listWidget.itemChanged.connect(self.itemClicked_event)
        self.checkBox.toggled.connect(self.checkToggled)
        if self.checkBox_2.isChecked() == True:
            print("1")

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = Main()
    window.show()
    sys.exit(app.exec_())