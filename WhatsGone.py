import subprocess
from datetime import datetime
import psutil
import time
import csv

def call_executable(executable_path, arguments):
    try:
        # Combine the executable path and arguments into a single list
        command = [executable_path] + arguments
        
        # Run the executable with the arguments
        result = subprocess.run(command, capture_output=True, text=True, check=True)
        
        # Print the output from the executable
        print("Output:", result.stdout)
        print("Error:", result.stderr)
    except subprocess.CalledProcessError as e:
        print(f"Error occurred: {e}")
    except FileNotFoundError:
        print("Executable not found. Please check the path.")

# Example usage
# executable = "path/to/your/executable"
# args = ["--arg1", "value1", "--arg2", "value2"]
# call_executable(executable, args)

def get_files_with_wiztree(wiztree_path, drive, directory, output_file):
    try:

        
        # Command to call WizTree with the specified directory and output file
        command = [wiztree_path, drive, f"/filter={directory}", f"/export=\"{output_file}\"", r"/admin=1", r"/exportfolders=0"]
        
        admin_command = ["powershell", "-Command", f"Start-Process -FilePath '{command[0]}' -ArgumentList '{' '.join(command[1:])}' -Verb RunAs"]

        # Run the WizTree command with elevated privileges
        result = subprocess.run(admin_command, capture_output=True, text=True, check=True, shell=True)
        
        # Wait for WizTree to finish
        wait_for_process_to_finish("WizTree64.exe")
        wait_for_process_to_finish("WizTree.exe")

        # Print the output from WizTree
        print("WizTree Output:", result.stdout)
        print("WizTree Error:", result.stderr)
    except subprocess.CalledProcessError as e:
        print(f"Error occurred while running WizTree: {e}")
    except FileNotFoundError:
        print("WizTree executable not found. Please check the path.")

# Example usage
# wiztree_executable = r"C:\Program Files\WizTree\WizTree64.exe"
# directory_to_scan = "C:/path/to/directory"
# output_file_path = "C:/path/to/output.txt"
# get_files_with_wiztree(wiztree_executable, directory_to_scan, output_file_path)

def wait_for_process_to_finish(process_name, check_interval=1):
        while any(proc.name().lower() == process_name.lower() for proc in psutil.process_iter(attrs=['name'])):
            print(f"Waiting for {process_name} to finish...", end="\r", flush=True)
            time.sleep(check_interval)
        
        print("")
        print(f"{process_name} has finished.")

if __name__ == "__main__":
    # Example usage of call_executable
    # executable = "path/to/your/executable"
    # args = ["--arg1", "value1", "--arg2", "value2"]
    # call_executable(executable, args)

    # Example usage of get_files_with_wiztree
    # Get the current timestamp in the desired format
    date_time = datetime.now().strftime("%Y%m%d_%H%M%S")
    wiztree_executable = "C:/Program Files/WizTree/WizTree64.exe"
    drive = "X:"
    # directory_to_scan = "X:\\Videos\\Movies\\"
    # output_file_path = rf"C:/WhatsGone/{date_time}_movies.txt"
    # get_files_with_wiztree(wiztree_executable, drive, directory_to_scan, output_file_path)

    # directory_to_scan = "X:\\Videos\\TV Shows\\"
    # output_file_path = rf"C:/WhatsGone/{date_time}_tv_shows.txt"
    # get_files_with_wiztree(wiztree_executable, drive, directory_to_scan, output_file_path)

    drive = "X:"
    directories = ["Videos\\Movies", "Videos\\TV"]
    directory_to_scan = "|".join([f"\"{directory}\"" for directory in directories])
    #directory_to_scan = f"\"{directory_to_scan}\""
    #output_file_path = rf"C:/WhatsGone/{date_time}_all.txt"
    output_file_path = rf"C:/WhatsGone/X_all.txt"
    get_files_with_wiztree(wiztree_executable, drive, directory_to_scan, output_file_path)

    # Read the output file and extract the first item from each row
    with open(output_file_path, 'r', encoding='utf-8') as file:
        reader = csv.reader(file)
        next(reader, None)  # Skip the header or first line
        first_items = [row[0] for row in reader if row and len(row) > 0]

    # Write the extracted items back to the same file, overwriting the original content
    with open(output_file_path, 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        for item in first_items:
            writer.writerow([item])