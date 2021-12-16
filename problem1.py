code_key = {
    0:'0',
    1:'1',
    2:'2',
    3:'3',
    4:'4',
    5:'5',
    6:'6',
    7:'7',
    8:'8',
    9:'9',
    10:'A',
    11:'B',
    12:'C',
    13:'D',
    14:'E',
    15:'F'
}

version_number_sum = 0

def equal(arrayOfNum):
    if arrayOfNum[0] == arrayOfNum[1]:
        return 1
    else:
        return 0

def lessThan(arrayOfNum):
    if arrayOfNum[0] < arrayOfNum[1]:
        return 1
    else:
        return 0

def greaterThan(arrayOfNum):
    if arrayOfNum[0] > arrayOfNum[1]:
        return 1
    else:
        return 0

def multiplyList(myList) :
    result = 1
    for x in myList:
         result = result * x
    return result

def parseLiteral(literal):
    last = False
    literal_value = ''
    usedCount = 0

    while not last:
        indicator = literal[usedCount]
        usedCount+=1
        literal_value += literal[usedCount:usedCount+4]
        if indicator == '0' : last=True
        usedCount+=4
    return {'result':int(literal_value,2), 'usedChars':usedCount}

def parseOperator(packet, type):
    usedChars = 0
    length_type_ID = packet[usedChars]
    usedChars+=1
    if length_type_ID == '0':
        length_code = packet[usedChars:usedChars+15]
        length = int(length_code,2)
        usedChars+=15
        tempused = usedChars
        tempStorage = []
        while usedChars != tempused+length:
            result = processPacket(packet[usedChars:usedChars+length])
            usedChars += result['usedChars']
            tempStorage.append(result['result'])
    elif length_type_ID == '1':
        length_code = packet[usedChars:usedChars+11]
        length = int(length_code,2)
        usedChars+=11
        tempStorage = []
        while length != 0:
            result = processPacket(packet[usedChars:])
            usedChars += result['usedChars']
            tempStorage.append(result['result'])
            length -= 1

    if type == 0:
        return {'result':sum(tempStorage), 'usedChars':usedChars}
    elif type == 1:
        return {'result':multiplyList(tempStorage), 'usedChars':usedChars}
    elif type == 2:
        return {'result':min(tempStorage), 'usedChars':usedChars}
    elif type == 3:
        return {'result':max(tempStorage), 'usedChars':usedChars}
    elif type == 5:
        return {'result':greaterThan(tempStorage), 'usedChars':usedChars}
    elif type == 6:
        return {'result':lessThan(tempStorage), 'usedChars':usedChars}
    elif type == 7:
        return {'result':equal(tempStorage), 'usedChars':usedChars}

def processPacket(packet):
    global version_number_sum

    if int(packet,2) == 0:
        return

    packet_version = packet[0:3]
    version_number_sum += int(packet_version,2)
    packet_type_ID = packet[3:6]
    usedChars = 6
    if code_key[int(packet_type_ID,2)] == '4':
        result = parseLiteral(packet[usedChars:])
        usedChars += result['usedChars']
        return {'result':result['result'], 'usedChars':usedChars}
    else:
        result = parseOperator(packet[usedChars:], int(packet_type_ID,2))
        usedChars += result['usedChars']
        return {'result': result['result'], 'usedChars':usedChars}

with open('finaldata.txt') as file:
    for line in file:
        n=2
        hexcodes = [line[i:i+n] for i in range(0,len(line.strip()),n)]

num_of_bits = 8
binary_code = ''
for hexcode in hexcodes:
    binary_code += bin(int(hexcode, 16))[2:].zfill(num_of_bits)

result = processPacket(binary_code)

print('Result: ',result)
print (version_number_sum)