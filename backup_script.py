import subprocess

#function definitions

"""pull_upate_local function will update the local repo by pulling the changes from remote repo it any"""

def pull_update_local():
  try:
    subprocess.run(['git','-C', "/home/vboxuser/Back_it_up", 'pull', 'origin', 'main'], check=True)
    print("Upated the local repository")
  except subprocess.CalledProcessError:
    print("Could not update local repository");
    

#function calls

	
pull_update_local()

