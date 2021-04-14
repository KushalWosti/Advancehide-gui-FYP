from tkinter import *
from tkinter import ttk
from my_database import get_session, User, qry_activate_user, qry_remove_user,\
    qry_remove_admin, qry_add_admin
db_session = get_session()
# db_session.query(User).filter(User.is_admin == True).with_entities("username", "email", "is_admin").all()


def user_activate():
    selected = tv.selection()
    for record in selected:
        values = tv.item(record, 'values')
        username = values[1]
        # values[5] = True
        print(username)
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
        print(username)
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
        print(username)
        qry_remove_user(username)
        tv.delete(record)
        print("hello")


def add_admin():
    selected = tv.selection()
    for record in selected:
        values = tv.item(record, 'values')
        username = values[1]
        #values[5] = True
        print(username)
        qry_add_admin(username)
        #tv.delete(record)
        print("hello")

    items = tv.selection()
    #print(items())
    for record in items:
        print("")


def user_mgmt(username, flag, uuid, win):
    global tv, user_info
    win.destroy()
    admin_win = Tk()
    admin_win.title("Advance hide")
    admin_win.geometry("850x400")
    admin_win.configure(background="light gray")
    #admin_win.resizable(width=False, height=False)
    lower_frame = LabelFrame(admin_win)
    lower_frame.pack(side=BOTTOM, pady="5")
    btn_back = Button(lower_frame, text="Back", command=lambda: [])
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


