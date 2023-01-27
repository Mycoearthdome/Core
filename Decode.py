#!/usr/bin/python3

import gnupg, os, subprocess, pickle, importlib, hmac, hashlib
import tkinter as tk
from tkinter import filedialog

def write_new_modules(module_name, source):
    filename = module_name + "2.py"
    f = open(filename,'w')
    f.write(source)
    f.close()
    return True
    
def modify_and_check(module_name, package, Version, modification_func=False, modification_func2=False, modification_func3=False, modification_func4=False):
    spec = importlib.util.find_spec(module_name, package)
    source = spec.loader.get_source(module_name)
    if modification_func:
        new_source = modification_func(source)
        if modification_func2:
            new_source2 = modification_func2(new_source)
            new_source = new_source2
            if modification_func3:
                new_source3 = modification_func3(new_source)
                new_source = new_source3
                if modification_func4:
                    new_source4 = modification_func4(new_source)
                    new_source = new_source4
    if hmac.compare_digest(hashlib.sha512(source.encode(encoding="UTF-8")).hexdigest(),Version[module_name]):
        if modification_func:
            write_new_modules(module_name, new_source)
        return True
    else:
        return False

#Initializations
Version1 = {}
Version1.update({"Matryoshka":'a014e5e5db2c49c28da8da8e5fed72875f08b5a76cd6e0be3ea954d8ae6d8a996d2b40d94170541ad16ccab2ee46094fa638a6daa1dac1f046ead61070f03ab2'})
Version1.update({"RarSteg":'f02ad51fdeb49b4f2234ae983605d5174d7abb249bec34572ec29205a062921b9a3929360e42332ca8fbf08876f7bc5323b0ef853f84638eb1230e208e96cfd8'})
Version1.update({'magicnumber':'cd117b98979afe50687fae7c33a03dc637ab736fa0daf22cf856b0020df837bff7f8b4b3235d2ac1262f52341253e72d38b022b47172666a8ccdea561fdcac1e'})
Version1.update({"perfect":'a246a2f3afffde3641b64942a6271605bdb1719156ab6ecd1acba4b3136f409a71f5d89a7ace17d7a6a1eca093c8e24c34124fe58455e25096a5fcf37dbf31ea'})
db = 'Matryoshka.db'

if os.path.exists("Matryoshka_DB2.db.gpg"):
    f = open("Matryoshka_DB2.db.gpg", "rb")
    Command = "gpg -d"
    Completed_Process = subprocess.Popen(Command,stdin=f, stdout=subprocess.PIPE, shell=True)
    stdout, err = Completed_Process.communicate()
    dict_salts = pickle.loads(stdout)
    f.close()
    print("Please choose your RAR file!")
    RarFile = tk.filedialog.askopenfilename(filetypes=[("RAR files","*.RAR *.rar")])
    FileCreationTime = os.path.getctime(RarFile)
    
    #Execution keys
    salt, salt2, salt3, salt4 = dict_salts[FileCreationTime]
    
else:
    print("Failed to recover Matryoshka Database file: Matryoshka_DB2.gpg.--QUITTING!")
    quit()


if not modify_and_check("Matryoshka", None, Version1, lambda src: src.replace("|jordan|", salt), lambda src: src.replace("|Jordan_Legare|", salt2),lambda src: src.replace("batman is okay i guess", salt3), lambda src: src.replace("|fileinfo|", salt4)):
    print("File: Matroyshka.py has been changed! - QUITTING!")
    quit() #Files were altered.
if not modify_and_check("RarSteg", None, Version1, lambda src: src.replace("|jordan|", salt), lambda src: src.replace("|jordan-file||", salt2),lambda src: src.replace("|>ENCODED<|", salt3)):
    print("File: RarSteg.py has been changed! - QUITTING!")
    quit() #Files were altered.
if not modify_and_check("magicnumber", None, Version1, lambda src: src.replace("|jordan|", salt), lambda src: src.replace("batman is okay i guess", salt3)):
    print("File: magic_number.py has been changed! - QUITTING!")
    quit() #Files were altered.
if not modify_and_check("perfect", None, Version1):
    print("File: perfect.py has been changed! - QUITTING!")
    quit()

#if os.path.exists(db):
#    os.remove(db)

f = open(RarFile,'rb')
Command = "python3 RarSteg2.py d"
Completed_Process = subprocess.Popen(Command,stdin=f.fileno(), stdout=subprocess.PIPE, shell=True)
stdout, err = Completed_Process.communicate()
if stdout:
    Command = "python3 perfect.py d"
    Completed_Process2 = subprocess.Popen(Command,stdin=subprocess.PIPE, stdout=subprocess.PIPE, shell=True)
    stdout, err = Completed_Process2.communicate(stdout)
    if stdout:
        Command = "gpg -d -q"
        Completed_Process3 = subprocess.Popen(Command,stdin=subprocess.PIPE, stdout=subprocess.PIPE, shell=True)
        stdout, err = Completed_Process3.communicate(stdout)
        if stdout:
            Command = "python3 Matryoshka2.py -r"
            Completed_Process4 = subprocess.Popen(Command,stdin=subprocess.PIPE, shell=True)
            stdout, err = Completed_Process4.communicate(stdout)

#Cleaning up
os.remove('RarSteg2.py')
os.remove('Matryoshka2.py')
os.remove('magicnumber2.py')

print("DONE!")