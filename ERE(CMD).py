import sys
import subprocess
from os import system
from getpass import getpass
from pyAesCrypt import encryptFile, decryptFile


def Choice():
    try:
        print(
            """
███████╗██████╗ ███████╗
██╔════╝██╔══██╗██╔════╝
█████╗  ██████╔╝█████╗
██╔══╝  ██╔══██╗██╔══╝
███████╗██║  ██║███████╗
╚══════╝╚═╝  ╚═╝╚══════╝v.0.5 by busjr
--------------------------------------
[1] - Encrypt
[2] - Decipher
[3] - Back
[4] - Enable context menu
[5] - Disable context menu
[6] - Exit"""
        )
        input_user = int(input(">"))
        if input_user == 1:
            Encrypt()
        elif input_user == 2:
            Decrypt()
        elif input_user == 4:
            menu()
        elif input_user == 5:
            menu_delete()
        elif input_user == 6:
            exit()
        else:
            system("cls")
            Choice()
    except ValueError:
        system("cls")
        Choice()


def menu():
    try:
        script_path = sys.argv[0]
        base_path = r"HKEY_CLASSES_ROOT\Directory\Background\shell"
        key_name = "ERE"
        command_key_path = f"{base_path}\\{key_name}\\command"
        subprocess.run(
            [
                "reg",
                "add",
                f"{base_path}\\{key_name}",
                "/ve",
                "/t",
                "REG_SZ",
                "/d",
                "Open in ERE",
                "/f",
            ],
            check=True,
        )
        subprocess.run(
            [
                "reg",
                "add",
                command_key_path,
                "/ve",
                "/t",
                "REG_SZ",
                "/d",
                script_path,
                "/f",
            ],
            check=True,
        )
        system("cls")
        print("Done")
        Choice()
    except Exception:
        system("cls")
        print(
            "\033[31m"
            + (
                'If you want to enable the context menu, click "Yes" '
                "(When moving .exe file, choice here again)." + "\033[0m"
            )
        )
        Choice()


def menu_delete():
    try:
        path = r"HKEY_CLASSES_ROOT\Directory\Background\shell\ERE"
        command = ["reg", "delete", path, "/f"]
        subprocess.run(command, check=True)
        system("cls")
        print("Done")
        Choice()
    except Exception:
        system("cls")
        print(
            "\033[31m"
            + (
                'If you want to enable the context menu, click "Yes" '
                "(When moving .exe file, choice here again)." + "\033[0m"
            )
        )
        Choice()


def Encrypt():
    try:
        path = input("Path file for encrypt: ")
        if path != "3":
            path.replace("/", "\\")
            password = getpass("password: ", stream="*")
            encryptFile(path, path + ".aes", password)
        else:
            system("cls")
            Choice()
    except Exception:
        system("cls")
        print(
            "\033[31m"
            + (
                "ERROR: File not found or file extension not "
                "supported. (Please check the full path to the "
                "file or its .aes extension and open the program "
                "with administrator rights." + "\033[0m"
            )
        )
        Choice()


def Decrypt():
    try:
        path = input("Path file for decrypt: ")
        if path != "3":
            path.replace("/", "\\")
            password = getpass("password: ", stream="*")
            decryptFile(path, path + " dataout.txt", password)
        else:
            system("cls")
            Choice()
    except Exception:
        system("cls")
        print(
            "\033[31m"
            + (
                "ERROR: File not found or file extension not "
                "supported. (Please check the full path to the "
                "file or its .aes extension and open the program "
                "with administrator rights." + "\033[0m"
            )
        )
        Choice()


if __name__ == "__main__":
    Choice()
