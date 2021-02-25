#-*- coding: utf-8 -*-
import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *


class MyApp(QMainWindow):

    def __init__(self):
        super().__init__()
        # 캔버스 초기화 
        self.image = QImage(QSize(400, 400), QImage.Format_RGB32)
        # 캔버스를 하얀색으로 채운다        
        self.image.fill(Qt.white) #  (255,255,255)
        
        self.drawing = False
        
        # 브러시 사이즈와 색상
        self.brush_size = 5
        self.brush_color = Qt.black
        # 아마도.. 마지막 그리는 지점 정보?
        self.last_point = QPoint() # Point (x,y)
        self.initUI()

    def initUI(self):
        # QMainWindow에서 정의된, menuBar
        # Menubar 인스턴스 선언
        menubar = self.menuBar()
        menubar.setNativeMenuBar(False)
        
        # 메뉴 추가
        filemenu = menubar.addMenu('File')
        filemenu_2 = menubar.addMenu('Setting')
        #filemenu_2 = menubar.addMenu('Color')

        save_action = QAction('Save', self)
        save_action.setShortcut('Ctrl+S')
        save_action.triggered.connect(self.save)

        clear_action = QAction('Clear', self)
        clear_action.setShortcut('Ctrl+C')
        clear_action.triggered.connect(self.clear)

        color_action = QAction('Color', self)
        color_action.triggered.connect(self.color)

        filemenu.addAction(save_action)
        filemenu.addAction(clear_action)
        filemenu_2.addAction(color_action)
        

        self.setWindowTitle('Simple Painter')
        self.setGeometry(300, 300, 400, 400)
        self.show()

    # Events 
    def paintEvent(self, e):
        canvas = QPainter(self)
        canvas.drawImage(self.rect(), self.image, self.image.rect())
    # 
    def mousePressEvent(self, e):
        if e.button() == Qt.LeftButton:
            self.drawing = True
            self.last_point = e.pos()

    def mouseMoveEvent(self, e):
        if (e.buttons() & Qt.LeftButton) & self.drawing:
            painter = QPainter(self.image)
            painter.setPen(QPen(self.brush_color, self.brush_size, Qt.SolidLine, Qt.RoundCap))
            painter.drawLine(self.last_point, e.pos())
            self.last_point = e.pos()
            self.update()

    def mouseReleaseEvent(self, e):
        if e.button() == Qt.LeftButton:
            self.drawing = False

    def save(self):
        # 저장 기능 구현
        fpath, _ = QFileDialog.getSaveFileName(self, 'Save Image', '', "PNG(*.png);;JPEG(*.jpg *.jpeg);;All Files(*.*) ")
        
        if fpath:
            self.image.save(fpath)

    def clear(self):
        self.image.fill(Qt.white)
        self.update()

    def color(self):
        new_color = QColorDialog.getColor()
        if new_color.isValid():
            self.brush_color = new_color


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyApp()
    sys.exit(app.exec_())