from tkinter import *
from tkinter import Button, filedialog, messagebox
#import wave
from image_validation import *
from audio_ext_validation import *
import sys
import json
import base64
from requester import file_transferto_api
import tkinter as tk
from enc_dec import *
from img_steg import *
root = Tk()
dest = "C:/Users/kushal/Pictures/encrypic.PNG"
secret_key2 = ""
pathimg1 = ""
pathimg2 = ""
pathaudio1 = ""
pathaudio2 = ""
secret_mgs1 = ""
secret_mgs2 = ""
plaintext1 = ""
plaintext2 = ""


def upload_image1():
    global pathimg1
    pathimg1 = filedialog.askopenfilename(initialdir="Pictures",
                                          title="Select file", filetypes=[("png files", ".png")])


def upload_image2():
    global pathimg2
    pathimg2 = filedialog.askopenfilename(initialdir="Pictures",
                                          title="Select file", filetypes=[("png files", ".png")])

    print("pathimg2")


def upload_audio1():
    global pathaudio1
    pathaudio1 = filedialog.askopenfilename(initialdir="Pictures",
                                            title="Select file", filetypes=[("wave files", ".wav")])


def upload_audio2():
    global pathaudio2
    pathaudio2 = filedialog.askopenfilename(initialdir="Pictures",
                                            title="Select file", filetypes=[("wave files", ".wave")])


def extracter1(pathimg2):
    global secret_mgs1
    secret_key = bytes(in_secret_key2.get(), 'utf-8')
    try:
        if pathimg2 != "":
            print("success")
            if secret_key != "":
                secret_mgs1 = ext_image(pathimg2, secret_key)
                txt_display1.insert(1.0, secret_mgs1)
            else:
                tk.messagebox.showinfo(title="No secret message",
                                       message="Secret message is missing!Please enter your secret")
                print("extraction could not be performed")
        else:
            tk.messagebox.showinfo(title="Missing image file",
                                   message="Please select image file to hide your secret message")
            print("please select image file")
    except:
        pass


def extracter2(pathaudio2):
    global secret_mgs2
    secret_key = bytes(in_secret_key4.get(), 'utf-8')
    try:
        if pathaudio2 != "":
            print("success")
            if secret_key != "":
                secret_mgs2 = ext_from_audio(pathaudio2, secret_key)
                txt_display2.insert(1.0, secret_mgs2)
            else:
                tk.messagebox.showinfo(title="No secret message",
                                       message="Secret message is missing!Please enter your secret key")
                print("extraction could not be performed")
        else:
            tk.messagebox.showinfo(title="Missing audio file",
                                   message="Please select audio file to hide your secret message")
            print("please select audio file")
    except EXCEPTION as e:
        pass


def save_emb_image(enc_img):
    img_dest = filedialog.asksaveasfilename(initialdir="Documents", title="Save file",
                                            defaultextension='.png', filetypes=[("PNG File", ".png")])
    enc_img.save(img_dest)


def save_emb_audio(song, frame_modified):
    audio_dest = filedialog.askopenfilename(initialdir="Documents", title="Select file",
                                            filetypes=[("wave files", ".wave")])
    with wave.open(audio_dest, 'wb') as fd:
        fd.setparams(song.getparams())
        fd.writeframes(frame_modified)


def save_msg(secret_msg):
    try:
        if secret_msg != "":
            save_secret = filedialog.asksaveasfilename(initialdir="Documents", title="Save file",
                                                       defaultextension='.txt', filetypes=[("Text File", ".txt")])
            f = open(save_secret, "x")
            try:
                f.write(secret_msg)
                f.truncate()
            except OSError as e:
                pass
            f = open(save_secret, "w")
            try:
                f.write(secret_msg)
                f.close()
            except OSError as e:
                pass
        else:
            tk.messagebox.showinfo(title="missing extraction",
                                   message="PLease extract message before saving it")
    except:
        pass


