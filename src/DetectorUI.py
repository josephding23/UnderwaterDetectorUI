from PyQt5.QtWidgets import QWidget, QPushButton, QLabel,\
    QHBoxLayout, QVBoxLayout, QApplication, QMainWindow
from PyQt5.QtGui import QFont, QCursor, QIcon
from PyQt5.QtCore import Qt, QSize
from src.VideoDisplay import VideoDisplay
from src.CVideoDisplay import CVideoDisplay
import sys
import cv2

class DetectorUI(QWidget):

    def __init__(self):
        self.FPS = 60
        self.countNum = 100
        self.videoLength = 90
        self.playedLength = 30
        self.cap = cv2.VideoCapture(0)
        self.capturing = False
        self.camera_open = False

        self.player_type = 1

        self.btnSheet = '''
                QPushButton{background-color:#458B74; color:#E0FFFF; font-size:18px}
                QPushButton:hover{background-color:#9BCD9B; color:#BCEE68;}
                QPushButton:checked{background-color:#458B74; color:#E0FFFF;}
                QPushButton:pressed{background-color:#9BCD9B; font-size:20px; color:#87CEEB;}
                '''

        self.lblSheet = 'QLabel{font-size: 18px;}'

        self.wholeStyleSheet = '''
                        QMainWindow{
                            padding-right:0.5px;
                            padding-left:0.5px;
                            margin-top:0.5px;
                            margin-bottom:0.5px;
                            border:4px solid rgb(0,0,205);
                        }
                        '''

        self.video_name = ''
        self.videoPlayer = VideoDisplay()
        self.cvideoPlayer = CVideoDisplay()
        super().__init__()
        self.initUI()

    def initUI(self):

        '''
        self.openVideoBtn = QPushButton('打开视频', self)
        self.openVideoBtn.setFont(QFont('楷体'))
        self.openVideoBtn.setFixedSize(140, 60)
        self.openVideoBtn.setStyleSheet(self.btnSheet)
        #self.openVideoBtn.clicked[bool].connect(self.videoPlayer.openFile)
        #self.openVideoBtn.clicked[bool].connect(self.file_name_response)
        '''

        self.alterPlayerBtn = QPushButton('变更为OpenCV播放')
        self.alterPlayerBtn.setCursor(QCursor(Qt.PointingHandCursor))
        self.alterPlayerBtn.setFont(QFont('楷体'))
        self.alterPlayerBtn.setFixedSize(140, 60)
        self.alterPlayerBtn.setStyleSheet(self.btnSheet)
        self.alterPlayerBtn.setCheckable(True)
        self.alterPlayerBtn.clicked[bool].connect(self.alter_player)

        self.openCameraBtn = QPushButton('开启/关闭摄像头', self)
        self.openCameraBtn.setCursor(QCursor(Qt.PointingHandCursor))
        self.openCameraBtn.setFont(QFont('楷体'))
        self.openCameraBtn.setFixedSize(140, 60)
        self.openCameraBtn.setStyleSheet(self.btnSheet)
        self.openCameraBtn.clicked[bool].connect(self.camera_open_response)

        self.processVideoBtn = QPushButton('分析处理', self)
        self.processVideoBtn.setCursor(QCursor(Qt.PointingHandCursor))
        self.processVideoBtn.setFont(QFont('楷体'))
        self.processVideoBtn.setFixedSize(140, 60)
        self.processVideoBtn.setStyleSheet(self.btnSheet)

        self.saveVideoBtn = QPushButton('保存视频', self)
        self.saveVideoBtn.setCursor(QCursor(Qt.PointingHandCursor))
        self.saveVideoBtn.setFont(QFont('楷体'))
        self.saveVideoBtn.setFixedSize(140, 60)
        self.saveVideoBtn.setStyleSheet(self.btnSheet)

        self.btnBox = QVBoxLayout()
        #self.btnBox.addWidget(self.openVideoBtn)
        self.btnBox.addWidget(self.alterPlayerBtn)
        self.btnBox.addWidget(self.openCameraBtn)
        self.btnBox.addWidget(self.processVideoBtn)
        self.btnBox.addWidget(self.saveVideoBtn)
        self.btnBox.setSpacing(40)

        self.videoPlace = QMainWindow()
        self.videoPlace.setCentralWidget(self.videoPlayer)
        #self.videoPlace.setStyleSheet(self.wholeStyleSheet)
        self.videoBox = QVBoxLayout()
        self.videoBox.addWidget(self.videoPlace)

        self.videoNameLbl = QLabel('视频名称: N/A')
        self.videoNameLbl.setWordWrap(True)
        self.videoNameLbl.setMaximumWidth(250)
        self.videoNameLbl.setStyleSheet(self.lblSheet)
        self.videoNameLbl.setFont(QFont('楷体'))

        self.fpsLbl = QLabel('FPS: ' + str(self.FPS))
        self.fpsLbl.setStyleSheet(self.lblSheet)
        self.fpsLbl.setFont(QFont('楷体'))

        self.countNumLbl = QLabel('数目: ' + str(self.countNum))
        self.countNumLbl.setStyleSheet(self.lblSheet)
        self.countNumLbl.setFont(QFont('楷体'))

        self.infoBox = QVBoxLayout()
        self.infoBox.addWidget(self.videoNameLbl)
        self.infoBox.addWidget(self.fpsLbl)
        self.infoBox.addWidget(self.countNumLbl)
        self.infoBox.setSpacing(40)

        self.wholeLayout = QHBoxLayout()
        self.wholeLayout.addLayout(self.btnBox)
        self.wholeLayout.addLayout(self.videoBox)
        self.wholeLayout.addLayout(self.infoBox)
        self.wholeLayout.setStretch(0, 30)
        self.wholeLayout.setStretch(1, 80)
        self.wholeLayout.setStretch(2, 40)
        self.wholeLayout.setSpacing(30)

        self.setLayout(self.wholeLayout)

    def file_name_response(self):
        self.video_name = self.videoPlayer.get_video_name()
        self.videoNameLbl.setText('视频名称: ' + self.video_name)

    def alter_player(self):
        if self.alterPlayerBtn.isChecked():
            self.cvideoPlayer = CVideoDisplay()
            self.videoPlace.setCentralWidget(self.cvideoPlayer)
            self.alterPlayerBtn.setText('变更为QtMedia播放')

        else:
            self.videoPlayer = VideoDisplay()
            self.videoPlace.setCentralWidget(self.videoPlayer)
            self.alterPlayerBtn.setText('变更为OpenCV播放')


    def camera_open_response(self):
        self.camera_open = not self.camera_open

        if self.camera_open == True:
            self.capturing = True
            capture = self.cap
            while (self.capturing):
                ret, frame = capture.read()
                cv2.imshow("Capture", frame)
                cv2.waitKey(5)
            cv2.destroyAllWindows()

        if self.camera_open == False:
            self.capturing = False

    def camera_close_response(self):
        self.capturing = False


class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        desktop = QApplication.desktop()

        self.setCentralWidget(DetectorUI())
        self.resize(1200, 580)
        self.setFixedSize(self.width(), self.height())

        width = desktop.width()
        height = desktop.height()
        self.move(round((width - self.width())/2), round((height - self.height())/2))

        self.windowStyleSheet = 'QMainWindow {background-color: #B0E0E6}'
        self.setWindowTitle('See Cucumber')
        self.setWindowIcon(QIcon('../icons/aquaman.png'))
        self.setStyleSheet(self.windowStyleSheet)
        self.show()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MainWindow()
    #ex.setWindowOpacity(0.95)
    sys.exit(app.exec_())