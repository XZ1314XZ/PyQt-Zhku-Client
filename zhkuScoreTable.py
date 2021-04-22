#  Copyright (c) 2020. Lorem ipsum dolor sit amet, consectetur adipiscing elit.
#  Morbi non lorem porttitor neque feugiat blandit. Ut vitae ipsum eget quam lacinia accumsan.
#  Etiam sed turpis ac ipsum condimentum fringilla. Maecenas magna.
#  Proin dapibus sapien vel ante. Aliquam erat volutpat. Pellentesque sagittis ligula eget metus.
#  Vestibulum commodo. Ut rhoncus gravida arcu.
import time

from PyQt5.QtWidgets import QWidget

from Ui_ScoreTableWidget import Ui_Form


class ScoreTableWidget(QWidget, Ui_Form):
    def __init__(self, *args, **kwargs):
        super(ScoreTableWidget, self).__init__(*args, **kwargs)
        self.setupUi(self)
        """
        初始化year 和 semester
        """
        self.year = time.localtime(time.time())[0]
        self.mouth = time.localtime(time.time())[1]
        if self.mouth > 8 or self.mouth < 3:
            self.options_seme = '0'
        else:
            self.options_seme = '1'
        self.comboBox.addItems([str(i) for i in range(self.year,self.year-8,-1)])
        self.comboBox_2.addItem('第1学期')
        if self.options_seme=='1':
            self.comboBox_2.addItem('第2学期')

        self.comboBox.currentIndexChanged.connect(self.changeCombox2)

    def changeCombox2(self):
        """
        当选择小于当年的第一学期时 要出现第二学期
        :return:
        """
        if self.options_seme=='0':
            if self.comboBox.currentIndex()>0 :
                self.comboBox_2.clear()
                self.comboBox_2.addItem('第1学期')
                self.comboBox_2.addItem('第2学期')
            else :
                self.comboBox_2.clear()
                self.comboBox_2.addItem('第1学期')