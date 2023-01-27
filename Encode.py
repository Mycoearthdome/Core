#!/usr/bin/python3

import importlib, hashlib, random, hmac, gnupg
from datetime import datetime as time
import os, sys, subprocess
from io import BytesIO
import tkinter as tk
from tkinter import filedialog
import tkinter.font as tkFont
import pickle

class App:
    def __init__(self, root, public_keyring):
        #setting title
        root.title("PUBLIC KEYRING - Please select recipident's GPG email.")
        #setting window size
        width=600
        height=500
        screenwidth = root.winfo_screenwidth()
        screenheight = root.winfo_screenheight()
        alignstr = '%dx%d+%d+%d' % (width, height, (screenwidth - width) / 2, (screenheight - height) / 2)
        root.geometry(alignstr)
        root.resizable(width=False, height=False)

        self.Selection = []
        
        
                
        self.GLineEdit_692=tk.Listbox(root)
        self.GLineEdit_692["borderwidth"] = "1px"
        self.GLineEdit_692["font"] = tkFont.Font(family='Times',size=18)
        self.GLineEdit_692["fg"] = "#333333"
        self.GLineEdit_692["justify"] = "center"
        self.GLineEdit_692["selectmode"] = "multiple"
        self.GLineEdit_692.place(x=20,y=20,width=550,height=230)
        
        self.ScrollBar = tk.Scrollbar(self.GLineEdit_692, orient="vertical")
        self.ScrollBar["command"] = self.GLineEdit_692.yview
        self.ScrollBar.pack(side="right", fill="y")
        
        i = 1
        for email in public_keyring:
            self.GLineEdit_692.insert(i,email)
            i + i + 1
        self.GLineEdit_692.select_set(0)
       
        GButton_857=tk.Button(root)
        GButton_857["bg"] = "#e9e9ed"
        ft = tkFont.Font(family='Times',size=10)
        GButton_857["font"] = ft
        GButton_857["fg"] = "#000000"
        GButton_857["justify"] = "center"
        GButton_857["text"] = "Wrap with those!"
        GButton_857.place(x=200,y=320,width=177,height=80)
        GButton_857["command"] = self.GButton_857_command

        GLabel_315=tk.Label(root)
        ft = tkFont.Font(family='Times',size=20)
        GLabel_315["font"] = ft
        GLabel_315["fg"] = "#333333"
        GLabel_315["justify"] = "center"
        GLabel_315["text"] = "Please select recipidents from the list!"
        GLabel_315.place(x=20,y=260,width=551,height=30)

    def GButton_857_command(self):
        self.Selection = [self.GLineEdit_692.get(i) for i in self.GLineEdit_692.curselection()]
        root.destroy()

gpg = gnupg.GPG(gnupghome='/home/jordan/.gnupg') #path to your .gnupg folder in your home directory. TODO:REPLACE THIS

myself = gpg.list_keys()[0]['uids'][0] #the main key
public_keyring = []
for identity in gpg.list_keys():
    email = identity['uids'][0].split("<")[1].split(">")[0]
    public_keyring.append(email)

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

#Execution keys
salt = hashlib.md5(str(random.randint(0, 65535)).encode("UTF-8")).hexdigest()
salt2 = hashlib.sha512(str(random.randint(0,65535)).encode("UTF-8")).hexdigest()
salt3 = hashlib.blake2s(str(random.randint(0,65535)).encode("UTF-8")).hexdigest()
salt4 = hashlib.md5(str(random.randint(0, 65535)).encode("UTF-8")).hexdigest()

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

if os.path.exists(db):
    os.remove(db)

#Building the magic_number database
print("Building the database...")
Completed_Process = subprocess.run("python3 magicnumber2.py", shell=True)
if Completed_Process.returncode == 0:
    print("Please select your carrier file!")
    Carrier_File = filedialog.askopenfile()
    if Carrier_File:
        print("Please select files to be concealed inside carrier file!")
        Files_Concealed = filedialog.askopenfilenames()
        Command = "python3 Matryoshka2.py"
        for filename in Files_Concealed:
                Command = Command + " " + filename
        #Summoning Matryoshka
        Completed_Process = subprocess.Popen(Command,stdin=Carrier_File.fileno(), stdout=subprocess.PIPE, shell=True)
        stdout, err = Completed_Process.communicate()
        if stdout:
            #piping the content to gpg
            root = tk.Tk()
            app = App(root, public_keyring)
            root.mainloop() #invoking user attention.
            Command = "gpg -e -q"
            for email in app.Selection: #That's everyone....might want to finetune that! tK shit.
                Command = Command + " -r " + email
            Completed2_Process = subprocess.Popen(Command,stdin=subprocess.PIPE, stdout=subprocess.PIPE, shell=True)
            stdout, err = Completed2_Process.communicate(stdout)
            if stdout:
                #make the file perfect
                Command = "python3 perfect.py e"
                Completed3_Process = subprocess.Popen(Command,stdin=subprocess.PIPE, stdout=subprocess.PIPE, shell=True)
                stdout, err = Completed3_Process.communicate(stdout)
                if stdout:
                    RarFile = tk.filedialog.askopenfilename(filetypes=[("RAR files","*.RAR *.rar")])
                    Command = "python3 RarSteg2.py e -f" + " " + RarFile
                    Completed4_Process = subprocess.Popen(Command,stdin=subprocess.PIPE, stdout=subprocess.PIPE, shell=True)
                    stdout, err = Completed4_Process.communicate(stdout)
                    if stdout:
                        Filename = RarFile.split(".")[0] +"_OUT_SEND.rar"
                        FileCreationTime = os.path.getctime(Filename)
                        if not os.path.exists("Matryoshka_DB2.db.gpg"):
                            #do something to save salts in a dictionary and secure the file with gpg armor.
                            dict_salts = {}
                            dict_salts.update({FileCreationTime:(salt, salt2, salt3, salt4)})
                            dict_pickled = pickle.dumps(dict_salts,protocol=pickle.HIGHEST_PROTOCOL)
                            Command = "gpg -e -r " + app.Selection[0] #Your GPG key.
                            Completed5_Process = subprocess.Popen(Command,stdin=subprocess.PIPE, stdout=subprocess.PIPE, shell=True)
                            stdout, err = Completed5_Process.communicate(dict_pickled)
                            f = open("Matryoshka_DB2.db.gpg", "wb")
                            f.write(stdout)
                            f.close()
                        else:
                            f = open("Matryoshka_DB2.db.gpg", "rb")
                            gpgdb = f.read()
                            f.close()
                            Command = "gpg -d"
                            Completed5_Process = subprocess.Popen(Command,stdin=subprocess.PIPE, stdout=subprocess.PIPE, shell=True)
                            stdout, err = Completed5_Process.communicate(gpgdb)
                            dict_salts = pickle.loads(stdout)
                            dict_salts.update({FileCreationTime:(salt, salt2, salt3, salt4)})
                            dict_pickled = pickle.dumps(dict_salts,protocol=pickle.HIGHEST_PROTOCOL)
                            Command = "gpg -e -r " + app.Selection[0] #Your GPG key.
                            Completed6_Process = subprocess.Popen(Command,stdin=subprocess.PIPE, stdout=subprocess.PIPE, shell=True)
                            stdout, err = Completed6_Process.communicate(dict_pickled)
                            f = open("Matryoshka_DB2.db.gpg", "wb")
                            f.write(stdout)
                            f.close()
                            
else:   
    quit()

#Cleaning up
os.remove('RarSteg2.py')
os.remove('Matryoshka2.py')
os.remove('magicnumber2.py')




    