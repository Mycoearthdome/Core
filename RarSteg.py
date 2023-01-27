#!/usr/bin/python3

import binascii, sys, time, random, os
from binascii import crc32
from rarfile import load_vint
from secrets import token_bytes

def find_crc_end(hdata):
    header_crc = hdata[8:12]
    i = 12
    j = 1000
    crc = crc32(hdata[i:j]).to_bytes(4, byteorder='little')
    while header_crc != crc:
        j = j - 1
        crc = crc32(hdata[i:j]).to_bytes(4, byteorder='little')
        #print(i,"-->", j, "[", header_crc, "-->", crc)

        if j == 0:
            break
    return j

def patch(hdata, padding):

    pos = 0
    end_crc = find_crc_end(hdata)

    magic_number_signature = hdata[:8]
    header_crc = crc32(hdata[12:end_crc])
    header_size, pos = load_vint(hdata, 12)
    header_type, pos = load_vint(hdata, pos)
    header_flags, pos = load_vint(hdata, pos)
    if header_flags == 5:
        extra_area_size, pos = load_vint(hdata, pos)
    header_archive_flags, pos = load_vint(hdata, pos)
    if header_archive_flags == 0: #patching!
        pos = pos - 1
        hdata = hdata[:pos] + b'\x08' + hdata[pos+1:] #recovery record present
        crc = crc32(hdata[12:end_crc]).to_bytes(4, byteorder='little')
        hdata = hdata[:8] + crc + hdata[12:] #crc patched
        #hdata = hdata + bytes(bytearray(8)) #Time field added. NULL bytes.
    extra_area_type, pos = load_vint(hdata, pos)
    locator_size, pos = load_vint(hdata, pos)
    locator_type, pos = load_vint(hdata, pos)
    locator_flags, pos = load_vint(hdata, pos)
    locator_quick_open_offset, pos = load_vint(hdata, pos)
    #moving to Quick Open header
    pos = locator_quick_open_offset + 4 #skipping crc header #TODO:fix the crc after the change.
    quick_open_crc = hdata[locator_quick_open_offset:locator_quick_open_offset + 4]
    quick_open_structure_size, pos = load_vint(hdata, pos)
    pos = pos + quick_open_structure_size - 5
    #quick_open_structure_flags, pos = load_vint(hdata, pos)
    #quick_open_structure_offset, pos = load_vint(hdata, pos)
    #quick_open_structure_data_size, pos = load_vint(hdata, pos)
    #changing data size to reflect the patch.
    #pos = pos - 1
    #hdata = hdata[:pos] + bytes(str(len(hdata[pos:])+len(padding)), encoding="ASCII") + hdata[pos+1:] #data adjusted
    
    #crc = crc32(hdata[locator_quick_open_offset+4:] + padding).to_bytes(4, byteorder='little') #fixing crc -> Structure Size on...
    #hdata = hdata[:locator_quick_open_offset] + crc + hdata[locator_quick_open_offset+4:] #crc patched
    
    return pos + 100 #quick_open_structure_offset + quick_open_structure_data_size + 10 #ADD more if the file get's corrupt!
                            
def encode_RAR(filename, padding):
    ##STEG-IN
    t = open(filename,'rb')
    data = t.read()
    t.close()
    
    position = patch(data, padding)
                        
    footer = bytes(binascii.unhexlify('77565103050400'))
    data2 = data[:position]
    if len(data) > (len(data2) + len(bytearray(random.randint(5,10))) + len(b'|jordan|') + len(padding) + len(footer)):
        #extra padding to avoid corruption
        more = len(data) - (len(data2) + len(b'|jordan|') + len(padding) + len(footer))
        data2 = data2 + token_bytes(more) + b'|jordan|' + padding + footer
    else:
        data2 = data2 + token_bytes(random.randint(5,10)) + b'|jordan|' + padding + footer
    
    filename_out = filename.split(".")[0] + "_OUT_SEND.rar"                   
    t = open(filename_out,"wb")
    t.write(data2)
    t.close()
    
    return data2

def inline_encode_RAR(padding):
    #implement later (Rar in Rar)
    return data2

