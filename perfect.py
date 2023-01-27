#!/usr/bin/python3
from io import BytesIO
import os, progressbar
import sys
#from bitstring import bitarray

list_perfect = []
######################################PERFECT_NUMBERS_131_HEXADECIMAL
list_perfect.append(16777215)
list_perfect.append(520617983)
list_perfect.append(68207251455)
list_perfect.append(76788824063)
list_perfect.append(1112516018047)
list_perfect.append(6649035607967)
list_perfect.append(8280713719327)
list_perfect.append(8754864689183)
list_perfect.append(10954961752175)
list_perfect.append(11086026463151)
list_perfect.append(14406206596943)
list_perfect.append(15514376325007)
list_perfect.append(19951384353719)
list_perfect.append(24379734215575)
list_perfect.append(27708555342695)
list_perfect.append(31028738646983)
list_perfect.append(31028747035591)
list_perfect.append(32136905204551)
list_perfect.append(32141229499207)
list_perfect.append(33245074932615)
list_perfect.append(33249399227271)
list_perfect.append(34357574173447)
list_perfect.append(42110433021339)
list_perfect.append(45439254148459)
list_perfect.append(48759437452747)
list_perfect.append(48759445841355)
list_perfect.append(48763770136011)
list_perfect.append(49867604010315)
list_perfect.append(49871936693579)
list_perfect.append(50975773738379)
list_perfect.append(50980098033035)
list_perfect.append(52088264590603)
list_perfect.append(55401766926771)
list_perfect.append(55412781767091)
list_perfect.append(63169952756067)
list_perfect.append(76459365871197)
list_perfect.append(77567535599261)
list_perfect.append(93081889532629)
list_perfect.append(94190064478805)
list_perfect.append(94194380384853)
list_perfect.append(95298234206869)
list_perfect.append(95302550112917)
list_perfect.append(95324302062229)
list_perfect.append(96406400764437)
list_perfect.append(99735225062053)
list_perfect.append(102006761823429)
list_perfect.append(103055405195845)
list_perfect.append(104163574923909)
list_perfect.append(110812596727001)
list_perfect.append(111529847818585)
list_perfect.append(111920754895961)
list_perfect.append(111920763284569)
list_perfect.append(111925079190617)
list_perfect.append(111925087579225)
list_perfect.append(112630701754777)
list_perfect.append(113028924624025)
list_perfect.append(113028933012633)
list_perfect.append(113033257307289)
list_perfect.append(114137091181593)
list_perfect.append(114137099570201)
list_perfect.append(114141415476249)
list_perfect.append(114141423864857)
list_perfect.append(116357754139753)
list_perfect.append(117465923867817)
list_perfect.append(121894273729673)
list_perfect.append(125223112030321)
list_perfect.append(126331281758385)
list_perfect.append(130759631620241)
list_perfect.append(134088452747361)
list_perfect.append(138516802609217)
list_perfect.append(142958174101438)
list_perfect.append(147386523963294)
list_perfect.append(149464878673950)
list_perfect.append(150715345090414)
list_perfect.append(155143694952270)
list_perfect.append(156251864680334)
list_perfect.append(159580702980982)
list_perfect.append(164009052842838)
list_perfect.append(165117222570902)
list_perfect.append(167333552845798)
list_perfect.append(167333561234406)
list_perfect.append(167337877140454)
list_perfect.append(167337885529062)
list_perfect.append(168441719403366)
list_perfect.append(168446043698022)
list_perfect.append(168446052086630)
list_perfect.append(169549889131430)
list_perfect.append(169549897520038)
list_perfect.append(169554213426086)
list_perfect.append(169554221814694)
list_perfect.append(170662379983654)
list_perfect.append(177311401786746)
list_perfect.append(178419571514810)
list_perfect.append(181739751648602)
list_perfect.append(185068575946218)
list_perfect.append(186172426597738)
list_perfect.append(186176742503786)
list_perfect.append(187280596325802)
list_perfect.append(187284912231850)
list_perfect.append(188393087178026)
list_perfect.append(203907441111394)
list_perfect.append(205015610839458)
list_perfect.append(218305023954588)
list_perfect.append(226062194943564)
list_perfect.append(229386712120052)
list_perfect.append(230494878677620)
list_perfect.append(230499202972276)
list_perfect.append(231603040017076)
list_perfect.append(231607372700340)
list_perfect.append(232711206574644)
list_perfect.append(232715530869300)
list_perfect.append(232715539257908)
list_perfect.append(235627990306196)
list_perfect.append(236035722562196)
list_perfect.append(239364543689316)
list_perfect.append(247117402537208)
list_perfect.append(248225577483384)
list_perfect.append(248229901778040)
list_perfect.append(249333747211448)
list_perfect.append(249338071506104)
list_perfect.append(250446229675064)
list_perfect.append(250446238063672)
list_perfect.append(253766421367960)
list_perfect.append(257095242495080)
list_perfect.append(261523592356936)
list_perfect.append(265960600385648)
list_perfect.append(267068770113712)
list_perfect.append(270388950247504)
list_perfect.append(272678900465632)
list_perfect.append(274825941102688)
list_perfect.append(280362460692608)


