import threading
import time
from typing import Union

from PyQt5 import QtCore
from PyQt5.QtCore import QPoint, QSize, QPropertyAnimation, QRect, pyqtSignal, pyqtSlot, QTimer
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtWidgets import QLineEdit, QLabel, QGraphicsEffect, QGraphicsOpacityEffect


class ShowVCodeLineEdit(QLineEdit):
    def __init__(self, *args, **kwargs):
        super(ShowVCodeLineEdit, self).__init__(*args, **kwargs)

        self.par = self.parent().parent().parent().parent()
        self.codeImage = QPixmap("img/yzm.jpg")
        self.codeImage = self.codeImage.scaled(self.width() / 2, self.height())
        self.codeLabel = QLabel(self.parent())
        self.codeLabel.resize(self.codeImage.size())
        self.codeLabel.hide()
        self.codeLabel.setPixmap(self.codeImage)
    def mouseDoubleClickEvent(self, a0) -> None:
        self.par.spider.zk_user.Get_login_cookies()
        self.par.spider.zk_user.Get_code()
        codeImage = QPixmap("img/yzm.jpg")
        codeImage = codeImage.scaled(self.width() / 2, self.height())
        self.codeLabel.resize(codeImage.size())
        self.codeLabel.setPixmap(codeImage)
        self.codeLabel.move(QPoint(self.pos().x() + self.width() / 2, self.pos().y()))
    def focusInEvent(self, a0) -> None:
        """
        改写 焦点事件 要弹出 验证码
        """
        super().focusInEvent(a0)
        """
        线程更新一次验证码
        """

        def getCode(self):
            print(self)
            self.par.spider.zk_user.Get_login_cookies()
            self.par.spider.zk_user.Get_code()
            codeImage = QPixmap("img/yzm.jpg")
            codeImage = codeImage.scaled(self.width() / 2, self.height())
            self.codeLabel.resize(codeImage.size())
            self.codeLabel.setPixmap(codeImage)
            self.codeLabel.move(QPoint(self.pos().x() + self.width() / 2, self.pos().y()))
            # self.a = QPropertyAnimation(self)
            # self.a.setTargetObject(self.codeLabel)
            # self.a.setPropertyName(b'geometry')
            # self.a.setDuration(1000)
            # self.a.setStartValue(QRect(self.pos().x() + self.width() / 2, self.pos().y(), 0, self.codeLabel.height()))
            # self.a.setEndValue(self.codeLabel.geometry())
            #
            self.codeLabel.show()

        if self.codeLabel.isHidden():
            t = threading.Thread(target=getCode, args=[self])
            t.start()



    def focusOutEvent(self, a0) -> None:
        super(ShowVCodeLineEdit, self).focusOutEvent(a0)
        if not self.codeLabel.isHidden():
            self.codeLabel.hide()
