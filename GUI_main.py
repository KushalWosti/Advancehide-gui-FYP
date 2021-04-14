from tkinter import *
from tkinter import ttk, messagebox, Button, filedialog
from uuid import uuid4
from requester import *
from my_database import *
from tkinter import *
from image_validation import *
from audio_ext_validation import *
import sys
import os
import io
import json
import base64, re
import tkinter as tk
from enc_dec import *
from img_steg import *


regex = '^(\w|\.|\_|\-)+[@](\w|\_|\-|\.)+[.]\w{2,3}$'
Pattern = re.compile("[9][8][0-9]{8}")
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
username = ""
uuid = ""


def user_activate():
    selected = tv.selection()
    for record in selected:
        values = tv.item(record, 'values')
        username = values[1]
        # values[5] = True
        qry_activate_user(username)
        # tv.delete(record)
        print("hello")

    items = tv.selection()
    # print(items())
    for record in items:
        print("")

def remove_admin():
    selected = tv.selection()
    for record in selected:
        values = tv.item(record, 'values')
        username = values[1]
        # values[5] = True
        qry_remove_admin(username)
        # tv.delete(record)
        print("hello")

    items = tv.selection()
    # print(items())
    for record in items:
        print("")


def remove_user():
    selected = tv.selection()
    for record in selected:
        print(record)
        values = tv.item(record, 'values')
        username = values[1]
        qry_remove_user(username)
        tv.delete(record)
        print("hello")


def add_admin():
    selected = tv.selection()
    for record in selected:
        values = tv.item(record, 'values')
        username = values[1]
        #values[5] = True
        qry_add_admin(username)
        #tv.delete(record)
        print("hello")

    items = tv.selection()
    #print(items())
    for record in items:
        print("")


def clear_sign_up():
    input_fullname.delete(0, END)
    input_email.delete(0, END)
    input_phone_num.delete(0, END)
    input_username.delete(0, END)
    input_password.delete(0, END)
    input_con_password.delete(0, END)
    pass


def clear_sign_in():
    try:
        input_username.delete(0, END)
        input_password.delete(0, END)
    except:
        pass
def upload_image1():
    global pathimg1
    pathimg1 = filedialog.askopenfilename(initialdir="Pictures",
                                          title="Select file", filetypes=[("png files", ".png")])


def upload_image2():
    global pathimg2
    pathimg2 = filedialog.askopenfilename(initialdir="Pictures",
                                          title="Select file", filetypes=[("png files", ".png")])


def upload_audio1():
    global pathaudio1
    pathaudio1 = filedialog.askopenfilename(initialdir="Music",
                                            title="Select file", filetypes=[("wave files", ".wav")])


def upload_audio2():
    global pathaudio2
    pathaudio2 = filedialog.askopenfilename(initialdir="Music",
                                            title="Select file", filetypes=[("wave files", ".wav")])


def extracter1(pathimg2):
    global secret_mgs1
    secret_key = bytes(in_secret_key2.get(), 'utf-8')
    try:
        if pathimg2 != "":
            if secret_key != "":
                secret_mgs1 = ext_image(pathimg2, secret_key)
                txt_display1.insert(1.0, secret_mgs1)
            else:
                tk.messagebox.showinfo(title="No secret key",
                                       message="Secret key is missing!Please enter your secret")

        else:
            tk.messagebox.showinfo(title="Missing image file",
                                   message="Please select image file for hiding secret message")
    except:
        pass


def extracter2(pathaudio2):
    global secret_mgs2
    secret_key = bytes(in_secret_key4.get(), 'utf-8')
    try:
        if pathaudio2 != "":
            if secret_key != "":
                secret_mgs2 = ext_from_audio(pathaudio2, secret_key)
                txt_display2.insert(1.0, secret_mgs2)
            else:
                tk.messagebox.showinfo(title="Missing secret key",
                                       message="Secret key is missing!Please enter your secret key")
        else:
            tk.messagebox.showinfo(title="Missing audio file",
                                   message="Please select audio file for hiding the secret message")
    except EXCEPTION as e:
        tk.messagebox.showinfo(title="no secret message",
                               message="audio file does not contain secret message or secret key is invalid ")
        pass


