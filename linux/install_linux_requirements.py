import subprocess

from constants import DEBUGGING

required_packages: list = [
   'ffmpeg'
]

if DEBUGGING:
    required_packages.append('gnome-terminal')

def run_command(command):
    print(f"Running command: {' '.join(command)}")

    process = subprocess.Popen(command, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

    while process.poll() is None:
        output = process.stdout.readline().rstrip()
        error = process.stderr.readline().rstrip()
        if output:
            print(f"Output: {output}")
        if error:
            print(f"Error: {error}")

    output, error = process.communicate()
    if output:
        print(f"Output: {output}")
    if error:
        print(f"Error: {error}")

    return process.returncode, output, error

def update_packages():
    update_command = ['sudo', 'apt-get', 'update']
    return run_command(update_command)

def install_packages(packages):
    install_command = ['sudo', 'apt-get', 'install', '-y'] + packages
    return run_command(install_command)

def update_and_install_packages(packages_to_install):
    update_return_code, _, update_error = update_packages()
    if update_return_code != 0:
        print(f"Error updating packages: {update_error}")
    else:
        install_return_code, _, install_error = install_packages(packages_to_install)
        if install_return_code != 0:
            print(f"Error installing packages: {install_error}")
        else:
            print("Packages installed successfully!")

def run():
    update_and_install_packages(required_packages)
