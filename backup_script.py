import subprocess
import shutil
from datetime import datetime
import requests
import os
from datetime import timedelta
import json

#variables

Project_dir = "/home/vboxuser/Back_it_up"
Curl_enable = True
Webhook_url = "https://webhook.site/e45e6bab-8f6f-4525-a95e-314c029bae1a"
Gdrive_folder= "Back_it_up"
Back_daily = 1
Back_weekly = 7
Back_monthly = 12
tstamp = datetime.now().strftime("||%m--%d--%Y||%H::%M::%S")


#function definitions

"""
-------------------------------------------------------------------------------------
pull_upate_local() 

  Will update your local repo by pulling the changes from remote repo it any
-------------------------------------------------------------------------------------
"""

def pull_update_local():
  try:
    subprocess.run(['git','-C', Project_dir , 'pull', 'origin', 'main'], check=True)
    print("Updated the local repository")
  except subprocess.CalledProcessError:
    print("Could not update local repository");
    
      
"""
-------------------------------------------------------------------------------------
make_backup()  

  1. Create the local repos zip an store it in local backup folder with the timestamp
  2. Upload the folder to google drive 
  3. Delete the local backup that we created
-------------------------------------------------------------------------------------
"""
 
def make_backup():
  #1
  local_backup = f"{Project_dir}/Backup{tstamp}"
  shutil.make_archive(local_backup , "zip" , Project_dir)
  #2
  subprocess.run(["rclone","copy",f"{local_backup}.zip","remote:{Gdrive_folder}/"], check= True)
  #3
  os.remove(f"{local_backup}.zip")
   	

"""
-------------------------------------------------------------------------------------
check_rotation()  

  1. Check daily rotation delete unwanted backups
  2. Check weekly rotation delete unwanted backups
  3. Check monthly rotation delete unwanted backups
-------------------------------------------------------------------------------------
"""
def delete(filename):
  rm_file = f"remote:{Gdrive_folder}/{filename}"
  subprocess.run(["rclone", "delete", rm_file])

def daily_check_rotation():
  remote = f"remote:{Gdrive_folder}"
  daily = Back_daily
  remote_files = subprocess.check_output(["rclone", "lsjson", remote]).decode('utf-8')
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
        remote_files = subprocess.check_output(["rclone", "lsjson", remote]).decode('utf-8')
        backup_info = json.loads(remote_files)
        sorted_backups = sorted(backup_info, key=lambda x: datetime.fromisoformat(x["ModTime"][:-1]), reverse=True)
        today = datetime.today().date()
        weekly_backups = [backup for backup in sorted_backups if (today - datetime.fromisoformat(backup["ModTime"][:-1]).date()).days <= weekly]

        for backup in sorted_backups[weekly:]:
            print(f"Deleting: {backup['Name']}")
            delete(backup["Name"])

def monthly_check_rotation():
    
        monthly = 1
        remote_files = subprocess.check_output(["rclone", "lsjson", remote]).decode('utf-8')
        backup_info = json.loads(remote_files)
        sorted_backups = sorted(backup_info, key=lambda x: datetime.fromisoformat(x["ModTime"][:-1]), reverse=True)
        today = datetime.today().date()
        monthly_backups = [backup for backup in sorted_backups if (today - datetime.fromisoformat(backup["ModTime"][:-1]).date()).days <= monthly]

        for backup in sorted_backups[monthly:]:
            print(f"Deleting: {backup['Name']}")
            delete(backup["Name"])


"""
-------------------------------------------------------------------------------------
notify() 

  Will notify on successfull execution of the script
-------------------------------------------------------------------------------------
"""

def notify():
  curl = Curl_enable
  if curl:
    response = requests.post(Webhook_url, json={"project" : Project_dir ,"date": tstamp, "test":"Success"}) 
    if response.ok:
    	print("Request was successful")
    else:
    	print("Request failed")
    	
    	
    	
    	



