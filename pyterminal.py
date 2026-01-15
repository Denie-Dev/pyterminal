print("Loading pyterminal")
print("importing modules")
import time
import platform
import os
import sys
import urllib.request
import json
import logging
import ssl

version_json_path = os.path.join(os.path.dirname(__file__), 'version.json')
if os.path.exists(version_json_path):
    logging.info("Removing version.json")
    os.remove(version_json_path)

print("setting variables")
log_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'log.txt')
log_level_file = os.path.join(os.path.dirname(__file__), 'log_level.txt')
# Load log level from file

try:
    with open(log_level_file, 'r') as f:
        log_level = int(f.read().strip())
except (FileNotFoundError, ValueError):
    log_level = 3
print(log_file)
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
terminal = ""
__version__ = "1.6"  # current local version
GITHUB_RAW_URL = "https://raw.githubusercontent.com/Denie-Dev/pyterminal/main/pyterminal.py"
GITHUB_VERSION_URL = "https://raw.githubusercontent.com/Denie-Dev/pyterminal/main/version.json"
os.environ["RF_LIMIT"] = "5000"

print("setting functions")
def check_for_update():
    try:
        with urllib.request.urlopen(GITHUB_VERSION_URL, timeout=5, context=ssl._create_unverified_context()) as resp:
            data = resp.read().decode("utf-8")
        info = json.loads(data)
        latest = info.get("version", "").strip()
        if not latest:
            return
        if latest != __version__:
            logging.info(f"Update available: {latest}")
            do_update()
    except Exception as e:
        logging.error(f"Update check failed: {str(e)}")
        if os.environ.get("DEBUG") == "1":
            print("error: " + str(e))
        pass


def do_update():
    try:
        logging.info("Starting update download")
        print("downloading latest")
        with urllib.request.urlopen(GITHUB_RAW_URL, timeout=10, context=ssl._create_unverified_context()) as resp:
            new_code = resp.read()

        script_path = os.path.realpath(__file__)
        backup_path = script_path + ".bak"

        try:
            if os.path.exists(backup_path):
                os.remove(backup_path)
            os.rename(script_path, backup_path)
        except Exception:
            logging.warning("Backup creation failed")
            print("backup error")

        with open(script_path, "wb") as f:
            f.write(new_code)

        logging.info("Update completed successfully")
        print("update finished")
        time.sleep(2)
        sys.exit(0)
    except Exception as e:
        logging.error(f"Update failed: {str(e)}")
        print("Update failed:", e)
        print("using old version")

print("checking for update")
check_for_update()
try:
    os.chdir(os.path.expanduser('~'))
except PermissionError:
    logging.error("Failed to start: Home folder PermissionError")
    print("pyterminal failed to start: Home folder PermissionError")
    exit()
except FileNotFoundError:
    logging.error("Failed to start: No home folder")
    print("pyterminal failed to start: No home folder")
    exit()
if "idlelib" in sys.modules:
    logging.warning("Using IDLE shell - slow performance")
    print("using idle shell,\nslow preformance")
