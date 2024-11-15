from customtkinter import *
from tkinter import *
import tkinter.messagebox as tmsg
import os
import sys
import subprocess
from PIL import ImageTk
import easygui

# Global Variables
PRESENCE = False
FONT = ('Book Antiqua',19,'bold')
THEME = 'dark'

# checking theme.dll
dll = open('theme.dll',"r")
THEME = dll.read()
dll.close()

# ffmpeg check on startup
# Flag for 'ffmpeg version' as subprocess gave error regardless of ffmpeg's presence in system
check = subprocess.run('ffmpeg',shell=True,capture_output=True,text=True)
if 'ffmpeg version' in check.stderr:
    PRESENCE = True
else:
    PRESENCE = False  


# Main Window
app_window = CTk()


# Add FFmpeg to environment
def addenv():
    if PRESENCE:
        tmsg.showinfo("Installed","FFmpeg is alread Installed on your system")
    else:
        CWD = os.getcwd()
        dir_list = os.listdir(CWD)
        if "FFmpeg" in dir_list:
            ask = tmsg.askyesno("Install FFmpeg","Do you wish to install FFmpeg in your system?")
            if ask:
                subprocess.run(f"SETX PATH {CWD}\\FFmpeg",shell=True,capture_output=True)
                tmsg.showinfo("Closing","The application is rebooted to properly work after instaallation")
                sys.exit(0)
            else:
                pass
        else:
            tmsg.showerror("Error","Necessary files are missing, try reinstalling the application")

#open File Function   
def open_file():
    file_path = filedialog.askopenfilenames(title="Select the file to process",filetypes=[("MP4 Files", "*.mp4")])
    print(file_path)
    app_window.state('zoomed')
    

# closing function
def closing():
    ask = tmsg.askyesno("Exiting Remux +","Do you want to close the application")
    if ask:
        app_window.destroy()
        
# Set theme
def set_theme(theme):
    dll = open('theme.dll',"w")
    dll.write(theme)
    THEME = theme
    dll.close()
    set_appearance_mode(theme)
        
        
# Menubar
menubar = Menu(app_window)
app_window.config(menu=menubar)

file_menu = Menu(menubar,tearoff=0)

file_menu.add_command(label='Install FFmpeg',command=addenv)
sub_menu = Menu(file_menu, tearoff=0)
sub_menu.add_command(label='Dark 😎',command=lambda : set_theme('dark'))
sub_menu.add_command(label='Light 💩',command=lambda : set_theme('light'))
file_menu.add_cascade(label="color theme",menu=sub_menu)
file_menu.add_command(label='Exit',command=closing)
menubar.add_cascade(label="File",menu=file_menu,underline=0)

help_menu = Menu(menubar,tearoff=0)

help_menu.add_command(label='GitHub Page')
help_menu.add_command(label='My Channel')
help_menu.add_command(label='Check for updates')
menubar.add_cascade(label="Help",menu=help_menu,underline=0)

# Dimensions
WIDTH = 930
HEIGHT = 700
screen_widht = app_window.winfo_screenwidth()
screen_height = app_window.winfo_screenheight()
x_pos = (screen_widht/2) - (WIDTH / 2)
y_pos = (screen_height/2) - (HEIGHT / 2)
app_window.geometry(f"{WIDTH}x{HEIGHT}+{int(x_pos)}+{int(y_pos)}")
app_window.minsize(WIDTH,HEIGHT)
app_window.resizable(0,0)
# app_window.maxsize(WIDTH,HEIGHT)


#Attributes
app_window.title("Remus +")
app_window.wm_iconbitmap(r'Assets\Images\icon.ico')
set_appearance_mode(THEME)
# set_default_color_theme("sweetkind")

# Main Frame
main_frame = CTkFrame(app_window,border_width=5)
main_frame.pack(pady=50)

# open Button
btn_img = ImageTk.PhotoImage(file=r'Assets\Images\magnifying-glass.png')
open_btn = CTkButton(main_frame,
                     text="Open File",
                     command=open_file,
                     compound='right',
                     font=FONT,
                     image=btn_img)
open_btn.pack(padx=20,pady=20)

label_frame = CTkFrame(app_window,border_width=5)
label_frame.pack()

description_file = open(r"Assets\Description.txt","r")
description = description_file.read()
description_file.close()

description_lbl = CTkLabel(label_frame,
               text=description,
               font=FONT)
description_lbl.pack(pady=30,padx=30)


app_window.wm_protocol('WM_DELETE_WINDOW',closing)
app_window.mainloop()