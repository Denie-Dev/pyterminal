print("Starting pyterminal")

#---------------------Import Modules------------------
print("importing modules")
import time
import platform
import os
import sys
import urllib.request
import json
import logging
import ssl
#----------------------------------------------------

#----------------------------------Variable Setup--------------------------------
print("setting variables")

command = ""

#------------------------File Paths----------------------
log_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'log.txt')
log_level_file = os.path.join(os.path.dirname(__file__), 'log_level.txt')
version_json_path = os.path.join(os.path.dirname(__file__), 'version.json')
#--------------------------------------------------------

#----------------Update Variables--------------
__version__ = "1.6.2"  # current local version
GITHUB_RAW_URL = "https://raw.githubusercontent.com/Denie-Dev/pyterminal/main/pyterminal.py"
GITHUB_VERSION_URL = "https://raw.githubusercontent.com/Denie-Dev/pyterminal/main/version.json"
#----------------------------------------------

os.environ["RF_LIMIT"] = "5000"
#--------------------------------------------------------------------------------------------

try:
    with open(log_level_file, 'r') as f:
        log_level = int(f.read().strip())
except (FileNotFoundError, ValueError):
    log_level = 3
logging.basicConfig(filename=log_file, level=logging.DEBUG,
                    format='%(asctime)s - %(levelname)s - %(message)s',
                    filemode='a') # Set logging level based on log_level
if log_level == 1:
    logging.getLogger().setLevel(logging.ERROR)
elif log_level == 2:
    logging.getLogger().setLevel(logging.WARNING)
else:
    logging.getLogger().setLevel(logging.INFO)
logging.info("PyTerminal started")

# variable setup


#----------------------------------Check for Update Function--------------------------------------
print("setting functions")
def check_for_update():
    try:
        with urllib.request.urlopen(GITHUB_VERSION_URL, timeout=5, context=ssl._create_unverified_context()) as resp:
            data = resp.read().decode("utf-8")
        json_file = json.loads(data)
        latest_version = json_file.get("version", "").strip()
        if not latest_version:
            return
        if latest_version != __version__:
            logging.info(f"update available: {latest_version}")
            print("updating to version " + latest_version)
            do_update()
    except Exception as e:
        logging.error(f"update check failed: {str(e)}")
        if os.environ.get("DEBUG") == "1":
            print("error: " + str(e))
        pass
#----------------------------------------------------------------------------------

#----------------------------------Perform Update---------------------------------
def do_update():
    try:
        logging.info("starting update")
        logging.info("downloading latest")
        with urllib.request.urlopen(GITHUB_RAW_URL, timeout=10, context=ssl._create_unverified_context()) as resp:
            new_file = resp.read()

        file_path = os.path.realpath(__file__)
        backup_path = file_path + ".bak"

        try:
            if os.path.exists(backup_path):
                os.remove(backup_path)
            os.rename(file_path, backup_path)
        except Exception:
            logging.warning("Backup creation failed")
            print("backup error")

        with open(file_path, "wb") as f:
            f.write(new_file)

        logging.info("update completed")
        print("update finished")
        time.sleep(2)
        sys.exit(0)
    except Exception as e:
        logging.error(f"update failed: {str(e)}")
        print("update failed: " + str(e))
#----------------------------------------------------------------------------------

#------------------Check For Update---------------
print("checking for update")
check_for_update()

if os.path.exists(version_json_path): # remove temporary version.json
    logging.info("removing version.json")
    os.remove(version_json_path)
#--------------------------------------------------

#--------------------------------Home Directory---------------------------------
try:
    os.chdir(os.path.expanduser('~'))
except PermissionError:
    logging.error("failed to start: home folder PermissionError")
    print("pyterminal failed to start: home folder PermissionError")
    exit()
except FileNotFoundError:
    logging.error("failed to start: No home folder")
    print("pyterminal failed to start: No home folder")
    exit()
