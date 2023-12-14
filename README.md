# Backup It Up

## Overview

The **Backup Script** streamlines the backup process by automating the creation of backups, uploading them to Google Drive using rclone, and implementing a rotation system to maintain only the latest backups. Additionally, the script offers notification capabilities to keep users informed about the backup status.

## Dependencies

- Python 3
- rclone

## Configuration

Before executing the script, ensure proper configuration of the `config.json` file with the following parameters:

```json
{
  "Project_dir": "/home/vboxuser/Back_it_up",
  "Curl_enable": true,
  "Webhook_url": "https://webhook.site/e45e6bab-8f6f-4525-a95e-314c029bae1a",
  "Gdrive_folder": "Back_it_up",
  "Back_daily": 4,
  "Back_weekly": 7,
  "Back_monthly": 12
}

- **Project_dir:** Local directory for backup storage.
- **Curl_enable:** Enable or disable cURL for notifications.
- **Webhook_url:** URL for webhook notifications.
- **Gdrive_folder:** Google Drive folder for storing backups.
- **Back_daily:** Number of daily backups to retain.
- **Back_weekly:** Number of weekly backups to retain.
- **Back_monthly:** Number of monthly backups to retain.

## Functions

- **pull_update_local():** Updates the local repository by pulling changes from the remote repository.
- **make_backup():** Creates a local backup, uploads it to Google Drive, and removes the local backup.
- **check_rotation():** Manages daily, weekly, and monthly rotations, eliminating unnecessary backups.
- **notify():** Sends notifications upon successful script execution.

## File Structure

Ensure the following file structure for the script to function correctly:


- **config/:** Directory containing the configuration file (`config.json`).
- **backup_script.py:** Primary script for backup, rotation, and notification.
- **runner.py:** Script to execute the main backup script.
- **README.md:** General information and setup instructions.
- **docs/:** Directory containing documentation files.

## Running the Script

1. Open a terminal.
2. Navigate to the project root directory.
3. Update the `config.json` file with your desired configuration.
4. Run the script:

```bash
python runner.py


## Additional Notes

- Ensure that you have the required dependencies installed (Python 3, rclone).
- Make sure the specified Google Drive folder exists.
- Review the notifications section in the `config.json` for webhook configuration.

Note: Customize the configuration parameters in `config.json` according to your specific setup and preferences.