else:
    logging.info("PyTerminal started successfully")
    print("pyterminal started")
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
while terminal != "exit":
    if len(os.getcwd()) > 30:
        short_path = "..." + str(os.getcwd())[-(30 - 3):]
    else:
        short_path = os.getcwd()
    terminal = input(f"{short_path}> ")
    logging.info(f"Command executed: {terminal}")
    if terminal == "exit":
        logging.info("PyTerminal exiting")
        print("Exiting pyterminal")
        break
    elif terminal == "ds": # ds section
        print(f"\nSystem: {platform.uname().system}")
        print(f"Node Name: {platform.uname().node}")
        print(f"Release: {platform.uname().release}")
        print(f"Version: {platform.uname().version}")
        print(f"Machine: {platform.uname().machine}")
        print(f"Processor: {platform.uname().processor}\n")
    elif terminal == "ver": # ver section
        print(f"PyTerminal Release {__version__}\nBy Dennis")
    elif terminal.startswith("lf"): # lf section
        if terminal.startswith("lf "):
            terminal = terminal.replace("lf ", "")
            try:
                print(os.listdir(terminal))
            except FileNotFoundError:
                print("directory doesen't exist")
            except PermissionError:
                print("invalid permissions")
        elif terminal == "lf":
            try:
                print(os.listdir(os.getcwd()))
            except PermissionError:
                print("invalid permissions")
    elif terminal == "cwd": # cwd section
        print(str(os.getcwd()))
    elif terminal.startswith("cd"): # cd section
        if terminal == "cd":
            if str(os.getcwd()) == os.path.expanduser('~'):
                print("at home folder")
            else:
                os.chdir(os.path.expanduser('~'))
        elif terminal.startswith("cd "):
            terminal = terminal.replace("cd ", "")
            if terminal == ".." and os.getcwd() == "/":
                print("at root folder")
                break
            try:
                os.chdir(terminal)
                print("success")
            except FileNotFoundError:
                print("directory doesen't exist")
            except PermissionError:
                print("invalid permissions")
        else:
            print("invalid cd statement")
    elif terminal.startswith("df"): # df section
        if terminal == "df":
            print("argument missing")
        elif terminal.startswith("df "):
            terminal = terminal.replace("df ", "")
            confirm = input("delete file? (y): ")
            if confirm == "y":
                try:
                    os.remove(terminal)
                    print("success")
                except FileNotFoundError:
                    print("file doesen't exist")
            else:
                print("canceled")
        else:
            print("invalid df statement")
    elif terminal.startswith("md"): # md section
        if terminal == "md":
            print("missing argument")
            break
        elif terminal.startswith("md "):
            terminal = terminal.replace("md ", "")
            try:
                os.mkdir(terminal)
            except FileExistsError:
                print("directory exists")
            print("success")
        else:
            print("invalid md statement")
    elif terminal.startswith("mf"): # mf section
        if terminal == "mf":
            print("missing argument")
            break
        elif terminal.startswith("mf "):
            terminal = terminal.replace("mf ", "")
            try:
                open(terminal, "x").close()
                print("success")
            except FileExistsError:
                print("file exists")
    elif terminal.startswith("cf"): # cf section
        parts = terminal.split(" ", 2)
        if len(terminal) < 3:
            print("missing arguments")
        else:
            file1 = terminal[1].strip()
            file2 = terminal[2].strip()
            try:
                with open(file1, "r") as src_file:
                    content = src_file.read()
                with open(file2, "x") as dst_file:
                    dst_file.write(content)
                print("success")
            except FileNotFoundError:
                print("file1 doesn't exist")
            except FileExistsError:
                print("file2 exists")
            except PermissionError:
                print("invalid permissions")
    elif terminal.startswith("log"): # log section
        if terminal == "log":
            print("missing arguments")
        elif terminal.startswith("log "):
            parts = terminal.split(" ", 2)
            if len(parts) < 2:
                print("missing subcommand")
            else:
                subcommand = parts[1]
                if subcommand == "w":
                    if len(parts) < 3:
                        print("missing text to write")
                    else:
                        text = parts[2]
                        try:
                            with open(log_file, "a") as f:
                                f.write(text + "\n")
                            print("success")
                        except PermissionError:
                            print("invalid permissions")
                elif subcommand == "clear":
                    try:
                        with open(log_file, "w") as f:
                            f.write("")
                        print("log cleared")
                    except PermissionError:
                        print("invalid permissions")
                elif subcommand == "level":
                    if len(parts) < 3:
                        print(log_level)
                    else:
                        try:
                            level = int(parts[2])
                            if level == 1:
                                log_level = 1
                                logging.getLogger().setLevel(logging.ERROR)
                                print("log level set to 1")
                            elif level == 2:
                                log_level = 2
                                logging.getLogger().setLevel(logging.WARNING)
                                print("log level set to 2")
                            elif level == 3:
                                log_level = 3
                                logging.getLogger().setLevel(logging.INFO)
                                print("log level set to 3")
                            else:
                                print("invalid level (1-3)")
                                continue
                            # Save the new log level to file
                            with open(log_level_file, 'w') as f:
                                f.write(str(log_level))
                        except ValueError:
                            print("invalid level number")
                else:
                    print("invalid log subcommand")
        else:
            print("invalid log statement")
    elif terminal.startswith("af"): # af section
        parts = terminal.split(" ", 2)
        if len(parts) < 3:
            print("missing arguments")
        else:
            filename = parts[1].strip()
            text = parts[2]
            try:
                with open(filename, "a") as f:
                    f.write(text + "\n")
                print("success")
            except FileNotFoundError:
                print("file doesen't exist")
            except PermissionError:
                print("invalid permmisions")
    elif terminal.startswith("rf"): # rf section
        if terminal == "rf":
            print("missing argument")
        elif terminal.startswith("rf "):
            terminal = terminal.replace("rf ", "")
            try:
                with open(terminal, "r") as file:
                    content = file.read()
                    if len(content) > int(os.environ.get("RF_LIMIT", "5000")):
                        print("file exceeds limit")
                    else:
                        print(content)
            except FileNotFoundError:
                print("file doesn't exist")
            except PermissionError:
                print("invalid permissions")
    elif terminal.startswith("ot"): # ot section
        if terminal == "ot":
            print("missing argument")
        elif terminal.startswith("ot "):
            terminal = terminal.replace("ot ", "")
            print(terminal)
    elif terminal.startswith("sev"):
        if terminal == "sev":
            print("missing arguments")
        elif terminal.startswith("sev "):
            terminal = terminal.split(" ", 2)
            if len(terminal) < 3:
                print("missing arguments")
            else:
                part1 = terminal[1]
                part2 = terminal[2]
                os.environ[part1] = part2
                print("success")
        else:
            print("invalid sev statement")
    elif terminal.startswith("rev"):
        if terminal == "rev":
            print("missing argument")
        elif terminal.startswith("rev "):
            terminal = terminal.replace("rev ", "")
            try:
                if str(os.environ.get(terminal)) == "None":
                    print("ev doesen't exist")
                else:
                    print(os.environ.get(terminal))
            except PermissionError:
                print("invalid permissions")
            except KeyError:
                print("ev doesen't exist")
        else:
            print("invalid rev statement")
    elif terminal == "help":
        print("rev - read enviormental variables\nsev - set enviormental variables\ncs - clear screen\nrf - read file\not - output text\nmd - make directory\naf - append (to) file\ndf - delete file\nds - device specifications\nver - version\nlf - list files\ncwd - current working directory\nmf - make file\ncp - copy file\ncd - change directory\nlog - change log settings\n    log w <text> - append text to log\n    log clear - clear log\n    log level <1-3> - set log level\nexit - exit pyterminal")
    elif terminal == "cs": # cs section
        for i in range(150):
            print("\n")
    else: # invalid command section
        print("invalid command")
