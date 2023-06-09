import os
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.Qsci import *
from PyQt5.QtGui import *
from PyQt5.QtCore import Qt





from pathlib import Path
import sys


from editor import Editor
from fuzzy_searcher import SearchItem, SearchWorker
from file_manager import FileManager

from bs4 import BeautifulSoup
from graphviz import Digraph
import tempfile
import logging

#configure logging
logging.basicConfig(level=logging.INFO)


class MainWindow(QMainWindow):
    def __init__(self):
        super(QMainWindow, self).__init__()
        self.side_bar_clr = "#185141"
        self.realtime = False
        self.init_ui()

        self.current_editor = None
        self.current_file = None
        self.current_side_bar = None
        self.file_watcher = QFileSystemWatcher()
        self.file_watcher.fileChanged.connect(self.gen_DOM)

    def init_ui(self):

        self.setWindowTitle("PyQt5 editor")
        self.resize(1300, 900)

        self.setStyleSheet(open("./src/css/style.css", "r").read())

        ##alternative consolel
        self.window_font = QFont("Fire Code")
        self.window_font.setPointSize(12)
        self.setFont(self.window_font)

        self.set_up_menu()
        self.set_up_body()
        self.statusBar().showMessage("hi!")
        self.set_up_status_bar()


        self.show()
    
    def set_up_status_bar(self):
        #Create status bar
        stat = QStatusBar(self)
        stat.setStyleSheet("color: #abb2bf;")
        stat.showMessage("Ready",300)
        self.setStatusBar(stat)
        
        
        


    def set_up_menu(self):
        menu_bar = self.menuBar()
        #file menu
        file_menu = menu_bar.addMenu("File")

        new_file = file_menu.addAction("New")
        new_file.setShortcut("Ctrl+N")
        new_file.triggered.connect(self.new_file)

        open_file = file_menu.addAction("Open File")
        open_file.setShortcut("Ctrl+O")
        open_file.triggered.connect(self.open_file)

        file_menu.addSeparator()
        save_file = file_menu.addAction("Save")
        save_file.setShortcut("Ctrl+S")
        save_file.triggered.connect(self.save_file)
        save_file.triggered.connect(self.gen_DOM)

        save_as = file_menu.addAction("Save As")
        save_as.setShortcut("Ctrl+Shift+S")
        save_as.triggered.connect(self.save_as)


        open_folder = file_menu.addAction("Open Folder")
        open_folder.setShortcut("Ctrl+K")
        open_folder.triggered.connect(self.open_folder)
        
        open_image_action = file_menu.addAction("Open Image")
        open_image_action.setShortcut("Ctrl+I")
        open_image_action.triggered.connect(self.open_image)

        #edit menu

        edit_menu = menu_bar.addMenu("Edit")

        copy_action = edit_menu.addAction("Copy")
        copy_action.setShortcut("Ctrl+C")
        copy_action.triggered.connect(self.copy)

        paste_action = edit_menu.addAction("Paste")
        paste_action.setShortcut("Ctrl+V")
        paste_action.triggered.connect(self.paste)

        cut_action = edit_menu.addAction("Cut")
        cut_action.setShortcut("Ctrl+X")
        cut_action.triggered.connect(self.cut)

        #More menu

        more_menu = menu_bar.addMenu("More")

        gen_DomAction = more_menu.addAction("Generate DOM")
        gen_DomAction.setShortcut("Ctrl+G")
        gen_DomAction.triggered.connect(self.gen_DOM)
        
        close_dom_action = more_menu.addAction("close DOM view")
        close_dom_action.triggered.connect(self.close_image_label)
        


    def get_editor(self) -> QsciScintilla:

        editor = Editor(self)
        return editor
        
    
    def is_binary(self, path):
        #########################
        ### check if path is binary ###
        #########################
        with open(path, "rb") as f:
            return b'\0' in f.read(1024)
        
    def is_image(self, path):
        image_extensions = ['.jpg', '.jpeg', '.png', '.gif', '.bmp']
        ext = os.path.splitext(path)[1].lower()
        return ext in image_extensions
    
    def set_new_tab(self, path: Path, is_new_file=False):
        editor = self.get_editor()

        if is_new_file:
            self.tab_view.addTab(editor,"untitled")
            self.setWindowTitle("untitled")
            self.statusBar().showMessage("Opened untitled")
            self.tab_view.setCurrentIndex(self.tab_view.count () - 1)
            self.current_file = None
            return

        if not path.is_file():
            return

        if self.is_binary(path):
            self.statusBar().showMessage("Binary file can't be opened")
            
        if self.is_image(path):
            
            self.current_file = path
            image_file = str(self.current_file)
            logging.info(f"Image file {image_file}")
            if image_file == '':
                self.statusBar().showMessage("Canceled", 2000)
                return

            # Crear una nueva pestaña y mostrar la imagen en un QLabel
            image_label = QLabel()
            image_label.setScaledContents(True)
            pixmap = QPixmap(image_file)
            scaled_pixmap = pixmap.scaled(image_label.size(), Qt.AspectRatioMode.KeepAspectRatio)
            image_label.setPixmap(scaled_pixmap)
            self.tab_view.addTab(image_label, path.name)
            self.setWindowTitle("Image")
            self.tab_view.setCurrentIndex(self.tab_view.count() - 1)
            self.current_file = None

        #check if file is already opened

        for i in range(self.tab_view.count()):
            if self.tab_view.tabText(i) == path.name:
                self.tab_view.setCurrentIndex(i)
                self.current_file = path
                return
        if not self.is_binary(path):


            #Create new tabe
            self.tab_view.addTab(editor, path.name)
            editor.setText(path.read_text())
            self.setWindowTitle(path.name)
            self.current_file = path
            self.tab_view.setCurrentIndex(self.tab_view.count() - 1)
            self.statusBar().showMessage(f'opened {path.name}',2000)
            self.current_editor = editor
            editor.textChanged.connect(self.gen_DOM)

    def set_cursor_pointer(self, e):
        self.setCursor(Qt.PointingHandCursor)

    def set_cursor_arrow(self, e):
        self.setCursor(Qt.ArrowCursor)

    def get_side_bar_label(self,path,name):
        label =QLabel()
        label.setPixmap(QPixmap(path).scaled(QSize(30,30)))
        label.setAlignment(Qt.AlignmentFlag.AlignTop)
        label.setFont(self.window_font)
        label.mousePressEvent = lambda e: self.show_hide_tab(e,name)
        #chanig cursor on hover
        label.enterEvent = self.set_cursor_pointer
        label.leaveEvent = self.set_cursor_arrow
        return label

    def get_frame(self) -> QFrame:
        frame = QFrame()
        frame.setFrameShape(QFrame.NoFrame)
        frame.setFrameShadow(QFrame.Plain)
        frame.setContentsMargins(0,0,0,0)
        frame.setStyleSheet('''
                                      QFrame{
                                          background-color: #05251C;
                                          border-radius: 5px;
                                          border: none;
                                          padding: 5px;
                                          color: #ADDED1;
                                        }
                                        QFrame:hover{
                                            color: #00ff00;
                                            
                                        }
            ''')
        return frame

    def set_up_body(self):
        #body
        body_frame = QFrame()
        body_frame.setFrameShape(QFrame.NoFrame)
        body_frame.setFrameShadow(QFrame.Plain)
        body_frame.setLineWidth(0)
        body_frame.setMidLineWidth(0)
        body_frame.setContentsMargins(0, 0, 0, 0)
        body_frame.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        body = QHBoxLayout()
        body.setContentsMargins(0, 0, 0, 0)
        body.setSpacing(0)
        body_frame.setLayout(body)

        ##################
        ####TAB VIEW####

        ## tab widget to add editor to
        self.tab_view = QTabWidget()
        self.tab_view.setContentsMargins(0,0,0,0)
        self.tab_view.setTabsClosable(True)
        self.tab_view.setMovable(True)
        self.tab_view.setDocumentMode(True)
        self.tab_view.tabCloseRequested.connect(self.close_tab)

         #####################
        ###SIDE BAR####

        self.side_bar = QFrame()
        self.side_bar.setFrameShape(QFrame.StyledPanel)
        self.side_bar.setFrameShadow(QFrame.Plain)
        self.side_bar.setStyleSheet('''
                                    background-color: {self.side_bar_clr};
                                    ''')
        side_bar_layout = QVBoxLayout()
        side_bar_layout.setContentsMargins(5,10,5,0)
        side_bar_layout.setSpacing(0)
        side_bar_layout.setAlignment(Qt.AlignTop | Qt.AlignCenter)

        ###setup labels
        folder_label = self.get_side_bar_label("./src/icons/folder-icon-blue.svg","folder-icon")
        side_bar_layout.addWidget(folder_label)

        search_label = self.get_side_bar_label("./src/icons/search-icon","search-icon")
        side_bar_layout.addWidget(search_label)

        self.side_bar.setLayout(side_bar_layout)


        #split view
        self.hsplit = QSplitter(Qt.Horizontal)

        #####################
        ###FILE MANAGER####

        #frame and layout to hod tree view (file manager window)
        self.file_manager_frame = self.get_frame()
        self.file_manager_frame.setMaximumWidth(400)
        self.file_manager_frame.setMinimumWidth(200)

        self.file_manager_layout = QVBoxLayout()
        self.file_manager_layout.setContentsMargins(0,0,0,0)
        self.file_manager_layout.setSpacing(0)

        self.file_manager = FileManager(
            tab_view=self.tab_view,
            set_new_tab=self.set_new_tab,
            main_window=self
        )

        # setup layout
        self.file_manager_layout.addWidget(self.file_manager)
        self.file_manager_frame.setLayout(self.file_manager_layout)



        #create file system model to show in tree view


        self.model = QFileSystemModel()
        self.model.setRootPath(os.getcwd())
        #file system filter
        self.model.setFilter(QDir.NoDotAndDotDot | QDir.AllDirs | QDir.Files)

         #####################
          ###FILE VIEWER####

        self.tree_view = QTreeView()
        self.tree_view.setFont(QFont("Helvetica",13))
        self.tree_view.setModel(self.model)
        self.tree_view.setRootIndex(self.model.index(os.getcwd()))
        self.tree_view.setSelectionMode(QTreeView.SingleSelection)
        self.tree_view.setSelectionBehavior(QTreeView.SelectRows)
        self.tree_view.setEditTriggers(QAbstractItemView.NoEditTriggers)
        # add custom context menu

        self.tree_view.setContextMenuPolicy(Qt.CustomContextMenu)
        self.tree_view.customContextMenuRequested.connect(self.tree_view_context_menu)
        #handling click

        self.tree_view.clicked.connect(self.tree_view_clicked)
        self.tree_view.setIndentation(10)
        self.tree_view.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        #hide header and other stuff

        self.tree_view.setHeaderHidden(True)
        self.tree_view.setColumnHidden(1,True)
        self.tree_view.setColumnHidden(2,True)
        self.tree_view.setColumnHidden(3,True) 

        ##search view##
        self.search_frame = self.get_frame()
        self.search_frame.setMaximumWidth(400)
        self.search_frame.setMinimumWidth(200)

        search_layout = QVBoxLayout()
        search_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        search_layout.setContentsMargins(0, 10, 0, 0)
        search_layout.setSpacing(0)

        search_input = QLineEdit()
        search_input.setPlaceholderText("Search")
        search_input.setFont(self.window_font)
        search_input.setAlignment(Qt.AlignmentFlag.AlignTop)


         ############# CHECKBOX ################
        self.search_checkbox = QCheckBox("Search in modules")
        self.search_checkbox.setFont(self.window_font)
        self.search_checkbox.setStyleSheet("color: white; margin-bottom: 10px;")
        
        self.search_worker = SearchWorker()
        self.search_worker.finished.connect(self.search_finshed)

        search_input.textChanged.connect(self.seachonpath)
        search_input.textChanged.connect(
            lambda text: self.search_worker.update(
                text,
                self.seachonpath(),
                self.search_checkbox.isChecked()
            )
        )
        
        # search_input.textChanged.connect(
        #     lambda text: self.search_worker.update(
        #         text,
        #         self.model.rootDirectory().absolutePath(),
        #         self.search_checkbox.isChecked()
        #     )
        # )

        
        #####################
        ###SEARCH ListView####
        self.search_list_view = QListWidget()
        self.search_list_view.setFont(QFont("FiraCode", 13))
        self.search_list_view.setStyleSheet("""
        QListWidget {
            background-color: #0C3127;
            border-radius: 5px;
            border: 1px solid #21B48B;
            padding: 5px;
            color: #21B48B;
        }
        """)

        self.search_list_view.itemClicked.connect(self.search_list_view_clicked)

        search_layout.addWidget(self.search_checkbox)
        search_layout.addWidget(search_input)
        search_layout.addSpacerItem(QSpacerItem(5, 5, QSizePolicy.Minimum, QSizePolicy.Minimum))
        search_layout.addWidget(self.search_list_view)

        self.search_frame.setLayout(search_layout)

          #####################
        ###SETUP WIDGENTS####
        #add tree view and tab view
        self.hsplit.addWidget(self.file_manager_frame)
        body.addWidget(self.side_bar)
        self.hsplit.addWidget(self.tab_view)

        body.addWidget(self.hsplit)
        body_frame.setLayout(body)

        self.setCentralWidget(body_frame)
        
    def seachonpath(self):
        #print(self.current_file)
        # lambda text: self.search_worker.update(
        #         text,
        #         self.current_file,  # Ruta del archivo específico
        #         self.search_checkbox.isChecked()
        # )
        return str(self.current_file)

        

    def search_finshed(self, items):
        self.search_list_view.clear()
        for i in items:
            self.search_list_view.addItem(i)

    def search_list_view_clicked(self, item):
        self.set_new_tab(Path(item.full_path))
        editor: Editor = self.tab_view.currentWidget()
        editor.setCursorPosition(item.lineno, item.end)
        editor.setFocus()  
    
    def show_dialog(self, title, msg) -> int:
        dialog = QMessageBox(self)
        dialog.setFont(self.font())
        dialog.font().setPointSize(14)
        dialog.setWindowTitle(title)
        dialog.setWindowIcon(QIcon(":/icons/close-icon.svg"))
        dialog.setText(msg)
        dialog.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        dialog.setDefaultButton(QMessageBox.No)
        dialog.setIcon(QMessageBox.Warning)
        return dialog.exec_()
    
    
    def close_tab(self, index):
        editor: Editor = self.tab_view.currentWidget()
        self.tab_view.removeTab(index)
         
        
    def show_hide_tab(self,e,type_):
        if type_ == "folder-icon":
            if not (self.file_manager_frame in self.hsplit.children()):
                self.hsplit.replaceWidget(0, self.file_manager_frame)
        elif type_ == "search-icon":
            if not (self.search_frame in self.hsplit.children()):
                self.hsplit.replaceWidget(0, self.search_frame)
        
        if self.current_side_bar == type_:
            frame = self.hsplit.children()[0]
            if frame.isHidden():
                frame.show()
            else:
                frame.hide()
        self.current_side_bar = type_
     

    def tree_view_context_menu(self):
        pass
        
    def find_tab_index(self, tab_name):
        for i in range(self.tab_view.count()):
            if self.tab_view.tabText(i) == tab_name:
                return i
        return -1
    
    def tree_view_clicked(self, index: QModelIndex):
        path = self.model.filePath(index)
        p = Path(path)
        self.set_new_tab(p)
        
        
    def new_file(self):
            self.set_new_tab(None,is_new_file=True)

    def save_file(self):
        self.current_file is None and self.tab_view.count() > 0
        #self.save_as()

        editor = self.tab_view.currentWidget()
        self.current_file.write_text(editor.text())
        self.statusBar().showMessage(f"Saved{self.current_file.name}", 2000)

    def save_as(self):
        #Save as
        editor = self.tab_view.currentWidget()
        if editor is None:
            return
        
        file_path = QFileDialog.getSaveFileName(self, "Save as", os.getcwd())[0]
        if file_path == '':
            self.statusBar().showMessage("Cancelled", 2000)
            return
        path = Path(file_path)
        path.write_text(editor.text())
        self.tab_view.setTabText(self.tab_view.currentIndex(),path.name)
        self.statusBar().showMessage(f"Saved {path.name}",2000)
        self.current_file = path


    def open_file(self):
        ops = QFileDialog.Options()
        ops |= QFileDialog.DontUseNativeDialog

        new_file, _ = QFileDialog.getOpenFileName(self,
                    "Pick A File", "","All Files (*);;Python Files (*.py)", 
                    options=ops)
        if new_file == '':
            self.statusBar().showMessage("Canceled", 2000)
            return
        f = Path(new_file)
        self.set_new_tab(f)

    def open_folder(self):
        new_folder = QFileDialog.getExistingDirectory(
            self, "Pick A Folder", ""
        )
        if new_folder:
            self.file_manager.model.setRootPath(new_folder)
            self.file_manager.setRootIndex(self.file_manager.model.index(new_folder))
            self.statusBar().showMessage(f"Opened {new_folder}", 2000)
        
    def copy(self):
        editor = self.tab_view.currentWidget()
        if editor is not None:
            editor.copy()

    def paste(self):
        ...
    def cut(self):
        ...
                    
    def gen_DOM(self):
        file_path = self.current_file
        logging.info('Generating DOM; path: {}'.format(file_path))
        
        if not str(file_path).endswith(".html"):
            logging.info(f'no es html {file_path}')
            return
        
        
            

        if file_path:
            content = self.current_editor.text()
            #content = file.read()

            # Generar el gráfico del DOM dentro de generate_dom_graph
            def generate_dom_graph(html):
                # Analizar el HTML con BeautifulSoup
                soup = BeautifulSoup(html, 'html.parser')

                # Crear un gráfico de Graphviz
                graph = Digraph(format='png')

                # Función recursiva para generar el gráfico del DOM
                def generate_dom(node, parent_id=None):
                    # Obtener el nombre de la etiqueta HTML
                    tag_name = node.name if node.name else 'text'

                    # Generar un identificador único para el nodo
                    node_id = f'{tag_name}_{id(node)}'

                    # Agregar el nodo al gráfico
                    graph.node(node_id, label=tag_name)

                    # Agregar una arista desde el padre (si existe)
                    if parent_id:
                        graph.edge(parent_id, node_id)

                    # Recorrer los hijos del nodo
                    for child in node.children:
                        # Solo procesar nodos del tipo Tag
                        if child.name:
                            generate_dom(child, node_id)

                # Generar el gráfico del DOM comenzando desde el nodo raíz
                generate_dom(soup)

                return graph

                # Generar el gráfico del DOM utilizando la función generate_dom_graph
            graph = generate_dom_graph(content)

            # Obtener el nombre del archivo
            file_name = os.path.basename(file_path)

            # Obtener la extensión del archivo
            file_ext = os.path.splitext(file_name)[1]

            # Ruta de la carpeta de destino
            temp_dir = tempfile.gettempdir()
            output_folder = os.path.join(temp_dir, 'DOOMS')

            # Crear la carpeta de destino si no existe
            os.makedirs(output_folder, exist_ok=True)

            # Ruta del archivo PNG
            png_name = f'{os.path.splitext(file_name)[0]}_dom_graph'
            png_path = os.path.join(output_folder, png_name)

            # Ruta del archivo DOT
            dot_name = f'{os.path.splitext(file_name)[0]}_dom_graph.dot'
            dot_path = os.path.join(output_folder, dot_name)

            # Guardar el gráfico como archivo de imagen PNG
            graph.render(png_path, view=False)

            # Guardar el gráfico como archivo DOT
            with open(dot_path, 'w') as dot_file:
                dot_file.write(graph.source)
                
            index = self.find_tab_index("DOM")
            if index != -1:
                self.tab_view.removeTab(index)

            # Abrir la imagen generada
            self.show_DOM(png_path)
                    
    def open_image(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog

        image_file, _ = QFileDialog.getOpenFileName(self,
                    "Pick An Image", "", "Image Files (*.png *.jpg *.jpeg *.bmp)",
                    options=options)
        logging.info(f"Image File: {image_file}")
        if image_file == '':
            self.statusBar().showMessage("Canceled", 2000)
            return

        # Crear una nueva pestaña y mostrar la imagen en un QLabel
        image_label = QLabel()
        pixmap = QPixmap(image_file)
        image_label.setPixmap(pixmap)

        self.tab_view.addTab(image_label, "Image")
        self.setWindowTitle("Image")
        self.tab_view.setCurrentIndex(self.tab_view.count() - 1)
        self.current_file = None
        
    def show_DOM(self, image_file):
        image_file = os.path.splitext(image_file)[0] + ".png"
        logging.info(f"Image file {image_file}")
        if image_file == '':
            self.statusBar().showMessage("Canceled", 2000)
            return

        # Obtén el editor actual en la pestaña activa
        editor = self.tab_view.currentWidget()

        # Verifica si el editor tiene un layout
        if editor.layout() is None:
            # Si no tiene un layout, crea uno
            editor.setLayout(QVBoxLayout())

        # Elimina cualquier QLabel existente en el layout del editor
        layout = editor.layout()
        while layout.count() > 0:
            item = layout.takeAt(0)
            if item.widget() is not None:
                item.widget().deleteLater()

        # Crea un QLabel para mostrar la imagen
        image_label = QLabel()
        image_label.setFixedSize(400, 300)


        # Calcula el nuevo tamaño de la imagen
        pixmap = QPixmap(image_file)
        scaled_pixmap = pixmap.scaled(image_label.size(), Qt.AspectRatioMode.KeepAspectRatio)
        image_label.setPixmap(scaled_pixmap)

        # Agrega el QLabel al layout del editor
        layout.addWidget(image_label)
        layout.setAlignment(Qt.AlignTop | Qt.AlignRight)

        # Asegúrate de que el editor sea el widget actual en el tab_view
        self.tab_view.setCurrentWidget(editor)
        
        
        

    def close_image_label(self):
    # Obtén el editor actual en la pestaña activa
        editor = self.tab_view.currentWidget()

        # Verifica si el editor tiene un layout
        if editor.layout() is not None:
            # Elimina cualquier QLabel existente en el layout del editor
            layout = editor.layout()
            while layout.count():
                child = layout.takeAt(0)
                if child.widget():
                    child.widget().deleteLater()
        
        
        
        
        

        
            


if __name__ == "__main__":
    app = QApplication([])
    window = MainWindow()
    sys.exit(app.exec_())
