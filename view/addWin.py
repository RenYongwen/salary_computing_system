from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QWidget
from ui.Ui_addWin import Ui_Form
from util.common_util import msg_box, APP_ICON, SYS_STYLE
from util.dbutil import DBHelp
from threading import Thread

class AddWin(Ui_Form, QWidget):
    add_done_signal = pyqtSignal()
    init_done_signal = pyqtSignal()

    def __init__(self,table_name,primary_key,header, win='add', info=None):
        self.header = header
        super(AddWin, self).__init__()
        self.setupUi(self,header=self.header)
        if win=='add':
            self.setWindowModality(Qt.ApplicationModal)
            self.setWindowFlags(Qt.WindowCloseButtonHint)
            self.setWindowTitle('添加窗口')
            self.add_pushButton.clicked.connect(self.add_info)
            self.setWindowIcon(QIcon(APP_ICON))
            self.add_pushButton.setProperty('class', 'Aqua')
            self.setStyleSheet(SYS_STYLE)
            self.table_name = table_name
            self.primary_key = primary_key
        else:
            self.info = info
            self.init_ui()
            self.current_info = list()
            self.init_done_signal.connect(self.init_data)
            self.add_pushButton.clicked.connect(self.update_info)
            th = Thread(target=self.get_info)
            self.table_name = table_name
            self.primary_key = primary_key
            th.start()

    def add_info(self):
        new_info = []
        for i in range(self.formLayout.rowCount()-1):
            new_info.append(self.formLayout.itemAt(i).itemAt(1).widget().text())
        if '' in new_info:
            msg_box(self, '错误', '请输入关键记录!')
            return
        db = DBHelp()
        count, res = db.query_super(table_name=self.table_name, column_names=self.primary_key, conditions=new_info)
        if count:
            msg_box(self, '错误', '已存在该记录!')
            return
        db.add_super(table_name=self.table_name,data=new_info)
        db.db_commit()
        db.instance = None
        del db
        self.add_done_signal.emit()
        self.close()
        msg_box(self, '提示', '添加新记录成功!')

    def init_ui(self):
        self.setWindowTitle('编辑窗口')
        self.setWindowModality(Qt.ApplicationModal)
        self.add_pushButton.setText('保存信息')
        self.setWindowIcon(QIcon(APP_ICON))
        self.setWindowFlags(Qt.WindowCloseButtonHint)
        self.add_pushButton.setProperty('class', 'Aqua')
        self.setStyleSheet(SYS_STYLE)
        self.add_pushButton.setMinimumWidth(60)

    def get_info(self):
        db = DBHelp()
        count, res = db.query_all(table_name=self.table_name)
        self.current_info = list(res[0])
        self.init_done_signal.emit()
        db.instance = None
        del db

    def init_data(self):
        for i in range(len(self.current_info)):
            self.formLayout.itemAt(i).itemAt(1).widget().setText(str(self.current_info[i]))

    def update_info(self):
        new_info = []
        for i in range(len(self.current_info)):
            new_info.append(self.formLayout.itemAt(i).itemAt(1).widget().text())
        if '' in new_info:
            msg_box(self, '错误', '关键信息不能为空!')
            return
        is_update = False
        for new_inf in new_info:
            if new_inf not in self.current_info:
                db = DBHelp()
                db.update_super(table_name=self.table_name, column_names=self.primary_key, conditions=self.current_info,data=new_info)
                db.db_commit()
                db.instance = None
                del db
                is_update = True
        if is_update:
                msg_box(self, '提示', '图书信息更新成功!')
        self.close()
