from cx_Freeze import setup, Executable

base = None

executables = [Executable("main.py", base=base)]

packages = ["idna","os","PyQt5","pathlib","sys","PyQt5.QtWidgets","PyQt5.QtCore","PyQt5.Qsci","PyQt5.QtGui","re","msilib.schema","multiprocessing","random","keyword","pkgutil","types","json","keyword","builtins"]
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