def Check_Missing(list_perfect, list_48, list_combo, byte, check=True, seek=False):
    i = 0
    j = 0
    length = 8
    l = 0
    find = []
    found = True
    String2 = ""
    blocks = 48 #27 and up
    Transform = ""
    #list_combo = []
    #list_48 = [''.join(list_char[i:i+6]) for i in range(0,len(list_char))]
    #list_48 = [bin(list_perfect[i])[2:].zfill(48) for i in range(0,len(list_perfect))]
    #list_48 = [list_48[i:i+8] for i in range(0,len(list_48))]
    
    #list_combo = [list_perfect[i:i+8] for i in range(0,len(list_perfect))]
    list_parallel_combo = []
    parallel_item = 0
    parallel_block = 0
    
    list_sin = []
    for item in list_48:
        for j in range(0,blocks):
            try:
                Transform = Transform + item[0][j]
                Transform = Transform + item[1][j]
                Transform = Transform + item[2][j]
                Transform = Transform + item[3][j]
                Transform = Transform + item[4][j]
                Transform = Transform + item[5][j]
                Transform = Transform + item[6][j]
                Transform = Transform + item[7][j]
                list_sin.append(Transform)
                if seek:
                    if bin(int(byte, base=16))[2:].zfill(8) == Transform:
                        list_parallel_combo.append([parallel_item,parallel_block,list_combo[parallel_item]])
                parallel_block = parallel_block + 1
                Transform = ""
                Transform = Transform + item[8][j] #BUG.
            except:
                    continue #BUG fix.
        parallel_item = parallel_item + 1
        parallel_block = 0
    list_48 = []
    list_48 = ["".join(list_sin[i:i+6]) for i in range(0,len(list_sin))]

    for segment in list_48:
        if len(segment) == 48: #BUG
            for i in range(0,int(len(segment)/2)+1):
                if segment[i] != segment[len(segment)-1-i]:
                    l = l + 1
            if l > 0: #adjust this for more results.....
                #print(l)
                if segment not in find:
                    find.append(segment)
            l = 0

    find.sort()
    list_sin2 = []
    #for item in find:
    #    print(int(item, base=2))


    for item in find:
        Transform = ""
        for j in range(0,blocks):
            try:
                Transform = Transform + item[0][j]
                Transform = Transform + item[1][j]
                Transform = Transform + item[2][j]
                Transform = Transform + item[3][j]
                Transform = Transform + item[4][j]
                Transform = Transform + item[5][j]
                Transform = Transform + item[6][j]
                Transform = Transform + item[7][j]
                if Transform not in list_sin2:
                    list_sin2.append(Transform)
                Transform = ""
                Transform = Transform + item[8][j] #BUG.
            except:
                continue #BUG fix.
    i = 0
    dict_bytes = {}
    for i in range(0,256):
        dict_bytes.update({hex(i)[2:]:False})
        

    for item in list_sin2:
        i = i + 1
        if hex(int(item, base=2))[2:] in dict_bytes:
            dict_bytes[hex(int(item, base=2))[2:]] = True

    #Misssing... 
    m = 0       
    for i in range(0,256):
        if dict_bytes[hex(i)[2:]] == False:
            m = m + 1
            print(hex(i)[2:])
            
    if check == True:        
        return m
    else:
        return list_parallel_combo
    
def Find_byte(list_perfect, list_48, list_combo, dict_blocks, byte):
    j = 0
    length = 8
    blocks = dict_blocks[int(byte,base=16)] #27 and up
    Transform = ""
    #list_combo = []
    #list_48 = [''.join(list_char[i:i+6]) for i in range(0,len(list_char))]
    #list_48 = [bin(list_perfect[i])[2:].zfill(48) for i in range(0,len(list_perfect))]
    #list_48 = [list_48[i:i+8] for i in range(0,len(list_48))]
    
    #list_combo = [list_perfect[i:i+8] for i in range(0,len(list_perfect))]
    list_parallel_combo = []
    parallel_item = 0
    parallel_block = 0
    Found = False

    for item in list_48:
        try:
            Transform = ""
            Transform = Transform + item[0][blocks]
            Transform = Transform + item[1][blocks]
            Transform = Transform + item[2][blocks]
            Transform = Transform + item[3][blocks]
            Transform = Transform + item[4][blocks]
            Transform = Transform + item[5][blocks]
            Transform = Transform + item[6][blocks]
            Transform = Transform + item[7][blocks]
            if bin(int(byte, base=16))[2:].zfill(8) == Transform:
                list_parallel_combo.append([parallel_item,blocks,list_48[parallel_item]])
                Found = True
                break
            parallel_block = parallel_block + 1
            #Transform = ""
            #Transform = Transform + item[8][j] #BUG.
        except:
            if not Found:
                raise #BUG fix.
            else:
                Found = False
                break
        parallel_item = parallel_item + 1
        if Found:
            Found = False
            break
        
    
    return list_parallel_combo

