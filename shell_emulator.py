import io
import tarfile
import os
import xml.etree.ElementTree as ET
import tkinter as tk
from datetime import datetime

class ShellEmulator:
    def __init__(self, config=None, config_path=None):
        if config:
            self.config = config
        elif config_path:
            self.config = self.load_config(config_path)
        else:
            raise ValueError("Either 'config' or 'config_path' must be provided.")
        
        self.user = self.config['user']
        self.hostname = self.config['hostname']
        self.filesystem_path = self.config['filesystem_path']
        self.log_file = self.config['log_file']
        self.startup_script = self.config['startup_script']

        # Initialize tar file, directory, etc.
        self.tar = self.load_tar_to_memory(self.filesystem_path)
        self.current_dir = "/"  # Root directory
        self.created_files = []  # Track created files during runtime
        
        # GUI setup
        self.root = tk.Tk()
        self.root.title(f"{self.hostname} - Shell Emulator")
        self.output_text = tk.Text(self.root, height=20, width=60)
        self.output_text.pack()
        self.command_entry = tk.Entry(self.root, width=60)
        self.command_entry.pack()
        self.command_entry.bind("<Return>", self.execute_command)

        self.output_text.insert(tk.END, f"Welcome to {self.hostname} Shell Emulator\n")
        self.output_text.insert(tk.END, f"User: {self.user}\n")

        # Run the startup script if provided
        self.run_startup_script()

    def load_config(self, config_path):
        tree = ET.parse(config_path)
        root = tree.getroot()
        return {
            'user': root.find('user').text,
            'hostname': root.find('hostname').text,
            'filesystem_path': root.find('filesystem_path').text,
            'log_file': root.find('log_file').text,
            'startup_script': root.find('startup_script').text
        }

    def load_tar_to_memory(self, archive_path):
        with open(archive_path, 'rb') as f:
            tar_bytes = f.read()
            tar_file = io.BytesIO(tar_bytes)
            return tarfile.open(fileobj=tar_file)

    def run_startup_script(self):
        if self.startup_script:
            self.execute_script(self.startup_script)

    def execute_script(self, script_path):
        try:
            with open(script_path, 'r') as script_file:
                for command in script_file:
                    command = command.strip()
                    if command:
                        self.handle_command(command)
        except FileNotFoundError:
            self.output_text.insert(tk.END, f"Startup script not found: {script_path}\n")

    def execute_command(self, event):
        command = self.command_entry.get()
        self.command_entry.delete(0, tk.END)
        self.handle_command(command)

    def handle_command(self, command):
        self.log_action(command)
        if command == "ls":
            self.list_files()
        elif command.startswith("cd "):
            self.change_directory(command[3:])
        elif command == "exit":
            self.exit_shell()
        elif command.startswith("chown "):
            self.change_owner(command)
        elif command.startswith("find "):
            self.find_files(command)
        elif command.startswith("touch "):
            self.create_file(command)
        else:
            self.output_text.insert(tk.END, f"Unknown command: {command}\n")

    def list_files(self):
        try:
            # Always print the current directory before listing files
            self.output_text.insert(tk.END, f"Current directory: {self.current_dir}\n")

            members = [member for member in self.tar.getmembers() 
                    if member.name.startswith(self.current_dir.lstrip('/')) and 
                    member.name.count('/') == self.current_dir.count('/')]

            # Include created files in the ls output (but ensure they are in the current directory)
            for created_file in self.created_files:
                if created_file.startswith(self.current_dir.lstrip('/')):
                    members.append(tarfile.TarInfo(created_file))

            if not members:
                self.output_text.insert(tk.END, f"No files in directory: {self.current_dir}\n")
            else:
                for member in members:
                    display_name = member.name.lstrip('./')
                    self.output_text.insert(tk.END, f"{display_name}\n")
        except Exception as e:
            self.output_text.insert(tk.END, f"Error listing files: {str(e)}\n")

    def change_directory(self, path):
        try:
            # If the path is absolute (starts with /), use it directly
            if path.startswith('/'):
                new_path = path
            else:
                # If the path is relative, join it with the current directory
                new_path = os.path.normpath(os.path.join(self.current_dir.rstrip("/"), path.strip("/"))).replace("\\", "/")
            
            # Check if the directory exists in the tar archive
            members = [member for member in self.tar.getmembers() if member.name == new_path]

            # If it exists and is a directory, update the current directory
            if any(member.isdir() for member in members):
                self.current_dir = new_path.rstrip("/") + "/"
                self.output_text.insert(tk.END, f"Changed directory to {self.current_dir}\n")
            else:
                self.output_text.insert(tk.END, f"No such directory: {path}\n")
        except Exception as e:
            self.output_text.insert(tk.END, f"Error changing directory: {str(e)}\n")

    def exit_shell(self):
        self.output_text.insert(tk.END, "Exiting shell...\n")
        self.root.quit()

    def change_owner(self, command):
        try:
            _, owner, file = command.split()
            self.output_text.insert(tk.END, f"Changed owner of {file} to {owner}\n")
        except ValueError:
            self.output_text.insert(tk.END, "Usage: chown <owner> <file>\n")

    def find_files(self, command):
        try:
            _, pattern = command.split()
            matches = [member.name for member in self.tar.getmembers() if pattern in member.name]
            if matches:
                self.output_text.insert(tk.END, "\n".join(matches) + "\n")
            else:
                self.output_text.insert(tk.END, f"No files found matching pattern: {pattern}\n")
        except ValueError:
            self.output_text.insert(tk.END, "Usage: find <pattern>\n")

    def create_file(self, command):
        try:
            _, filename = command.split()
            # Add the new file to the in-memory list of created files
            self.created_files.append(filename)
            self.output_text.insert(tk.END, f"Created empty file: {filename}\n")
        except ValueError:
            self.output_text.insert(tk.END, "Usage: touch <filename>\n")

    def log_action(self, action):
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        log_data = ET.Element('log')
        action_element = ET.SubElement(log_data, 'action')
        action_element.text = action
        user_element = ET.SubElement(log_data, 'user')
        user_element.text = self.user
        timestamp_element = ET.SubElement(log_data, 'timestamp')
        timestamp_element.text = timestamp

        tree = ET.ElementTree(log_data)
        tree.write(self.log_file)

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    emulator = ShellEmulator(config_path="config.xml")
    emulator.run()