def save_emb_image(enc_img):
    img_dest = filedialog.asksaveasfilename(initialdir="Documents", title="Save file",
                                            defaultextension='.png', filetypes=[("PNG File", ".png")])
    enc_img.save(img_dest)


def save_emb_audio(song, frame_modified):
    audio_dest = filedialog.asksaveasfilename(initialdir="Documents", title="Select file",
                                            defaultextension='.wav', filetypes=[("wave files", ".wav")])
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
        if img_src1 != "":
            if secret_key1 != "":
                secret_key = bytes(secret_key1, 'utf')
                img_size = os.path.getsize(img_src1)
                text_size = sys.getsizeof(plaintext1)
                if img_size / 3 >= text_size:
                    try:
                        data_byte = bytes(plaintext1, 'utf-8')
                        enc_dic_img = encrypt(data_byte, secret_key)
                        cipher_msg_img = json.dumps(enc_dic_img)
                        try:
                            en_img = Img_Encoder(img_src1, cipher_msg_img)
                            flag_file = "image"
                            print("data hiding sucessfully")
                            last_window(en_img, flag_file)
                        except:
                            tk.messagebox.askretrycancel(title="Error",
                                                         message="Error while data embedding!Please try again")
                            pass
                    except:
                        tk.messagebox.showerror(title="Error",
                                                message="Error during encryption!Please try again")
                        pass
                else:
                    tk.messagebox.showinfo(title="Info",
                                           message="Insufficient file size.Please select another image")
            else:
                tk.messagebox.showinfo(title="Info",
                                       message="Secret key is missing!!!Please enter secret key")
        else:
            tk.messagebox.showinfo(title="Info",
                                   message="Image file is missing!!!Please select Image file")
    else:
        tk.messagebox.showinfo(title="Empty Input",
                               message="Secret message field is empty.Please enter message")


def emb_in_audio(audio_src1):
    global frame_modified
    plaintext2 = txt_secret2.get("1.0", END)
    secret_key3 = in_secret_key3.get()
    if len(plaintext2) != 1:
        if audio_src1 != "":
            if secret_key3 != "":
                secret_key = bytes(secret_key3, 'utf')
                audio_size = os.path.getsize(audio_src1)
                text_size = sys.getsizeof(plaintext2)
                if audio_size / 3 >= text_size:
                    try:
                        data_byte = bytes(plaintext2, 'utf-8')
                        enc_dic_aud = encrypt(data_byte, secret_key)
                        cipher_msg_aud = json.dumps(enc_dic_aud)
                        try:
                            en_audio, frame_modified = enc_sound(audio_src1, cipher_msg_aud)
                            flag_file = "audio_ext"
                            last_window(en_audio, flag_file)
                        except:
                            tk.messagebox.askretrycancel(title="Error",
                                                         message="Error while data embedding!Please try again")
                            pass
                    except:
                        tk.messagebox.showerror(title="Error",
                                                message="Error during encryption!Please try again")
                        pass
                else:
                    tk.messagebox.showinfo(title="Info",
                                           message="Insufficient file size.Please select another Audio File")
            else:
                tk.messagebox.showinfo(title="Info",
                                       message="Secret key is missing!!!Please enter secret key")
        else:
            tk.messagebox.showinfo(title="Error", message="Please select Audio file")
    else:
        tk.messagebox.showinfo(title="Empty Input",
                               message="Secret message field is empty.Please enter secret message")