def emb_in_img(img_src1):
    secret_key1 = in_secret_key1.get()
    plaintext1 = txt_secret1.get("1.0", END)
    if len(plaintext1) != 1:
        print("success1(no empty box)")
        if img_src1 != "":
            print("success (no empty path name)")
            if secret_key1 != "":
                secret_key = bytes(secret_key1, 'utf')
                img_size = os.path.getsize(img_src1)
                text_size = sys.getsizeof(plaintext1)
                if img_size / 3 >= text_size:
                    try:
                        data_byte = bytes(plaintext1, 'utf-8')
                        enc_dic_img = encrypt(data_byte, secret_key)
                        print(enc_dic_img)
                        cipher_msg_img = json.dumps(enc_dic_img)
                        print("encoded sucessfully")
                        try:
                            en_img = Img_Encoder(img_src1, cipher_msg_img)
                            print(en_img)
                            flag_file = "img_ext"
                            print("data hiding sucessfully")
                            last_window(en_img, flag_file)
                        except:
                            tk.messagebox.askretrycancel(title="Error",
                                                         message="Error while data embedding!Please try again")
                            pass
                    except:
                        print("Problem during encryption")
                        tk.messagebox.showerror(title="Error",
                                                message="Error during encryption!Please try again")
                        pass
                else:
                    tk.messagebox.showinfo(title="Info",
                                           message="Insufficient file size.Please select another image")
                    print("Insufficient file size.Please select another image")
            else:
                tk.messagebox.showinfo(title="Info",
                                       message="Secret key is missing!!!Please enter secret key")
        else:
            tk.messagebox.showinfo(title="Info",
                                   message="Image file is missing!!!Please select Image file")
            print("error2")
    else:
        print("error1")
        tk.messagebox.showinfo(title="Empty Input",
                               message="Secret message field is empty.Please enter message")

# user = db_session.query(User).filter(User.username == username).first()
# uuid = user.uuid


def emb_in_audio(audio_src1):
    plaintext2 = txt_secret2.get("1.0", END)
    secret_key3 = in_secret_key3.get()
    if len(plaintext2) != 1:
        print(len(plaintext2))
        print("success1(no empty box)")
        if audio_src1 != "":
            print("success (no empty path name)")
            if secret_key3 != "":
                secret_key = bytes(secret_key3, 'utf')
                audio_size = os.path.getsize(audio_src1)
                text_size = sys.getsizeof(plaintext2)
                if audio_size / 3 >= text_size:
                    try:
                        data_byte = bytes(plaintext2, 'utf-8')
                        enc_dic_aud = encrypt(data_byte, secret_key)
                        cipher_msg_aud = json.dumps(enc_dic_aud)
                        print("Audio encoded sucessfully")
                        try:
                            en_audio = enc_sound(audio_src1, cipher_msg_aud)
                            flag_file = "audio_ext"
                            print("data hiding sucessfully")
                            last_window(en_audio, flag_file)
                        except:
                            tk.messagebox.askretrycancel(title="Error",
                                                         message="Error while data embedding!Please try again")
                            pass
                    except:
                        print("problem during encryption")
                        tk.messagebox.showerror(title="Error",
                                                message="Error during encryption!Please try again")
                        pass
                else:
                    tk.messagebox.showinfo(title="Info",
                                           message="Insufficient file size.Please select another Audio File")
                    print("Insufficient file size.Please select another image")
            else:
                tk.messagebox.showinfo(title="Info",
                                       message="Secret key is missing!!!Please enter secret key")
        else:
            tk.messagebox.showinfo(title="Error", message="Please select Audio file")
    else:
        tk.messagebox.showinfo(title="Empty Input",
                               message="Secret message field is empty.Please enter secret message")


def file_transfer(file, flag_file, unique_id, username):
    if flag_file == "image":
        pass
        file_name = in_receiver.get() + ".PNG",
        b64_encoder_img = base64.b64encode(file.read())
        file_transferto_api(unique_id, username, file_name, b64_encoder_img)

    else:
        file_name = in_receiver.get() + ".WAV"
        b64_encoder_img = base64.b64encode(file.read())
        file_transferto_api(unique_id, username, file_name, b64_encoder_img)


