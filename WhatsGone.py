import subprocess
from datetime import datetime
import psutil
import time
import csv
import os
import shutil

"""
This script provides functionality to interact with the WizTree application for scanning directories on a specified drive,
extracting file information, and processing the results. It includes the following key components:

1. `get_files_with_wiztree`: A function to execute WizTree with specified parameters, filter directories, and export results to a file.
2. `wait_for_process_to_finish`: A helper function to monitor and wait for a specific process to complete execution.
3. Main script logic:
    - Configures WizTree executable path, drive, and directories to scan.
    - Executes WizTree to generate a file containing directory information.
    - Processes the output file to extract only file paths and overwrite the file with just the file paths.

The script is designed to work with administrative privileges and assumes WizTree is installed and accessible at the specified path.
""" 

def get_files_with_wiztree(wiztree_path, drive, tag, include_filter, exclude_filter, output_file):
    """
    Executes the WizTree application to retrieve file information from a specified directory 
    on a given drive and exports the results to an output file.
    Args:
        wiztree_path (str): The file path to the WizTree executable.
        drive (str): The drive letter to scan (e.g., "C:").
        include_filter (str): The directory to filter include the specified drive.
        exclude_filter (str): The directory to filter exclude the specified drive.
        output_file (str): The file path where the WizTree output will be saved.
    Raises:
        subprocess.CalledProcessError: If the WizTree command fails to execute properly.
        FileNotFoundError: If the WizTree executable is not found at the specified path.
    Notes:
        - This function requires administrative privileges to execute WizTree.
        - The function waits for the WizTree process to finish before proceeding.
        - Ensure that the WizTree executable is accessible and the provided paths are valid.
    """


    try:

        print(f"STARTED {tag}: Scanning {drive}\\ using include=\"{include_filter}\" and exclude=\"{exclude_filter}\"")

        # Ensure the folder path for the output file exists
        ensure_folder_exists(output_file_path)
        
        # Command to call WizTree with the specified directory and output file
        command = [wiztree_path, drive, f"/filter={include_filter}", f"/filterexclude={exclude_filter}", f"/export=\"{output_file}\"", r"/admin=1", r"/exportfolders=0"]
        
        admin_command = ["powershell", "-Command", f"Start-Process -FilePath '{command[0]}' -ArgumentList '{' '.join(command[1:])}' -Verb RunAs"]

        # Run the WizTree command with elevated privileges
        result = subprocess.run(admin_command, capture_output=True, text=True, check=True, shell=True)
        
        # Wait for WizTree to finish
        wait_for_process_to_finish("WizTree64.exe")
        #wait_for_process_to_finish("WizTree.exe")        

        # Print the output from WizTree
        # print("WizTree Output:", result.stdout)
        # print("WizTree Error:", result.stderr)
    except subprocess.CalledProcessError as e:
        print(f"Error occurred while running WizTree: {e}")
    except FileNotFoundError:
        print("WizTree executable not found. Please check the path.")

def wait_for_process_to_finish(process_name, check_interval=1):
        """
        Waits for a process with the specified name to finish execution.
        This function continuously checks if a process with the given name is running.
        It prints a message indicating that it is waiting for the process to finish
        and pauses for the specified interval between checks. Once the process is no
        longer running, it prints a confirmation message.
        Args:
            process_name (str): The name of the process to monitor. The comparison is case-insensitive.
            check_interval (int, optional): The time interval (in seconds) between consecutive checks. Defaults to 1.
        Returns:
            None
        """
        
        while any(proc.name().lower() == process_name.lower() for proc in psutil.process_iter(attrs=['name'])):
            print(f"Waiting for {process_name} to finish...", end="\r", flush=True)
            time.sleep(check_interval)
        
        print(f"Waiting for {process_name} to finish...")

        print(f"DONE: {process_name} has finished")

