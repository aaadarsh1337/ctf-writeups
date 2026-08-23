import base64
import pyshark

key = b'H0t3lSt@ff0NlyK3epS3cr3t!'

"""
Flow:
    1. character is encoded to utf-8
    2. xor is applied to the character
    3. Finally, it is encoded to base64
    
Decryption flow:
    1. Decode the base64
    2. Make it into a list again
    3. Reapply the xor
    4. Decode the char
    
"""

def decode(char):
    decoded = base64.b64decode(char)
    rawchars = list(decoded)

    q = []

    for i in rawchars:
        q.append(i ^ key[rawchars.index(i) % 25])

    return bytes(q).decode()


cap = pyshark.FileCapture('newtraffic.pcapng')

i = 0

l = []

while True:
    try:
        l.append(cap[i]['HTTP'].cookie_pair.removeprefix('hotel_sess_state='))
        i += 1
    except:
        break

for i in l:
    print(decode(i), end='')
