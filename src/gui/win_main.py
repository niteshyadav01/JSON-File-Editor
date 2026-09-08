# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'win_main.ui'
##
## Created by: Qt User Interface Compiler version 6.9.3
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QAction, QBrush, QColor, QConicalGradient,
    QCursor, QFont, QFontDatabase, QGradient,
    QIcon, QImage, QKeySequence, QLinearGradient,
    QPainter, QPalette, QPixmap, QRadialGradient,
    QTransform)
from PySide6.QtWidgets import (QAbstractItemView, QApplication, QHBoxLayout, QHeaderView,
    QMainWindow, QMenu, QMenuBar, QPlainTextEdit,
    QPushButton, QSizePolicy, QSpacerItem, QSplitter,
    QStatusBar, QTreeView, QVBoxLayout, QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(1000, 650)
        self.actionopen = QAction(MainWindow)
        self.actionopen.setObjectName(u"actionopen")
        self.actionedit = QAction(MainWindow)
        self.actionedit.setObjectName(u"actionedit")
        self.actionSave_As = QAction(MainWindow)
        self.actionSave_As.setObjectName(u"actionSave_As")
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.verticalLayout = QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.buttonLayout = QHBoxLayout()
        self.buttonLayout.setObjectName(u"buttonLayout")
        self.btnAdd = QPushButton(self.centralwidget)
        self.btnAdd.setObjectName(u"btnAdd")

        self.buttonLayout.addWidget(self.btnAdd)

        self.btnDelete = QPushButton(self.centralwidget)
        self.btnDelete.setObjectName(u"btnDelete")

        self.buttonLayout.addWidget(self.btnDelete)

        self.buttonSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.buttonLayout.addItem(self.buttonSpacer)


        self.verticalLayout.addLayout(self.buttonLayout)

        self.splitter = QSplitter(self.centralwidget)
        self.splitter.setObjectName(u"splitter")
        self.splitter.setOrientation(Qt.Orientation.Horizontal)
        self.listView = QTreeView(self.splitter)
        self.listView.setObjectName(u"listView")
        self.listView.setAlternatingRowColors(True)
        self.listView.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.splitter.addWidget(self.listView)
        self.listView.header().setMinimumSectionSize(100)
        self.listView.header().setDefaultSectionSize(250)
        self.listView.header().setStretchLastSection(True)
        self.jsonPreview = QPlainTextEdit(self.splitter)
        self.jsonPreview.setObjectName(u"jsonPreview")
        self.jsonPreview.setReadOnly(True)
        self.splitter.addWidget(self.jsonPreview)

        self.verticalLayout.addWidget(self.splitter)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 1000, 33))
        self.menuFile = QMenu(self.menubar)
        self.menuFile.setObjectName(u"menuFile")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.menubar.addAction(self.menuFile.menuAction())
        self.menuFile.addAction(self.actionopen)
        self.menuFile.addAction(self.actionedit)
        self.menuFile.addAction(self.actionSave_As)

        self.retranslateUi(MainWindow)
        self.actionopen.triggered.connect(MainWindow.open_file)
        self.actionedit.triggered.connect(MainWindow.save_file)
        self.actionSave_As.triggered.connect(MainWindow.save_as)
        self.btnAdd.clicked.connect(MainWindow.add_item)
        self.btnDelete.clicked.connect(MainWindow.delete_item)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"JSON Editor", None))
        self.actionopen.setText(QCoreApplication.translate("MainWindow", u"Upload", None))
        self.actionedit.setText(QCoreApplication.translate("MainWindow", u"Save", None))
        self.actionSave_As.setText(QCoreApplication.translate("MainWindow", u"Save As", None))
        self.btnAdd.setText(QCoreApplication.translate("MainWindow", u"Add", None))
        self.btnDelete.setText(QCoreApplication.translate("MainWindow", u"Delete", None))
        self.jsonPreview.setPlaceholderText(QCoreApplication.translate("MainWindow", u"JSON preview", None))
        self.menuFile.setTitle(QCoreApplication.translate("MainWindow", u"File", None))
    # retranslateUi

