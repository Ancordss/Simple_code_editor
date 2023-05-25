def gen_DOM(self):
        file_dialog = QFileDialog()
        options = file_dialog.Options()
        options |= file_dialog.DontUseNativeDialog
        file_path, _ = file_dialog.getOpenFileName(self, "Abrir archivo HTML", "", "HTML Files (*.html)",
                                                   options=options)

        if file_path:
            with open(file_path, "r") as file:
                content = file.read()

                # Generar el gráfico del DOM dentro de generateDOM
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

                # Generar el gráfico del DOM utilizando la función generate_dom_graph dentro de generateDOM
                graph = generate_dom_graph(content)

                # Guardar el gráfico como archivo de imagen
                save_dialog = QFileDialog()
                save_path, _ = save_dialog.getSaveFileName(self, "Guardar gráfico del DOM", "", "PNG Files (*.png)",
                                                           options=options)

                if save_path:
                    graph.render(save_path, view=True)