print("Loading pyterminal")
print("importing time")
import time
print("importing platform")
import platform
print("importing os")
import os
print("importing sys")
import sys
terminal = ""
try:
    os.chdir(os.path.expanduser('~'))
except PermissionError:
    print("pyterminal failed to start: Home folder PermissionError")
    exit()
except FileNotFoundError:
    print("pyterminal failed to start: No home folder")
    exit()
if "idlelib" in sys.modules:
    print("using idle shell,\nslow preformance")
else:
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
    if terminal == "exit":
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
        print("PyTerminal Release 1.3\nBy Dennis")
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
    elif terminal.startswith("cf"): # cf section
        if terminal == "cf":
            print("missing argument")
            break
        elif terminal.startswith("cf "):
            terminal = terminal.replace("cf ", "")
            try:
                open(terminal, "x").close()
                print("success")
            except FileExistsError:
                print("file exists")
    elif terminal.startswith("af "): # af section
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
                    if len(content) > 5000:
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
        print("rev - read enviormental variables\nsev - set enviormental variables\ncs - clear screen\nrf - read file\not - output text\nmd - make directory\naf - append (to) file\ndf - delete file\nds - device specifications\nver - version\nlf - list files\ncwd - current working directory\ncf - create file\ncd - change directory")
    elif terminal == "cs": # cls section
        for i in range(150):
            print("\n")
    else: # invalid command section
        print("invalid command")
