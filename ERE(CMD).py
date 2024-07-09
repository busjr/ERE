import pyAesCrypt

print("""
███████╗██████╗ ███████╗
██╔════╝██╔══██╗██╔════╝
█████╗  ██████╔╝█████╗  
██╔══╝  ██╔══██╗██╔══╝  
███████╗██║  ██║███████╗
╚══════╝╚═╝  ╚═╝╚══════╝v.0.4 by busjr""")

def Choice():
    print("""----------------------------------------
[1] - Encrypt
[2] - Decipher
[3] - Back
[4] - Exit""")
    input_user = int(input("Choice:"))
    if input_user == 1:
        Encrypt()
    elif input_user == 2:
        Decrypt()
    elif input_user == 4:
        exit()
    else:
        Choice()

def Encrypt_Ere(dir): 
    try:
        input_user = input("password: ")
        if input_user != '3':
            password = input_user
            pyAesCrypt.encryptFile(dir, dir + ".aes", password)
            Choice()
        else:
            Choice()
    except ValueError:
            print('File not found or file extension not supported.(Please check the full path to the file or its .txt extension.)')

def Decipher_Ere(dir):
    try:
        input_user = input("password: ")
        if input_user != '3':
            password = input_user
            pyAesCrypt.decryptFile(dir, dir + " dataout.txt", password)
            Choice()
        else:
            Choice()
    except ValueError:
        print('File not found or file extension not supported.(Please check the full path to the file or its .aes extension.)')

def Encrypt():
    input_user = input('Path file for encrypt: ')
    if input_user != '3':
        dir = input_user
        dir.replace("/", "\\")
        Encrypt_Ere(dir)
    else:
        Choice()
    
def Decrypt():
    input_user = input('Path file for decrypt: ')
    if input_user != '3':
        dir = input_user
        dir.replace("/", "\\")
        Decipher_Ere(dir)
    else:
        Choice()

Choice()