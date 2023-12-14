import subprocess
import shutil
from datetime import datetime
import requests
import os
from datetime import timedelta
import json

# Access configuration values

with open('config/config.json', 'r') as file:
    config = json.load(file)

Project_dir = config.get('Project_dir', '')
Curl_enable = config.get('Curl_enable', False)
Webhook_url = config.get('Webhook_url', '')
Gdrive_folder = config.get('Gdrive_folder', '')
Back_daily = config.get('Back_daily', 0)
Back_weekly = config.get('Back_weekly', 0)
Back_monthly = config.get('Back_monthly', 0)
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
    subprocess.run(['git','-C', Project_dir , 'pull', 'origin', 'main'], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    print("\n\tUpdated repository\n")
  except subprocess.CalledProcessError:
    print("\n\tCould not update repository");
    
      
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
  remote = f"remote:{Gdrive_folder}"
  local_backup = f"{Project_dir}/Backup{tstamp}"
  shutil.make_archive(local_backup , "zip" , Project_dir)
  #2
  subprocess.run(["rclone","copy",f"{local_backup}.zip",remote], check= True)
  #3
  os.remove(f"{local_backup}.zip")
  print("\tBackup uploaded\n")	

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
  
#1
def daily_check_rotation():
  remote = f"remote:{Gdrive_folder}"
  daily = Back_daily
  remote_files = subprocess.check_output(["rclone", "lsjson", remote]).decode('utf-8')
  backup_info = json.loads(remote_files)
  sorted_backups = sorted(backup_info, key=lambda x: datetime.fromisoformat(x["ModTime"][:-1]), reverse=True)
  today = datetime.today().date()
  daily_backups = sorted_backups[:daily]
  print("\tPerforming rotation check")	
  for backup in sorted_backups[daily:]:
    print(f"\tDeleting: {backup['Name']}\n")
    delete(backup["Name"])

#2
def weekly_check_rotation():
  weekly = Back_weekly
  remote = f"remote:{Gdrive_folder}"
  remote_files = subprocess.check_output(["rclone", "lsjson", remote]).decode('utf-8')
  backup_info = json.loads(remote_files)
  sorted_backups = sorted(backup_info, key=lambda x: datetime.fromisoformat(x["ModTime"][:-1]), reverse=True)
  today = datetime.today().date()
  weekly_backups = [backup for backup in sorted_backups if (today - datetime.fromisoformat(backup["ModTime"][:-1]).date()).days <= weekly]
  for backup in sorted_backups[weekly:]:
    print(f"\tDeleting: {backup['Name']}\n")
    delete(backup["Name"])

#3
def monthly_check_rotation():
  monthly = Back_monthly
  remote = f"remote:{Gdrive_folder}"
  remote_files = subprocess.check_output(["rclone", "lsjson", remote]).decode('utf-8')
  backup_info = json.loads(remote_files)
  sorted_backups = sorted(backup_info, key=lambda x: datetime.fromisoformat(x["ModTime"][:-1]), reverse=True)
  today = datetime.today().date()
  monthly_backups = [backup for backup in sorted_backups if (today - datetime.fromisoformat(backup["ModTime"][:-1]).date()).days <= monthly]
  for backup in sorted_backups[monthly:]:
    print(f"\tDeleting: {backup['Name']}\n")
    delete(backup["Name"])
  print("\tBackup rotation checked\n")	


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
    	print("\tNotification sent\n")
    else:
    	print("\tCant send notification!!\n")
    	




