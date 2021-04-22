import os
import sys

from PyQt5.QtCore import QTimer, QPropertyAnimation, QRect, QPoint, QEasingCurve
from PyQt5.QtWidgets import QApplication, QMainWindow, QGraphicsOpacityEffect, QSpacerItem

from Ui_ZhkuMainWindow import Ui_ZhkuMainWindow
from contentWidget import ContentWidget
from loginWidget import LoginWidget
from zhkuScoreTable import ScoreTableWidget


class ZhkuMainWindow(QMainWindow, Ui_ZhkuMainWindow):

    def __init__(self, *args, **kwargs):
        super(ZhkuMainWindow, self).__init__(*args, **kwargs)
        self.setupUi(self)
        # 属性初始化
        self.ContentWidget = ContentWidget(self)

        self.LoginWidget = LoginWidget(self)
        self.ScoreTableWidget = ScoreTableWidget(self)

        self.ScoreTableWidget.hide()
        self.ContentWidget.hide()
        #

        self.widgetOpacity = 0

        self.opacityEffect = QGraphicsOpacityEffect()

        # connect
        self.ScoreTableWidget.pushButton.clicked.connect(self.retrieveResults)
        # 调用函数
        self.login()

    def retrieveResults(self):

        t = QTimer(self)
        t.timeout.connect(
            lambda: self.LoginWidget.spider.Get_SemesterScore(self.ScoreTableWidget.comboBox.currentText(), \
                                                              {'第1学期': '0', '第2学期': '1'}[
                                                                  self.ScoreTableWidget.comboBox_2.currentText()]
                                                              , self.ScoreTableWidget.radioButton_2.isChecked(), \
                                                              [self.ScoreTableWidget.horizontalLayout_5.itemAt(
                                                                  c).widget().isChecked() for c in
                                                               range(self.ScoreTableWidget.horizontalLayout_5.count())], \
                                                              self.ScoreTableWidget.radioButton_6.isChecked(),\
                                                              self
                                                              )
        )
        t.setSingleShot(True)
        t.start()

    def checkResults(self):
        """
        登录 后 查询成绩 对应的是widget_2
        :return:
        """
        # tab

        # self.horizontalLayout_2.setStretchFactor(self.ScoreTableWidget, 1)
        self.ScoreTableWidget.show()
        ani = QPropertyAnimation(self.ScoreTableWidget, b'geometry', self)
        ani.setDuration(2000)
        # ani.setEasingCurve(QEasingCurve.InQuint)
        ani.setStartValue(
            QRect(self.widget.pos().x() + self.widget.width(), self.ScoreTableWidget.pos().y(), 0,
                  self.height()))
        ani.setEndValue(
            QRect(self.widget.pos().x() + self.widget.width(), self.ScoreTableWidget.pos().y(),
                  self.width() - self.widget.width(),
                  self.height()))
        ani.start()
        ani.finished.connect(lambda:
                             self.horizontalLayout_3.addWidget(self.ScoreTableWidget)
                             )
        ani.finished.connect(lambda: self.removeSpacer(self.horizontalLayout_2))
        e = QGraphicsOpacityEffect()
        e.setOpacity(0.6)
        t = QTimer()

        self.ScoreTableWidget.setGraphicsEffect(e)

    def fadeWidget(self, w, t, *args):
        if not t.isActive():

            w.setGraphicsEffect(self.opacityEffect)
            t.setInterval(80)
            t.timeout.connect(lambda: self.fadeWidget(w, t, *args))
            t.start()
        else:

            if self.widgetOpacity >= 0.05:
                self.widgetOpacity -= 0.05
                self.opacityEffect.setOpacity(self.widgetOpacity)
            else:
                # w.hide()
                t.stop()
                # w.lower()
                self.widgetOpacity = 0
                for arg in args:
                    if arg != None:
                        arg()

    def emergedWidget(self, w, t, *args):

        if not t.isActive():
            w.setGraphicsEffect(self.opacityEffect)
            t.setInterval(60)
            t.timeout.connect(lambda: self.emergedWidget(w, t, *args))
            t.start()
            self.widgetOpacity = 0
        else:

            if self.widgetOpacity <= 0.95:
                self.widgetOpacity += 0.05
                self.opacityEffect.setOpacity(self.widgetOpacity)
            else:
                w.show()
                w.raise_()
                t.stop()
                self.widgetOpacity = 1
                for arg in args:
                    if arg != None:
                        arg()

    def loginShow(self):

        self.ScoreTableWidget.hide()
        t = QTimer(self)
        t2 = QTimer(self)

        self.fadeWidget(self.ContentWidget, t, self.ContentWidget.hide,
                        self.setStyleSheet("""
        QMainWindow#ZhkuMainWindow{
border-image:url(:/img/img/ece414499b12f26fc1cdc8ccd7e019ea.jpg)}
        """), lambda: self.login(False))

        # self.LoginWidget.t2.timeout.connect(lambda: self.LoginWidget.fadedWidget(bg, False))
        # self.LoginWidget.t2.timeout.connect(lambda: self.ContentWidget.hide())

        self.removeSpacer(self.horizontalLayout_2)
        self.LoginWidget.spider.zk_user.home_cookies = {}
        if os.path.exists('cookies.cok'):
            os.remove('cookies.cok')

    def removeSpacer(self, layout):
        for i in range(layout.count()):
            item = layout.itemAt(i)
            # print(item)
            if type(item) == QSpacerItem:
                layout.removeItem(item)
        print()

    def contentShow(self):

        # 去除 弹簧

        self.LoginWidget.hide()
        self.removeSpacer(self.horizontalLayout_2)
        self.widget_2.show()
        self.horizontalLayout_2.setStretchFactor(self.widget, 3)
        self.horizontalLayout_2.setStretchFactor(self.widget_2, 7)

        self.horizontalLayout.addWidget(self.ContentWidget)

        self.ContentWidget.show()
        pass

        """
        变大的原因是 margin的问题
        """

        #

    def login(self, auto=True):
        self.horizontalLayout_2.setStretchFactor(self.widget, 6)

        self.horizontalLayout_2.setStretchFactor(self.widget_2, 3)
        self.LoginWidget.show()
        self.horizontalLayout_3.addWidget(self.LoginWidget)
        self.horizontalLayout_2.addStretch(1)

        t = QTimer(self)
        self.emergedWidget(self, t, lambda: self.LoginWidget.autoLogin(auto),self.widget_2.show)

        pass

    def closeEvent(self, a0) -> None:
        self.close()


if __name__ == '__main__':
    s1='123ad'
    s2='345'
    s3=s1
    s1+='sa'
    print(s3)
    # print(s1.title())
    # app = QApplication(sys.argv)
    # win = ZhkuMainWindow()
    # win.show()
    # sys.exit(app.exec_())
