import sys
from cx_Freeze import setup, Executable
ico_path = '.\\ui\\ico_f.png'

excludes = ['Tkinter']
packages = ['DB','PyQt5','psutil', 'win32com','sqlalchemy']

options = {'build.exe':{
                        'packages':packages,
                        'excludes':excludes,
                        "icon": ico_path
                        }
           }

setup(  name = 'CH_Serv',
        version = '0.1',
        options =options,
        executables = [Executable('MainForm.py', base = "Win32GUI")]
)