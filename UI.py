# Create in 2019-05-29
# Project: Store data from Zhihu in Mysql Database
# Author: SHIELD_QIQI

import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5 import Qt
from ZhihuCrawler import *
from bar import *

class FirstUI(QWidget):
    def __init__(self):
        super().__init__()
        self.message = QMessageBox()
        self.EnterButton = QPushButton('开始爬取',self)
        self.EnterButton.setStyleSheet("font-size:20px;color:red;border: 3px solid blue;border-radius:20px")
        self.EnterButton.setGeometry(600,300,300,50)
        window_pale = QPalette()
        window_pale.setBrush(self.backgroundRole(), QBrush(QPixmap("./image/background.jpg")))
        self.setPalette(window_pale)
        self.initUI()
    def initUI(self):
        self.setGeometry(150, 50, 1510, 948)
        self.setWindowTitle('知乎大数据            copyright@qi.shield95@gamil.com')
        self.setWindowIcon(QIcon('image/ZhiHU.jpg'))
        self.EnterButton.clicked.connect(self.EnterButtonClicked)
        self.show()
    def EnterButtonClicked(self):
        self.s = SecondUI()
        self.s.show()
        self.hide()
        self.message.setGeometry(750, 150, 1000, 250)
        self.message.information(self, "Notice", "如果数据已经爬取，本次将直接加载原有数据", QMessageBox.Yes | QMessageBox.No)

