from euclid import *
import math
def bitmaptoarray(div,array):
    array = array[::-1]
    bitmap = 0b0001;
    encrypted = 0
    for a in array:
        e = div & bitmap
        if e:
            encrypted = encrypted + a
        bitmap = bitmap << 1
    return encrypted

def encrypt(a,m,w,message):
    b = [(w * x)% m for x in a]
    print('Public Key:',b)
    block = 0
    div = []
    for s in message:
        c = ord(s.upper()) - 65
        block = (block<<5) + c
    encrypted_msg = []
    n = len(a)
    mask = 2 ** n - 1
    #print(mask)
    numblocks = math.ceil(len(message)*5/n)
    j = 0
    if len(message)*5 % n:
        j = n - (len(message)*5 % n)
    #print('j',j)
    #print(numblocks)
    for i in range(1, numblocks+1):
        #print(bin(block))
        if i < numblocks:
            div.append((block >> (n*(numblocks-i)-j)) & mask)
        else:
            div.append((block << j) & mask)
        #print('div',bin(div[i-1]))
        encrypted_msg.append(bitmaptoarray(div[i-1], b))
    return encrypted_msg

def arraytobits(array, base):
    a_rev = array[::-1]
    #print(a_rev)
    bits = 0
    if base == 0:
        return 0
    for a in a_rev:
        q = base%a
        if q != base:
            #print('ind: ',a_rev.index(a),bits)
            base = q
            bits = bits + (2 ** a_rev.index(a))
            #print('bits ',bits)
        if q == 0:
            return bits



def decrypt(a,m,w,encrypted_msg):
    #print(encrypted_msg)
    d = [(modinv(w, m)*x)%m for x in encrypted_msg]
    #print(d)
    block = 0
    n = len(a)
    #print(a)
    for x in d:
        k = arraytobits(a,x)
        block = (block<<n) + k
    #print(bin(block))
    decrypted_msg = ""
    j = len(encrypted_msg)-1
    lenmsg = math.floor(len(encrypted_msg)*n/5)
    #print(lenmsg)
    for i in range(1, lenmsg + 1):
        if (len(encrypted_msg)*n)%5 == 0:
            i = 0
        if n*j-i >= 0:
            #print(bin(block>>n*j-i))
            c = block>>n*j-i & 0x001F
        decrypted_msg = decrypted_msg + (str(chr(c + 65)))
        j = j-1
    #print(decrypted_msg)
    return decrypted_msg




if __name__ == '__main__':
    #default values:
    a = [1,2,4,10,20]
    m = 120
    w = 53
    message = "ciao"
    mode = 1
    #a = [1,2,4,27]
    #m = 61
    #w = 17

    from argparse import ArgumentParser

    parser = ArgumentParser(description='Encrypt/Decrypt Message using Public Crypto')
    parser.add_argument('-a', type=int, nargs='+', help='the superincreasing vector', required=False)
    parser.add_argument('-m', type=int, nargs=1, help='modulo value', required=False)
    parser.add_argument('-w', type=int, nargs=1, help='relatively prime to m', required=False)
    parser.add_argument('-mode', type=int, nargs=1, help='1 if Encrypt mode, 0 if Decrypt mode ', required=False)
    parser.add_argument('-message', type=str, nargs=1, help='Message to be encrypted', required=False)
    args = parser.parse_args()
    if args.a:
        a = args.a
    if args.m:
        m = args.m[0]
    if args.w:
        w = args.w[0]
    if args.mode:
        mode = args.mode[0]
    if args.message:
        message = args.message[0]
    print(a[0])
    print(m)
    if m < 2*a[len(a)-1]:
        print('Invalid m')
    if gcd(m, w) != 1:
        print('Invalid w and m pair')
    if modinv(w,m) == 0:
        print("Invalid pair")
    if mode:
        print('Message:', message)
        encrypted_msg = encrypt(a, m, w, message)
        print('cipher: ',encrypted_msg)
        decrypted_msg = decrypt(a, m, w, encrypted_msg)
        print('Decrypted message:',decrypted_msg)