def last_window(file, flag_file):
    global in_receiver
    lwin = Toplevel()
    lwin.title("Advance hide")
    lwin.geometry("240x180")
    lwin.configure(background="light gray")
    top_frame = LabelFrame(lwin, text="File Transfer", padx=40, pady=10)
    top_frame.configure(background="dim grey")
    top_frame.pack()
    buttom_frame = LabelFrame(lwin, padx=10, pady=10)
    buttom_frame.configure(background="dim gray")
    buttom_frame.pack(pady=5)
    l_receiver = Label(top_frame, text="file name", bg="dim gray")
    l_receiver.pack()
    in_receiver = Entry(top_frame)
    in_receiver.pack()
    b_transfer = Button(top_frame, text="Send", padx=10)
    b_transfer.pack(pady=5)
    b_save = Button(buttom_frame, text="Save", padx=10,
                    command=lambda: [save_emb_image(file)])
    b_save.pack(side=LEFT, padx=5)
    b_back = Button(buttom_frame, text="Back", padx=10, command=lwin.destroy)
    b_back.pack(side=LEFT,padx=10)
    b_exit = Button(buttom_frame, text="Exit", padx=10, command=lwin.destroy)
    b_exit.pack(side=LEFT)


def img_steg_window():
    global txt_display1, frameimg2, txt_secret1, in_secret_key2, in_secret_key1
    iwin = Toplevel()
    iwin.title("Advance hide")
    iwin.geometry("850x400")
    iwin.configure(background="light gray")
    iwin.resizable(width=False, height=False)
    b_exit_img = Button(iwin, text="Exit", command=iwin.destroy, padx=20)
    b_exit_img.pack(side=BOTTOM, pady=5)
    topframe1 = LabelFrame(iwin)
    topframe1.configure(background="dim gray")
    topframe1.pack(anchor=NE)
    b_exit_audio = Button(topframe1, text="Audio", padx=20, command=audio_steg_window)
    b_exit_audio.pack(side=RIGHT)
    b_exit_audio = Button(topframe1, text="Image", padx=20)
    b_exit_audio.pack(side=RIGHT)
    frameimg1 = LabelFrame(iwin, text="Embed in Image File", padx=10, pady=10)
    frameimg1.configure(background="dim gray")
    frameimg1.pack(side=LEFT, padx=10, pady=10)
    l_secret1 = Label(frameimg1, text="Secret Message", bg="dim gray")
    txt_secret1 = Text(frameimg1, width=40, height=10)
    l_secret_key1 = Label(frameimg1, text="Secret Key", bg="dim gray")
    in_secret_key1 = Entry(frameimg1, show="*")
    b_upload_img = Button(frameimg1, text="Choose File", command=upload_image1)
    b_hide_img = Button(frameimg1, text="Embed", command=lambda: [emb_in_img(pathimg1)])

    # shoving it onto the screen
    l_secret1.pack(side=TOP, pady=5)
    txt_secret1.pack(side=TOP, pady=5)
    l_secret_key1.pack(side=LEFT, pady=8, padx=5)
    in_secret_key1.pack(side=LEFT, pady=8)
    b_upload_img.pack(side=TOP, pady=5)
    b_hide_img.pack(side=BOTTOM, padx=5, pady=5)
#frameimg2
    frameimg2 = LabelFrame(iwin, text="Extract from Image File", padx=10, pady=10)
    frameimg2.configure(background="dim gray")
    frameimg2.pack(side=RIGHT, padx=10, pady=10)

    b_save = Button(frameimg2, text="Save", padx=10,
                    command=lambda: [save_msg(secret_mgs1)])
    b_save.pack(side=BOTTOM, padx=5)

    txt_display1 = Text(frameimg2, width=40, height=10)
    txt_display1.pack(side=BOTTOM, anchor=NW, pady=5)

    l_output_msg1 = Label(frameimg2, text="Secret Message", bg="dim gray")
    l_output_msg1.pack(side=BOTTOM, anchor=NW)

    b_upload_img2 = Button(frameimg2, text="Choose File", command=upload_image2)
    b_upload_img2.pack(side=LEFT, padx=10, pady=5)
    print("this is babal")

    l_secret_key2 = Label(frameimg2, text="Secret Key", bg="dim gray")
    in_secret_key2 = Entry(frameimg2, show="*")

    l_secret_key2.pack(side=LEFT, padx=10, pady=5)
    in_secret_key2.pack(side=LEFT, pady=5, padx=10)

    b_extract_img = Button(frameimg2, text="Extract", padx=10,
                           command=lambda: [extracter1(pathimg2)])
    b_extract_img.pack(pady=5, padx=10)