def Encode(list_combo_byte, byte):
    
    #blocks = 27
    
    list_48 = [list_combo_byte[0][2][i] for i in range(0,8)]
    
    parallel_block = bin(list_combo_byte[0][1])[2:].zfill(8)
    
    encoded = "".join(list_48) + parallel_block
    
    return int(encoded, base=2).to_bytes(56, byteorder='big')

def Decode(encoded_bytes):
    blocks = 27
    number_block = 8
    parallel_block = 8
    length = blocks * number_block + parallel_block
    list_48 = []
    
    binary_string = "{:56b}".format(int(encoded_bytes.hex(),16)).zfill(392)
    
    
    #print(binary_string)
    ############STRUCT
    list_48.append(binary_string[0:48])
    list_48.append(binary_string[48:96])
    list_48.append(binary_string[96:144])
    list_48.append(binary_string[144:192])
    list_48.append(binary_string[192:240])
    list_48.append(binary_string[240:288])
    list_48.append(binary_string[288:336])
    list_48.append(binary_string[336:384])
    parallel_block = int(binary_string[384:392],base=2)
    ############STRUCT
    
    #print(list_48)
    #print(len(list_48[0]))
    #print(parallel_block)        
    
    Transform = ""
    
    Transform = Transform + list_48[0][parallel_block]
    Transform = Transform + list_48[1][parallel_block]
    Transform = Transform + list_48[2][parallel_block]
    Transform = Transform + list_48[3][parallel_block]
    Transform = Transform + list_48[4][parallel_block]
    Transform = Transform + list_48[5][parallel_block]
    Transform = Transform + list_48[6][parallel_block]
    Transform = Transform + list_48[7][parallel_block]
    
    #print(Transform)
    
    return int(Transform, base=2).to_bytes(1, byteorder="big")


def Encode_File(filename, list_perfect, list_48, list_combo, dict_blocks):
    i = 0
    if os.path.exists(filename):
        filesize = os.path.getsize(filename)
        out_filename = filename.split(".")[0] + ".enc"
        f = open(filename, 'rb')
        g = open(out_filename, "wb")
        with progressbar.ProgressBar(max_value=filesize) as bar:
            while True:
                byte = f.read(1)
                if i != filesize: # not EOF
                    byte = byte.hex()
                    #if not Check_Missing(list_perfect, list_48, list_combo, byte): #in case encoding becomes an issue. leave this one.
                    list_combo_byte = Find_byte(list_perfect, list_48, list_combo, dict_blocks, byte)
                    encoded_byte = Encode(list_combo_byte,byte)
                    g.write(encoded_byte)
                    #else:
                    #    raise
                else:
                    break
                i = i + 1
                bar.update(i)
        g.close()
        f.close()
    return True

def Decode_File(filename, list_perfect):
    i = 0
    if os.path.exists(filename):
        filesize = os.path.getsize(filename)
        out_filename = filename.split(".")[0]+".decoded"
        f = open(filename, 'rb')
        g = open(out_filename, "wb")
        with progressbar.ProgressBar(max_value=filesize) as bar:
            while True:
                bytes_read = f.read(56)
                if i != filesize: # not EOF
                    decoded_bytes = Decode(bytes_read)
                    g.write(decoded_bytes)
                else:
                    break
                i = i + 56
                bar.update(i)
        g.close()
        f.close()
    return True

