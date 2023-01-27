#!/usr/bin/python3
    
import io, sys, ast, lzma, hmac, hashlib, pickle
from os.path import exists, getsize


"""
Matryoshka

 Returns:
        _type_: file encapsulation tool
"""

_type_ = """
Matryoshka - File encapsulation tool.

Matryoshka accepts STDOUT and concatenates LZMA files outputs to SDTOUT.

USAGE:  Matryoshka [OPTION] [file]...[file]

OPTION:
-r Rebuilds files from a mingled file.
"""

dict_magic_numbers = {}
db = "Matryoshka.db"
key = "batman is okay i guess"
lzma_filters = [
    {"id": lzma.FILTER_DELTA, "dist": 5},
    {"id": lzma.FILTER_LZMA2, "preset": 7 | lzma.PRESET_EXTREME},
]

def write_db(filename, key, dict_raw, lzma_filters):
    
    bytes_key = bytes(key, 'UTF-8')
    bytes_dict = pickle.dumps(dict_raw)
    ###print(bytes_dict) 
    h = hmac.new(bytes_key, bytes_dict, hashlib.sha512 )

    if not exists(filename):
        with lzma.open(filename, 'wb', format=lzma.FORMAT_RAW, check=lzma.CHECK_NONE, filters=lzma_filters) as f:
            pickle.dump(dict_raw, f, protocol=pickle.HIGHEST_PROTOCOL)
            length = f.write(bytes(h.hexdigest(),encoding="UTF-8"))
            f.write(bytes("|jordan|",encoding="UTF-8"))
            f.write(bytes(str(length), encoding="UTF-8"))
        f.close()
        
    return h

def read_db(filename, key, lzma_filters):
    bytes_key = bytes(key, 'UTF-8')
    with lzma.open(filename,"rb", format=lzma.FORMAT_RAW, filters=lzma_filters) as f:
        hashing = bytearray(bytes(f.read()))
        if b'|jordan|' in hashing:
            index = hashing.find(b'|jordan|')
            
            ###print(index,"-->",len(hashing))
            
            length = int(bytes(hashing[index + 32:]).decode("UTF-8")) #signature is 32 bytes
            
            pickled = bytes(hashing[:index-length]) #unpacked from lzma.
            
            hashing = hashing[index-length:index] #recovered from the file
            
            with io.BytesIO(pickled) as g:
                    
                old = g.getvalue()
                
                old = bytearray(old)
                    
                old[1] = old[1] -1 #TODO: FIGURE OUT WHY THERE IS ALWAYS +1 ON THAT BYTE.
                    
                old = bytes(old)
                    
                with io.BytesIO(old) as k:
                    h = hmac.new(bytes_key,k.getbuffer(),hashlib.sha512)
                
                    if bytes(hashing).decode("UTF-8") == h.hexdigest():
                        #probably safe to load the pickle file
                        dict_recovered = pickle.load(g)
                    k.close()
                        
                g.close()
        else:
            print("Could not find the hashing in the file!")
        f.close()
        
   
    return dict_recovered

