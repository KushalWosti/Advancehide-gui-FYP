from audio_steg import *
from enc_dec import *
import tkinter as tk
from tkinter import messagebox
import json
global original_text
audio_scr2 = "C:/Users/kushal/Music/song_embedded.wav"
secret_key4 = b"kushalwosti12345"


def ext_from_audio(audio_scr2, secret_key4):
    try:
        str_msg_aud = dec_sound(audio_scr2)
        print(str_msg_aud)
        dec_cipher_msg = json.loads(str_msg_aud)
        print("extraction completed")
        try:
            original_text2 = decrypt(dec_cipher_msg, secret_key4)
            print(original_text2)
            return original_text2
        except:
            tk.messagebox.showerror(title="Error", message="Error during decryption process!Please try again")
            pass
    except:
        tk.messagebox.showerror(title="Error", message="Error while data Extraction process!Please try again ")
        pass
