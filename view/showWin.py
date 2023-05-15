import os
from threading import Thread

from PyQt5.QtCore import pyqtSignal, Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QWidget, QHeaderView, QTableWidgetItem, QAbstractItemView, QMenu, QAction, QMessageBox,QFileDialog
from ui.Ui_showWin import Ui_Form
from view.addWin import AddWin
from util.dbutil import DBHelp
from util.common_util import msg_box, DELETE_ICON, EDIT_ICON

class ShowWin(Ui_Form, QWidget):
    query_done_signal = pyqtSignal(list)

    def resetWin(self,table_name):
        self.table_name = table_name
        db = DBHelp()
        self.header = db.get_header(table_name=table_name)
        self.primary_key = db.get_primary_key(table_name=table_name)
        del db
        self.resetUi(self,self.header)
        self.add_win = None
        self.edit_win = None
        self.init_ui()
        # self.init_slot()
        self.init_data()

    def __init__(self,table_name):
        super(ShowWin, self).__init__()
        self.table_name = table_name
        db = DBHelp()
        self.header = db.get_header(table_name=table_name)
        self.primary_key = db.get_primary_key(table_name=table_name)
        del db
        self.setupUi(self,self.header)
        self.add_win = None
        self.edit_win = None
        self.init_ui()
        self.init_slot()
        self.init_data()

    def init_ui(self):
        self.tableWidget.verticalHeader().setVisible(False)
        # self.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
        # 获取水平头部
        # 获取第0列的所有标签文本长度
        model = self.tableWidget.model()
        length = 0
        for i in range(model.columnCount()):
            length += len(model.headerData(i, Qt.Horizontal))
        win_width = self.width()
        if length*20 <win_width:
            # 如果表格列宽足够大，则使用QHeaderView.Stretch模式以填充所有可用空间
            self.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        else:
            # 如果表格列宽太小以至于无法容纳所有标签，则使用ResizeToContents模式来调整列宽以适应内容
            self.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
        print(length*20,win_width)

        self.tableWidget.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.tableWidget.setContextMenuPolicy(Qt.CustomContextMenu)
        self.tableWidget.customContextMenuRequested.connect(self.generate_menu)

    def generate_menu(self, pos):
        row_num = -1
        for i in self.tableWidget.selectionModel().selection().indexes():
            row_num = i.row()
        if row_num == -1:
            return
        menu = QMenu()
        edit_action = QAction(u'编辑记录')
        edit_action.setIcon(QIcon(EDIT_ICON))
        menu.addAction(edit_action)

        delete_action = QAction(u'删除记录')
        delete_action.setIcon(QIcon(DELETE_ICON))
        menu.addAction(delete_action)

        action = menu.exec_(self.tableWidget.mapToGlobal(pos))
        if action == edit_action:
            self.edit_win = AddWin(self.table_name,self.primary_key,header=self.header, win='edit', info=self.tableWidget.item(row_num, 0).text())
            self.edit_win.show()

        if action == delete_action:
            reply = QMessageBox.warning(self, '消息', '确定删除该记录吗?',QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
            if reply == QMessageBox.Yes:
                db = DBHelp()
                conditions = []
                for i in range(len(self.primary_key)):
                    conditions.append(self.tableWidget.item(row_num,i).text())
                db.delete_super(table_name=self.table_name, column_names=self.primary_key, conditions=conditions)
                db.db_commit()
                db.instance = None
                del db
                self.refresh_pushButton.click()
                msg_box(self, '提示', '删除记录操作成功!')

    def init_slot(self):
        self.query_done_signal.connect(self.show)
        self.search_pushButton.clicked.connect(lambda: self.btn_slot('search'))
        self.add_pushButton.clicked.connect(lambda: self.btn_slot('add'))
        self.refresh_pushButton.clicked.connect(lambda: self.btn_slot('refresh'))
        self.import_pushButton.clicked.connect(lambda: self.btn_slot('import'))
        self.export_pushButton.clicked.connect(lambda: self.btn_slot('export'))

    def init_data(self):
        self.get_info()

    def show(self, info_result):
        for i in range(self.tableWidget.rowCount()):
            self.tableWidget.removeRow(0)
        infos = info_result[1]
        for info in infos:
            self.tableWidget.insertRow(self.tableWidget.rowCount())
            for i in range(len(info)):
                self.tableWidget.setItem(self.tableWidget.rowCount() - 1, i, QTableWidgetItem(str(info[i])))

    def btn_slot(self, tag):
        if tag == 'add':
            self.add_win = AddWin(table_name= self.table_name,primary_key= self.primary_key,header=self.header)
            self.add_win.add_done_signal.connect(self.add_done)
            self.add_win.show()

        if tag == 'search':
            search_type = self.search_comboBox.currentText()
            search_content = self.search_content_lineEdit.text()
            if search_content == '':
                msg_box(self, '提示', '请输入搜索内容~')
                return
            db = DBHelp()
            count, res = db.query_super(table_name=self.table_name, column_names=[search_type],conditions=[search_content])
            if count == 0:
                msg_box(self, '提示', '您所搜索的记录不存在!')
                return
            self.show([count, res])

        if tag == 'refresh':
            self.get_info()

        if tag == 'import':
            options = QFileDialog.Options()
            file_name, _ = QFileDialog.getOpenFileName(self, "选择文件", "", "Excel Files (*.xlsx *.xls)", options=options)
            db = DBHelp()
            res = db.import_to_sql(file_name=file_name,table_name=self.table_name)
            del db
            self.refresh_pushButton.click()
            if res == True:
                msg_box(self, '提示', '信息成功导入!')
                return
            else:
                msg_box(self, '提示', '信息导入失败!')
                return
        if tag == 'export':
            file_name, _ = QFileDialog.getSaveFileName(self, 'Save file', os.getcwd(), "Excel files (*.xlsx)")
            db = DBHelp()
            res = db.export_to_excel(table_name=self.table_name,file_name=file_name)
            del db
            if res == True:
                msg_box(self, '提示', '信息成功导出到'+file_name+'!')
                return
            else:
                msg_box(self, '提示', '信息导出失败!')
                return

    def get_info(self):
        th = Thread(target=self.info_th)
        th.start()

    def info_th(self):
        db = DBHelp()
        count, res = db.query_all(table_name=self.table_name)
        self.query_done_signal.emit([count, res])

    def add_done(self):
        self.refresh_pushButton.click()