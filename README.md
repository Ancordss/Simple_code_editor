# Simple_code_editor


### requisitos

instala graphviz [Aqui](https://graphviz.org/download/)


## requisitos para copilar desde 0

### windows

#### nota!!! recomiendo usar scoop como administrador de paquetes puedes descargarlo e instalar desde [Aqui!](https://scoop.sh/)'''

- [x] instala python
```
scoop install python
```

- [x] clona el repositorio y ejecuta este comando para crear un entorno virtual
(adentro de la carpeta del repositorio)
```
python3 -m venv venv
```
- [x] activa el entorno virtual siguiendo estos pasos:

- desde la terminal entra a la carpeta venv luego a Scripts y escribe

```
\Activate.ps1
```

- si todo sale bien te aparece adelante de la barra de la terminal esto (env)

- [x] ejecutar el siguiente comando para tener los dapendencias 

```
pip3 install -r requirements
```

- [x] ejecuta para probar el programa:  (no es obligatorio) 

```
python3 main.py
```

- [x] copila el binario

- para eso ejecuta este comando
```
python3 setup.py build 
```

el .exe estara en la carpeta build generada

### Linux (ubuntu)

- [x] actuliza python (en caso de que no lo tengas)
```
sudo apt update
sudo apt upgrade
```
- ahora vamos a instalar unas dependencias en caso de que no las tengas 
```
sudo apt install git curl make build-essential libssl-dev zlib1g-dev libbz2-dev libreadline-dev libsqlite3-dev wget llvm libncursesw5-dev xz-utils tk-dev libxml2-dev libxmlsec1-dev libffi-dev liblzma-dev

```
- instalaremos pyenv (salta este paso si tienes una version de python arriba de 3.10)

```
curl https://pyenv.run | bash
export PATH="$HOME/.pyenv/bin:$PATH"
eval "$(pyenv init --path)"
source ~/.bashrc
```

- ahora puedes instalar la version de python que quieras usar en este caso puedes usar python 3.11.3

```
pyenv install 3.11.3

```

puedes configurar la version como global con
```
pyenv global 3.11.3
```


- [x] clona el repositorio y ejecuta este comando para crear un entorno virtual
(adentro de la carpeta del repositorio)
```
python3 -m venv venv
```
- [x] activa el entorno virtual:


- desde la terminal entra a la carpeta venv luego a Scripts y escribe

```
chmod +x
./Activate
```

si todo sale bien te aparece adelante de la barra de la terminal esto (env)

- ahora solo tienes que ejecutar el siguiente comando para tener los dapendencias 

```
pip3 install -r requirements
```

- ejecuta: 

```
python3 main.py
```

- [x] copilar el binario:

```
python3 setup.py build 
```

el ejecutable estara en la carpeta build generada.