def unmingle(mingled, db, key, lzma_filters, last=False, First=True):
    i = 0
    Found = False
    packed_mingled = False
    EOF = False
    magic_numbers_dict = read_db(db, key, lzma_filters)
    for magic_number in magic_numbers_dict:
        if magic_number in mingled[len(mingled)-50:]: #50 last bytes
            ###print("UNMINGLE- FOUND MAGIC NUMBER")
            Found = True
            if magic_number[len(magic_number)] == mingled[len(mingled)]: #last byte match
                if magic_number[len(magic_number)-1:] == mingled[len(mingled)-1:]: #last two bytes match
                    #process the unmingling
                    with io.BytesIO(mingled) as m:
                        mingled_file = m.read()
                        m.close()
                        fileinfo = mingled_file.split(b'|fileinfo|')
                        filename = fileinfo[1].decode("ASCII")
                        #print(fileinfo[2])
                        filesize = int(fileinfo[2].decode("ASCII"))
                        #print(filename)
                        #print(filesize)
                        signature = fileinfo[0].split(b'|jordan|')
                        #print(len(signature))
                        length = int(signature[1])
                        #print(length)
                        hashing = signature[0][len(signature[0])-length:]
                        #print(hashing.decode('ASCII'))
                        mingled_bytes_lzma = signature[0][:len(signature[0])-length]
                        bruteforce = True
                        i = 0
                        while bruteforce:
                            try:
                                recovered_mingled = lzma.decompress(mingled_bytes_lzma,format=lzma.FORMAT_RAW, filters=lzma_filters)
                                if recovered_mingled:
                                    bytes_key = bytes(key, 'UTF-8')
                                    h = hmac.new(bytes_key, recovered_mingled, hashlib.sha512)
                                    ###print(h.hexdigest())
                                    if hmac.compare_digest(h.hexdigest(), hashing.decode('ASCII')):
                                        ###print("YEP! RECOVERED!")
                                        bruteforce = False
                                    else:
                                        raise Exception("Almost...")
                                else:
                                    raise Exception("get bruteforced!")
                            except:
                                i = i + 1
                                mingled_bytes_lzma = signature[0][len(signature[0])-filesize-length-i:len(signature[0])-length]#signature[0][len(signature[0])-filesize-length+i:]
                                continue
                        bytes_key = bytes(key, 'UTF-8')
                        h = hmac.new(bytes_key, recovered_mingled, hashlib.sha512)
                        ###print(h.hexdigest())
                        if hmac.compare_digest(h.hexdigest(), hashing.decode('ASCII')):
                            ###print("OK")
                            mingled_bytes_recovered = pickle.loads(recovered_mingled)
                            magic_number = mingled_bytes_recovered[len(mingled_bytes_recovered)-10:] #OK
                            unmingled_bytes = magic_number + mingled_bytes_recovered[:len(mingled_bytes_recovered)-10]
                            ###print(magic_number)
                            #original = unmingled_bytes # OK
                            unmingled = unmingled_bytes
                        else:
                            bruteforce = True
                            i = 0
                            while bruteforce:
                                try:
                                    if not hmac.compare_digest(h.hexdigest(), hashing.decode('ASCII')):
                                        raise Exception("KEEP TRYING!")
                                    else:
                                        bruteforce = False
                                except:
                                    i = i + 1
                                    h = hmac.new(bytes_key, recovered_mingled[len(recovered_mingled)-i:], hashlib.sha512)
                                    if i == len(recovered_mingled):
                                        #print("file is irrecoverable...sorry")
                                        quit()
                                    continue
                            packed_mingled = recovered_mingled[:len(recovered_mingled)-i]
                            recovered_mingled = recovered_mingled[len(recovered_mingled)-i:]
                            ##print("Size=",i)
                            mingled_bytes_recovered = pickle.loads(recovered_mingled)
                            magic_number = mingled_bytes_recovered[len(mingled_bytes_recovered)-10:] #OK
                            unmingled_bytes = magic_number + mingled_bytes_recovered[:len(mingled_bytes_recovered)-10]
                            ###print(magic_number)
                            #original = unmingled_bytes # OK
                            unmingled = unmingled_bytes
  
            #check position of the magic number. THE END.
    if not Found:
            with io.BytesIO(mingled) as m:
                mingled_file = m.read()
                m.close()
                if b'|Jordan_Legare|' in mingled_file:
                    EOF=False
                    last=False
                else:
                    EOF=True
                    last=True
                fileinfo = mingled_file.split(b'|fileinfo|')
                filename = fileinfo[1].decode("ASCII")
                #print(fileinfo[2])
                filesize = int(fileinfo[2].decode("ASCII"))
                #print(filename)
                #print(filesize)
                signature = fileinfo[0].split(b'|jordan|')
                #print(len(signature))
                length = int(signature[1])
                #print(length)
                hashing = signature[0][len(signature[0])-length:]
                #print(hashing.decode('ASCII'))
                mingled_bytes_lzma = signature[0][:len(signature[0])-length]
                
                if b'|Jordan_Legare|' in mingled_file:
                    packet = mingled_file.split(b'|Jordan_Legare|')
                if First:
                    recovered_mingled = lzma.decompress(packet[len(packet)-1], format=lzma.FORMAT_RAW, filters=lzma_filters)
                    bytes_key = bytes(key, 'UTF-8')
                    h = hmac.new(bytes_key, recovered_mingled, hashlib.sha512)
                else:
                    bytes_key = bytes(key, 'UTF-8')
                    if last:
                        h = hmac.new(bytes_key, mingled_bytes_lzma, hashlib.sha512)
                    else:
                        fileinfo = packet[1].split(b'|fileinfo|')
                        filename = fileinfo[1].decode("ASCII")
                        ##print(fileinfo[2])
                        filesize = int(fileinfo[2].decode("ASCII"))
                        ##print(filename)
                        ##print(filesize)
                        signature = fileinfo[0].split(b'|jordan|')
                        ##print(len(signature))
                        length = int(signature[1])
                        ##print(length)
                        hashing = signature[0][len(signature[0])-length:]
                        #print(hashing.decode('ASCII'))
                        mingled_bytes_lzma = signature[0][:len(signature[0])-length]
                        h = hmac.new(bytes_key, mingled_bytes_lzma, hashlib.sha512)
                        
                                 
                ###print(h.hexdigest())
                if hmac.compare_digest(h.hexdigest(), hashing.decode('ASCII')):
                    ###print("OK")
                    if First:
                        mingled_bytes_recovered = pickle.loads(recovered_mingled)
                    else:
                        mingled_bytes_recovered = pickle.loads(mingled_bytes_lzma)
                    magic_number = mingled_bytes_recovered[len(mingled_bytes_recovered)-10:] #OK
                    unmingled_bytes = magic_number + mingled_bytes_recovered[:len(mingled_bytes_recovered)-10]
                    ###print(magic_number)
                    #original = unmingled_bytes # OK
                    unmingled = unmingled_bytes
                    if not last:
                        packed_mingled = lzma.decompress(packet[0], format=lzma.FORMAT_RAW, filters=lzma_filters)
                else:
                    bruteforce = True
                    i = 0
                    while bruteforce:
                        try:
                            if not hmac.compare_digest(h.hexdigest(), hashing.decode('ASCII')):
                                raise Exception("KEEP TRYING!")
                            else:
                                bruteforce = False
                        except:
                            i = i + 1
                            h = hmac.new(bytes_key, recovered_mingled[len(recovered_mingled)-i:], hashlib.sha512)
                            if i == len(recovered_mingled):
                                print("Info: ",filename, " is irrecoverable...sorry")
                                quit()
                            continue
                    
                    packed_mingled = recovered_mingled[:len(recovered_mingled)-i]
                    recovered_mingled = recovered_mingled[len(recovered_mingled)-i:]
                    ##print("Size=",i)
                    mingled_bytes_recovered = pickle.loads(recovered_mingled)
                    magic_number = mingled_bytes_recovered[len(mingled_bytes_recovered)-10:] #OK
                    unmingled_bytes = magic_number + mingled_bytes_recovered[:len(mingled_bytes_recovered)-10]
                    ###print(magic_number)
                    #original = unmingled_bytes # OK
                    unmingled = unmingled_bytes
                        
    ###print(packed_mingled)
                        
    return unmingled, filename, packed_mingled, EOF

