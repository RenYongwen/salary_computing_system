from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Form(object):
    
    def resetUi(self,Form, header):
        self.header = header
        self.tableWidget.setColumnCount(len(self.header))
        self.tableWidget.setRowCount(0)
        self.tableWidget.setHorizontalHeaderLabels(self.header)
        self.search_comboBox.clear()
        for i in range(len(self.header)):
            self.search_comboBox.addItem("")
        self.retranslateUi(Form)

    def setupUi(self,Form, header):
        Form.setObjectName("Form")
        Form.resize(644, 452)
        self.header = header
        self.gridLayout = QtWidgets.QGridLayout(Form)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setObjectName("gridLayout")

        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        
        self.search_comboBox = QtWidgets.QComboBox(Form)
        self.search_comboBox.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.search_comboBox.setStyleSheet("font: 12pt \"宋体\";")
        self.search_comboBox.setObjectName("search_comboBox")
        for i in range(len(self.header)):
            self.search_comboBox.addItem("")
        
        self.search_content_lineEdit = QtWidgets.QLineEdit()

        self.search_pushButton = self.create_button("search_pushButton", "搜索")
        self.refresh_pushButton = self.create_button("refresh_pushButton", "刷新")
        self.add_pushButton = self.create_button("add_pushButton", "添加")
        self.import_pushButton = self.create_button("import_pushButton", "导入")
        self.export_pushButton = self.create_button("export_pushButton", "导出")
        
        # 将按钮添加到水平布局
        self.horizontalLayout.addWidget(self.search_comboBox)
        self.horizontalLayout.addWidget(self.search_content_lineEdit)
        self.horizontalLayout.addWidget(self.search_pushButton)
        self.horizontalLayout.addWidget(self.refresh_pushButton)
        self.horizontalLayout.addWidget(self.add_pushButton)
        self.horizontalLayout.addWidget(self.import_pushButton)
        self.horizontalLayout.addWidget(self.export_pushButton)

        self.verticalLayout.addLayout(self.horizontalLayout)

        self.tableWidget = QtWidgets.QTableWidget(Form)
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setColumnCount(len(self.header))
        self.tableWidget.setRowCount(0)
        self.tableWidget.setHorizontalHeaderLabels(self.header)

        self.verticalLayout.addWidget(self.tableWidget)
        self.gridLayout.addLayout(self.verticalLayout, 0, 0, 1, 1)
     

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def create_button(self, name, text):
        button = QtWidgets.QPushButton(text)
        button.setStyleSheet("font: 12pt \"宋体\";")
        button.setObjectName(name)
        button.setProperty("class","Aqua");
        button.setMinimumWidth(60)

        return button
    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        for i in range(len(self.header)):
            self.search_comboBox.setItemText(i, _translate("Form", self.header[i]))
        self.search_pushButton.setText(_translate("Form", "搜索"))
        self.refresh_pushButton.setText(_translate("Form", "刷新"))
        self.add_pushButton.setText(_translate("Form", "添加"))
        self.import_pushButton.setText(_translate("Form", "导入"))
        self.export_pushButton.setText(_translate("Form", "导出"))
        for i, head in enumerate(self.header):
            self.tableWidget.horizontalHeaderItem(i).setText(_translate("Form", head))