class SecondUI(QWidget):
    def __init__(self):
        super().__init__()

        self.AnsID = 0

        # 创建界面按钮表格等模块
        self.button0 = QPushButton('', self)
        self.button0.setStyleSheet("font-size:1px;color:red;border: 3px solid white;border-radius:20px")
        self.button0.setGeometry(10,10,380,928)
        self.frame = QFrame()
        self.frame.setStyleSheet("font-size:1px;color:red;border: 3px solid white;border-radius:20px")
        self.frame.setGeometry(10,10,380,928)
        self.lable = QLabel(self)
        self.lable.setStyleSheet("border: 2px solid white;border-radius:20px")
        self.lable.setGeometry(400,10,1100,928)
        self.lable.hide()
        self.button1 = QPushButton('显示该问题下所有回答', self)
        self.button1.setStyleSheet("font-size:20px;color:red;border: 3px solid blue;border-radius:20px")
        self.button1.setGeometry(50, 100, 300, 50)
        self.button2 = QPushButton('显示该回答下所有评论', self)
        self.button2.setStyleSheet("font-size:20px;color:red;border: 3px solid blue;border-radius:20px")
        self.button2.setGeometry(50, 200, 300, 50)
        self.button3 = QPushButton('显示该评论下词云', self)
        self.button3.setStyleSheet("font-size:20px;color:red;border: 3px solid blue;border-radius:20px")
        self.button3.setGeometry(50, 300, 300, 50)
        self.button4 = QPushButton('回答作者标签词云', self)
        self.button4.setStyleSheet("font-size:20px;color:red;border: 3px solid blue;border-radius:20px")
        self.button4.setGeometry(50, 400, 300, 50)
        self.button5 = QPushButton('评论词性分析', self)
        self.button5.setStyleSheet("font-size:20px;color:red;border: 3px solid blue;border-radius:20px")
        self.button5.setGeometry(50, 500, 300, 50)
        self.button6 = QPushButton('回答作者标签分析', self)
        self.button6.setStyleSheet("font-size:20px;color:red;border: 3px solid blue;border-radius:20px")
        self.button6.setGeometry(50, 600, 300, 50)
        self.MyTable = QTableWidget(0, 7)
        self.MyTable.setGeometry(400,10,1100,928)
        self.MyTable.setHorizontalHeaderLabels(['回答ID','作者名','作者标签', '赞同数','评论数', '感谢数','回答链接'])
        self.MyTable.horizontalHeader().setSectionResizeMode(QHeaderView.Interactive)
        self.MyTable.horizontalHeader().setStretchLastSection(True)
        self.MyTable.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeToContents)
        self.MyTableForComment = QTableWidget(0, 4)
        self.MyTableForComment.setGeometry(400,10,1100,928)
        self.MyTableForComment.setHorizontalHeaderLabels(['回答ID','评论ID','评论人昵称','评论'])
        self.MyTableForComment.horizontalHeader().setStretchLastSection(True)
        self.MyTableForComment.horizontalHeader().setSectionResizeMode(3, QHeaderView.Interactive)
        # 导出数据至 回答表格
        answer_num = mysql.cur.execute("select * from answer")
        for i in range(0,answer_num):
            rowcont = self.MyTable.rowCount()
            self.MyTable.insertRow(rowcont)
            TupleData = mysql.cur.fetchone()
            for j in range(0,7):
                self.MyTable.setItem(rowcont,j,QTableWidgetItem(str(TupleData[j])))
        self.MyTable.setWindowTitle("该问题下所有回答")

        self.initUI()
        window_pale = QPalette()
        window_pale.setBrush(self.backgroundRole(), QBrush(QPixmap("./image/background2.png")))
        self.setPalette(window_pale)

    def initUI(self):
        self.setGeometry(150, 50, 1510, 948)
        self.setWindowTitle('知乎大数据')
        self.setWindowFlag(Qt.Qt.FramelessWindowHint)
        self.setWindowIcon(QIcon('image/ZhiHU.jpg'))


        self.button3.clicked.connect(self.button3Clicked)
        self.button1.clicked.connect(self.button1Clicked)
        self.button2.clicked.connect(self.button2Clicked)
        self.button4.clicked.connect(self.button4Clicked)
        self.button5.clicked.connect(self.button5Clicked)
        self.button6.clicked.connect(self.button6Clicked)
        self.MyTable.itemClicked.connect(self.changeAnsID)

        # 设置界面布局
        hbox = QHBoxLayout(self)
        hbox.addWidget(self.frame)
        hbox.setSpacing(400)
        hbox.addWidget(self.MyTable)
        hbox.addWidget(self.MyTableForComment)
        self.MyTableForComment.hide()
        self.setLayout(hbox)

        self.show()

    # 槽函数
    def button3Clicked(self):
        self.MyTable.hide()
        self.MyTableForComment.hide()
        self.frame.hide()
        self.lable.setStyleSheet("background-image: url(./image/wordcloud.png)")
        self.lable.show()
    def button1Clicked(self):
        self.MyTable.show()
        self.frame.show()
        self.lable.hide()
        self.MyTableForComment.hide()
    def button2Clicked(self):
        # 清空表格中原有数据
        self.MyTableForComment.clearContents()
        # 导出数据至 评论表格
        comment_num = mysql.cur.execute("select * from comments")
        rowcont = 0
        for i in range(0,comment_num):
            TupleData = mysql.cur.fetchone()
            if str(TupleData[0]) == str(self.AnsID):
                self.MyTableForComment.insertRow(rowcont)
                for j in range(0,4):
                    self.MyTableForComment.setItem(rowcont,j,QTableWidgetItem(str(TupleData[j])))
                rowcont += 1
        self.MyTableForComment.setWindowTitle("该回答下所有评论")
        self.MyTableForComment.show()
        self.MyTable.hide()
        self.frame.show()
        self.lable.hide()
        print("")
    def button4Clicked(self):
        self.MyTable.hide()
        self.MyTableForComment.hide()
        self.frame.hide()
        self.lable.setStyleSheet("background-image: url(./image/authorcloud.png)")
        self.lable.show()
    def button5Clicked(self):
        self.MyTable.hide()
        self.MyTableForComment.hide()
        self.frame.hide()
        self.lable.setStyleSheet("background-image: url(./image/comment.png)")
        self.lable.show()
    def button6Clicked(self):
        self.MyTable.hide()
        self.MyTableForComment.hide()
        self.frame.hide()
        self.lable.setStyleSheet("background-image: url(./image/lable.png)")
        self.lable.show()
    def changeAnsID(self, Item =None):
        if Item==None:
            return
        self.AnsID = Item.text()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = FirstUI()
    sys.exit(app.exec_())