def audio_steg_window():
    global txt_display2, txt_secret2, frame_audio2, in_secret_key4, in_secret_key3
    awin = Toplevel()
    awin.title("Advance hide")
    awin.geometry("850x450")
    awin.configure(background="light gray")
    awin.resizable(width=False, height=False)
    b_exit_audio = Button(awin, text="Exit", command=awin.destroy, padx=20)
    b_exit_audio.pack(side=BOTTOM, pady=5)
    topframe2 = LabelFrame(awin)
    topframe2.configure(background="dim grey")
    topframe2.pack(anchor=NE)
    b_audio = Button(topframe2, text="Audio", padx=20)
    b_audio.pack(side=RIGHT)
    b_img = Button(topframe2, text="Image", padx=20)
    b_img.pack(side=RIGHT)
    frame_audio1 = LabelFrame(awin, text="Embed in Audio File", padx=10, pady=10)
    frame_audio1.configure(background="dim grey")
    frame_audio1.pack(side=LEFT, padx=10, pady=10)
    l_secret3 = Label(frame_audio1, text="Secret Message",bg="dim gray")
    txt_secret2 = Text(frame_audio1, width=40, height=10)
    l_secret_key3 = Label(frame_audio1, text="Secret Key", bg="dim gray")
    in_secret_key3 = Entry(frame_audio1, show="*")
    b_upload_audio1 = Button(frame_audio1, text="Choose File",
                             command=upload_audio1)
    b_save1 = Button(frame_audio1, text="Save", command=save_msg)

    b_hide_audio = Button(frame_audio1, text="Embedded",
                          command=lambda: [emb_in_audio(pathaudio1)])

    # shoving it onto the screen
    l_secret3.pack(side=TOP, pady=5)
    txt_secret2.pack(side=TOP, pady=5)
    l_secret_key3.pack(side=LEFT, pady=8)
    in_secret_key3.pack(side=LEFT, pady=8)
    b_upload_audio1.pack(side=TOP, pady=5)
    # b_save1.grid(row=4, column=1, padx=5, pady=5)
    # b_transfer.grid(row=4, column=2, padx=5, pady=5)
    b_hide_audio.pack(side=BOTTOM, padx=5, pady=5)
    # frame audio 2
    frame_audio2 = LabelFrame(awin, text="Extract from Audio File", padx=10, pady=10)
    frame_audio2.configure(background="dim grey")
    frame_audio2.pack(side=RIGHT, padx=10, pady=10)

    b_save2 = Button(frame_audio2, text="Save", padx=20,
                     command=lambda: [save_msg(secret_mgs2)])
    b_save2.pack(side=BOTTOM, pady=5)
    txt_display2 = Text(frame_audio2, width=40, height=10)
    txt_display2.configure(state='disable')
    txt_display2.pack(side=BOTTOM, anchor=NW)

    l_output_msg2 = Label(frame_audio2, text="Secret Message",
                          pady=10, bg="dim gray")
    l_output_msg2.pack(side=BOTTOM, anchor=NW)

    b_upload_audio2 = Button(frame_audio2, text="Choose File",
                             command=upload_audio2)
    b_upload_audio2.pack(side=LEFT, padx=10, pady=5)

    l_secret_key4 = Label(frame_audio2, text="Secret Key", bg="dim gray")
    in_secret_key4 = Entry(frame_audio2, show="*")

    l_secret_key4.pack(side=LEFT, padx=10, pady=5)
    in_secret_key4.pack(side=LEFT, pady=5, padx=10)

    b_extract_audio = Button(frame_audio2, text="Extract",
                             padx=10, command=lambda: [extracter2(pathaudio2)])
    b_extract_audio.pack(pady=5, padx=10)

#to show the text in the text box
#txt_display1.insert(INSERT,[print(i) for i in ext_img_msg)
#txt_display2.insert(INSERT,[print(i) for i in ext_aud_msg)


btn_test = Button(root, text="trial", command=img_steg_window)
btn_test.pack()

root.mainloop()