def file_transfer(file, flag_file, unique_id, username):
    file_name = in_receiver.get()
    if file_name != "":
        if flag_file == "image":
            buf = io.BytesIO()
            file.save(buf, format='PNG')
            byte_im = buf.getvalue()
            b64_encoder_img = base64.b64encode(byte_im).decode('utf-8')
            file_name = file_name+".png"
            file_transferto_api(unique_id, username, file_name, b64_encoder_img)
        else:
            file_name = file_name + ".wav"
            with wave.open("encode_audio.wav", 'wb') as fd:
                fd.setparams(file.getparams())
                fd.writeframes(frame_modified)
            b64_encoder1 = open("encode_audio.wav", "rb").read()
            b64_encoder_audio = base64.b64encode(b64_encoder1).decode('utf-8')
            file_transferto_api(unique_id, username, file_name, b64_encoder_audio)
            os.remove("encode_audio.wav")
    else:
        try:
            root.messagebox.showinfo(title="Name missing",
                                   message="Please specify name to transfer image file")
        except:
            pass



def check_sign_up():
    unique_uuid = uuid4()
    unique_uuid = str(unique_uuid)
    s_fullname = input_fullname.get()
    s_email = input_email.get()
    s_phone_num = input_phone_num.get()
    s_username = in_username.get()
    s_password = in_password.get()
    s_gender = gender_choosen.get()
    s_password2 = input_con_password.get()
    if s_fullname != "" and s_email != "" and s_phone_num != "" and s_username != "" \
            and s_password != "" and s_password2 != "":
        if s_gender == "Male" or s_gender == "Female" or s_gender == "Other":
            if re.search(regex, s_email):
                if Pattern.match(s_phone_num):
                    if s_password == s_password2:
                        try:
                            add_user = {"uuid": unique_uuid, "full_name": s_fullname, "email": s_email,
                                        "phone_num": s_phone_num, "gender": s_gender,
                                        "username": s_username, "password": s_password2}
                            createUserToApi(unique_uuid, s_username)
                            sign_up(add_user)
                            messagebox.showinfo(title="Account created ",
                                                message="User account created sucessfully")
                            top.destroy()
                        except Exception as e:
                            messagebox.showinfo(title="Error ",
                                                message="Username already exist!! Please try with different user name")
                            pass
                    else:
                        messagebox.showinfo(title="Invalid Input ",
                                            message="Password and confirm password does not match!! Please try again")
                else:
                    messagebox.showinfo(title="Invalid Input ",
                                        message="Invalid phone number!! Please enter valid Phone number")
            else:
                messagebox.showinfo(title="Invalid Input ",
                                    message="Invalid email address!! Please enter your valid email address")
        else:
            messagebox.showinfo(title="Invalid Input ",
                                message="Missing Gender!! Please select your gender")
    else:
        messagebox.showinfo(title="Invalid Input ",
                            message="Empty field found!Field cannot be empty")
    pass


def check_sign_in():
    global unique_id, username
    username = input_username.get()
    password = input_password.get()
    if username == "" and password == "":
        messagebox.showinfo(title="Invalid Input ",
                            message="Password and Username is missing!! Please enter Username and Password")
    elif username == "":
        messagebox.showinfo(title="Invalid Input ",
                            message="Username is missing!Please enter Username")
    elif password == "":
        messagebox.showinfo(title="Invalid Input ",
                            message="Password is missing!Please enter Password")
    else:
        try:
            response = qry_sign_in(username, password)
            sign_in_bool = response.get("sign_in")
            is_admin_bool = response.get("is_admin")
            unique_id = response.get("uid")
            if sign_in_bool and is_admin_bool:
                flag = "admin"
                clear_sign_in()
                root.destroy()
                img_steg_window(username, flag, unique_id)

                pass
            elif sign_in_bool and not is_admin_bool:
                flag = "not_admin"
                root.destroy()
                img_steg_window(username, flag, unique_id)

                pass
            else:
                clear_sign_in()
                messagebox.showinfo(title="incorrect credential",
                                    message="Enter valid Username or Password!! Please try again")
                pass
        except:
            clear_sign_in()
            messagebox.showinfo(title="incorrect credential",
                                message="error during sign in!! Please try again")
            pass


