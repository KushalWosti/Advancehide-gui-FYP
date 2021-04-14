import sys, json
import tkinter as tk
from tkinter import messagebox
from enc_dec import *
from img_steg import *
pathimg1 = "akzmi"
img_src2 = "C:/Users/kushal/Pictures/prgressql1.PNG"
img_dest = "C:/Users/kushal/Pictures/encrypic.PNG"
plaintext1 = "asedcfeda sdada shebdasdlsjdnda"
secret_key1 = b"kushal@wosti1234578896"
# open method used to open different extension image file
#secret_key="tom hardy"
#with Image.open("C:/Users/kushal/Pictures/prgressql1.PNG") as img:
def emb_in_img(plaintext1,img_src1,secret_key1):
    if plaintext1 != "":
        print("success1(no empty box)")
        if img_src1 != "":
            print("success (no empty path name)")
            img_size = os.path.getsize(img_src1)
            text_size = sys.getsizeof(plaintext1)
            if img_size / 3 >= text_size:
                try:
                    data_byte = bytes(plaintext1, 'utf-8')
                    enc_dic_img = encrypt(data_byte, secret_key1)
                    print(enc_dic_img)
                    cipher_msg_img = json.dumps(enc_dic_img)
                    print("encoded sucessfully")
                    try:
                        en_img = Img_Encoder(img_src1, cipher_msg_img, img_dest)
                        print("data hiding sucessfully")
                        return en_img
                    except:
                        tk.messagebox.askretrycancel(title="Error", message="Error while data embedding!Please try again")
                        pass
                except:
                    print("Problem during encryption")
                    tk.messagebox.showerror(title="Error", message="Error during encryption!Please try again")
                    pass
            else:
                tk.messagebox.showinfo(title="Info", message="Insufficient file size.Please select another image")
                print("Insufficient file size.Please select another image")
        else:
            tk.messagebox.showinfo(title="Error", message="Please select Image file")
            print("error2")
    else:
        print("error1")
        tk.messagebox.showinfo(title="Empty Input", message="Secret message field is empty.Please enter message")

emb_in_img(plaintext1,img_src2,secret_key1)