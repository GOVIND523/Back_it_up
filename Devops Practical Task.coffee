**Task: Automated Backup and Rotation Script**

**Scenario:**
You are tasked with creating a backup management script for a project hosted on GitHub. The project contains code files that need to be regularly backed up. Assume that the project folder and rotation strategy will be passed as script arguments or set as variables.

**Objective:**
Develop a script that automates the backup process for the project's code files, implements a rotational backup strategy, and integrates with Google Drive to push the backups to a specified folder. Additionally, implement deletion of older backups and send a cURL request on successful backup.

**Requirements:**

1. **Backup Code:**
   - Create a script that can generate zip from a specified project folder.
   - Organize the backup files in a structured manner, such as a timestamped directory.

2. **Google Drive Integration:**
   - Utilize CLI tools for Google Drive to upload the backup files to a designated folder on Google Drive.
   - Provide clear instructions on using CLI tools for Google Drive push.

   *Hints for Google Drive Integration using CLI tools:*
   - Consider using tools like `gdrive`, `rclone`, or `grive` for command-line-based Google Drive interactions.
   - Provide instructions on installing and configuring the selected CLI tool.
   - Demonstrate how to authenticate and push backups to Google Drive using the chosen tool.

3. **Rotational Backup:**
   - Implement a rotational backup strategy with flexibility for customization through script arguments or variables.
   - Preserve the last 'x' daily backups, the last 'x' weekly backups, and the last 'x' monthly backups.
   - Delete older backups according to the rotational strategy.

   *Example:*
   - If 'x' is set to 7:
     - Keep the backups of the last 7 days.
     - Keep the backups of the last 4 Sundays (weekly).
     - Keep the backups of the last 3 months.
     - Delete older backups beyond the specified retention periods.

4. **Output and Notification:**
   - Optionally, output a simple log file with relevant information, including success/failure messages and timestamps.
   - On successful backup, make a cURL request to a specified URL with a POST request containing a message indicating the successful backup, including project name, date, and a test identifier.

   *Example cURL Request:*
   ```bash
   curl -X POST -H "Content-Type: application/json" -d '{"project": "YourProjectName", "date": "BackupDate", "test": "BackupSuccessful"}' https://webhook.site/your-unique-url
   ```

5. **Documentation:**
   - Provide clear instructions on how to configure and run the script, including project folder and rotation strategy settings.
   - Include details on using CLI tools for Google Drive push.
   - Explain the rotational backup strategy implemented with examples.

**Submission:**
- Submit the script along with any necessary configuration files.
- Include a README.md file with clear instructions on how to set up and use the script.

**Evaluation Criteria:**
- Proper implementation of the backup and rotational backup strategy.
- Successful integration with Google Drive using CLI tools.
- Proper deletion of older backups according to the rotational strategy.
- Successful cURL request on backup success with correct information.
- Clear and concise documentation.
- Demonstrated understanding of the rotational backup concept.

**Note:**
Ensure that the script provides an option to disable the cURL request for testing purposes and that the deletion of older backups is implemented securely, considering potential risks.