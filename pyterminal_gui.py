import time
import platform
import os
import sys
import urllib.request
import json
import logging
import ssl
import tkinter as tk
from tkinter import scrolledtext, messagebox, filedialog

version_json_path = os.path.join(os.path.dirname(__file__), 'version.json')
if os.path.exists(version_json_path):
    logging.info("Removing version.json")
    os.remove(version_json_path)

log_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'log.txt')
log_level_file = os.path.join(os.path.dirname(__file__), 'log_level.txt')

# Load log level from file
try:
    with open(log_level_file, 'r') as f:
        log_level = int(f.read().strip())
except (FileNotFoundError, ValueError):
    log_level = 3

logging.basicConfig(
    filename=log_file,
    level=logging.INFO,
    format='(GUI) %(asctime)s - %(levelname)s - %(message)s',
    filemode='a'
)

if log_level == 1:
    logging.getLogger().setLevel(logging.ERROR)
elif log_level == 2:
    logging.getLogger().setLevel(logging.WARNING)
else:
    logging.getLogger().setLevel(logging.INFO)

logging.info("PyTerminal started (GUI)")

__version__ = "1.6"  # current local version
GITHUB_RAW_URL = "https://raw.githubusercontent.com/Denie-Dev/pyterminal/main/pyterminal.py"
GITHUB_VERSION_URL = "https://raw.githubusercontent.com/Denie-Dev/pyterminal/main/version.json"

os.environ["RF_LIMIT"] = "5000"

print("setting functions")

def check_for_update():
    try:
        with urllib.request.urlopen(
            GITHUB_VERSION_URL, timeout=5, context=ssl._create_unverified_context()
        ) as resp:
            data = resp.read().decode("utf-8")
            info = json.loads(data)
            latest = info.get("version", "").strip()
            if not latest:
                return None
            if latest != __version__:
                logging.info(f"Update available: {latest}")
                return latest
    except Exception as e:
        logging.error(f"Update check failed: {str(e)}")
        if os.environ.get("DEBUG") == "1":
            print("error: " + str(e))
    return None


def do_update():
    try:
        logging.info("Starting update download")
        if os.environ.get("DEBUG") == "1":
            print("downloading latest")
        with urllib.request.urlopen(
            GITHUB_RAW_URL, timeout=10, context=ssl._create_unverified_context()
        ) as resp:
            new_code = resp.read()

        script_path = os.path.realpath(__file__)
        backup_path = script_path + ".bak"

        try:
            if os.path.exists(backup_path):
                os.remove(backup_path)
            os.rename(script_path, backup_path)
        except Exception:
            logging.warning("Backup creation failed")
            if os.environ.get("DEBUG") == "1":
                print("backup error")

        with open(script_path, "wb") as f:
            f.write(new_code)

        logging.info("Update completed successfully")
        if os.environ.get("DEBUG") == "1":
            print("update finished")
        return True
    except Exception as e:
        logging.error(f"Update failed: {str(e)}")
        if os.environ.get("DEBUG") == "1":
            print("Update failed:", e)
            print("using old version")
        return False


# start in home directory as before
try:
    os.chdir(os.path.expanduser('~'))
except PermissionError:
    logging.error("Failed to start: Home folder PermissionError")
    print("pyterminal failed to start: Home folder PermissionError")
    sys.exit(1)
except FileNotFoundError:
    logging.error("Failed to start: No home folder")
    print("pyterminal failed to start: No home folder")
    sys.exit(1)

if "idlelib" in sys.modules:
    logging.warning("Using IDLE shell - slow performance")
    if os.environ.get("DEBUG") == "1":
        print("using idle shell,\nslow preformance")
else:
    logging.info("PyTerminal started successfully")
    if os.environ.get("DEBUG") == "1":
        print("pyterminal started")