def login_window():
    global input_username, input_password, root
    root = Tk()
    root.title("Advance hide")
    root.geometry("500x500")
    root.configure(background="SpringGreen4")
    # Creating lable widget
    heading = Label(root, text="Welcome to Advance hide", bg="SpringGreen4")
    heading.pack(pady=50)
    first_frame = LabelFrame(root, text="Sign In", padx=20)
    first_frame.configure(background="dim gray")
    first_frame.pack()
    inner_frame = LabelFrame(first_frame, padx=20, pady=20)
    inner_frame.configure(background="dim gray")
    inner_frame.pack(pady=30)
    l_username = Label(inner_frame, text="Username", bg="dim gray")
    l_password = Label(inner_frame, text="Password", bg="dim gray")
    input_username = Entry(inner_frame, borderwidth=2)
    input_password = Entry(inner_frame, borderwidth=2, show='*')

    # shoving it onto the screen
    l_username.grid(row=1, column=1)
    input_username.grid(row=2, column=1, padx=30, pady=5)
    l_password.grid(row=3, column=1, padx=30)
    input_password.grid(row=4, column=1, pady=10)
    # creating button
    b_sign_in = Button(inner_frame, text="Sign In", padx=30, command=lambda: [check_sign_in()])
    b_sign_in.grid(row=5, column=1)
    b_sign_up = Button(first_frame, text="Create Account", padx=15, command=signup_window)
    b_exit = Button(first_frame, text="Exit", padx=20, command=root.destroy)
    b_sign_up.pack(side=LEFT, padx=10, pady=5)
    b_exit.pack(side=LEFT, padx=10, pady=5)

    root.mainloop()


def signup_window():
    global input_fullname, input_email, input_phone_num, in_username, in_password, input_con_password, gender_choosen, top
    top = Toplevel()
    top.title("Advance hide")
    top.geometry("500x500")
    top.configure(background="SpringGreen4")
    l_welcome = Label(top, text="Welcome to Advance hide", bg="SpringGreen4")
    l_welcome.pack(pady=30)
    first_frame = LabelFrame(top, text="User Details", padx=30, pady=20)
    first_frame.configure(background="dim gray")
    first_frame.pack()
    input_fullname = Entry(first_frame)
    input_email = Entry(first_frame)
    input_phone_num = Entry(first_frame)
    in_username = Entry(first_frame)
    in_password = Entry(first_frame, show='*')
    input_con_password = Entry(first_frame, show='*')

    l_fullname = Label(first_frame, text="Full Name", bg="dim gray")
    l_email = Label(first_frame, text="Email Address", bg="dim gray")
    l_phone_num = Label(first_frame, text="Phone Number", bg="dim gray")
    l_gender = Label(first_frame, text="Gender", bg="dim gray")
    l_username = Label(first_frame, text="Username", bg="dim gray")
    l_password = Label(first_frame, text="Password", bg="dim gray")
    l_con_password = Label(first_frame, text="Confirm Password", bg="dim gray")
    b_exit = Button(first_frame, text="Exit", padx=30, command=root.destroy)
    b_back = Button(first_frame, text="back", padx=30,command=top.destroy)
    b_sign_up = Button(first_frame, text="Create Account", padx=20,
                       command=lambda: [check_sign_up(), clear_sign_up()])

    # shoving it onto the screen

    l_fullname.grid(row=1, column=6, pady=5)
    input_fullname.grid(row=1, column=7, pady=5)
    l_email.grid(row=2, column=6, pady=5)
    input_email.grid(row=2, column=7, pady=5)
    l_phone_num.grid(row=3, column=6, pady=5)
    input_phone_num.grid(row=3, column=7, pady=5)
    l_gender.grid(row=4, column=6, pady=5)
    l_username.grid(row=5, column=6, pady=5)
    in_username.grid(row=5, column=7, pady=5)
    l_password.grid(row=6, column=6, pady=5)
    in_password.grid(row=6, column=7, pady=5)
    l_con_password.grid(row=7, column=6, pady=5)
    input_con_password.grid(row=7, column=7, pady=5)
    b_sign_up.grid(row=8, column=7, pady=5, padx=10)
    b_exit.grid(row=9, column=6, pady=5)
    b_back.grid(row=9, column=7, pady=5)
    # combo box
    gender_choosen = ttk.Combobox(first_frame, values=['Select Gender', 'Male', 'Female', 'Other'])
    gender_choosen.grid(row=4, column=7)
    gender_choosen.current(0)