def search_filesizes():
    filesizes = []
    for file in listdir():
        try:
            filesizes.append([file,getsize(file)])
        except: #directories
            continue
    return filesizes

def trail(file, db, key, lzma_filters, magic_number=False, mingled=False, tag=False, packaged=False, last=False, arguments=False):
    if mingled:
        if magic_number:
            with io.BytesIO(tag) as m:
                unmingled = m.read()
                m.close()
                magic_number = unmingled[:len(magic_number)] #TODO:check number of bytes
                unmingled = unmingled[len(magic_number):]
                mingled = unmingled + magic_number
                mingled_bytes = pickle.dumps(mingled,protocol=pickle.HIGHEST_PROTOCOL)
                bytes_key = bytes(key, 'UTF-8')
                h = hmac.new(bytes_key, mingled_bytes, hashlib.sha512) #tagged, mingled, pickled
                if packaged:
                    mingled_bytes = packaged + mingled_bytes #encapsulated
                
                length = len(bytes(h.hexdigest(),encoding="UTF-8"))
                if not last:
                    #signature
                    mingled_bytes = mingled_bytes + bytes(h.hexdigest(),encoding="UTF-8")
                    mingled_bytes = mingled_bytes + bytes(b"|jordan|")
                    mingled_bytes = mingled_bytes + bytes(str(length), encoding="UTF-8")
                    mingled_bytes = mingled_bytes + bytes(b'|fileinfo|')
                    mingled_bytes = mingled_bytes + bytes(str(file), encoding="UTF-8")
                    mingled_bytes = mingled_bytes + bytes(b'|fileinfo|')
                    mingled_bytes = mingled_bytes + bytes(str(len(mingled_bytes)), encoding="UTF-8")

                    mingled_bytes_lzma = lzma.compress(mingled_bytes, format=lzma.FORMAT_RAW, check=lzma.CHECK_NONE, filters=lzma_filters)
                    mingled_bytes_lzma = mingled_bytes_lzma + bytes(b'|Jordan_Legare|')
                else:
                    if len(arguments) > 2: #multiple files
                        mingled_bytes_lzma = bytes(b'|Jordan_Legare|')
                        mingled_bytes_lzma = mingled_bytes_lzma + lzma.compress(mingled_bytes, format=lzma.FORMAT_RAW, check=lzma.CHECK_NONE, filters=lzma_filters)
                    else:
                        mingled_bytes_lzma = bytes(b'|Jordan_Legare|') ######REMOVE
                        mingled_bytes_lzma = mingled_bytes_lzma + lzma.compress(mingled_bytes, format=lzma.FORMAT_RAW, check=lzma.CHECK_NONE, filters=lzma_filters)
                    
                    #signature
                    mingled_bytes_lzma = mingled_bytes_lzma + bytes(h.hexdigest(),encoding="UTF-8")
                    mingled_bytes_lzma = mingled_bytes_lzma + bytes(b"|jordan|")
                    mingled_bytes_lzma = mingled_bytes_lzma + bytes(str(length), encoding="UTF-8")
                    mingled_bytes_lzma = mingled_bytes_lzma + bytes(b'|fileinfo|')
                    mingled_bytes_lzma = mingled_bytes_lzma + bytes(str(file), encoding="UTF-8")
                    mingled_bytes_lzma = mingled_bytes_lzma + bytes(b'|fileinfo|')
                    mingled_bytes_lzma = mingled_bytes_lzma + bytes(str(len(mingled_bytes)), encoding="UTF-8")

                                        
                packed = mingled_bytes_lzma

    else:
        if tag:
            with io.BytesIO(tag) as m:
                unmingled = m.read()
                m.close()
                magic_number = unmingled[:10] #10 bytes.
                unmingled = unmingled[10:]
                mingled = unmingled + magic_number
                mingled_bytes = pickle.dumps(mingled,protocol=pickle.HIGHEST_PROTOCOL)
                bytes_key = bytes(key, 'UTF-8')
                h = hmac.new(bytes_key, mingled_bytes, hashlib.sha512) #tagged, mingled, pickled
                if packaged:
                    mingled_bytes = packaged + mingled_bytes #encapsulated
                
                length = len(bytes(h.hexdigest(),encoding="UTF-8"))
                
                if not last:
                    #signature
                    mingled_bytes = mingled_bytes + bytes(h.hexdigest(),encoding="UTF-8")
                    mingled_bytes = mingled_bytes + bytes(b"|jordan|")
                    mingled_bytes = mingled_bytes + bytes(str(length), encoding="UTF-8")
                    mingled_bytes = mingled_bytes + bytes(b'|fileinfo|')
                    mingled_bytes = mingled_bytes + bytes(str(file), encoding="UTF-8")
                    mingled_bytes = mingled_bytes + bytes(b'|fileinfo|')
                    mingled_bytes = mingled_bytes + bytes(str(len(mingled_bytes)), encoding="UTF-8")

                    mingled_bytes_lzma = lzma.compress(mingled_bytes, format=lzma.FORMAT_RAW, check=lzma.CHECK_NONE, filters=lzma_filters)
                    mingled_bytes_lzma = mingled_bytes_lzma + bytes(b'|Jordan_Legare|')
                else:
                    if len(arguments) > 2: #multiple files
                        mingled_bytes_lzma = bytes(b'|Jordan_Legare|')
                        mingled_bytes_lzma = mingled_bytes_lzma + lzma.compress(mingled_bytes, format=lzma.FORMAT_RAW, check=lzma.CHECK_NONE, filters=lzma_filters)
                    else:
                        mingled_bytes_lzma = bytes(b'|Jordan_Legare|') ###REMOVE
                        mingled_bytes_lzma = mingled_bytes_lzma + lzma.compress(mingled_bytes, format=lzma.FORMAT_RAW, check=lzma.CHECK_NONE, filters=lzma_filters)
                    #signature
                    mingled_bytes_lzma = mingled_bytes_lzma + bytes(h.hexdigest(),encoding="UTF-8")
                    mingled_bytes_lzma = mingled_bytes_lzma + bytes(b"|jordan|")
                    mingled_bytes_lzma = mingled_bytes_lzma + bytes(str(length), encoding="UTF-8")
                    mingled_bytes_lzma = mingled_bytes_lzma + bytes(b'|fileinfo|')
                    mingled_bytes_lzma = mingled_bytes_lzma + bytes(str(file), encoding="UTF-8")
                    mingled_bytes_lzma = mingled_bytes_lzma + bytes(b'|fileinfo|')
                    mingled_bytes_lzma = mingled_bytes_lzma + bytes(str(len(mingled_bytes)), encoding="UTF-8")
                    
                packed = mingled_bytes_lzma
            
    return packed #trailling_bytes_lzma

