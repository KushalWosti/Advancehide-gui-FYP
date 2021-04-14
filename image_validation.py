from img_steg import *
from enc_dec import *
import tkinter as tk
from tkinter import messagebox
import json

#dest = "C:/Users/kushal/Pictures/encrypic.PNG"
#pathimg2 = "aa"
#secret_key2 = b"kushal@wosti1234578896"


def ext_image(pathimg2, secret_key2):
    try:
        str_msg_img = Img_Decoder(pathimg2)
        print(str_msg_img)
        dec_cipher_msg = json.loads(str_msg_img)
        print("extraction completed")
        try:
            original_text = decrypt(dec_cipher_msg, secret_key2)
            return original_text
        except:
            tk.messagebox.showerror(title="Error", message="Error during decryption process!Please try again")
            pass
    except:
        tk.messagebox.showerror(title="Error", message="Error while data Extraction process!Please try again ")
        pass