def New_Perfect_Numbers(list_48, list_combo):
    j = 0
    length = 8
    blocks = 48 #27 and up
    dict_blocks = {}
    Transform = ""
    #list_combo = []
    #list_48 = [''.join(list_char[i:i+6]) for i in range(0,len(list_char))]
    #list_48 = [bin(list_perfect[i])[2:].zfill(48) for i in range(0,len(list_perfect))]
    #list_48 = [list_48[i:i+8] for i in range(0,len(list_48))]
    
    #list_combo = [list_perfect[i:i+8] for i in range(0,len(list_perfect))]
    list_parallel_combo = []
    parallel_item = 0
    parallel_block = 0
    Found = False

    for FF in range(0,256):
        for item in list_48:
            for j in range(0,blocks):
                try:
                    Transform = ""
                    Transform = Transform + item[0][j]
                    Transform = Transform + item[1][j]
                    Transform = Transform + item[2][j]
                    Transform = Transform + item[3][j]
                    Transform = Transform + item[4][j]
                    Transform = Transform + item[5][j]
                    Transform = Transform + item[6][j]
                    Transform = Transform + item[7][j]
                    if bin(FF)[2:].zfill(8) == Transform:
                        list_parallel_combo.append([parallel_item,parallel_block,list_combo[parallel_item]])
                        if FF not in dict_blocks:
                            dict_blocks.update({FF:parallel_block})
                        #print(FF,"-->",list_combo[parallel_item])
                        Found = True
                        break
                    parallel_block = parallel_block + 1
                    #Transform = ""
                    #Transform = Transform + item[8][j] #BUG.
                except:
                    if not Found:
                        raise #BUG fix.
                    else:
                        Found = False
                        break
            #print(parallel_block)
            parallel_block = 0
            parallel_item = parallel_item + 1
            if Found:
                Found = False
                break
        parallel_item = 0
    return list_parallel_combo, dict_blocks

def inline_crypt(data, list_perfect, list_48, list_combo, dict_blocks):
    f = BytesIO(data)
    encoded_data_output = bytes()
    data2 = f.read()
    f.close()
    i = 0
    while i < len(data2): #EOF
        byte = hex(data2[i])[2:]
        list_combo_byte = Find_byte(list_perfect, list_48, list_combo, dict_blocks, byte)
        encoded_data_output = encoded_data_output + Encode(list_combo_byte,byte)
        i = i + 1
    return encoded_data_output

def inline_decrypt(data):
    f = BytesIO(data)
    decoded_bytes = bytes()
    data2 = f.read()
    f.close()
    i = 0
    while i < len(data2): #EOF
        bytes_read = data2[i:i+56]
        decoded_bytes = decoded_bytes + Decode(bytes_read)
        i = i + 56
    return decoded_bytes


arguments = sys.argv

data = bytes()
filename = ""
OPTION = ""
list_files = []


#GLOBALS
list_48 = [bin(list_perfect[i])[2:].zfill(48) for i in range(0,len(list_perfect))]
list_48 = [list_48[i:i+8] for i in range(0,len(list_48))]
    
list_combo = [list_perfect[i:i+8] for i in range(0,len(list_perfect))]

#INITIALIZE:
list_perfect = []
list_combo, dict_blocks = New_Perfect_Numbers(list_48, list_combo)
for combo in list_combo:
    for pn in combo[2]:
        if pn not in list_perfect:
            list_perfect.append(pn)
            
list_combo_bin = []
list_combo_bin_temp = []
i = 0
for combo in list_combo:
    for j in range(0, len(combo[2])):
        list_combo_bin.append(bin(list_combo[i][2][j])[2:].zfill(48))
    list_combo_bin_temp.append(list_combo_bin)
    list_combo_bin=[]
    i = i + 1

list_48 = list_combo_bin_temp

#ADJUSTED
#list_48 = [bin(list_perfect[i])[2:].zfill(48) for i in range(0,len(list_perfect))]
#list_48 = [list_48[i:i+8] for i in range(0,len(list_48))]
list_48 = list_combo_bin_temp

list_combo = [i for i in range(0,len(list_48))]

#####TEST
#for i in range(0,256):
#    Check_Missing(list_perfect, list_48, list_combo, str(i))
#    print(i)
#quit()
######PASSED

if not sys.stdin.isatty():
    data = bytes(sys.stdin.buffer.read())

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
        print("Usage: ./Perfect.py [OPTIONS] -f File \n\nOPTIONS:\ne --> encode\nd --> decode")
        print("Perfect accepts piped information.")
        quit()
    else:
        if filename:
            if OPTION == "e":
                if data: #Piped content
                    data2 = inline_crypt(data, list_perfect, list_48, list_combo, dict_blocks)
                else:
                    Encode_File(filename, list_perfect, list_48, list_combo, dict_blocks)
            if OPTION == "d":
                if data: #piped content
                    data2 = inline_decrypt(data)
                else:
                    Decode_File(filename, list_perfect)
        if data:
            if not sys.stdin.isatty():
                if OPTION == "e":
                    data2 = inline_crypt(data, list_perfect, list_48, list_combo, dict_blocks)
                if OPTION == "d":
                    data2 = inline_decrypt(data)
                        
                sys.stdout.buffer.write(data2)
#else:
#    print("Usage: ./Perfect.py [OPTIONS] -f File \n\nOPTIONS:\ne --> encode\nd --> decode")
#    print("Perfect accepts piped information.")