def mingle(magic_numbers_dict, tag):
    i = 0
    for magic_number in magic_numbers_dict:
        if magic_number in tag:
            #Make sure it's found in the first bytes. Confirm Magic number.
            j = 0
            for byte in tag[:len(magic_number)]:
                ###print(byte)
                ###print(tag[:len(magic_number)][j])
                if byte != tag[:len(magic_number)][j]:
                #if ast.literal_eval(byte) != ast.literal_eval(tag[:len(magic_number)][j]):
                    break
                j = j + 1
            if j == len(magic_number):
                ###print(magic_numbers_dict[magic_number], "MAGIC NUMBER, [", magic_number, "] FOUND!")
                mingled = tag[len(magic_number):] #stripped magic number
            else:
                magic_number = False
        i = i + 1
    return mingled, magic_number

def ident_file(tag,db,key,lzma_filters):
    extended = False
    magic_numbers_dict = read_db(db, key, lzma_filters)
    for magic_number in magic_numbers_dict:
        if magic_number in tag:
            extended = magic_numbers_dict[magic_number]
    return magic_numbers_dict, extended

def watermark(file, db, key, lzma_filters, last=False, arguments=False):
    f = open(file,"rb")
    tag = bytes(f.read())
    f.close()
    magic_numbers_dict, extended = ident_file(tag, db, key, lzma_filters)
    if extended:
        ###print("FOUND-->",extended)
        ###print("Stripping magic number!...please wait...")
        mingled, magic_number = mingle(magic_numbers_dict, tag)
        magic_number_lzma = trail(file, db, key, lzma_filters, magic_number=magic_number, mingled=mingled, tag=tag, last=last, arguments=arguments)
    else:
        magic_number_lzma = trail(file, db, key, lzma_filters,tag=tag, last=last, arguments=arguments)
    return magic_number_lzma

