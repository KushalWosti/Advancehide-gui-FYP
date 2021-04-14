import numpy as np
from PIL import Image

def Img_Encoder(source, msg):
    img = Image.open(source, 'r')
    img_width, img_height = img.size
    img_array = np.array(list(img.getdata()))

    if img.mode == 'RGB':
        n = 3
        m = 0
    elif img.mode == 'RGBA':
        n = 4
        m = 1

    total_pixels = img_array.size//n
    msg += "~@$t3g"
    b_msg = ''.join([format(ord(i), "08b") for i in msg])
    req_pixels = len(b_msg)
    index = 0
    for p in range(total_pixels):
        for q in range(m, n):
            if index < req_pixels:
                img_array[p][q] = int(bin(img_array[p][q])[2:9] + b_msg[index], 2)
                index += 1

    img_array = img_array.reshape(img_height, img_width, n)
    enc_img = Image.fromarray(img_array.astype('uint8'), img.mode)
    #enc_img.save(dest)
    print("Image Encoded Successfully")
    return enc_img


def Img_Decoder(src):
    global final_msg
    img = Image.open(src,'r')
    img_array = np.array(list(img.getdata()))

    if img.mode == 'RGB':
        n = 3
        m = 0
    elif img.mode == 'RGBA':
        n = 4
        m = 1

    total_pixels = img_array.size//n

    hidden_bits = ""
    for p in range(total_pixels):
        for q in range(m, n):
            hidden_bits += (bin(img_array[p][q])[2:][-1])

    hidden_bits = [hidden_bits[i:i+8] for i in range(0, len(hidden_bits), 8)]

    msg = ""
    for i in range(len(hidden_bits)):
        if msg[-6:] == "~@$t3g":
            break
        else:
            msg += chr(int(hidden_bits[i], 2))
    if "~@$t3g" in msg:
        final_msg = msg[:-6]
    else:
        print("No Hidden Message Found")
    return final_msg


    #Img_Encoder(img_src, cipher_msg, dest)
    #Img_Decoder(dest)