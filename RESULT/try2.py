import sys

# PYQT5 를 이용하기 위한 모듈갱신
from PyQt5.QtWidgets import *
from PyQt5 import uic

# 불러오고자 하는 .ui 파일
# .py 파일과 같은 위치에 있어야 한다 *****
form_class = uic.loadUiType("tryout.ui")[0]

class MyWindow(QDialog, form_class):

# 초기 설정해주는 init
   def __init__(self):
       super().__init__()
       self.setupUi(self)
# 시그널(이벤트루프에서 발생할 이벤트) 선언
# self.객체명.객체함수.connect(self.슬롯명)
       self.pushButton.clicked.connect(self.btn_click)

# 시그널을 처리할 슬롯
   def btn_click(self):
       self.textEdit.setText("hello world!")

if __name__ == "__main__":
   app = QApplication(sys.argv)
   # myWindow 라는 변수에 GUI 클래스 삽입
   myWindow = MyWindow()
   # GUI 창 보이기
   myWindow.show()
#########################
# 이벤트루프 진입전 작업할 부분
#########################

# 이벤트루프 진입
   app.exec_()
