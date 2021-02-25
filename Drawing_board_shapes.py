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


        # drawing 안하고 있을때
        self.drawing = False
        
        # Draw type
        self.shape_type = 'brush'

        # 리스트 선언
        self.brush_list = []
        self.rectangles_list = []
        self.rectangles_color_list = []

        # 브러시 사이즈와 색상
        self.brush_size = 5
        self.shape_color = Qt.black
        # 아마도.. 마지막 그리는 지점 정보?
        self.last_point = QPoint() # Point (x,y)
        self.init_ui()
        
    def init_ui(self):
        # QMainWindow에서 정의된, menuBar
        # Menubar 인스턴스 선언
        menubar = self.menuBar()
        menubar.setNativeMenuBar(False)
        
        # 메뉴 추가
        filemenu = menubar.addMenu('File')
        filemenu_2 = menubar.addMenu('Setting')
        filemenu_3 = menubar.addMenu('Shapes')

        #'save'라는 action 추가
        save_action = QAction('Save', self)
        save_action.setShortcut('Ctrl+S')
        save_action.triggered.connect(self.save)

        #'clear'라는 action 추가
        clear_action = QAction('Clear', self)
        clear_action.setShortcut('Ctrl+C')
        clear_action.triggered.connect(self.clear)

        #'color'라는 action 추가
        color_action = QAction('Color', self)
        color_action.triggered.connect(self.color)

        #'brush'라는 action 추가
        brush_action = QAction('brush', self)
        brush_action.triggered.connect(self.brush)

        #'rectangle'라는 action 추가
        rectangle_action = QAction('rectangle', self)
        rectangle_action.triggered.connect(self.rectangle)

        #menu들 안으로 어떤 action 추가했는지
        filemenu.addAction(save_action)
        filemenu.addAction(clear_action)
        filemenu_2.addAction(color_action)
        filemenu_3.addAction(brush_action)
        filemenu_3.addAction(rectangle_action)

        self.setWindowTitle('Simple Painter')
        self.setGeometry(300, 300, 400, 400)
        self.show()

    # Events 
    def paintEvent(self, e) : 
        canvas = QPainter(self)
        canvas.drawImage(self.rect(), self.image, self.image.rect())
        #painter = QPainter(self.image)
        # line들을 그리기.
        
        for line in self.brush_list :    
            # [ last_point, cursor_point ]
            canvas.setPen(QPen(self.shape_color, self.brush_size, Qt.SolidLine, Qt.RoundCap))
            canvas.drawLine(line[0], line[1])

        ''' # Method 1.
        for rect in self.rectangles_list :
            color = rect[0]
            canvas.setBrush(color)
            canvas.setPen(color)

            #시작 좌표
            x = rect[1][0]
            y = rect[1][1]
            #Width 
            w = rect[-1][0] - rect[1][0]
            #height
            h = rect[-1][1] - rect[1][1]

            print(x,y,w,h)
            canvas.drawRect(x, y, w, h)
        '''
        # Method 2.

        
        # 시긱향 컬러 리스트를 따로 선언을 한 후에,
        # 인덱스를 순회하면서 사각형을 그려내는 방식.
        for i in range(0, len(self.rectangles_list)) :
            color = self.rectangles_color_list[i]
            canvas.setBrush(color)
            canvas.setPen(color)
                 
            #시작 좌표
            x = self.rectangles_list[i][0][0]
            y = self.rectangles_list[i][0][1]
            #Width 
            w = self.rectangles_list[i][-1][0] - self.rectangles_list[i][0][0]
            #height
            h = self.rectangles_list[i][-1][1] - self.rectangles_list[i][0][1]

            print(x,y,w,h)
            canvas.drawRect(x, y, w, h)


    def mousePressEvent(self, e):
        if e.button() == Qt.LeftButton:
            self.drawing = True
            self.last_point = e.pos()

            ''' # Method 1.
            if self.shape_type == 'rect' : 
                # e.pos()는 QPoint 인스턴스를 반환한다.
                #self.test = e.pos()

                current_color = self.shape_color       
                rect_list = [ current_color, (e.pos().x(), e.pos().y()) ]
                self.rectangles_list.append(rect_list)
                #current_color = self.shape_color
            '''
            if self.shape_type == 'rect' : 
                # e.pos()는 QPoint 인스턴스를 반환한다.
                #self.test = e.pos()

                current_color = self.shape_color       
                rect_list = [ (e.pos().x(), e.pos().y()) ]
                
                self.rectangles_list.append(rect_list)
                self.rectangles_color_list.append(current_color)
                #current_color = self.shape_color
                

    # canvas.drawRect(시작 x, 시작 y, 높이, 너비)

    def mouseMoveEvent(self, e):
        # if draw brush.
        if (e.buttons() & Qt.LeftButton) & self.drawing and self.shape_type == 'brush':
            self.brush_list.append([self.last_point,e.pos()])
            
            self.last_point = e.pos()
            self.update()
        # Draw Rect.
        elif (e.buttons() & Qt.LeftButton) & self.drawing and self.shape_type == 'rect': 
            # rectangles -> [ 사각형1, 사각형2, 사각형3 ]
            #  사각형1 -> [(시작좌표),(좌표1),(좌표2), +++ ]

            #현재 cursor 좌표 rectangles list에 추가
            self.rectangles_list[-1].append((e.pos().x(), e.pos().y()))
            #self.shape_color = 
            self.update()
        

    def mouseReleaseEvent(self, e):
        if e.button() == Qt.LeftButton:
            self.drawing = False

    #define what 'save' action does
    def save(self):
        # 저장 기능 구현
        fpath, _ = QFileDialog.getSaveFileName(self, 'Save Image', '', "PNG(*.png);;JPEG(*.jpg *.jpeg);;All Files(*.*) ")
        
        if fpath:
            self.image.save(fpath)

    #define what 'clear' action does
    def clear(self):
        self.image.fill(Qt.white)
        self.update()

    #define what 'color' action does
    def color(self):
        new_color = QColorDialog.getColor()
        if new_color.isValid():
            self.shape_color = new_color

    #define what 'brush' action does
    def brush(self):
        self.shape_type = 'brush'
    
    #define what 'rectangle' action does
    def rectangle(self):
        self.shape_type = 'rect'

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyApp()
    sys.exit(app.exec_())