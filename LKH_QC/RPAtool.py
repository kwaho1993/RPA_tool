import os
import sys
exe_folder = os.path.dirname(os.path.abspath(__file__))
print(exe_folder)
site_site_packages_path = os.path.join(exe_folder, r'site-site-packages')
sys.path.append(site_site_packages_path)

from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow, QApplication, QVBoxLayout, QMessageBox
from PyQt5.QtCore import Qt

from common_module.lkh_ui_Style import *
import traceback


# 예외처리 에러메세지 적용 데코레이터 - 버튼에 연결된 함수에 데코
from functools import wraps
def ifException_showMSGBOX(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            func(*args, **kwargs)
        except Exception as e:
            tb = traceback.format_exc()
            QMessageBox.information(None, "ERROR 발생", str(e) +'\n\n' + str(tb))
    return wrapper

print(exe_folder)
main_ui_path = os.path.join(exe_folder, r'ui_data\main_RPA.ui')
form_main = uic.loadUiType(main_ui_path)[0]



class Mainwindow_RPA(QMainWindow, form_main) :
    # 드래그 창이동을 위한 함수1 - 원하는 frame 객체의 mousePressEvent 에 오버라이드
    def start_drag(self, event):
        if event.buttons() == Qt.LeftButton:
            self.drag_position = event.globalPos() - self.frameGeometry().topLeft()
            event.accept()
    
    # 드래그 창이동을 위한 함수2  - 원하는 frame 객체의 mouseMoveEvent 에 오버라이드
    def drag(self, event):
        if event.buttons() == Qt.LeftButton and self.drag_position is not None:
            self.move(event.globalPos() - self.drag_position)
            event.accept()

    ############ Sytyle 수정 함수들 ############                                                                           ############ Sytyle 수정 함수들 ############
    ############ Sytyle 수정 함수들 ############                                                                           ############ Sytyle 수정 함수들 ############

    def __init__(self) :
        super().__init__()
        self.setupUi(self)

        self.main_exe_path = exe_folder
        self.site_site_packages_path = os.path.join(exe_folder, r'site-site-packages')

        self.wiget_background1 = 'background-color: rgba(228, 255, 248, 0.5);'

        self.setWindowFlags(self.windowFlags() | Qt.FramelessWindowHint) # 창의 프레임 없애기
        self.setAttribute(Qt.WA_TranslucentBackground) # 창 배경을 투명하게 만들기

        self.header.mousePressEvent = self.start_drag # 드래그 창이동을 위한 오버라이드1
        self.header.mouseMoveEvent = self.drag # 드래그 창이동을 위한 오버라이드1

        style_mainwindow(self)

        ############ header 부분 ############                                                                            ############ header 부분 ############
        ############ header 부분 ############                                                                            ############ header 부분 ############

        # if not self.windowFlags() & Qt.WindowStaysOnTopHint:
        style_button_1(self.bt_pin)
        style_button_1(self.bt_close)
        style_button_1(self.bt_minimize)


        def toggleAlwaysOnTop():
            if self.windowFlags() & Qt.WindowStaysOnTopHint:
                # always-on-top 상태일 때
                self.setWindowFlags(self.windowFlags() & ~Qt.WindowStaysOnTopHint)
                style_button_1(self.bt_pin)
                self.show()  # 창을 다시 표시하여 변경 사항 적용
            else:
                # always-on-top 상태가 아닐 때
                self.setWindowFlags(self.windowFlags() | Qt.WindowStaysOnTopHint)
                self.bt_pin.setStyleSheet('background-color: rgba(255, 255, 255, 0.5);')
                self.show()  # 창을 다시 표시하여 변경 사항 적용
        self.bt_pin.clicked.connect(toggleAlwaysOnTop)
        self.bt_close.clicked.connect(self.close) 
        self.bt_minimize.clicked.connect(self.showMinimized)


        ############ mainbody 부분 ############                                                                            ############ mainbody 부분 ############
        ############ mainbody 부분 ############                                                                            ############ mainbody 부분 ############

        ############ 사이드메뉴(treeWidget) 부분 ############                                                    ############ 사이드메뉴(treeWidget) 부분 ############
        ############ 사이드메뉴(treeWidget) 부분 ############                                                    ############ 사이드메뉴(treeWidget) 부분 ############
        style_button_3(self.bt_setting)

        # 트리위젯 안에 버튼넣기
        def treeWidget_itemPathList_Func_Connect(treeWidget, path_li, func):
            # 트리위젯에서 경로 리스트 기준으로 아이템 반환하기
            def find_treeItem(treeWidget, path):
                current_item = treeWidget.invisibleRootItem()  # 최상위 트리 아이템부터 시작

                for item_name in path:
                    found = False
                    for index in range(current_item.childCount()):
                        child_item = current_item.child(index)
                        if child_item.text(0) == item_name:
                            current_item = child_item  # 현재 아이템을 찾은 자식으로 업데이트
                            found = True
                            break
                    if not found:
                        return None  # 해당 경로에 해당하는 아이템을 찾지 못함

                return current_item  # 경로에 해당하는 아이템을 반환

            item = find_treeItem(treeWidget, path_li)
            item.setToolTip(0, path_li[-1])

            
            def item_doubleclick(_item, column):
                if _item.text(0) == path_li[-1]:
                    func()
            item.treeWidget().itemDoubleClicked.connect(item_doubleclick) # 더블클릭 시, 시그널 발생(item, column)
        
        ########  ######## 기능위젯프레임 비우기 ########  ########
        def clear_frame():
            if widgetLayout.count():
                widgetLayout.itemAt(0).widget().deleteLater()  # widgetLayout 의 widget이 있다면 해제한다.







        ############ 사이드 버튼에 위젯 연결하기  ############   ############ 사이드 버튼에 위젯 연결하기  ############ ############ 사이드 버튼에 위젯 연결하기  ############



        @ifException_showMSGBOX
        def referlab_send(self):
            clear_frame()
            from widgets.referlab.referlab_send.referlab_send import Widget_referlab_send
            widgetLayout.addWidget(Widget_referlab_send(self))
        treeWidget_itemPathList_Func_Connect(self.treeWidget, ['위탁', '위탁 보내기'], lambda: referlab_send(self))

        ############ Typing  ############
        @ifException_showMSGBOX
        def receptNGS(self):
            clear_frame()
            from widgets.Typing.ReceptNGS.receptNGS import Widget_receptNGS
            widgetLayout.addWidget(Widget_receptNGS(self))
        treeWidget_itemPathList_Func_Connect(self.treeWidget, ['Typing', 'NGS 검체 접수'], lambda: receptNGS(self))

        @ifException_showMSGBOX
        def anlaysisNGS(self):
            clear_frame()
            from widgets.Typing.AnalysisNGS.analysisNGS import Widget_analysisNGS
            widgetLayout.addWidget(Widget_analysisNGS(self))
        treeWidget_itemPathList_Func_Connect(self.treeWidget, ['Typing', 'NGS 분석'], lambda: anlaysisNGS(self))

        @ifException_showMSGBOX
        def lmimUploadNGS(self):
            clear_frame()
            from widgets.Typing.lmimUploadNGS.lmimUploadNGS import Widget_lmimUploadNGS
            widgetLayout.addWidget(Widget_lmimUploadNGS(self))
        treeWidget_itemPathList_Func_Connect(self.treeWidget, ['Typing', '원내홈피 업로드'], lambda: lmimUploadNGS(self))

        # @ifException_showMSGBOX
        # def PDFdoc_manager(self):
        #     clear_frame()
        #     from widgets.PDFdoc_manager.PDFdoc_manager import Widget_PDFdoc_manager
        #     widgetLayout.addWidget(Widget_PDFdoc_manager(self))
        # treeWidget_itemPathList_Func_Connect(self.treeWidget, ['PDF 전자문서', '스캔파일 자동정리'], lambda: PDFdoc_manager(self))






        ############ 사이드 버튼에 위젯 연결하기  ############   ############ 사이드 버튼에 위젯 연결하기  ############ ############ 사이드 버튼에 위젯 연결하기  ############




        ############ 위젯화면(fr_showWidget) 부분 ############                                                    ############ 위젯화면(fr_showWidget) 부분 ############
        ############ 위젯화면(fr_showWidget) 부분 ############                                                    ############ 위젯화면(fr_showWidget) 부분 ############

        widgetLayout = QVBoxLayout() 
        self.fr_showWidget.setLayout(widgetLayout) # fr_showWidget의 layout을 설정

if __name__ == "__main__":
    # QApplication : 프로그램을 실행시켜주는 클래스
    app = QApplication(sys.argv)
    # WindowClass의 인스턴스 생성
    mainwindow = Mainwindow_RPA()
    # 프로그램 화면을 보여주는 코드
    mainwindow.show()
    # 프로그램을 이벤트루프로 진입시키는(프로그램을 작동시키는) 코드
    app.exec_()