def inline_decode_RAR(padding):
    footer = bytes(binascii.unhexlify('77565103050400')) #Rar Footer.
    if b'|jordan|' in padding:
        gpg_data = padding.split(b'|jordan|')
        gpg_data = gpg_data[1].split(footer)
        #print(len(gpg_data))
        gpg_data = gpg_data[0]
    else:
        print("ERROR---file impossible to recover")
    return gpg_data


def decode_RAR(filename):
    ###STEG-OUT
    t = open(filename,"rb")
    data = t.read()
    t.close()

    footer = bytes(binascii.unhexlify('77565103050400')) #Rar Footer.
    if not sys.stdin.isatty():
        if b'|jordan|' in data:
            #print("FOUND!")
            gpg_data = data.split(b'|jordan|')
            gpg_data = gpg_data[1].split(footer)
            #print(len(gpg_data))
            gpg_data = gpg_data[0]
        
            #filename_out = filename.split(".")[0] + ".gpg"                            
            #t = open(filename_out,"wb")
            #t.write(gpg_data)
            #t.close()
            
            return gpg_data
    else:
        data2 = bytes()
        if b'|jordan|' in data:
            files = data.split(b'|jordan-file||')[1:]
            for item in files:
                data2 = item.split(b'|>ENCODED<|')
                filename = data2[0].decode()
                data2 = data2[1]
                t = open(filename, "wb")
                t.write(data2)
                t.close()
        else:
            print("ERROR-decoding failed.")
    return True

def check_files_exist(arguments):
    list_files = []
    for i in range(1,len(arguments)):
        if arguments[i] == "-f":
            list_files = arguments[i+2:]
    
    for item in list_files:
        if not os.path.exists(item):
            list_files.remove(item)
            print("File:",item, " not found --> ignoring file")
    
    return list_files

def concatenate(list_files):
    data = bytes()
    
    for item in list_files:
        f = open(item,"rb")
        file_delimiter = b'|jordan-file||' + bytes(item, encoding="ASCII") + b'|>ENCODED<|'
        data = data + file_delimiter + f.read()
        f.close()
    
    return data


arguments = sys.argv

padding = bytes()
data = bytes()
filename = ""
OPTION = ""
list_files = []

if not sys.stdin.isatty():
    padding = bytes(sys.stdin.buffer.read())

if len(arguments) > 1:
    for i in range(1,len(arguments)):
            ###print(sys.argv[i])
            if arguments[i] == "-f":
                filename = arguments[i+1]
                for j in range(1,len(arguments)):
                    if arguments[j] == "e": #ENCODE
                        OPTION = arguments[j]
                    else:
                        if arguments[j] == "d": #DECODE
                            OPTION = arguments[j]
                    
            if arguments[i] == "e":
                OPTION = arguments[i]
            if arguments[i] == "d":
                OPTION = arguments[i]


    if OPTION == "":
        print("Usage: ./RarSteg [OPTIONS] -f RAR_File [File...File]\n\nOPTIONS:\ne --> encode\nd --> decode\n-f RAR_file")
        print("WARNING: Avoid file corruption with adding recovery record to your rar files.")
        quit()
    else:
        if filename:
            if OPTION == "e":
                if padding: #Piped content
                    data = encode_RAR(filename, padding)
                else:
                    list_files = check_files_exist(arguments)
                    if len(list_files) > 0:
                        padding = concatenate(list_files)
                        encode_RAR(filename, padding)
            if OPTION == "d":
                data = decode_RAR(filename)
        
        if not sys.stdin.isatty():
            if OPTION == "e":
                sys.stdout.buffer.write(data)
                #data2 = inline_encode_RAR(padding)
            if OPTION == "d":
                data = inline_decode_RAR(padding)
                sys.stdout.buffer.write(data)
#else:
#    print("Usage: ./RarSteg [OPTIONS] -f RAR_File [File...File]\n\nOPTIONS:\ne --> encode\nd --> decode\n-f RAR_file")
#    print("WARNING: Avoid file corruption with adding recovery record to your rar files.")