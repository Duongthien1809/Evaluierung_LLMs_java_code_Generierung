import platform
import subprocess
import sys


def check_maven_installed():
    """Check if Maven is installed by running 'mvn -v'. Return True if installed, False otherwise."""
    try:
        subprocess.run(['mvn', '-v'], check=True, capture_output=True, text=True)
        return True
    except FileNotFoundError:
        return False


def install_maven():
    """Install Maven depending on the operating system."""
    os_type = platform.system()

    if os_type == 'Linux':
        print("Installing Maven on Linux...")
        subprocess.run(['sudo', 'apt-get', 'install', '-y', 'maven'], check=True)
    elif os_type == 'Darwin':  # MacOS
        print("Installing Maven on MacOS...")
        subprocess.run(['brew', 'install', 'maven'], check=True)
    elif os_type == 'Windows':
        print("Please install Maven manually from https://maven.apache.org/download.cgi")
        sys.exit(1)
    else:
        raise Exception("Unsupported OS for automatic Maven installation.")


def run_maven_build(command):
    project_directory = './project'

    # Check if Maven is installed
    if not check_maven_installed():
        print("Maven not found. Installing Maven...")
        install_maven()

    # Proceed with running the Maven command
    result = subprocess.run(
        ['mvn', 'clean', command],
        cwd=project_directory,  # Directory to run Maven command in
        capture_output=True,
        text=True
    )

    return result.returncode, result.stdout, result.stderr


# Example usage:
if __name__ == "__main__":
    returncode, stdout, stderr = run_maven_build('install')
    print(f"Return Code: {returncode}")
    print("Output:")
    print(stdout)
    print("Errors:")
    print(stderr)