#------------------------------------------------------------------------------

#------------------Startup Messages-------------------
if "idlelib" in sys.modules: # idle shell check
    logging.warning("Using IDLE shell - slow performance")
    print("using idle shell,\nslow preformance")
else:
    logging.info("PyTerminal started successfully")
    print("pyterminal started")
#--------------------------------------------------

#-------------------------------------------PyTerminal Logo------------------------------------------------
if os.environ.get("PY_LOGO_STARTUP") == "1":
    time.sleep(1)
    print("             _                      _             _ ".center(os.get_terminal_size().columns))
    time.sleep(1)
    print(" _ __  _   _| |_ ___ _ __ _ __ ___ (_)_ __   __ _| |".center(os.get_terminal_size().columns))
    time.sleep(1)
    print("| '_ \\| | | | __/ _ \\ '__| '_ ` _ \\| | '_ \\ / _` | |".center(os.get_terminal_size().columns))
    time.sleep(1)
    print("| |_) | |_| | ||  __/ |  | | | | | | | | | | (_| | |".center(os.get_terminal_size().columns))
    time.sleep(1)
    print("| .__/ \\__, |\\__\\___|_|  |_| |_| |_|_|_| |_|\\__,_|_|".center(os.get_terminal_size().columns))
    time.sleep(1)
    print("|_|    |___/                                        ".center(os.get_terminal_size().columns))
#--------------------------------------------------------------------------------------------------------------

