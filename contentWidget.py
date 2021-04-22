#  Copyright (c) 2020. Lorem ipsum dolor sit amet, consectetur adipiscing elit.
#  Morbi non lorem porttitor neque feugiat blandit. Ut vitae ipsum eget quam lacinia accumsan.
#  Etiam sed turpis ac ipsum condimentum fringilla. Maecenas magna.
#  Proin dapibus sapien vel ante. Aliquam erat volutpat. Pellentesque sagittis ligula eget metus.
#  Vestibulum commodo. Ut rhoncus gravida arcu.

from PyQt5.QtWidgets import QWidget

from Ui_Content import Ui_Content


class ContentWidget(QWidget, Ui_Content):
    def __init__(self, *args, **kwargs):
        super(ContentWidget, self).__init__(*args, **kwargs)
        self.setupUi(self)
        self.par=self.parent()

        # connect
        self.pushButton_3.clicked.connect(self.par.loginShow)
        self.pushButton_24.clicked.connect(self.par.checkResults)


