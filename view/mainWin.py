"""
coding:utf-8
file: main_window.py
@author: jiangwei
@contact: jiangwei_1994124@163.com
@time: 2020/5/9 19:52
@desc:
"""
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QMainWindow, QMessageBox, QWidget
from ui.Ui_mainWin import Ui_MainWindow
from util.common_util import  APP_ICON, SYS_STYLE
from view.showWin import ShowWin

# noinspection PyCallByClass
class MainWindow(Ui_MainWindow, QMainWindow):

    def __init__(self,login=None, username=None, role=None):
        super(MainWindow, self).__init__()
        self.setupUi(self)
        self.is_change_user = False
        self.username = username
        self.login_win = login
        self.role = role
        self.init_slot()
        self.init_ui()

    def init_ui(self):
        self.pushButton.setProperty('class', 'Aqua')
        self.pushButton.setMinimumWidth(60)
        self.setStyleSheet(SYS_STYLE)
        self.setWindowIcon(QIcon(APP_ICON))
        self.setWindowTitle('工资结算系统-Version 1.0.0.0 Beta')
        # 获取第一行对应的 QTreeWidgetItem 对象,将第一行设为当前选中项
        first_item = self.treeWidget.topLevelItem(0)
        self.treeWidget.setCurrentItem(first_item)

        self.current_username_label.setText(self.username)
        self.current_role_label.setText(self.role)
        self.stackedWidget.removeWidget(self.page)
        self.stackedWidget.removeWidget(self.page_2)
        self.stackedWidget.addWidget(QWidget())
        self.stackedWidget.addWidget(ShowWin(table_name="员工基本信息表"))
        if self.role == '普通用户':
            self.treeWidget.topLevelItem(0).setHidden(True)
            self.treeWidget.topLevelItem(1).setHidden(True)
            self.treeWidget.topLevelItem(2).setHidden(True)
        if self.role == '管理员':
            self.treeWidget.topLevelItem(0).setHidden(True)

    def init_slot(self):
        self.treeWidget.currentItemChanged.connect(self.item_changed)
        self.pushButton.clicked.connect(self.log_out)

    def item_changed(self):
        current_table = self.treeWidget.currentItem().text(0)
        if isinstance(self.stackedWidget.widget(1),ShowWin):
            if self.treeWidget.currentItem().parent() is not None:
                self.stackedWidget.setCurrentIndex(1)
                self.stackedWidget.widget(1).resetWin(table_name=current_table)
            else:
                self.stackedWidget.setCurrentIndex(0)

    def log_out(self):
        self.is_change_user = True
        self.close()

    def closeEvent(self, event):
        if self.is_change_user:
            reply = QMessageBox.question(self, '消息', '确定退出当前账号吗?',
                                         QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        else:
            reply = QMessageBox.question(self, '消息', '确定退出系统吗?',
                                         QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            event.accept()
            if self.is_change_user:
                self.login_win.show()
        else:
            event.ignore()
            self.is_change_user = False