def Pack_em(packaged, file, db, key, lzma_filters, last=False, arguments=False):
    f = open(file,"rb")
    tag = bytes(f.read())
    f.close()
    magic_numbers_dict, extended = ident_file(tag, db, key, lzma_filters)
    if extended:
        ###print("FOUND-->",extended)
        ###print("Stripping magic number!...please wait...")
        mingled, magic_number = mingle(magic_numbers_dict, tag)
        magic_number_lzma = trail(file, db, key, lzma_filters, magic_number=magic_number, mingled=mingled, tag=tag, packaged=packaged, last=last, arguments=False)
    else:
        magic_number_lzma = trail(file, db, key, lzma_filters,tag=tag, packaged=packaged, last=last, arguments=arguments)
    return magic_number_lzma
    

def save_recovered_file(filename, unmingled):
    print("Saving...",filename)
    if not exists(filename):
        f = open(filename,"wb")
        f.write(unmingled)
        f.close()
    return filename

def inline_rebuild_files(data, arguments, db, key, lzma_filters):
    if b'|jordan|' in data: #signature
        ##print("File mingled-->", file)
        ##############
        #TODO:find how to know if there is only one file.
        ##############
        if b'|Jordan_Legare|' in data:
            unmingled, filename, packed_mingled, EOF = unmingle(data, db, key, lzma_filters, First=True)
        else:
            unmingled, filename, packed_mingled, EOF = unmingle(data, db, key, lzma_filters, First=False)
        if unmingled:
            save_recovered_file(filename, unmingled)
            while not EOF:
                ##print("EOF=",EOF)
                try:
                    if b'|Jordan_Legare|' in packed_mingled:
                        packet = packed_mingled.split(b'|Jordan_Legare|')
                        for i in range(len(packet)).__reversed__():
                            if len(packet[i]) > 0: #ANYWAY
                                try:
                                    packed_mingled = lzma.decompress(packet[i], format=lzma.FORMAT_RAW, filters=lzma_filters)
                                except:
                                    packed_mingled = packet[i]
                                if b'|jordan|' in packed_mingled:
                                    #print("There is MORE...")
                                    unmingled, filename, packed_mingled, EOF = unmingle(packed_mingled, db, key, lzma_filters, First=False)
                                    save_recovered_file(filename, unmingled)
                    else:
                        if b'|jordan|' in packed_mingled:
                            #print("Last file...")
                            unmingled, filename, packed_mingled, EOF = unmingle(packed_mingled, db, key, lzma_filters, last=True, First=False)
                            save_recovered_file(filename, unmingled)
                        else:
                            EOF = True
                except:
                    if packed_mingled == False:
                        EOF = True, 
                        continue
    else:
        #file is not mingled!
        print("INFO: Payload is NOT mingled.")                
    return False

