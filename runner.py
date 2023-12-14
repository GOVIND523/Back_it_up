from backup_script import *	

#updating local repo	
pull_update_local()

#create a backup an upload on drive using rclone
make_backup()

#checking the rotations
daily_check_rotation()
weekly_check_rotation()
monthly_check_rotation()	

#notification
notify()
