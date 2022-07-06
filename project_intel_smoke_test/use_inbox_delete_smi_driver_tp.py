import platform
import os
import sys
import subprocess
import re
import time
import logging
import json



def catchTimeandError(consolePath):
    
    # record log file for error code
    realtime = time.strftime("%Y/%m/%d_%H:%M:%S", time.localtime())
    FORMAT = '%(asctime)s %(levelname)s: %(message)s'
    Filepath = consolePath+"/log/"+str(realtime)+"_errorcode.log"
    return Filepath, FORMAT


def get_driver_list(wrapper_path):
    os_env = platform.system()
    if os_env == 'Windows':
        power_reset_dir = os.path.join(wrapper_path, "power_reset")
        print("path:%s"%(power_reset_dir))
        os.chdir(power_reset_dir)
        cmd = ["pnputil", "-e"]
        r = subprocess.run(cmd, stdout=subprocess.PIPE)
        os.chdir(wrapper_path)                 
    else:
        print("Unsupported Platform")
        
    return r



def get_hwid_by_model(wrapper_path, model_name=None):
    hwid_list = []
    if model_name is None:
        print("Need a specific model_name")
        
    os_env = platform.system()
    if os_env == 'Windows':
        power_reset_dir = os.path.join(wrapper_path, "power_reset")
        print("path:%s"%(power_reset_dir))
        os.chdir(power_reset_dir)
        cmd = ["SmiCli.exe", "--info", "--init", "--commfile=SmiCli_output.json"]
        r = subprocess.run(cmd, stdout=subprocess.PIPE)
        time.sleep(1)
    else:
        print("Unsupported Platform")
        
    try:
        with open("SmiCli_output.json", 'r') as json_file:
            json_obj = json.load(json_file)
            for idx, drive_info in enumerate(json_obj["drive_info_list"]):
                if model_name in drive_info["model"]:
                    hwid_list.append(drive_info["hwid"])
                print(("drive_info[%d]:\n%s")%(idx, drive_info))
    except Exception as e:
            print("Maybe JSONDecodeError or FileNotFoundError\n")
            print("Error msg:%s"%(e))
            
    return hwid_list



def get_driver_published_name(wrapper_path):
    d_list = []
    print("Get driver published name")
    r = get_driver_list(wrapper_path)
    # Check pass or fail
    if r.returncode == 0:
        driver_list = str(r.stdout.decode('cp950')).split('\r\n\r\n')
        #print(r.stdout.decode('cp950'))
        for item in driver_list:
            if "SiliconMotion" in item:
                result = re.search(r'oem\d{1,2}.inf', item)
                if result is None:
                    print("Cannot find SiliconMotion's driver")
                    
                published_name = result.group(0)
                print("SMI driver is {}".format(published_name))
                d_list.append(published_name)
        if len(d_list) != 0:

            return d_list
        else:
            return None
    else:
        print("Execute command fail, r:{}".format(r))
        return None




def update_driver(wrapper_path, driver='C:/Windows/INF/stornvme.inf', hw_id='PCI\CC_010802'):
    print("driver:%s"%(driver))
    print("hw_id:%s"%(hw_id))
    os_env = platform.system()
    if os_env == 'Windows':
        power_reset_dir = os.path.join(wrapper_path, "power_reset")
        print("path:%s"%(power_reset_dir))
        os.chdir(power_reset_dir)
        cmd = ["devcon_amd64.exe", "update", driver, hw_id]
        r = subprocess.run(cmd, stdout=subprocess.PIPE)
        time.sleep(3)
        
    elif os_env == 'Linux':
        print("Unsupported Platform")
        return None
    else:
        print("Unsupported Platform")
        return None
    return r



def delete_driver(driver):
    print("driver:%s"%(driver))
    os_env = platform.system()
    if os_env == 'Windows':
        cmd = ["pnputil.exe", "/delete-driver", driver, "/force"]
        r = subprocess.run(cmd, stdout=subprocess.PIPE)
        time.sleep(3)
    else:
        print("Unsupported Platform")
        
    return r


# def reboot_reg(wrapper_path):
#     cmd_reg = ["reg", "add", "HKEY_LOCAL_MACHINE\Software\Microsoft\Windows\CurrentVersion\RunOnce", "/v", "RunScript", "/t", "REG_SZ", "/d", wrapper_path+"\\use_inbox_delete_smi_driver_tp.exe"]
#     r = subprocess.run(cmd_reg, stdout=subprocess.PIPE)
#     print(r)
#     if r.returncode == 0:
#         time.sleep(3)
#         rt = subprocess.run(["shutdown", "-r", "-t", "10"])
#     else:
#         print(r.returncode)
#         print("Fail to add registry, please implement by manual...")


def main():

    # determine if application is a script file or frozen exe
    if getattr(sys, 'frozen', False):
        wrapper_path = os.path.dirname(sys.executable)
    elif __file__:
        wrapper_path = os.path.dirname(__file__)

    try:    
        istep = 0
        #wrapper_path = os.path.dirname(os.path.realpath(__file__))
        published_name = get_driver_published_name(wrapper_path)

        # # Get hwid
        # hwid_list = get_hwid_by_model(model_name=mptool_config["model_name"])
        # if len(hwid_list) == 0:
        #     print("There is no %s deive."%(mptool_config["model_name"]))
        #     sys.exit(1)
        # elif len(hwid_list) > 1:
        #     print("There are more than one %s devices."%(mptool_config["model_name"]))
        #     sys.exit(1)
        # print("hwid:%s"%(str(hwid_list[0])))

        if published_name != None:
            while True:
                driverstatus = update_driver(wrapper_path)
                if driverstatus.returncode == 0:
                    print("Change inbox driver - PASS")
                    break
                elif driverstatus.returncode == 1:
                    print("Change inbox driver - PASS, but require reboot")

                    #reboot_reg(wrapper_path)
                    break
                    
                else:
                    istep = istep + 1
                    print("Change inbox driver - Fail")

                    if istep > 3:
                        print("Change inbox driver - Fail")

                        #reboot_reg(wrapper_path)
                        return "Change inbox driver - Fail"
        
        
            istep = 0
            for driver in published_name:
                while True:
                    deletestatus = delete_driver(driver)
                    if deletestatus.returncode == 0:
                        print("Delete smi driver {} - PASS".format(str(driver)))
                        break
                    else:
                        istep = istep + 1
                        print("Delete smi driver {} - Fail".format(str(driver)))
                        print("Retry delete smi driver {}".format(str(driver)))
                        if istep > 3:
                            print("Delete smi driver {} - Fail".format(str(driver)))
                            
                            #reboot_reg(wrapper_path)
                            return "Delete smi driver Fail"
            
            
            published_name = get_driver_published_name(wrapper_path)

            if published_name == None:
                print("There is no smi driver.")

        else:
            print("Cannot find SiliconMotion's driver")

        #os.system("pause")
        
    except Exception:
        Filepath, FORMAT = catchTimeandError(wrapper_path)
        logging.basicConfig(level=logging.DEBUG, filename=Filepath, filemode='w', format=FORMAT)
        logging.error("Catch an exception.", exc_info=True)

    
    

if __name__ == '__main__':
    main()