def last_window(file, flag_file):
    global in_receiver
    lwin = Toplevel()
    lwin.title("Advance hide")
    lwin.geometry("240x180")
    lwin.configure(background="SpringGreen4")
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
    b_transfer = Button(top_frame, text="Send", padx=10, command=lambda: [file_transfer(file, flag_file, unique_id, username)])
    b_transfer.pack(pady=5)
    b_save = Button(buttom_frame, text="Save", padx=10,
                    command=lambda: [save_emb_image(file)])
    if flag_file == "image":
        b_save.pack(side=LEFT, padx=5)
    else:
        b_save = Button(buttom_frame, text="Save", padx=10,
                        command=lambda: [save_emb_audio(file, frame_modified)])
        b_save.pack(side=LEFT, padx=5)
    b_back = Button(buttom_frame, text="Back", padx=10, command=lwin.destroy)
    b_back.pack(side=LEFT, padx=10)
    b_exit = Button(buttom_frame, text="Exit", padx=10, command=lwin.destroy)
    b_exit.pack(side=LEFT)


def img_steg_window(username, flag, uuid):
    global txt_display1, frameimg2, txt_secret1, in_secret_key2, in_secret_key1,iwin
    iwin = Tk()
    iwin.title("Advance hide")
    iwin.geometry("850x400")
    iwin.configure(background="SpringGreen4")
    iwin.resizable(width=False, height=False)
    b_exit_img = Button(iwin, text="Exit", command=iwin.destroy, padx=20)
    b_exit_img.pack(side=BOTTOM, pady=5)
    topframe1 = LabelFrame(iwin)
    topframe1.configure(background="dim gray")
    topframe1.pack(anchor=NE)
    btn_audio = Button(topframe1, text="Audio", padx=20, command=lambda: [audio_steg_window(username, flag, uuid)])
    btn_audio.pack(side=RIGHT)
    btn_img = Button(topframe1, text="Image", padx=20)
    btn_img.pack(side=RIGHT)
    btn_user_mgmt = Button(topframe1, text="User Mgmt", padx=20, command=lambda: [user_mgmt(username, flag, uuid, iwin)])
    if flag == "admin":
        btn_user_mgmt.pack(side=RIGHT)
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

    l_secret_key2 = Label(frameimg2, text="Secret Key", bg="dim gray")
    in_secret_key2 = Entry(frameimg2, show="*")

    l_secret_key2.pack(side=LEFT, padx=10, pady=5)
    in_secret_key2.pack(side=LEFT, pady=5, padx=10)

    b_extract_img = Button(frameimg2, text="Extract", padx=10,
                           command=lambda: [extracter1(pathimg2)])
    b_extract_img.pack(pady=5, padx=10)
    iwin.mainloop()


def audio_steg_window(username,flag,uuid):
    global txt_display2, txt_secret2, frame_audio2, in_secret_key4, in_secret_key3,awin
    iwin.destroy()
    awin = Tk()
    awin.title("Advance hide")
    awin.geometry("850x450")
    awin.configure(background="SpringGreen4")
    awin.resizable(width=False, height=False)
    b_exit_audio = Button(awin, text="Exit", command=awin.destroy, padx=20)
    b_exit_audio.pack(side=BOTTOM, pady=5)
    topframe2 = LabelFrame(awin)
    topframe2.configure(background="dim grey")
    topframe2.pack(anchor=NE)
    b_audio = Button(topframe2, text="Audio", padx=20)
    b_audio.pack(side=RIGHT)
    b_img = Button(topframe2, text="Image", command=lambda: [awin.destroy(), img_steg_window(username, flag, uuid)])
    b_img.pack(side=RIGHT)
    btn_user_mgmt = Button(topframe2, text="User Mgmt", padx=20,command=lambda: [awin.destory(), user_mgmt(username, flag, uuid, awin) ])
    if flag == "admin":
        btn_user_mgmt.pack(side=RIGHT)
    frame_audio1 = LabelFrame(awin, text="Embed in Audio File", padx=10, pady=10)
    frame_audio1.configure(background="dim grey")
    frame_audio1.pack(side=LEFT, padx=10, pady=10)
    l_secret3 = Label(frame_audio1, text="Secret Message",bg="dim gray")
    txt_secret2 = Text(frame_audio1, width=40, height=10)
    l_secret_key3 = Label(frame_audio1, text="Secret Key", bg="dim gray")
    in_secret_key3 = Entry(frame_audio1, show="*")
    b_upload_audio1 = Button(frame_audio1, text="Choose File",
                             command=upload_audio1)
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
    awin.mainloop()