# Optional: show logo if DEBUG=1
if os.environ.get("DEBUG") == "1" and os.environ.get("PY_LOGO_STARTUP") == "1":
    time.sleep(1)
    print(" _ _ _ ".center(os.get_terminal_size().columns))
    time.sleep(1)
    print(" _ __ _ _| |_ ___ _ __ _ __ ___ (_)_ __ __ _| |".center(os.get_terminal_size().columns))
    time.sleep(1)
    print("| '_ \\| | | | __/ _ \\ '__| '_ ` _ \\| | '_ \\ / _` | |".center(os.get_terminal_size().columns))
    time.sleep(1)
    print("| |_) | |_| | || __/ | | | | | | | | | | | (_| | |".center(os.get_terminal_size().columns))
    time.sleep(1)
    print("| .__/ \\__, |\\__\\___|_| |_| |_| |_|_|_| |_|\\__,_|_|".center(os.get_terminal_size().columns))
    time.sleep(1)
    print("|_| |___/ ".center(os.get_terminal_size().columns))


# ---------------------- core command handler (no input/print) ------------------

def handle_command(command: str) -> str:
    """
    Take a raw command string and return the output string.
    This is mostly the same logic as your while-loop, but
    using return strings instead of print/input.
    """
    global log_level

    command = command.strip()
    if not command:
        return ""

    logging.info(f"Command executed: {command}")

    # exit is handled by GUI separately, but we still respond here
    if command == "exit":
        logging.info("PyTerminal exiting")
        return "Exiting pyterminal"

    # ds section
    if command == "ds":
        u = platform.uname()
        return (
            f"\nSystem: {u.system}\n"
            f"Node Name: {u.node}\n"
            f"Release: {u.release}\n"
            f"Version: {u.version}\n"
            f"Machine: {u.machine}\n"
            f"Processor: {u.processor}\n"
        )

    # ver section
    if command == "ver":
        return f"PyTerminal Release {__version__}\nBy Dennis"

    # lf section
    if command.startswith("lf"):
        if command.startswith("lf "):
            path = command.replace("lf ", "", 1)
            try:
                return "\n".join(os.listdir(path))
            except FileNotFoundError:
                return "directory doesn't exist"
            except PermissionError:
                return "invalid permissions"
        else:  # "lf"
            try:
                return "\n".join(os.listdir(os.getcwd()))
            except PermissionError:
                return "invalid permissions"

    # cwd section
    if command == "cwd":
        return os.getcwd()

    # cd section
    if command.startswith("cd"):
        if command == "cd":
            if os.getcwd() == os.path.expanduser('~'):
                return "at home folder"
            else:
                os.chdir(os.path.expanduser('~'))
                return "success"
        elif command.startswith("cd "):
            path = command.replace("cd ", "", 1)
            if path == ".." and os.getcwd() == "/":
                return "at root folder"
            try:
                os.chdir(path)
                return "success"
            except FileNotFoundError:
                return "directory doesn't exist"
            except PermissionError:
                return "invalid permissions"
        else:
            return "invalid cd statement"

    # df section
    if command.startswith("df"):
        if command == "df":
            return "argument missing"
        elif command.startswith("df "):
            filename = command.replace("df ", "", 1)
            # in GUI we skip the interactive confirm and just delete
            try:
                os.remove(filename)
                return "success"
            except FileNotFoundError:
                return "file doesn't exist"
        else:
            return "invalid df statement"

    # md section
    if command.startswith("md"):
        if command == "md":
            return "missing argument"
        elif command.startswith("md "):
            dirname = command.replace("md ", "", 1)
            try:
                os.mkdir(dirname)
                return "success"
            except FileExistsError:
                return "directory exists"
            except PermissionError:
                return "invalid permissions"
        else:
            return "invalid md statement"

    # mf section
    if command.startswith("mf"):
        if command == "mf":
            return "missing argument"
        elif command.startswith("mf "):
            filename = command.replace("mf ", "", 1)
            try:
                open(filename, "x").close()
                return "success"
            except FileExistsError:
                return "file exists"
            except PermissionError:
                return "invalid permissions"
        else:
            return "invalid mf statement"

    # cf section
    if command.startswith("cf"):
        parts = command.split(" ", 2)
        if len(parts) < 3:
            return "missing arguments"
        _, file1, file2 = parts
        file1 = file1.strip()
        file2 = file2.strip()
        try:
            with open(file1, "r") as src_file:
                content = src_file.read()
            with open(file2, "x") as dst_file:
                dst_file.write(content)
            return "success"
        except FileNotFoundError:
            return "file1 doesn't exist"
        except FileExistsError:
            return "file2 exists"
        except PermissionError:
            return "invalid permissions"

    # log section
    if command.startswith("log"):
        parts = command.split(" ", 2)
        if len(parts) < 2:
            return "missing subcommand"
        subcommand = parts[1]

        if subcommand == "w":
            if len(parts) < 3:
                return "missing text to write"
            text = parts[2]
            try:
                with open(log_file, "a") as f:
                    f.write(text + "\n")
                return "success"
            except PermissionError:
                return "invalid permissions"

        elif subcommand == "clear":
            try:
                with open(log_file, "w") as f:
                    f.write("")
                return "log cleared"
            except PermissionError:
                return "invalid permissions"

        elif subcommand == "level":
            if len(parts) < 3:
                return str(log_level)
            else:
                try:
                    level = int(parts[2])
                    if level == 1:
                        log_level = 1
                        logging.getLogger().setLevel(logging.ERROR)
                        msg = "log level set to 1"
                    elif level == 2:
                        log_level = 2
                        logging.getLogger().setLevel(logging.WARNING)
                        msg = "log level set to 2"
                    elif level == 3:
                        log_level = 3
                        logging.getLogger().setLevel(logging.INFO)
                        msg = "log level set to 3"
                    else:
                        return "invalid level (1-3)"

                    with open(log_level_file, 'w') as f:
                        f.write(str(log_level))
                    return msg
                except ValueError:
                    return "invalid level number"
        return "invalid log subcommand"

    # af section
    if command.startswith("af"):
        parts = command.split(" ", 2)
        if len(parts) < 3:
            return "missing arguments"
        filename = parts[1].strip()
        text = parts[2]
        try:
            with open(filename, "a") as f:
                f.write(text + "\n")
            return "success"
        except FileNotFoundError:
            return "file doesn't exist"
        except PermissionError:
            return "invalid permissions"

    # rf section
    if command.startswith("rf"):
        if command == "rf":
            return "missing argument"
        elif command.startswith("rf "):
            filename = command.replace("rf ", "", 1)
            try:
                with open(filename, "r") as file:
                    content = file.read()
                limit = int(os.environ.get("RF_LIMIT", "5000"))
                if len(content) > limit:
                    return "file exceeds limit"
                else:
                    return content
            except FileNotFoundError:
                return "file doesn't exist"
            except PermissionError:
                return "invalid permissions"

    # ot section
    if command.startswith("ot"):
        if command == "ot":
            return "missing argument"
        elif command.startswith("ot "):
            return command.replace("ot ", "", 1)

    # sev section
    if command.startswith("sev"):
        if command == "sev":
            return "missing arguments"
        parts = command.split(" ", 2)
        if len(parts) < 3:
            return "missing arguments"
        part1 = parts[1]
        part2 = parts[2]
        os.environ[part1] = part2
        return "success"

    # rev section
    if command.startswith("rev"):
        if command == "rev":
            return "missing argument"
        name = command.replace("rev ", "", 1)
        try:
            value = os.environ.get(name)
            if value is None:
                return "ev doesn't exist"
            else:
                return value
        except PermissionError:
            return "invalid permissions"
        except KeyError:
            return "ev doesn't exist"

    # help section
    if command == "help":
        return (
            "rev - read environmental variables\n"
            "sev - set environmental variables\n"
            "cs - clear screen\n"
            "rf - read file\n"
            "ot - output text\n"
            "md - make directory\n"
            "af - append (to) file\n"
            "df - delete file\n"
            "ds - device specifications\n"
            "ver - version\n"
            "lf - list files\n"
            "cwd - current working directory\n"
            "mf - make file\n"
            "cf - copy file\n"
            "cd - change directory\n"
            "log - change log settings\n"
            " log w <text> - append text to log\n"
            " log clear - clear log\n"
            " log level <1-3> - set log level\n"
            "exit - exit pyterminal"
        )

    # cs section
    if command == "cs":
        # GUI clear is handled in the frontend; we just send a flag-like message
        return "__CLEAR__"

    # invalid command
    return "invalid command"


