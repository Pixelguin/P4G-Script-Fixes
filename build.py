import glob, os, shutil, subprocess
os.chdir(os.path.dirname(os.path.abspath(__file__))) # Set working directory to the .py file's location - needed if Python is running from PATH

# Set dependency file paths
COMPILER_EXE = "Enter the path to PM1MessageScriptEditor.exe"
SOURCE_DIR = "Enter the path to unpacked data_e"

# Set directory paths
MOD_DIR = os.getcwd() + "\mod"
OUTPUT_DIR = os.getcwd() + "\output"

def no_output_dir(path):
    """
    Removes OUTPUT_DIR from a file or directory path.
    Makes console output easier to read.
    """
    return path.replace(OUTPUT_DIR + "\\", "")

# Copy mod directory to use as a base for output directory
if os.path.exists(OUTPUT_DIR):
    shutil.rmtree(OUTPUT_DIR)
shutil.copytree(MOD_DIR, OUTPUT_DIR)
print("Created " + os.path.basename(OUTPUT_DIR) + " folder from " + os.path.basename(MOD_DIR) + " folder")

print("")

# Copy matching PM1 files for MSG files in output\event
for msg_file in glob.iglob(OUTPUT_DIR + "\event\**\*.msg", recursive=True):
    # Replace directory and extension and check if the PM1 file exists
    pm1_file = msg_file.replace(OUTPUT_DIR, SOURCE_DIR).replace("msg", "pm1")
    if os.path.exists(pm1_file):
        # Copy the matching PM1 file
        msg_dir = os.path.dirname(msg_file)
        shutil.copy(pm1_file, msg_dir)
        print("Copied " + os.path.basename(pm1_file) + " to " + no_output_dir(msg_dir), end="")
        # Remove read-only flag from PM1 file
        copied_pm1_file = msg_dir + "\\" + os.path.basename(pm1_file)
        if os.access(copied_pm1_file, os.W_OK) == False:
            os.system("attrib -r " + copied_pm1_file)
            print(" and removed read-only flag", end="")
        print("")

print("")

# Pack event MSG files into PM1 files
for msg_file in glob.iglob(OUTPUT_DIR + "\event\**\*.msg", recursive=True):
    if subprocess.run([COMPILER_EXE, msg_file], stdout=subprocess.DEVNULL).returncode == 0:
        print("Packed " + no_output_dir(msg_file) + " successfully!")
        os.remove(msg_file)
    else:
        print("Couldn't pack " + no_output_dir(msg_file))

input("\nAll done!\nPress Enter to exit.")