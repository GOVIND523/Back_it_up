import subprocess
import shutil
from datetime import datetime
import requests
import os
from datetime import timedelta
import json

#function definitions

"""
pull_upate_local function will update the local repo by pulling the changes from remote repo it any
"""

def pull_update_local():
  try:
    subprocess.run(['git','-C', "/home/vboxuser/Back_it_up", 'pull', 'origin', 'main'], check=True)
    print("Upated the local repository")
  except subprocess.CalledProcessError:
    print("Could not update local repository");
    
    
    
"""
make_backup function 
1. capture the timestamp
2. create the local repos zip an store it in local backup folder with the timestamp
3. upload the folder to google drive 
4. delete the local backup that we created
5. check curl value and send a backup notification if enabled
"""
 
def make_backup():
  #1
  tstamp = datetime.now().strftime("||%m--%d--%Y||%H::%M::%S")
  #2
  local_backup = f"/home/vboxuser/Back_it_up/Backup{tstamp}"
  shutil.make_archive(local_backup , "zip" , "/home/vboxuser/Back_it_up")
  #3
  subprocess.run(["rclone","copy",f"{local_backup}.zip","remote:Back_it_up/"], check= True)
  #4
  os.remove(f"{local_backup}.zip")
   	
   	
    	
"""
check_rotation function keeps only latest files as {daily} files daily, {monthly} files monthly, {weekly} files weekly
"""
def delete(filename):
    subprocess.run(["rclone", "delete", f"remote:Back_it_up/{filename}"])

def daily_check_rotation():

        daily = 4
        remote_files = subprocess.check_output(["rclone", "lsjson", "remote:Back_it_up"]).decode('utf-8')
        backup_info = json.loads(remote_files)
        sorted_backups = sorted(backup_info, key=lambda x: datetime.fromisoformat(x["ModTime"][:-1]), reverse=True)
        today = datetime.today().date()
        daily_backups = sorted_backups[:daily]

        for backup in sorted_backups[daily:]:
            print(f"Deleting: {backup['Name']}")
            delete(backup["Name"])

        print("Rotation Completed Successfully")

def weekly_check_rotation():
    
        weekly = 2
        remote_files = subprocess.check_output(["rclone", "lsjson", "remote:Back_it_up"]).decode('utf-8')
        backup_info = json.loads(remote_files)
        sorted_backups = sorted(backup_info, key=lambda x: datetime.fromisoformat(x["ModTime"][:-1]), reverse=True)
        today = datetime.today().date()
        weekly_backups = [backup for backup in sorted_backups if (today - datetime.fromisoformat(backup["ModTime"][:-1]).date()).days <= weekly]

        for backup in sorted_backups[weekly:]:
            print(f"Deleting: {backup['Name']}")
            delete(backup["Name"])

        print("Weekly Rotation Completed Successfully")


def monthly_check_rotation():
    
        monthly = 1
        remote_files = subprocess.check_output(["rclone", "lsjson", "remote:Back_it_up"]).decode('utf-8')
        backup_info = json.loads(remote_files)
        sorted_backups = sorted(backup_info, key=lambda x: datetime.fromisoformat(x["ModTime"][:-1]), reverse=True)
        today = datetime.today().date()
        monthly_backups = [backup for backup in sorted_backups if (today - datetime.fromisoformat(backup["ModTime"][:-1]).date()).days <= monthly]

        for backup in sorted_backups[monthly:]:
            print(f"Deleting: {backup['Name']}")
            delete(backup["Name"])

        print("Monthly Rotation Completed Successfully")


"""
notify() will notify on successfull execution of the script
"""

def notify():
  tstamp = datetime.now().strftime("||%m--%d--%Y||%H::%M::%S")
  Enable_Curl = True
  if Enable_Curl:
    response = requests.post("https://webhook.site/e45e6bab-8f6f-4525-a95e-314c029bae1a", json={"project" : "backitup","date": tstamp, "test":"Success"}) 
    if response.ok:
    	print("Request was successful")
    else:
    	print("Request failed")
    	
    	
    	
#function calls

#updating local repo	
pull_update_local()

#create a backup an upload on drive using rclone
make_backup()

#checking the rotations
daily_check_rotation()
weekly_check_rotation()
monthly_check_rotation()	

#notification
#notify()



