import io
import os
import tarfile
from datetime import datetime
from shell_emulator import ShellEmulator

class TestShellEmulator:
    def __init__(self):
        # Mock configuration data
        self.config = {
            'user': 'testuser',
            'hostname': 'testhost',
            'filesystem_path': 'test_filesystem.tar',  # Make sure this file exists or mock it
            'log_file': 'test_log.xml',
            'startup_script': ''
        }

        # Create a temporary tar file with some test data (directories and files)
        self.create_mock_tarfile()

        # Initialize the ShellEmulator instance using the mock configuration
        self.emulator = ShellEmulator(config=self.config)  # Use the 'config' argument

    def create_mock_tarfile(self):
        # Create a temporary tar file for testing
        with tarfile.open(self.config['filesystem_path'], 'w') as tar:
            # Simulate directories by adding files with directory paths
            tar.addfile(tarfile.TarInfo(name="home/"))
            tar.addfile(tarfile.TarInfo(name="home/user/"))
            tar.addfile(tarfile.TarInfo(name="home/user/file1.txt"))
            tar.addfile(tarfile.TarInfo(name="home/user/file2.txt"))
            tar.addfile(tarfile.TarInfo(name="lesson/"))
            tar.addfile(tarfile.TarInfo(name="lesson/lesson1.txt"))
            tar.addfile(tarfile.TarInfo(name="lesson/lesson2.txt"))

    def test_ls(self):
        print("Running test: ls")

        # Test `ls` command when the current directory is '/'
        self.emulator.current_dir = '/'
        self.emulator.list_files()

        # Capture the output of the `ls` command
        output = self.get_output()

        # Assert that home and lesson directories are listed
        assert "home/" in output, "Test failed: home directory not found in ls output"
        assert "lesson/" in output, "Test failed: lesson directory not found in ls output"
        print("ls test passed.")

    def test_cd(self):
        print("Running test: cd")

        # Test `cd` command to change to home directory
        self.emulator.change_directory('home')
        output = self.get_output()

        # Assert the current directory is now '/home'
        assert "/home" in output, "Test failed: Failed to change to home directory"

        # Test changing to a non-existent directory
        self.emulator.change_directory('nonexistent')
        output = self.get_output()

        # Assert the correct error message is displayed
        assert "No such directory" in output, "Test failed: No error for non-existent directory"
        print("cd test passed.")

    def test_touch(self):
        print("Running test: touch")

        # Test `touch` command to create a new file
        self.emulator.handle_command('touch newfile.txt')
        output = self.get_output()

        # Assert the file was created
        assert "Created empty file: newfile.txt" in output, "Test failed: touch command didn't create file"

        # Test listing files to ensure the new file is listed
        self.emulator.list_files()
        output = self.get_output()
        assert "newfile.txt" in output, "Test failed: new file not found in ls output"
        print("touch test passed.")

    def test_chown(self):
        print("Running test: chown")

        # Test `chown` command to change file ownership (mock behavior)
        self.emulator.handle_command('chown newowner file1.txt')
        output = self.get_output()

        # Assert the ownership change message is correct
        assert "Changed owner of file1.txt to newowner" in output, "Test failed: chown didn't change ownership"
        print("chown test passed.")

    def test_find(self):
        print("Running test: find")

        # Test `find` command to search for a file
        self.emulator.handle_command('find file1.txt')
        output = self.get_output()

        # Assert that the file is found
        assert "file1.txt" in output, "Test failed: file1.txt not found in find output"
        print("find test passed.")

    def test_exit(self):
        print("Running test: exit")

        # Test `exit` command to quit the shell emulator
        self.emulator.handle_command('exit')
        output = self.get_output()

        # Assert that exit message is displayed
        assert "Exiting shell..." in output, "Test failed: exit command didn't work"
        print("exit test passed.")

    def get_output(self):
        # Helper function to capture the output from the emulator
        return self.emulator.output_text.get("1.0", "end-1c")

# Run the tests
if __name__ == '__main__':
    test = TestShellEmulator()

    # Run all the tests
    test.test_ls()
    test.test_cd()
    test.test_touch()
    test.test_chown()
    test.test_find()
    test.test_exit()

    print("All tests passed.")