#---------------------------------Main Command Loop---------------------------
while command != "exit":
    if len(os.getcwd()) > 30:
        current_path = "..." + str(os.getcwd())[-(30 - 3):]
    else:
        current_path = os.getcwd()
    command = input(f"{current_path}> ")
    logging.info(f"command executed: {command}")

    #-----------------------exit section-----------------------
    if command == "exit":
        logging.info("exiting pyterminal")
        print("exiting pyterminal")
        break
    #--------------------------------------------------------

    #-----------------------ds section-----------------------
    elif command == "ds":
        print(f"\nSystem: {platform.uname().system}")
        print(f"Node Name: {platform.uname().node}")
        print(f"Release: {platform.uname().release}")
        print(f"Version: {platform.uname().version}")
        print(f"Machine: {platform.uname().machine}")
        print(f"Processor: {platform.uname().processor}\n")
    #--------------------------------------------------------

    #-----------------------ver section-----------------------
    elif command == "ver":
        print(f"PyTerminal Release {__version__}\nBy Dennis")
    #--------------------------------------------------------

    #-----------------------lf section-----------------------
    elif command.startswith("lf"):

        if command == "lf": # list current directory
            try:
                if os.listdir(os.getcwd()) == []:
                    print("directory empty")
                else:
                    print(os.listdir(os.getcwd()))
            except PermissionError:
                print("invalid permissions")
        
        elif command.startswith("lf "): # list specified directory
            argument = command.replace("lf ", "")
            try:
                print(os.listdir(argument))
            except FileNotFoundError:
                print("directory doesen't exist")
            except PermissionError:
                print("invalid permissions")

        else:
            print("invalid command")
        
    #--------------------------------------------------------

    #-----------------------cwd section-----------------------
    elif command.startswith("cwd"):
        if command == "cwd":
            print(str(os.getcwd()))
        elif command.startswith("cwd "):
            print(str(os.getcwd()))
    #--------------------------------------------------------

    #-----------------------cd section-----------------------
    elif command.startswith("cd"):

        if command == "cd": # go to home directory
            if str(os.getcwd()) == os.path.expanduser('~'):
                print("at home folder")
            else:
                os.chdir(os.path.expanduser('~'))
                print("success")

        elif command.startswith("cd "): # change directory
            argument = command.replace("cd ", "")
            if argument == ".." and os.getcwd() == "/":
                print("at root folder")
                continue
            try:
                os.chdir(argument) # successful change
                print("success")
            except FileNotFoundError: # FileNotFoundError
                print("directory doesen't exist")
            except PermissionError: # PermissionError
                print("invalid permissions")

        else:
            print("invalid command")
    #--------------------------------------------------------

    #-----------------------df section-----------------------
    elif command.startswith("df"):
        if command == "df":
            print("df - delete file\n\ndf {filename}")

        elif command.startswith("df "):
            argument = command.replace("df ", "")
            if os.path.exists(argument) == False:
                print("file doesen't exist")
                continue
            elif argument == "/" or argument == "\\" or argument == "" or argument == os.path.expanduser("/"):
                print("invalid operation")
                continue
            confirm = input("delete file? (y): ")
            if confirm == "y":
                try:
                    os.remove(argument)
                    print("success")
                except FileNotFoundError:
                    print("file doesen't exist")
            else:
                print("canceled")
        else:
            print("invalid command")
    #--------------------------------------------------------

    #-----------------------md section-----------------------
    elif command.startswith("md"):

        if command == "md":
            print("md - make directory\n\nmd {directory name}")
            continue

        elif command.startswith("md "):
            argument = command.replace("md ", "")
            try:
                os.mkdir(argument)
            except FileExistsError:
                print("directory exists")
                continue
            except FileNotFoundError:
                print("invalid name")
                continue
            except PermissionError:
                print("invalid permissions")
                continue
            print("success")
        else:
            print("invalid command")
    #--------------------------------------------------------

    #-----------------------mf section-----------------------
    elif command.startswith("mf"):
        if command == "mf":
            print("mf - make file\n\nmf {file name}")
            continue
        elif command.startswith("mf "):
            argument = command.replace("mf ", "")
            try:
                open(argument, "x").close()
                print("success")
            except FileExistsError:
                print("file exists")
    #--------------------------------------------------------

    #-----------------------cf section-----------------------
    elif command.startswith("cf"): # cf section
        arguments = command.split(" ", 2)

        if command == "cf":
            print("cf - copy file\n\ncf {file1} {file2}")
        
        elif len(arguments) < 3:
            print("missing arguments")

        elif len(arguments) == 3:
            file1 = arguments[1].strip()
            file2 = arguments[2].strip()
            try:
                with open(file1, "r") as file1:
                    content = file1.read()
                with open(file2, "x") as file2:
                    file2.write(content)
                print("success")
            except FileNotFoundError:
                print("file1 doesn't exist")
            except FileExistsError:
                print("file2 exists")
            except PermissionError:
                print("invalid permissions")

        else:
            print("invalid command")
    #--------------------------------------------------------

    #-----------------------log section-----------------------
    elif command.startswith("log"):
        if command == "log":
            print("log - modify log\n\nlog w {text} - append text to log\nlog clear - clear log\nlog level {1-3} - set log level")

        elif command.startswith("log "):
            arguments = command.split(" ", 2)
            if len(arguments) < 2:
                print("missing subcommand")
            else:
                subcommand = arguments[1]
                if subcommand == "w": # log w section
                    if len(arguments) < 3:
                        print("no text to write")
                    else:
                        text = arguments[2]
                        try:
                            with open(log_file, "a") as f:
                                f.write(text + "\n")
                            print("success")
                        except PermissionError:
                            print("invalid permissions")

                elif subcommand == "clear": # log clear section
                    try:
                        with open(log_file, "w") as f:
                            f.write("")
                        print("log cleared")
                    except PermissionError:
                        print("invalid permissions")

                elif subcommand == "level": # log level section
                    if len(arguments) < 3:
                        print(log_level)
                    else:
                        try:
                            level = int(arguments[2])
                            if level == 1:
                                log_level = 1
                                logging.getLogger().setLevel(logging.ERROR)
                                print("log level 1")
                            elif level == 2:
                                log_level = 2
                                logging.getLogger().setLevel(logging.WARNING)
                                print("log level 2")
                            elif level == 3:
                                log_level = 3
                                logging.getLogger().setLevel(logging.INFO)
                                print("log level 3")
                            else:
                                print("invalid level")
                                continue
                            with open(log_level_file, 'w') as f:
                                f.write(str(log_level))
                        except ValueError:
                            print("invalid level number")
                else:
                    print("invalid log statement")
        else:
            print("invalid command")
    #--------------------------------------------------------

    #-----------------------af section-----------------------
    elif command.startswith("af"):
        arguments = command.split(" ", 2)

        if len(arguments) < 3:
            print("af - append to file\n\naf {filename} {text}")

        else:
            filename = arguments[1].strip()
            text = arguments[2]
            try:
                with open(filename, "a") as f:
                    f.write(text + "\n")
                print("success")
            except FileNotFoundError:
                print("file doesen't exist")
            except PermissionError:
                print("invalid permmisions")
    #--------------------------------------------------------

    #-----------------------rf section-----------------------
    elif command.startswith("rf"):

        if command == "rf":
            print("rf - read file\n\nrf {filename}")

        elif command.startswith("rf "):
            argument = command.replace("rf ", "")
            try:
                with open(argument, "r") as file:
                    content = file.read()
                    if len(content) > int(os.environ.get("RF_LIMIT", "5000")):
                        print("file exceeds char limit")
                    else:
                        print(content)
            except FileNotFoundError:
                print("file doesn't exist")
            except PermissionError:
                print("invalid permissions")
            except IsADirectoryError:
                print("is a directory")
    #--------------------------------------------------------

    #-----------------------ot section-----------------------
    elif command.startswith("ot"): 
        if command == "ot":
            print("ot - output text\n\not {text}")
        elif command.startswith("ot "):
            argument = command.replace("ot ", "")
            print(argument)
    #--------------------------------------------------------

    #-----------------------sev section----------------------
    elif command.startswith("sev"):

        if command == "sev":
            print("sev - set enviormental variable\n\nsev {name} {value}")
        
        elif command.startswith("sev "):
            arguments = command.split(" ", 2)
            if len(arguments) < 3:
                print("missing arguments")
            else:
                part1 = arguments[1]
                part2 = arguments[2]
                os.environ[part1] = part2
                print("success")
        else:
            print("invalid command")
    #-------------------------------------------------------
    
    #-----------------------rev section-----------------------
    elif command.startswith("rev"):

        if command == "rev":
            print("rev - read enviormental variables\n\nrev {name}")

        elif command.startswith("rev "):
            argument = command.replace("rev ", "")
            try:
                if str(os.environ.get(argument)) == "None":
                    print("ev doesen't exist")
                else:
                    print(os.environ.get(argument))
            except PermissionError:
                print("invalid permissions")
            except KeyError:
                print("ev doesen't exist")
        else:
            print("invalid command")
    #--------------------------------------------------------

    #-----------------------help section-----------------------
    elif command == "help":
        print("cd - change directory" \
        "\ncwd - current working directory" \
        "\nlf - list files" \
        "\nmd - make directory" \
        "\naf - append (to) file" \
        "\ncp - copy file" \
        "\ndf - delete file" \
        "\nmf - make file" \
        "\not - output text" \
        "\nrf - read file" \
        "\nrev - read enviormental variables" \
        "\nsev - set enviormental variables" \
        "\nlog - change log settings" \
        "\n     log w <text> - append text to log" \
        "\n     log clear - clear log" \
        "\n     log level <1-3> - set log level" \
        "\nds - device specifications" \
        "\nver - version" \
        "\ncs - clear screen" \
        "\nexit - exit pyterminal")
    #--------------------------------------------------------

    #-----------------------cs section-----------------------
    elif command == "cs":
        for i in range(150):
            print("\n")
    #--------------------------------------------------------

    else: # invalid command
        print("invalid command")
