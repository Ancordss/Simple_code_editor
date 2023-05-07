from cx_Freeze import setup, Executable

base = None    

executables = [Executable("main.py", base=base)]

packages = ["idna","os","PyQt5","pathlib","sys","PyQt5.QtWidgets","PyQt5.QtCore","PyQt5.Qsci","PyQt5.QtGui"]
options = {
    'build_exe': {    
        'packages':packages,
        'include_files': ['src/'],
    },    
}

setup(
    name = "FCODE",
    options = options,
    version = "0.1",
    description = 'simple code editor for python and html',
    executables = executables
)