def user_mgmt(username, flag, uuid, win):
    global tv, user_info
    win.destroy()
    admin_win = Tk()
    admin_win.title("Advance hide")
    admin_win.geometry("850x400")
    admin_win.configure(background="SpringGreen4")
    #admin_win.resizable(width=False, height=False)
    lower_frame = LabelFrame(admin_win)
    lower_frame.pack(side=BOTTOM, pady="5")
    btn_back = Button(lower_frame, text="Back", command=lambda: [admin_win.destroy(),img_steg_window(username,flag,uuid)])
    btn_back.pack(side=LEFT)
    btn_exit = Button(lower_frame, text="Exit", command=lambda: [])
    btn_exit.pack(side=LEFT)
    mgt = LabelFrame(admin_win, text="User Management")
    mgt.pack(side=TOP, pady="5")

    btn_remove_admin = Button(mgt, text="Remove Admin", command=remove_admin)
    btn_remove_admin.pack(side=LEFT, padx="5", pady="5")
    btn_remove_user = Button(mgt, text="Remove User", command=remove_user)
    btn_remove_user.pack(side=LEFT, padx="5", pady="5")
    btn_add_admin = Button(mgt, text="Add Admin", command=add_admin)
    btn_add_admin.pack(side=LEFT, padx="5", pady="5")
    btn_add_admin = Button(mgt, text="Activate User", command=user_activate)
    btn_add_admin.pack(side=LEFT, padx="5", pady="5")

    user_info = LabelFrame(admin_win, text="User Details")
    user_info.pack(side=BOTTOM, pady="5")
    scroller = Scrollbar(user_info)
    scroller.pack(side=RIGHT, fill=Y)
    tv = ttk.Treeview(user_info, yscrollcommand=scroller.set, columns=(1, 2, 3, 4, 5, 6, 7), height="12",
                      show="headings")
    tv.pack()
    scroller.configure(command=tv.yview)
    tv.heading(1, text="Fullname", anchor="center")
    tv.heading(2, text="Username", anchor="center")
    tv.heading(3, text="Gender", anchor="center")
    tv.heading(4, text="Phone number", anchor="center")
    tv.heading(5, text="Email Address", anchor="center")
    tv.heading(6, text="Admin", anchor="center")
    tv.heading(7, text="Activated", anchor="center")
    tv.column(1, minwidth=0, width=120, stretch=YES)
    tv.column(2, minwidth=0, width=120, stretch=YES)
    tv.column(3, minwidth=0, width=80, stretch=NO)
    tv.column(4, minwidth=0, width=120, stretch=YES)
    tv.column(5, minwidth=0, width=180, stretch=YES)
    tv.column(6, minwidth=0, width=50, stretch=NO)
    tv.column(7, minwidth=0, width=50, stretch=NO)


    users = User.query.all()

    if users:
        Fullname = [user.full_name for user in users]
        Username = [user.username for user in users]
        gender = [user.gender for user in users]
        Phone_num = [user.phone_number for user in users]
        email = [user.email for user in users]
        admin1 = [user.is_admin for user in users]
        activated = [user.is_active for user in users]
        id_list = [user.id for user in users]
        total_id = 0
        for counter in id_list:
            total_id = total_id + 1
        for i in range(total_id):
            tv.insert('', i, values=(Fullname[i], Username[i], gender[i], Phone_num[i], email[i], admin1[i], activated[i]))

    admin_win.mainloop()


login_window()