def rebuild_files(arguments, db, key, lzma_filters):
    i=1
    for file in arguments[1:]:
        packed_mingled = False
        #if i == len(arguments):
        #    last=True
        EOF = False
        if file != "-r":
            ##print(file)
            f = open(file, "rb")
            mingled = f.read()
            unmingled = False
            f.close()
            if b'|jordan|' in mingled: #signature
                ##print("File mingled-->", file)
                ##############
                #TODO:find how to know if there is only one file.
                ##############
                if b'|Jordan_Legare|' in mingled:
                    unmingled, filename, packed_mingled, EOF = unmingle(mingled, db, key, lzma_filters, First=True)
                else:
                    unmingled, filename, packed_mingled, EOF = unmingle(mingled, db, key, lzma_filters, First=False)
                if unmingled:
                    save_recovered_file(filename, unmingled)
                    while not EOF:
                        ##print("EOF=",EOF)
                        try:
                            if b'|Jordan_Legare|' in packed_mingled:
                                packet = packed_mingled.split(b'|Jordan_Legare|')
                                for i in range(len(packet)).__reversed__():
                                    if len(packet[i]) > 0: #ANYWAY
                                        try:
                                            packed_mingled = lzma.decompress(packet[i], format=lzma.FORMAT_RAW, filters=lzma_filters)
                                        except:
                                            packed_mingled = packet[i]
                                        if b'|jordan|' in packed_mingled:
                                            #print("There is MORE...")
                                            unmingled, filename, packed_mingled, EOF = unmingle(packed_mingled, db, key, lzma_filters, First=False)
                                            save_recovered_file(filename, unmingled)
                            else:
                                if b'|jordan|' in packed_mingled:
                                    #print("Last file...")
                                    unmingled, filename, packed_mingled, EOF = unmingle(packed_mingled, db, key, lzma_filters, last=True, First=False)
                                    save_recovered_file(filename, unmingled)
                                else:
                                    EOF = True
                        except:
                            if packed_mingled == False:
                                EOF = True, 
                                continue
            else:
                #file is not mingled!
                print("INFO: File is NOT mingled.")
    return file

Rebuild = False
last=False
arguments = sys.argv

if not sys.stdin.isatty(): #NOT #TODO:CHECK LATER """"NOT"""
    tag = bytes()
    data = sys.stdin.buffer.read()
    #data = bytes() #REMOVE THAT LATER
    
    if len(arguments) >= 2:
        for i in range(1,len(arguments)):
            ###print(sys.argv[i])
            if arguments[i] == "-r":
                Rebuild = True
                data = inline_rebuild_files(data, arguments, db, key, lzma_filters)
                ###print("OK-->REBUILDING FILES!")
                #TODO:REBUILD-FILES!
                break
        if not Rebuild:
            packaged = bytes()
            #watermark the files
            for i in range(1,len(arguments)):
                if i == len(arguments)-1:
                    last = True
                if len(arguments) == 2: #one file to cat
                    ###print("1 file")
                    #quit()
                    packaged = watermark(arguments[i], db, key, lzma_filters, last=last, arguments=arguments)
                else: #multiple files to handle
                    ###print("multiple files")
                    #quit()
                    if i == 1:
                        packaged = watermark(arguments[i], db, key, lzma_filters, last=last, arguments=arguments)
                    else:
                        ##print("")
                        packaged = Pack_em(packaged, arguments[i], db, key, lzma_filters, last=last, arguments=arguments) #encapsulation
            data = data + packaged
    if data:
        sys.stdout.buffer.write(data)
else:
    #data = bytes(sys.stdin.buffer.read())
    
    for i in range(1,len(arguments)):
        if arguments[i] == "-r":
            Rebuild = True
            rebuild_files(arguments, db, key, lzma_filters)
            
    #if not Rebuild:
        #print(_type_)
        #print("INFO: use -r to rebuild. Takes piped information for encoding outputs to STDOUT.")