# ------------------------------ Tkinter GUI with Dynamic Scaling -----------------------------------

class PyTerminalGUI:
    def __init__(self, master):
        self.master = master
        master.title("PyTerminal GUI")
        
        # Set minimum window size for macOS
        master.minsize(400, 300)
        
        # Initial window size
        master.geometry("800x600")
        
        # Store previous window size for detecting resize events
        self.prev_width = 800
        self.prev_height = 600

        # output area
        self.output = scrolledtext.ScrolledText(
            master, wrap=tk.WORD, state="normal"
        )
        self.output.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
        self.output.insert(tk.END, "pyterminal started\nType 'help' for commands.\n\n")
        self.output.configure(state="disabled")

        # command entry
        self.entry = tk.Entry(master)
        self.entry.grid(row=1, column=0, padx=5, pady=5, sticky="we")
        self.entry.bind("<Return>", self.run_command_event)

        # grid weights (make output area grow with window)
        master.grid_rowconfigure(0, weight=1)
        master.grid_columnconfigure(0, weight=1)
        
        # Bind resize event for dynamic scaling
        master.bind("<Configure>", self.on_window_resize)

        # check updates (non-blocking-ish)
        master.after(100, self.check_update_startup)

    def on_window_resize(self, event):
        """Dynamically scale font sizes based on window size"""
        width = event.width
        height = event.height
        
        # Only update if window size actually changed
        if width == self.prev_width and height == self.prev_height:
            return
        
        self.prev_width = width
        self.prev_height = height
        
        # Calculate scale factor (width-based)
        # At 400px (min), use small font; at 1200px+, use large font
        scale_factor = max(0.8, min(1.5, (width - 400) / 800))
        
        # Base font size
        base_font_size = 12
        scaled_font_size = max(10, int(base_font_size * scale_factor))
        
        # Apply scaled font to output text
        font = ("Menlo" if platform.system() == "Darwin" else "Courier", scaled_font_size)
        self.output.configure(font=font)
        
        # Scale entry font slightly smaller
        entry_font = ("Menlo" if platform.system() == "Darwin" else "Courier", max(10, int(scaled_font_size * 0.95)))
        self.entry.configure(font=entry_font)

    def append_output(self, text: str):
        self.output.configure(state="normal")
        self.output.insert(tk.END, text + "\n")
        self.output.see(tk.END)
        self.output.configure(state="disabled")

    def clear_output(self):
        self.output.configure(state="normal")
        self.output.delete("1.0", tk.END)
        self.output.configure(state="disabled")

    def run_command_event(self, event):
        cmd = self.entry.get().strip()
        if not cmd:
            return

        # show the command in the output
        self.append_output(f"{str(os.getcwd())}> {cmd}")
        self.entry.delete(0, tk.END)

        if cmd == "exit":
            self.append_output("Exiting pyterminal")
            self.master.after(200, self.master.destroy)
            return

        result = handle_command(cmd)

        if result == "__CLEAR__":
            self.clear_output()
        elif result:
            self.append_output(result)

    def check_update_startup(self):
        latest = check_for_update()
        if latest is not None:
            if messagebox.askyesno(
                "Update Available", f"New version {latest} available. Update now?"
            ):
                ok = do_update()
                if ok:
                    messagebox.showinfo("Update", "Update finished. Restart the app.")
                else:
                    messagebox.showerror("Update", "Update failed, using old version.")


def main():
    root = tk.Tk()
    app = PyTerminalGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
