import os
import getpass
import shutil
from pathlib import Path

user_name = getpass.getuser()'''gets username'''


src = "/users/" + user_name + "/desktop"
dst = "/users/" + user_name + "/documents/"
trash = "/users/" + user_name + "/.trash"
types = {".docx": "DOC", ".pdf": "PDF", ".mp3": "MP3",
         ".png": "Images", ".jpg": "Images", ".jpeg": "Images"}


def get_path(pth_name):
    return os.path.abspath(pth_name)


def get_ext(pth_name):
    return os.path.splitext(pth_name)[1]


def fl_name(typ):
''' names folder for file type'''
    for i in types.keys():
        if i == typ:
            return types[i]


def copy_file(typ):
    f = fl_name(typ)
    for i in os.scandir(src):
        if os.path.isfile(i) and get_ext(get_path(i)) == typ:
            try:
                os.mkdir(dst + f)
                shutil.copy2(get_path(i), dst + f)
            except FileExistsError:
                shutil.copy2(get_path(i), dst + f)


for i in types.keys():
    copy_file(i)


def clean():
    a = input("Do you want to clean the desktop? [Y/N] : ")
    if a == "Y" or a == "y":
        for i in types.keys():
            copy_file(i)
        for j in os.scandir(src):
            if os.path.isfile(j) and get_ext(get_path(j)) in types.keys():
                try:
                    shutil.move(get_path(j), trash)
                except FileExistsError:
                    continue
        print("Done.")
    elif a == "N" or a == "n":
        print("Okay. Thanks!")


clean()
