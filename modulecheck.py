import subprocess
import sys


def check_python_environment():
    print("Python executable:", sys.executable)
    print("sys.path:", sys.path)

    try:
        import pypdf
        print("pypdf version:", pypdf.__version__)
    except ImportError as e:
        print("ImportError:", e)

    # Check installed packages
    installed_packages = subprocess.check_output([sys.executable, "-m", "pip", "list"]).decode("utf-8")
    print("Installed packages:", installed_packages)


def main():
    check_python_environment()


if __name__ == "__main__":
    main()
