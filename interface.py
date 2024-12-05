from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget, 
    QTableWidget, QTableWidgetItem, QSplitter, QLabel, QHBoxLayout, QLineEdit, QSizePolicy, QScrollArea, QComboBox, QMessageBox
)
from PyQt6.QtCore import Qt

import asyncio

import datetime


from database import Database

class Window(QMainWindow):
    
    def __init__(self) -> None:
        super().__init__()
        
        self.db = Database('postgresql://izeb:izeb@localhost:5432/main')
        self.loop = asyncio.get_event_loop()
        
        self.setWindowTitle("DB Viewer")
        self.resize(800, 600)

        self.splitter = QSplitter(Qt.Orientation.Horizontal)
        self.setCentralWidget(self.splitter)

        
        

        self.tables = {'client': "Клиенты",
                        'agreement': 'Договора',
                       'employee': 'Работники',
                       'product': 'Товары',
                       'sale': 'Продажи',
                       'add': 'Добавить запись'}
        
        self.input_fields = {
            "client": [
               "name", "lastname", "fatherly", "date_birth", "phone_number",
                "addres", "place_work", "TIN", "bank_card", "count_purchases", "document_type", "data", "issued_date", "issued_by"
            ],
            "agreement": ["employee_id", "client_id", "product_id", "date"],
            "employee": [
                "name", "lastname", "fatherly", "date_birth", "phone_number",
                "addres", "citizenship", "job_title", "job_salary",
                "experience", "schedule",  "document_type", "data", "issued_date", "issued_by"
            ],
            "product": [
                "title", "description", "date_release", "cost", "serial_number"
            ],
            "sale": ["client_id", "employee_id", "product_id", "date"],
            
        }

        
     
        self.block_styles = "background: gray; border-radius: 10px; "
        self.label_style = 'padding: 0px; margin: 0px;'
        menu_widget = QWidget()
        menu_layout = QVBoxLayout()
        menu_widget.setLayout(menu_layout)

        for _, name in self.tables.items():
            b = QPushButton(name.capitalize())
            b.clicked.connect(lambda _, x=_: self.load_data(x))
            menu_layout.addWidget(b)
            
   
        menu_layout.addStretch(1)

        self.splitter.addWidget(menu_widget)
        self.scroll_area = QScrollArea()
        self.splitter.addWidget(self.scroll_area)
        
        # self.load_data('client')
        # self.test()
        self.current_table = 'client'
        self.load_data('client')
        
        
        self.splitter.setSizes([200, 600])
        
 
        
    def load_data(self, table):
        if table == 'add':
            return self.load_inputs()
        if self.current_table != table:
            print(f'LOADING TABLE {table.upper()}')
        self.current_table = table
        items = None
        if table == 'client':
            items = self.loop.run_until_complete(self.db.find_users(user_type='client'))
        elif table == 'employee':
            items = self.loop.run_until_complete(self.db.find_users(user_type='employee'))
        elif table == 'agreement':
            items = self.loop.run_until_complete(self.db.find_items(item_type='agreement'))
        elif table == 'sale':
            items = self.loop.run_until_complete(self.db.find_items(item_type='sale'))
        elif table == 'product':
            items = self.loop.run_until_complete(self.db.find_all_from_table('product'))
            
            
        if not items: return
            
    
        self.scroll_area.setWidgetResizable(True)
        
        scroll_content = QWidget()
        scroll_layout = QVBoxLayout()
            
        for item in items:
            block = QWidget()
            block_layout = QVBoxLayout()
            block_layout.setContentsMargins(0, 0, 0, 0)
            block_layout.setSpacing(0)
            block.setMinimumHeight(90)
            block.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
            block.setStyleSheet(self.block_styles)
        
            block_labels = self.getLableText(table, item)
            for block_label in block_labels:
                block_layout.addWidget(block_label)
            block.setLayout(block_layout)
            
            scroll_layout.addWidget(block)


        scroll_content.setLayout(scroll_layout)        

        self.scroll_area.setWidget(scroll_content)
        
        self.splitter.replaceWidget(1, self.scroll_area)
        \
        
    def getLableText(self, table, item):
        if table == 'client':
            block_label = [QLabel(f"{item.lastname} {item.name} {item.fatherly} | {item.phone_number} | {item.addres} | {item.tin}\nДата рождения: {item.date_birth}\nДокументы: {item.document.type} - {item.document.data} от {item.document.issue_date} выдан {item.document.issue_by}")]
        elif table == 'employee':
            block_label = [QLabel(f"{item.lastname} {item.name} {item.fatherly} | {item.phone_number} | {item.addres}\nДата рождения: {item.date_birth}\nДокументы: {item.document.type} - {item.document.data} от {item.document.issue_date} выдан {item.document.issue_by}")]
        elif table == 'product':
            block_label = [QLabel(f"{item.title}: {item.description} - {item.cost}\nПродаж: {item.count_sales}")]
        elif table == 'agreement':
            block_label = [QLabel(f"Заказчик: {item.client.lastname} {item.client.name} {item.client.fatherly}\nИсполнитель: {item.employee.lastname} {item.employee.name} {item.employee.fatherly}\nТовар: {item.product.title} - {item.product.cost}\n\n{item.date}")]
        elif table == 'sale':
            block_label = [QLabel(f"Купил: {item.client.lastname} {item.client.name} {item.client.fatherly}\nПродал: {item.employee.lastname} {item.employee.name} {item.employee.fatherly}\nТовар: {item.product.title} - {item.product.cost}\n\n{item.date}")]
            
        block_label[0].setStyleSheet(self.label_style)
        
        return block_label
        
    def load_inputs(self):
        wd = QWidget()
        self.current_table = 'client'
        self.inputs_loaded = []
        self.combo_box = QComboBox(wd)
        self.combo_box.currentIndexChanged.connect(self.update_input_fields)
        self.combo_box.addItems([
            i[1] for i in self.tables.items()
            if i[0] != 'add'
        ])
        layout = QVBoxLayout()
        layout.addWidget(self.combo_box)
        inputs = self.input_fields.get('client')
        for input in inputs:
            input_field = QLineEdit()
            input_field.setPlaceholderText(f"Input for {input}")
            self.inputs_loaded.append(input_field)
            layout.addWidget(input_field)
            
        b = QPushButton('Добавить')
        b.clicked.connect(self.add_data_to_db)
        layout.addWidget(b)
        
        wd.setLayout(layout)
        self.splitter.replaceWidget(1, wd)
        
    def update_input_fields(self, index):
        wd = QWidget()
        self.inputs_loaded = []
        items = self.input_fields.items()
        for i, item in enumerate(items):
            if i == index:
                inputs = item[1]
                self.current_table = item[0]
        layout = QVBoxLayout()
        layout.addWidget(self.combo_box)
        for input in inputs:
            input_field = QLineEdit()
            input_field.setPlaceholderText(f"Input for {input}")
            self.inputs_loaded.append(input_field)
            layout.addWidget(input_field)
            
        layout.setAlignment(Qt.AlignmentFlag.AlignTop)
            
        b = QPushButton('Добавить')
        b.clicked.connect(self.add_data_to_db)
        layout.addWidget(b)
        
        wd.setLayout(layout)
        self.splitter.replaceWidget(1, wd)
            
    def add_data_to_db(self):
        data = {}
        for input, field in zip(self.inputs_loaded, self.input_fields[self.current_table]):
            data[field] = input.text() 
        
        if "" in data.values():
            self.show_alert('Заполните все поля')
        
        for val in data.items():
            if 'date' in val[0]:
                try:
                    print(val)
                    y, m, d = val[1].split('-')
                    y, m, d = int(y), int(m), int(d)
                except: return self.show_alert('Укажите дату в формате YYYY-MM-DD')
                else: data[val[0]] = datetime.date(y, m, d)
        
        if self.current_table == 'client':
            self.loop.run_until_complete(self.db.add_client(*data.values()))
        elif self.current_table == 'employee':
            self.loop.run_until_complete(self.db.add_employee(*data.values()))
        elif self.current_table == 'product':
            self.loop.run_until_complete(self.db.add_product(*data.values()))
        elif self.current_table == 'sale':
            self.loop.run_until_complete(self.db.add_sale(*data.values()))
        elif self.current_table == 'agreement':
            self.loop.run_until_complete(self.db.add_agreement(*data.values()))
            
        
            
        
    def show_alert(self, data):
        message = QMessageBox()
        message.setIcon(QMessageBox.Icon.Information)
        message.setWindowTitle("Добавление записи")
        message.setText("Ошибка")
        message.setInformativeText(data)
        message.exec()
            
if __name__ == "__main__":
    app = QApplication([])
    window = Window()
    window.show()
    app.exec()