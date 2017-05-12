# -*- coding: utf-8 -*-

"""
Module implementing MainWindow.
"""

from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from math import *
from Properties import PropertiesDialog

from Ui_test import Ui_MainWindow



        

class DynamicCanvas(QGraphicsScene):
    def __init__(self, parent=None):
        super(DynamicCanvas, self).__init__(parent)
        self.setSceneRect(-10000, -10000, 20000, 20000)
        self.PointItemList = list()
        self.LineItemList = list()
        self.ChainItemList = list()

    

    
class DynamicCanvasView(QGraphicsView):
    def __init__(self, parent=None):
        super(DynamicCanvasView, self).__init__(DynamicCanvas(), parent)
        self.setViewportUpdateMode(QGraphicsView.MinimalViewportUpdate)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.originPos = self.mapToScene(QPoint(self.width()/2, self.height()/2))
        self.Factor = 2.
        self.minFactor = .25
        self.maxFactor = 8.
        self.pointxy = QPointF(0., 0.)
        self.isDrag = False
    def mousePressEvent(self, event):
        super(DynamicCanvasView, self).mousePressEvent(event)
        if event.buttons()==Qt.MiddleButton:
            self.pointxy = self.mapToScene(event.pos())
            self.isDrag = True
    
    def mouseMoveEvent(self, event):
        super(DynamicCanvasView, self).mouseMoveEvent(event)
        if self.isDrag == True:
            self.centerOn(self.pointxy-self.mapToScene(event.pos()))
    def mouseReleaseEvent(self, event):
        super(DynamicCanvasView, self).mouseReleaseEvent(event)
        self.isDrag = False




class MainWindow(QMainWindow, Ui_MainWindow):
    """
    Class documentation goes here.
    """
    def __init__(self, parent=None):
        """
        Constructor
        
        @param parent reference to the parent widget
        @type QWidget
        """
        super(MainWindow, self).__init__(parent)
        self.setupUi(self)
        self.initform()
        angel = pi/4
        
        #self.matrix = QMatrix()
        #self.matrix.setMatrix(1, 2, 1, 1, 0, 0)
        self.pan = QPen(Qt.green, 3)
        self.DC = DynamicCanvas()
        self.DCV = DynamicCanvasView()
        self.graphics.addWidget(self.DCV)
        
        self.DCV.setScene(self.DC)
        self.transform =QTransform(2*cos(angel),  2*sin(angel), 2*-sin(angel), 2*cos(angel), 0, 0)
        #self.graphicsView.setTransform(self.transform)
        #text = self.DC.addText("Hello, world!")
        #text.setFlags(QGraphicsItem.ItemIsSelectable | QGraphicsItem.ItemIsMovable)  
        #text.setPos(QPointF(0., 0.))
        #line = self.DC.addLine(1, 1, 10, 10)
        #line.setFlag(QGraphicsItem.ItemIsSelectable)
        #line.setPos(QPointF(0., 0.))
        #ell = self.DC.addEllipse(0, 0, 30, 30, self.pan)
        #ell.setFlag(QGraphicsItem.ItemIsSelectable)
        #ell.setPos(QPointF(10., 10.))
        
    def initform(self):
        partList = ["Point", "Link"]
        self.partListBox.addItems(partList)
        self.partListBox.setCurrentIndex(len(partList) - 1)
    
        ##COMBOBOX setting
        
        
        
        ##Button setting
        self.AddButton.clicked.connect(self.AddPoint)
        self.PropertiesButton.clicked.connect(self.properties)
        self.LinkButton.clicked.connect(self.addlink)
        
    
    def addlink(self):
        self.link = self.DC.addLine(0, 0, 100, 100)
        self.link.setFlags(QGraphicsItem.ItemIsSelectable | QGraphicsItem.ItemIsMovable)
        self.link.setPos(QPointF(0., 0.))
    
    def properties(self):
        b = self.DC.items()
        points = [e.pos() for e in b if type(e)==QGraphicsEllipseItem]
        linePoint = [e.pos() for e in b if type(e)==QGraphicsLineItem]
        
        print('point {1},line {0}'.format(points, linePoint))
        dlg = PropertiesDialog()
        dlg.show()
        if dlg.exec_():
            pass

        
    def AddPoint(self):
        print("AddPoint")
        self.text = self.DC.addEllipse(0, 0, 30, 30, self.pan)
        self.text.setFlags(QGraphicsItem.ItemIsSelectable | QGraphicsItem.ItemIsMovable)  
        self.text.setPos(QPointF(0., 0.))
        

