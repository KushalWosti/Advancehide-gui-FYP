import sys,json
import tkinter as tk
from tkinter import messagebox
from enc_dec import *
from audio_steg import *

audio_src1 = "C:/Users/kushal/Music/wav.WAV"
dest = "C:/Users/kushal/Music/wav2.WAV"
plaintext2 = "asedcfeda sdada shebdasdlsjdnda"
secret_key3 = b"kushalwosti12345"
pathimg1 = "akzmi"
def emb_in_audio(plaintext2,audio_src1,secret_key3):
    if plaintext2 != "":
        print("success1(no empty box)")
        if pathimg1 != "":
            print("success (no empty path name)")
            audio_size = os.path.getsize(audio_src1)
            text_size = sys.getsizeof(plaintext2)
            if audio_size / 3 >= text_size:
                try:
                    data_byte = bytes(plaintext2, 'utf-8')
                    enc_dic_aud = encrypt(data_byte, secret_key3)
                    cipher_msg_aud = json.dumps(enc_dic_aud)
                    print("Audio encoded sucessfully")
                    try:
                        en_audio = enc_sound(audio_src1, cipher_msg_aud)
                        print("data hiding sucessfully")
                        return en_audio
                    except:
                        tk.messagebox.askretrycancel(title="Error", message="Error while data embedding!Please try again")
                        pass
                except:
                    print("problem during encryption")
                    tk.messagebox.showerror(title="Error", message="Error during encryption!Please try again")
                    pass
            else:
                tk.messagebox.showinfo(title="Info", message="Insufficient file size.Please select another Audio File")
                print("Insufficient file size.Please select another image")
        else:
            tk.messagebox.showinfo(title="Error", message="Please select Audio file")
    else:
        tk.messagebox.showinfo(title="Empty Input", message="Secret message field is empty.Please enter secret message")

emb_in_audio(plaintext2,audio_src1,secret_key3)