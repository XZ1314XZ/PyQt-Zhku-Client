#  Copyright (c) 2020. Lorem ipsum dolor sit amet, consectetur adipiscing elit.
#  Morbi non lorem porttitor neque feugiat blandit. Ut vitae ipsum eget quam lacinia accumsan.
#  Etiam sed turpis ac ipsum condimentum fringilla. Maecenas magna.
#  Proin dapibus sapien vel ante. Aliquam erat volutpat. Pellentesque sagittis ligula eget metus.
#  Vestibulum commodo. Ut rhoncus gravida arcu.
import os

from PyQt5.QtCore import QTimer, QPoint, QEasingCurve, QPropertyAnimation, QSize
from PyQt5.QtWidgets import QWidget, QMessageBox, QGraphicsOpacityEffect, QSpacerItem

from Ui_Login import Ui_LoginUi
from zhkumain import zk_spider

BGSWITCHSPEED = 0.008
BGPRELOADSPEED = 0.04


class LoginWidget(QWidget, Ui_LoginUi):
    DEBUG = 0

    def __init__(self, *args, **kwargs):
        super(LoginWidget, self).__init__(*args, **kwargs)
        self.setupUi(self)
        self.startValue = ''
        self.par = self.parent()
        self.oe = QGraphicsOpacityEffect()

        if os.path.exists('userLogin.ini'):
            with open('userLogin.ini')as f:
                inf = eval(f.read())
                self.lineEdit_2.setText(inf['user'])
                self.lineEdit.setText(inf['pw'])
        else:
            self.lineEdit_2.setText('201810224331')
            self.lineEdit.setText('yujiecong1')
        # 初始化爬虫
        self.spider = zk_spider()
        # 定时器
        self.t = QTimer(self)  # 开始的加载背景1
        self.t2 = QTimer(self)  # 使背景1隐藏
        self.t3 = QTimer(self)  # 让背景2浮现
        # 动画
        self.widget_2Ani = QPropertyAnimation(self.par.widget_2, b"pos",)

        # 变量
        self.bgOpacity = 0

        # oe
        self.setGraphicsEffect(self.oe)
        # connect
        self.pushButton.clicked.connect(self.login)
        # 函数

        # 如已有 cookies则直接登录

    def login(self):
        """
        开始判断是否登录成功,若成功,执行动画
        """
        # 获取账号, 密码, 验证码
        user = self.lineEdit_2.text()
        pw = self.lineEdit.text()
        code = self.lineEdit_3.text()
        hot = self.checkBox.checkState()
        auto = self.checkBox_2.checkState()

        if self.DEBUG:
            self.loginAni()
        else:
            if os.path.exists('cookies.cok'):
                os.remove('cookies.cok')
            self.spider.checkCookiesAndTryLogin(user, pw, code, False)
            if self.spider.login_success:
                self.loginAni()
            else:
                QMessageBox.warning(self, '用户名或密码 或验证码错误', '用户名或密码 或验证码错误')

        """
        若记住密码
        """
        if self.checkBox.isChecked():
            with open('userLogin.ini', 'w') as f:
                f.write(str({'user': user, 'pw': pw}))
        # 耦合性太强了 麻烦分离 这里开始login了

        pass



    def loginAni(self):

        if not self.widget_2Ani.state():
            self.widget_2Animation()
            self.autoHide()

    def autoHide(self, login=True):
        # 开始切换到content
        if login:
            t = QTimer(self)
            t2 = QTimer(self.par)
            self.par.fadeWidget(self.par, t,
                                self.par.widget_2.hide,
                                self.par.widget_2.lower,
                                 self.par.contentShow,
                                lambda: self.par.emergedWidget(self.par.ContentWidget, t2),
                                lambda :self.par.setStyleSheet("""
                    QMainWindow#ZhkuMainWindow{
            border-image:url(:/img/img/72e13cfaff5836b02aa0b0553584c7c7.jpg)}
                    """)
                                )

        else:
            # 显示login
            # 去除 弹簧
            self.par.removeSpacer(self.par.horizontalLayout_2)
            """
            hide的先后顺序会导致变大变小
            """
            self.par.ContentWidget.hide()

            # 显示 父控件scoretable

    def widget_2Animation(self):
        self.widget_2Ani.setStartValue(QPoint(self.par.widget_2.x(), self.par.widget_2.y()))
        self.widget_2Ani.setEndValue(QPoint(self.par.widget.x(), self.par.widget.y()))
        self.widget_2Ani.setDuration(3000)
        self.widget_2Ani.setEasingCurve(QEasingCurve.InOutElastic)
        self.widget_2Ani.start()

    def autoLogin(self, login=True):
        """
        自动更换背景
        """

        if login:
            print('尝试自动登录')
            if self.spider.login_success:
                self.loginAni()
        else:
            pass