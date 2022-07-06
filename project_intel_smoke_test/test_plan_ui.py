from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import sys
import mainui as ui
import subprocess
import use_inbox_delete_smi_driver_tp
import configparser
import os
import logging
import time

class Main(QMainWindow, ui.Ui_MainWindow):
    
    version_number = "20220428_BETA"
    # determine if application is a script file or frozen exe
    if getattr(sys, 'frozen', False):
        wrapper_path = os.path.dirname(sys.executable)
    elif __file__:
        wrapper_path = os.path.dirname(__file__)

        
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        #self.setAcceptDrops(True)
        self.initiAct()
        self.setAcceptDrops(True)
        

        self.list_add_text()
        self.pushButton_2.clicked.connect(self.removeSel)
        self.pushButton_3.clicked.connect(self.getfile)
        self.pushButton.clicked.connect(self.get_list_item)

        self.comboBox.currentIndexChanged.connect(self.enableCheckbox)
    


    def enableCheckbox(self):
        val = str(self.comboBox.currentText())

        if val == "DVT":
            self.checkBox.setEnabled(True)
            self.checkBox.setChecked(False)
        elif val == "3rd party":
            self.checkBox.setEnabled(False)
            self.checkBox.setChecked(True)
        else:
            self.checkBox.setEnabled(True)




    def loadini(self):

        settings = QSettings(Main.wrapper_path+'/config.ini', QSettings.IniFormat)

        return settings


    def initiAct(self):
        try:
            config = configparser.ConfigParser()
            config.read(Main.wrapper_path+'/config.ini')

            ini = self.loadini()

            ini_selection = ini.value("test_plan/selection")

            ini_branch = ini.value("Branch/branch")

            ini_SHA = ini.value("SHA/SHA")
            try:
                

                ini_file = config['%General']

                filelist = ini_file.parser._sections["%General"]
                
                for k,v in filelist.items():
                    
                    self.listWidget.addItem(filelist[k])

                self.comboBox.addItems(ini_selection)
            except:
                tigger = False
                with open(Main.wrapper_path+"/config.ini", 'r') as f:
                    for row in f:
                        if "[%General]" in row:
                            tigger = True
                            pass
                        if tigger == True:
                            #print(row)
                            if "filepath_" in row:
                                name = row.split("=")[1]
                                #print(name)
                                
                                self.listWidget.addItem(name)

            self.lineEdit.setText(ini_branch)
            self.lineEdit_2.setText(ini_SHA)
            self.run_memory()
        except Exception:
            Log_Format = "%(levelname)s %(asctime)s - %(message)s"
            real_time = time.strftime("%Y%m%d_%H%M%S", time.localtime())
            log_name = Main.wrapper_path+"/log/"+real_time+"_logfile.log"
            logging.basicConfig(filename = log_name,
                                filemode = "w",
                                format = Log_Format, 
                                level = logging.DEBUG)

            logger = logging.getLogger()

            #Testing our Logger

            logger.error("Error Message from initiAct", exc_info=True)
        

    def dragEnterEvent(self, event):

        
        event.accept()
        event.acceptProposedAction()
        



    def dropEvent(self,event):

        
        file_name = event.mimeData().text()

        if 'file:///' in file_name:
            file_name = file_name.replace('file:///', '')
            #print(file_name)
        
            self.listWidget.addItem(file_name) 
            


    def list_add_text(self):

        self.listWidget.setDragEnabled(True)
        self.listWidget.setAcceptDrops(True)

        return


    def removeSel(self):

        listItems = self.listWidget.selectedItems()

        config = configparser.ConfigParser()
        config.read(Main.wrapper_path+'/config.ini')
        if not listItems: return

        for item in listItems:
            
            a = self.listWidget.item(self.listWidget.row(item)).text()
            print(a)
            self.listWidget.takeItem(self.listWidget.row(item))

            
            for i in config.options("%General"):
                if config.get("%General", i) == a:

                    print(i, '=', config.get("%General", i))
                
                    if config.has_section("%General") == True:

                        config.remove_option("%General", i)
                        config.write(open(Main.wrapper_path+'/config.ini', 'w'))
            

    # def get_list_item(self):

    #     for i in range(self.listWidget.count()):
    #         #res = yield self.listWidget.item(i)
        
    #         print(self.listWidget.item(i).text())

    def create_batch_run(self, wrapper_path):
        file_name = 'RunOnce.bat'
        f = open(file_name, 'w+')
        script = "cd /d "+ wrapper_path + "\ncall " + wrapper_path+"\\test_plan_ui_"+Main.version_number+".exe"
        f.write(script)
        f.close()
        return



    def reboot_reg(self, wrapper_path):
        cmd_reg = ["reg", "add", "HKEY_LOCAL_MACHINE\Software\Microsoft\Windows\CurrentVersion\RunOnce", "/v", "RunScript", "/t", "REG_SZ", "/d", wrapper_path+"\\RunOnce.bat"]
        r = subprocess.run(cmd_reg, stdout=subprocess.PIPE)
        if r.returncode == 0:
            pass
        else:
            print(r.returncode)
        


    def getfile(self):

        
        ini = self.loadini()
        dig = QFileDialog.getExistingDirectory()
        # # setting gui can open any files
        # dig.setFileMode(QFileDialog.AnyFile)
        # #
        # dig.setFilter(QDir.Files)
        ini.setValue("Folder/path", dig)

        config = configparser.ConfigParser()
        config.read(Main.wrapper_path+'/config.ini')
        try:
            config.add_section('%General')
        except:
            pass

        if dig != "":
            filelist = os.listdir(dig)
            print(filelist)

            if len(filelist) != 0:
                
                filenumber = 0

                for i in range(len(filelist)):
                    
                    if ".bat" in filelist[i]:
                        
                        filenumber = filenumber + 1

                        self.listWidget.addItem(filelist[i])

                        config.set('%General',"filepath_"+str(filenumber), filelist[i])

                        newini = open("config.ini", 'w')
                        config.write(newini)
                        newini.close

                        #ini.setValue("General/filepath_"+str(i+1), filelist[i])

                    if ".exe" in filelist[i]:
                        
                        filenumber = filenumber + 1

                        self.listWidget.addItem(filelist[i])


                        config.set('%General',"filepath_"+str(filenumber), filelist[i])

                        newini = open(Main.wrapper_path+'/config.ini', 'w')
                        config.write(newini)
                        newini.close
            else:
                None


        return


    def renew_ini(self):
        
        new_scriptlist = []
        config = configparser.ConfigParser()
        config.read(Main.wrapper_path+'/config.ini')

        for i in range(self.listWidget.count()):
            #res = yield self.listWidget.item(i)
            scriptname = str(self.listWidget.item(i).text())
            new_scriptlist.append(scriptname)

        ini_file = config['%General']

        filelist = ini_file.parser._sections["%General"]
        
        istep = 0
        restigger = False
        for op,s in filelist.items():
            istep = istep + 1

            if restigger == True:
                config.set("Runonce_trigger", "started", op)
                restigger = False

            config.set("%General", op, new_scriptlist[istep-1])
            if "Restart" in new_scriptlist[istep-1]:
                restigger = True
                
            with open('config.ini', 'w') as configfile:
                config.write(configfile)
        
        



    def run_memory(self):
        
        try:
            config = configparser.ConfigParser()
            config.read(Main.wrapper_path+'/config.ini')

            tigger = config['Runonce_trigger']['tigger']
            path = config['Folder']['path']
            path = path.replace("/", "\\")
            started_tigger = False
            
            if tigger == "1":
                started = config['Runonce_trigger']['started']
                filelist = config['%General']
                for key in filelist:
                    
                    if key == started:
                        started_tigger = True
                        # print(key)
                        # print(config['%General'][key])
                    if started_tigger == True:
                        
                        next_file = config['%General'][key]
                        next_file = next_file.split(".")[0]
                        print("Run on next file or script : " + next_file)
                        #print(path+"\\"+next_file+".bat")
                        #r = subprocess.run(["cd", "/d", path], stdout=subprocess.PIPE)
                        r = subprocess.run([path+"/"+next_file+".bat"], stdout=subprocess.PIPE, shell=True)

                        if r.returncode != 0:
                            print("Got return code not success.")
                            print(r.stdout)

                config.set('Runonce_trigger',"tigger", "0")

                newini = open(Main.wrapper_path+'/config.ini', 'w')
                config.write(newini)
                newini.close
                
        except Exception:

            Log_Format = "%(levelname)s %(asctime)s - %(message)s"
            real_time = time.strftime("%Y%m%d_%H%M%S", time.localtime())
            log_name = Main.wrapper_path+"/log/"+real_time+"_logfile.log"
            logging.basicConfig(filename = log_name,
                                filemode = "w",
                                format = Log_Format, 
                                level = logging.DEBUG)

            logger = logging.getLogger()

            #Testing our Logger

            logger.error("Error Message from run_memory", exc_info=True)

        return



    def get_list_item(self):
        try:
            self.renew_ini()
            branch_input = self.lineEdit.text()
            SHA_input = self.lineEdit_2.text()

            setting = self.loadini()
            setting.setValue("Branch/branch", branch_input)
            setting.setValue("SHA/SHA", SHA_input)

            folderpath = setting.value("Folder/path")
            
            for i in range(self.listWidget.count()):
                #res = yield self.listWidget.item(i)
                scriptname = str(self.listWidget.item(i).text())

                file_path = folderpath + "/" + scriptname
                

                if scriptname != "":
                    
                    if "0-1_NVMe_Preparation_2269" in file_path:

                        if branch_input == "":

                            branch_input = ""

                        if SHA_input == "":

                            SHA_input = ""

                        procress = subprocess.run([file_path, branch_input, SHA_input])

                        if self.checkBox.isChecked():
                            command = use_inbox_delete_smi_driver_tp.main()
                            print(123)

                    elif "Restart" in file_path:

                        setting.setValue("Runonce_trigger/tigger", "1")
                        self.create_batch_run(Main.wrapper_path)
                        self.reboot_reg(Main.wrapper_path)
                        procress = subprocess.run([file_path])

                        break

                    else:

                        procress = subprocess.run([file_path])

                    if procress.returncode == 0:
                        pass
                    else:
                        print("Got return code not success.")
                        print(procress.stdout)


        except Exception:

            Log_Format = "%(levelname)s %(asctime)s - %(message)s"
            real_time = time.strftime("%Y%m%d_%H%M%S", time.localtime())
            log_name = Main.wrapper_path+"/log/"+real_time+"_logfile.log"
            logging.basicConfig(filename = log_name,
                                filemode = "w",
                                format = Log_Format, 
                                level = logging.DEBUG)

            logger = logging.getLogger()

            #Testing our Logger

            logger.error("Error Message from get_list_item", exc_info=True)

        
if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = Main()
    window.show()
    sys.exit(app.exec_())