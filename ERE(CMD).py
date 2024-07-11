import pyAesCrypt
from os import system
from getpass import getpass
    
def Choice():
    try:
        print("""
███████╗██████╗ ███████╗
██╔════╝██╔══██╗██╔════╝
█████╗  ██████╔╝█████╗  
██╔══╝  ██╔══██╗██╔══╝  
███████╗██║  ██║███████╗
╚══════╝╚═╝  ╚═╝╚══════╝v.0.4 by busjr
--------------------------------------
[1] - Encrypt
[2] - Decipher
[3] - Back
[4] - Exit""")
        input_user = int(input(">"))
        if input_user == 1:
            Encrypt()
        elif input_user == 2:
            Decrypt()
        elif input_user == 4:
            exit()
        else:
            system('cls')
            Choice()
    except ValueError:
        system('cls')
        Choice()

def Encrypt(): 
    try:
        path = input('Path file for encrypt: ')
        if  path != '3':
            path.replace("/", "\\")
            password = getpass("password: ",  stream="*")
            pyAesCrypt.encryptFile(path, path + ".aes", password)
        else:
            system('cls')
            Choice()
    except ValueError:
            system('cls')
            print("\033[31m" + 'ERORRE: File not found or file extension not supported.(Please check the full path to the file or its .aes extension and open the program with administrator rights.' + "\033[0m")
            Choice()

def Decrypt():
    try:
        path = input('Path file for decrypt: ')
        if path != '3':
            path.replace("/", "\\")
            password = getpass("password: ", stream="*")
            pyAesCrypt.decryptFile(path, path + " dataout.txt", password)
        else:
            system('cls')
            Choice()
    except ValueError:
        system('cls')
        print("\033[31m" + 'ERORRE: File not found or file extension not supported.(Please check the full path to the file or its .aes extension and open the program with administrator rights.' + "\033[0m")
        Choice()

if __name__ == "__main__":       
    Choice()