import sys
from os import system, name
from getpass import getpass
from pyAesCrypt import encryptFile, decryptFile


def ClearCMD():
    if name == 'nt':
        system("cls")
    else:
        system("clear")


def Main():
    while True:
        try:
            print(
                """
███████╗██████╗ ███████╗
██╔════╝██╔══██╗██╔════╝
█████╗  ██████╔╝█████╗
██╔══╝  ██╔══██╗██╔══╝
███████╗██║  ██║███████╗
╚══════╝╚═╝  ╚═╝╚══════╝v.0.6 by busjr
--------------------------------------
[1] - Encrypt
[2] - Decrypt
[3] - Back
[4] - Exit"""
            )
            input_user = int(input(">"))
            if input_user == 1:
                Encrypt()
            elif input_user == 2:
                Decrypt()
            elif input_user == 3:
                ClearCMD()
            elif input_user == 4:
                sys.exit()
            else:
                ClearCMD()
                print("\033[31mERROR: Invalid input.\033[0m")
        except ValueError:
            ClearCMD()
            print("\033[31mERROR: Invalid input.\033[0m")


def Encrypt():
    try:
        path = str(input("Path file for encrypt: "))
        if path != "3":
            path.replace("/", "\\")
            password = getpass("password: ")
            encryptFile(path, path + ".aes", password)
            ClearCMD()
            print("\033[32m" + path + "\033[0m")
        else:
            ClearCMD()
    except FileNotFoundError:
        ClearCMD()
        print("\033[31mERROR: File not found.\033[0m")
    except ValueError:
        ClearCMD()
        print("\033[31mERROR: Invalid input.\033[0m")
    except Exception:
        ClearCMD()
        print("\033[31mERROR: Invalid input.\033[0m")


def Decrypt():
    try:
        path = str(input("Path file for decrypt: "))
        if path != "3":
            path.replace("/", "\\")
            password = getpass("password: ", stream="*")
            decryptFile(path, path + " dataout.txt", password)
            ClearCMD()
            print("\033[32m" + path + "\033[0m")
        else:
            ClearCMD()
    except FileNotFoundError:
        ClearCMD()
        print("\033[31mERROR: File not found.\033[0m")
    except ValueError:
        ClearCMD()
        print("\033[31mERROR: Invalid input.\033[0m")
    except Exception:
        ClearCMD()
        print("\033[31mERROR: Invalid input.\033[0m")


if __name__ == "__main__":
    Main()
