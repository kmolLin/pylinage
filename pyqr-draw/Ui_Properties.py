# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\Users\Roger\eric6\pyqr-draw\Properties.ui'
#
# Created by: PyQt5 UI code generator 5.6
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_properties(object):
    def setupUi(self, properties):
        properties.setObjectName("properties")
        properties.resize(241, 192)
        properties.setSizeGripEnabled(True)
        self.verticalLayout = QtWidgets.QVBoxLayout(properties)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label_3 = QtWidgets.QLabel(properties)
        self.label_3.setObjectName("label_3")
        self.horizontalLayout.addWidget(self.label_3)
        self.lineEdit_3 = QtWidgets.QLineEdit(properties)
        self.lineEdit_3.setObjectName("lineEdit_3")
        self.horizontalLayout.addWidget(self.lineEdit_3)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.checkBox = QtWidgets.QCheckBox(properties)
        self.checkBox.setObjectName("checkBox")
        self.verticalLayout.addWidget(self.checkBox)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.label_4 = QtWidgets.QLabel(properties)
        self.label_4.setObjectName("label_4")
        self.horizontalLayout_2.addWidget(self.label_4)
        self.lineEdit = QtWidgets.QLineEdit(properties)
        self.lineEdit.setObjectName("lineEdit")
        self.horizontalLayout_2.addWidget(self.lineEdit)
        self.label_5 = QtWidgets.QLabel(properties)
        self.label_5.setObjectName("label_5")
        self.horizontalLayout_2.addWidget(self.label_5)
        self.lineEdit_2 = QtWidgets.QLineEdit(properties)
        self.lineEdit_2.setObjectName("lineEdit_2")
        self.horizontalLayout_2.addWidget(self.lineEdit_2)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        spacerItem = QtWidgets.QSpacerItem(20, 64, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem)
        self.buttonBox = QtWidgets.QDialogButtonBox(properties)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.verticalLayout.addWidget(self.buttonBox)

        self.retranslateUi(properties)
        self.buttonBox.accepted.connect(properties.accept)
        self.buttonBox.rejected.connect(properties.reject)
        QtCore.QMetaObject.connectSlotsByName(properties)

    def retranslateUi(self, properties):
        _translate = QtCore.QCoreApplication.translate
        properties.setWindowTitle(_translate("properties", "Properties"))
        self.label_3.setText(_translate("properties", "Name:"))
        self.checkBox.setText(_translate("properties", "Draw Circle"))
        self.label_4.setText(_translate("properties", "Coordinates:"))
        self.label_5.setText(_translate("properties", ","))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    properties = QtWidgets.QDialog()
    ui = Ui_properties()
    ui.setupUi(properties)
    properties.show()
    sys.exit(app.exec_())

