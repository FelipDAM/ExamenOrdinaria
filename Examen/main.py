from PySide6.QtWidgets import QApplication, QMainWindow, QTableWidget, QTableWidgetItem,QVBoxLayout, QWidget, QLineEdit, QPushButton, QHeaderView,QMenuBar,QMessageBox
from database import Database
import sys
import os
from PySide6.QtGui import QAction, QKeySequence
from PySide6.QtUiTools import QUiLoader


class ProductApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Gestió de Productes")
        self.setGeometry(100, 100, 600, 500)
        self.db = Database()

        loader = QUiLoader()
        ui_path = os.path.join(os.path.dirname(__file__), "window.ui")
        self.addwindow = loader.load(ui_path, None)
        

        self.menuBar = QMenuBar()
        menu_productes = self.menuBar.addMenu("&Productes")
        accion = QAction("&Afegir producte", self)
        accion.triggered.connect(self.add_product)
        accion2 = QAction("&Modificar producte", self)
        accion2.triggered.connect(self.edit_product)
        menu_productes.addAction(accion)
        menu_productes.addAction(accion2)

        # Widget principal
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        self.layout = QVBoxLayout()
        main_widget.setLayout(self.layout)
        # Widget principal
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        self.layout = QVBoxLayout()
        main_widget.setLayout(self.layout)
        self.layout.addWidget(self.menuBar)

        # Formulari (tot amb QLineEdit)
        #self.name_input = QLineEdit()
        #self.price_input = QLineEdit()  
        #self.category_input = QLineEdit()  

        #self.layout.addWidget(QLabel("Nom del Producte:"))
        #self.layout.addWidget(self.name_input)
        #self.layout.addWidget(QLabel("Preu (€):"))
        #self.layout.addWidget(self.price_input)
        #self.layout.addWidget(QLabel("Categoria:"))
        #self.layout.addWidget(self.category_input)
#
        ## Botons per afegir i modificar
        #self.add_button = QPushButton("Afegir Producte")
        #self.add_button.clicked.connect(self.add_product)
        #self.layout.addWidget(self.add_button)

        self.delete_button = QPushButton("Eliminar Producte")
        self.delete_button.clicked.connect(self.delete_product)
        self.layout.addWidget(self.delete_button)

        # Taula de productes
        self.table = self.create_table()
        self.layout.addWidget(self.table)

        self.load_products()
        self.show()

    def create_table(self):
        table = QTableWidget()
        table.setColumnCount(3)
        table.setHorizontalHeaderLabels(["Nom", "Preu", "Categoria"])
        table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        table.setSelectionBehavior(QTableWidget.SelectRows)
        return table

    def load_products(self):
        self.table.setRowCount(0)
        products = self.db.get_products()
        for row_index, (product_id, name, price, category) in enumerate(products):
            self.table.insertRow(row_index)
            self.table.setItem(row_index, 0, QTableWidgetItem(name))
            self.table.setItem(row_index, 1, QTableWidgetItem(price))
            self.table.setItem(row_index, 2, QTableWidgetItem(category))

    def add_product(self):

        self.addwindow.add_button.setText("Afegir")

        self.addwindow.name_input.clear()
        self.addwindow.price_input.clear()
        self.addwindow.category_input.clear()

        self.addwindow.exec()
        name = self.addwindow.name_input.text()
        price = self.addwindow.price_input.value() 
        category = self.addwindow.category_input.text()  

        if name and price and category:
            self.db.add_product(name, price, category)
            self.load_products()

    def edit_product(self):
        self.addwindow.add_button.setText("Modificar")
        selected_row = self.table.currentRow()
        if selected_row == -1:
            QMessageBox.warning(self,
            "Error",
            "No has seleccionat cap producte",
             )
            return
                
        product_id = self.db.get_products()[selected_row][0]
        name = self.db.get_products()[selected_row][1]
        price = self.db.get_products()[selected_row][2]
        category = self.db.get_products()[selected_row][3]

        self.addwindow.name_input.setText(name)
        self.addwindow.price_input.setValue(float(price))
        self.addwindow.category_input.setText(category)

        self.addwindow.exec()
        
        new_name = self.addwindow.name_input.text()
        new_price = self.addwindow.price_input.value()  
        new_category = self.addwindow.category_input.text()

        
        if new_name and new_price and new_category and new_name != name or new_price != price or new_category != category:
            boto_polsat = QMessageBox.warning(self,
            "Comfirmar canvis",
            "Segur que vols modificar el producte?",
            buttons=QMessageBox.Yes | QMessageBox.No
        )
        if boto_polsat == QMessageBox.Yes:
            self.db.update_product(product_id, new_name, new_price, new_category)
            self.load_products()
        else:
            return

    def delete_product(self):
        selected_row = self.table.currentRow()
        if selected_row == -1:
            return


        boto_polsat = QMessageBox.warning(self,
            "Comfirmar canvis",
            "Segur que vols borrar el producte?",
            buttons=QMessageBox.Yes | QMessageBox.No
        )
        if boto_polsat == QMessageBox.Yes:

            product_id = self.db.get_products()[selected_row][0]
            self.db.delete_product(product_id)
            self.load_products()
        else:
            return


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ProductApp()
    window.show()
    sys.exit(app.exec())
