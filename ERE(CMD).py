import pyAesCrypt

print("███████╗██████╗░███████╗")
print("██╔════╝██╔══██╗██╔════╝")
print("█████╗░░██████╔╝█████╗░░")
print("██╔══╝░░██╔══██╗██╔══╝░░")
print("███████╗██║░░██║███████╗")
print("╚══════╝╚═╝░░╚═╝╚══════╝ v.0.3 by busjr")

print('[1] - Encrypt')
print('[2] - Decipher')


def Encrypt_Ere(dir): 
    password = input("password: ")
    pyAesCrypt.encryptFile(dir, dir + ".aes", password)

def Decipher_Ere(dir):
    password = input("password: ")
    pyAesCrypt.decryptFile(dir, dir + " dataout.txt", password)

def Encrypt():
    dir = input('Path file for encrypt: ')
    dir.replace("/", "\\")
    Encrypt_Ere(dir)

a = input("Choice:")
a = int(a)
if a == 1:
    Encrypt()
elif a == 2:
    dir = input('Path file for decrypt: ')
    dir.replace("/", "\\")
    Decipher_Ere(dir)