def process_output_file(output_file_path):
        """
        Reads the output file, extracts the first item from each row, 
        and overwrites the file with the extracted items.
        
        Args:
            output_file_path (str): The path to the output file to process.
        """

        if not os.path.exists(output_file_path):
            print(f"ERROR: {output_file_path} does not exist.")
            return False

        # Read the output file and extract the first item from each row
        with open(output_file_path, 'r', encoding='utf-8') as file:
            reader = csv.reader(file)
            # assume user is going to use the free version of WizTree
            next(reader, None)  # Skip the header or first line
            first_items = [row[0] for row in reader if row and len(row) > 0]

        if len(first_items) == 0:
            print(f"ERROR: {output_file_path} has no files. Current files will not be overwritten.")
            return False

        print(f"RECORDED: {len(first_items)-1} files")

        # Write the extracted items back to the same file, overwriting the original content
        with open(output_file_path, 'w', newline='', encoding='utf-8') as file:
            for item in first_items:
                file.write(item.strip('"') + '\n')

        print(f"COMPLETED: {output_file_path} has all of the files.")

        return True

# Ensure the folder path for the output file exists
def ensure_folder_exists(file_path):
    """
    Ensures that the specified folder exists. If it does not exist, creates it.
    
    Args:
        file_path (str): The path of the file to check or create.
    """
    folder_path = os.path.dirname(file_path)

    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
        print(f"Created folder: {folder_path}")

if __name__ == "__main__":


    # Get the current timestamp in the desired format
    #date_time = datetime.now().strftime("%Y%m%d_%H%M%S")

    wiztree_executable = "C:/Program Files/WizTree/WizTree64.exe"

    scan_runs = {
        "Everything": {
            "Exclude": ["$", "WindowsApps"],
            "Drive": "X",
            "Output": "C:/WhatsGone",
            "Backup": "D:/WhatsGone"
        },
        "TV Shows": {
            "Include": ["Videos\\TV"],
            #"Exclude": ["Windows"],
            "Drive": "X",
            "Output": "C:/WhatsGone",
            "Backup": "D:/WhatsGone"
        },
        "Movies": {
            "Include": ["Videos\\Movies"],
            #"Exclude": ["Windows"],
            "Drive": "X",
            "Output": "C:/WhatsGone",
            "Backup": "D:/WhatsGone"
        },
        "Plex": {
            "Include": ["Videos\\Temporary", "Videos\\Plex"],
            #"Exclude": ["Windows"],
            "Drive": "F",
            "Output": "C:/WhatsGone",
            "Backup": "D:/WhatsGone"
        }
    }
    output_folder = "C:/WhatsGone"

    for tag, scan_parameters in scan_runs.items():
        if "Include" in scan_parameters:
            include_filter = scan_parameters["Include"]
        else:
            include_filter = []
        
        if "Exclude" in scan_parameters:
            exclude_filter = scan_parameters["Exclude"] 
        else:
            exclude_filter = []

        if "Drive" in scan_parameters:
            drive = scan_parameters["Drive"] 
        else:
            print(f"MISSING: Drive parameter not specified. Skipping {tag} scan.")
            continue

        scan_drive = drive + ":"
        output_file_path = rf"{scan_parameters['Output']}/{drive}_{tag}.txt"
        files_to_scan = "|".join([f"\"{directory}\"" for directory in include_filter])
        files_to_skip = "|".join([f"\"{directory}\"" for directory in exclude_filter])

        # Skip to the next item if the drive does not exist
        if not os.path.exists(drive + ":\\"):
            print(f"MISSING: Drive {drive}:\\ no longer exists. It's gone.")
            missing_file_path = os.path.join(scan_parameters["Output"], f"{drive}_missingdrive.txt")
            with open(missing_file_path, 'a', encoding='utf-8') as missing_file:
                missing_file.write(f"Drive {drive}:\\ is missing as of {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}.\n")
            print(f"INFO: Missing drive note written to {missing_file_path}")
            continue

        get_files_with_wiztree(wiztree_executable, scan_drive, tag, files_to_scan, files_to_skip, output_file_path)
        process_output_file(output_file_path)

        if "Backup" in scan_parameters:
            backup_file_path = rf"{scan_parameters['Backup']}/{drive}_{tag}.txt"
            ensure_folder_exists(backup_file_path)

            # Copy the output file to the backup location, overwriting if it exists
            try:
                shutil.copy(output_file_path, backup_file_path)
                print(f"COMPLETED: {output_file_path} has been backed up to {backup_file_path}.")
            except Exception as e:
                print(f"ERROR: Failed to back up {output_file_path} to {backup_file_path}. Reason: {e}")
            
        
        
