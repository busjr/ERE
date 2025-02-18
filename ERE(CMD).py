import sys
from os import system, name
from pathlib import Path
from getpass import getpass
from pyAesCrypt import encryptFile, decryptFile


def clear_cmd():
    if name == 'nt': # Windows
        system("cls")
    else: # macOS, Linux
        system("clear")


def clear_path(path):
    if name == 'nt': # Windows
        path = path.replace("/", "\\")
    else: # macOS, Linux
        path = path.replace("'", "")
    return path


def main():
    while True:
        try:
            print(
                """
███████╗██████╗ ███████╗
██╔════╝██╔══██╗██╔════╝
█████╗  ██████╔╝█████╗
██╔══╝  ██╔══██╗██╔══╝
███████╗██║  ██║███████╗
╚══════╝╚═╝  ╚═╝╚══════╝v.0.7 by busjr
--------------------------------------
[1] - Encrypt
[2] - Decrypt
[3] - Back
[4] - Exit"""
            )
            input_user = int(input(">"))
            if input_user == 1:
                encrypt()
            elif input_user == 2:
                decrypt()
            elif input_user == 3:
                clear_cmd()
            elif input_user == 4:
                sys.exit()
            else:
                clear_cmd()
                print("\033[31mERROR: Invalid input.\033[0m")
        except ValueError:
            clear_cmd()
            print("\033[31mERROR: Invalid input.\033[0m")


def encrypt():
    try:
        path = str(input("Path file for encrypt: "))
        if path != "3":
            path = clear_path(path)
            password = getpass("password: ")
            encryptFile(path, path + ".aes", password)
            clear_cmd()
            print("\033[32m" + path + "\033[0m")
        else:
            clear_cmd()
    except FileNotFoundError:
        clear_cmd()
        print("\033[31mERROR: File not found.\033[0m")
    except ValueError:
        clear_cmd()
        print("\033[31mERROR: Invalid input.\033[0m")
    except Exception:
        clear_cmd()
        print("\033[31mERROR\033[0m")


def decrypt():
    try:
        path = str(input("Path file for decrypt: "))
        if path != "3":
            path = clear_path(path)
            password = getpass("password: ")
            decryptFile(path, path + " dataout.txt", password)
            clear_cmd()
            print("\033[32m" + path + "\033[0m")
        else:
            clear_cmd()
    except FileNotFoundError:
        clear_cmd()
        print("\033[31mERROR: File not found.\033[0m")
    except ValueError:
        clear_cmd()
        print("\033[31mERROR: Invalid input.\033[0m")
    except Exception:
        clear_cmd()
        print("\033[31mERROR\033[0m")


if __name__ == "__main__":
    main()
