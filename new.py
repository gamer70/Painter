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
        #self.rectangles_color_list = []
        self.ellipse_list = []
        #self.ellipse_color_list = []

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

        #'ellipse'라는 action 추가
        ellipse_action = QAction('ellipse', self)
        ellipse_action.triggered.connect(self.ellipse)

        #menu들 안으로 어떤 action 추가했는지
        filemenu.addAction(save_action)
        filemenu.addAction(clear_action)
        filemenu_2.addAction(color_action)
        filemenu_3.addAction(brush_action)
        filemenu_3.addAction(rectangle_action)
        filemenu_3.addAction(ellipse_action)

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
            color = line['color']
            canvas.setPen(QPen(color, self.brush_size, Qt.SolidLine, Qt.RoundCap))
            
            canvas.drawLine(line['start_point'], line['last_point'])
            
            
            
            #test_dic = {'start_point' : e.pos(), 'last_point' : self.last_point }
            #print(test_dic['start_point'])

        # Method 3.
        for rectangle in self.rectangles_list :
            color = rectangle['color']
            canvas.setBrush(color)
            canvas.setPen(color)
                 
            #시작 좌표
            start_x = rectangle['start_point'][0]
            start_y = rectangle['start_point'][1]
            
            last_x = rectangle['last_point'][0]
            last_y = rectangle['last_point'][1]

            width = last_x - start_x
            height = last_y - start_y
            
            canvas.drawRect(start_x, start_y, width, height)
        
        for ellipse in self.ellipse_list :
            color = ellipse['color']
            canvas.setBrush(color)
            canvas.setPen(color)

            estart_x = ellipse['start_point'][0]
            estart_y = ellipse['start_point'][1]
            
            elast_x = ellipse['last_point'][0]
            elast_y = ellipse['last_point'][1]

            e_width = elast_x - estart_x
            e_height = elast_y - estart_y

            canvas.drawEllipse(estart_x, estart_y, e_width, e_height)

        
    def mousePressEvent(self, e):
        if e.button() == Qt.LeftButton:
            self.drawing = True
            self.last_point = e.pos()

            # Method 3.
            if self.shape_type == 'rect' : 
                # e.pos()는 QPoint 인스턴스를 반환한다.
                
                rectangle = {}                
                rectangle['start_point'] = [e.pos().x(), e.pos().y()]
                rectangle['color'] = self.shape_color

                self.rectangles_list.append(rectangle)

            elif self.shape_type == 'ellipse' :
                ellipse = {}
                ellipse['start_point'] = [e.pos().x(), e.pos().y()]
                ellipse['color'] = self.shape_color

                self.ellipse_list.append(ellipse)
                
    # canvas.drawRect(시작 x, 시작 y, 높이, 너비)

    def mouseMoveEvent(self, e):
        # if draw brush.
        if (e.buttons() & Qt.LeftButton) & self.drawing and self.shape_type == 'brush':
            brush = {}
            
            brush['color'] = self.shape_color
            brush['start_point'] = self.last_point
            brush['last_point'] = e.pos()
            self.brush_list.append(brush)

            self.last_point = e.pos()
            self.update()
        
        # Draw Rectangle Method 3
        elif (e.buttons() & Qt.LeftButton) & self.drawing and self.shape_type == 'rect': 
 
            #현재 cursor 좌표 rectangles list에 추가
            self.rectangles_list[-1]['last_point'] = [ e.pos().x(), e.pos().y() ]
            
            self.update()

        elif (e.buttons() & Qt.LeftButton) & self.drawing and self.shape_type == 'ellipse':
            #현재 cursor 좌표 ellipse list에 추가
            self.ellipse_list[-1]['last_point'] = [ e.pos().x(), e.pos().y() ]
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

    def ellipse(self):
        self.shape_type = 'ellipse'

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyApp()
    sys.exit(app.exec_())