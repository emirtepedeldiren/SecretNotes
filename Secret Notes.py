import os
import sys
from tkinter import *
from tkinter import messagebox
from cryptography.fernet import Fernet
import base64
import hashlib

#Root_settings

sw = Tk()
sw.title("Secret Notes")
sw.minsize(width=400 , height=700)
sw.config(padx=30 , pady=30 , bg="black")

#------------------------------FUNCTİONS---------------------------------#

def resource_path(relative_path):

    try:

        base_path = sys._MEIPASS
    except Exception:

        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


def password_to_key(password):

    digest = hashlib.sha256(password.encode()).digest()

    return base64.urlsafe_b64encode(digest)



def take_secret():
    title_hold = title_entry.get()
    secret = text_entry.get("1.0",END).strip()
    master_secret = mk_entry.get()

    if len(title_hold) == 0 or len(secret) == 0 or len(master_secret) == 0 :
        messagebox.showwarning(title="Warning!" , message = "Please enter all information.")
    else:
        try:
            key = password_to_key(master_secret)

            fernet = Fernet(key)

            encrypted_message = fernet.encrypt(secret.encode())


            with open("SecretInput.txt" , "a") as data_file:
                    data_file.write(f"\n{title_hold}\n{encrypted_message.decode()}")

            title_entry.delete(0,END)
            text_entry.delete("1.0",END)
            mk_entry.delete(0,END)

        except Exception as e:
            messagebox.showerror(title="Warning!" , message =f"Something went wrong: {e}")


def decrypt_message():
    encrypted_message = text_entry.get("1.0",END).strip()
    master_secret = mk_entry.get()

    if len(encrypted_message) == 0 or len(master_secret) == 0 :
        messagebox.showwarning(title="Warning!" , message="Please enter the text and the key.")
    else:
        try:
            key = password_to_key(master_secret)

            fernet = Fernet(key)

            decrypted_m = fernet.decrypt(encrypted_message.encode()).decode()

            text_entry.delete("1.0",END)
            text_entry.insert("1.0",decrypted_m)
            mk_entry.delete(0,END)

        except:
            messagebox.showerror(title="Warning!" , message ="The key not entered correctly.")


#--------------Uİ Settings-----------------#

# 1-İmage_Setting

image = PhotoImage(file=resource_path("topsecret.png"))

#İmage_label
image_label = Label(sw,image=image)
image_label.config(bg="Black")
image_label.image=image
image_label.pack(pady=5)

#icon settings

sw.iconbitmap(resource_path("ikon.ico"))

#-----------------------------------------------------------------------------------------#

# 2- Title__Setting

title_entry_label = Label(text="Enter your title: " , font=("Arial" , 13 , "italic"))
title_entry_label.config(fg="#FFFFFF" , bg ="black")
title_entry_label.pack(pady=(10,5))

#title_entry

title_entry = Entry(sw,width=30)
title_entry.pack()

#--------------------------------------------------------------------------------------#

# 3-Text_Settings

text_entry_label = Label(text="Enter your secret: " , font=("Arial" , 13 , "italic"))
text_entry_label.config(fg="#FFFFFF" , bg="black")
text_entry_label.pack(pady=(15,5))

#text_entry

text_entry = Text(width=30 , height=15)
text_entry.pack()

#-------------------------------------------------------------------------------------------#

# 4- Master_key_settings

mk_label = Label(text="Enter your master key: " , font=("Arial" , 10 , "italic" ))
mk_label.config(fg="#FFFFFF" , bg="black")
mk_label.pack(pady=(15,5))

#master_key_entry

mk_entry = Entry(sw, width=30 )
mk_entry.pack()

#---------------------------------------------------------------------------------------#

# 5- Save_button_settings

save_button = Button(text="Save & Encrypt" , command=take_secret )
save_button.config(fg="#FFFFFF" , bg="green")
save_button.pack(pady=10)

#------------------------------------------------------------------#

# 6- Decrypt_button

dec_button = Button(text="Decrypt" , command= decrypt_message)
dec_button.config(fg="#FFFFFF" , bg="red")
dec_button.pack(pady=5)


sw.mainloop()