from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QTextEdit, QScrollArea

class Ui_Form(object):

    def setupUi(self, Form, header):
        self.header = header
        Form.setObjectName("Form")
        Form.resize(610, 449)
        self.formLayout = QtWidgets.QFormLayout(Form)
        self.formLayout.setObjectName("formLayout")
        for i in range(len(self.header)):
            horizontalLayout = QtWidgets.QHBoxLayout()
            horizontalLayout.setObjectName(f"horizontalLayout_{i}")
            label = QtWidgets.QLabel(Form)
            label.setMinimumSize(QtCore.QSize(110, 0))
            label.setObjectName(f"label_{i}")
            horizontalLayout.addWidget(label)
            lineEdit = QtWidgets.QLineEdit(Form)
            lineEdit.setObjectName(f"lineEdit_{i}")
            horizontalLayout.addWidget(lineEdit)
            self.formLayout.addRow(horizontalLayout)
        self.add_pushButton = QtWidgets.QPushButton(Form)
        self.add_pushButton.setObjectName("add_pushButton")
        self.formLayout.addWidget(self.add_pushButton)

        scroll_area = QScrollArea()
        scroll_widget = QWidget()
        scroll_widget.setLayout(self.formLayout)
        scroll_area.setWidgetResizable(True)
        scroll_area.setWidget(scroll_widget)

        # 将滚动窗口添加到主窗口
        window_layout = QtWidgets.QFormLayout()
        window_layout.addWidget(scroll_area)
        self.setLayout(window_layout)

        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setWidget(self.formLayout.widget())

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        for i in range(self.formLayout.rowCount()-1):
            i,self.formLayout.itemAt(i).itemAt(0).widget().setText(_translate("Form", self.header[i]))
        self.add_pushButton.setText(_translate("Form", "添加"))
