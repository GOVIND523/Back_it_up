import subprocess
import shutil
from datetime import datetime
import requests
import os
from datetime import timedelta


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

def check_rotation():
    remote_files = subprocess.check_output(["rclone", "ls", f"remote:Back_it_up"]).decode('utf-8').splitlines()
    daily = 1
    weekly = 4
    monthly = 12
    today = datetime.today().date()
    backup_dates = [datetime.strptime(file.split("||")[1], "%m--%d--%Y").date() for file in remote_files]
   
    #daily
    daily_backups = [file for file, backup_date in zip(remote_files, backup_dates) if backup_date == today]
    keep_daily = daily
    daily_backups = daily_backups[-keep_daily:]
    remaining_files = [file for file in remote_files if file not in daily_backups]
    #week
    weekly_backups = [file for file, backup_date in zip(remaining_files, backup_dates) 
                      if backup_date.isocalendar()[1] == today.isocalendar()[1]]
    keep_weekly = weekly
    weekly_backups = weekly_backups[-keep_weekly:]
    remaining_files = [file for file in remaining_files if file not in weekly_backups]
    #month
    monthly_backups = [file for file, backup_date in zip(remaining_files, backup_dates) 
                       if backup_date.month == today.month]
    keep_monthly = monthly
    monthly_backups = monthly_backups[-keep_monthly:]

    backups_to_keep = set(daily_backups)# + weekly_backups + monthly_backups)
    backups_to_delete = set(remote_files) - backups_to_keep

    for old_backup in backups_to_delete:
        subprocess.run(["rclone", "delete", f"remote:Back_it_up/{old_backup.split()[-1]}"])
  
        
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
check_rotation()

#notification
notify()



