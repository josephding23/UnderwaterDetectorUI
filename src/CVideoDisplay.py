import time
import sys

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from cv2 import *

class CVideoDisplay(QWidget):

    def __init__(self, video_url=""):

        self.VIDEO_TYPE_OFFLINE = 0
        self.VIDEO_TYPE_REAL_TIME = 1
        self.STATUS_INIT = 0
        self.STATUS_PLAYING = 1
        self.STATUS_PAUSE = 2

        self.video_url = video_url
        self.video_name = ''
        self.auto_play = False
        self.video_type = 0
        self.status = self.STATUS_INIT

        self.roundBtnSheet = '''
                    QPushButton{
                        border-top: 1px transparent;
                        border-bottom: 1px transparent;
                        border-right: 7px transparent;
                        border-left: 7px transparent;
                    }
                '''

        self.wholeStyleSheet = '''
                QLabel{
                    padding-right:1px;
                    padding-left:1px;
                    margin-top:1px;
                    margin-bottom:1px;
                    height:450px;
                    width:800px;
                    border:4px solid #528B8B;
                }
                '''

        super().__init__()
        self.initUI()

    def initUI(self):

        self.pictureLabel = QLabel()
        self.pictureLabel.setStyleSheet(self.wholeStyleSheet)
        self.pictureLabel.setFixedSize(800, 450)
        self.init_image = QPixmap("../pic/no_signal.jpg").scaled(self.width(), self.height())
        self.pictureLabel.setPixmap(self.init_image)
        self.pictureLabel.setAlignment(Qt.AlignCenter)

        self.playerLayout = QHBoxLayout()
        self.playerLayout.addWidget(self.pictureLabel)
        self.playerFrame = QFrame()
        self.playerFrame.setLayout(self.playerLayout)
        #self.playerFrame.setStyleSheet(self.wholeStyleSheet)

        #self.playerWindow = QMainWindow()
        #self.playerWindow.setCentralWidget(self.playerFrame)

        self.openFileBtn = QPushButton(self)
        self.openFileBtn.setStyleSheet(self.roundBtnSheet)
        self.openFileBtn.setIcon(QIcon('../icons/Folder-Open-icon.png'))
        self.openFileBtn.setIconSize(QSize(50, 50))
        self.openFileBtn.clicked.connect(self.openFile)

        self.playButton = QPushButton(self)
        self.playButton.setStyleSheet(self.roundBtnSheet)
        self.playButton.setEnabled(False)
        self.playButton.setIcon(QIcon('../icons/Play-icon.png'))
        self.playButton.setIconSize(QSize(50, 50))
        self.playButton.clicked.connect(self.switch_video)

        self.control_box = QHBoxLayout()
        self.control_box.addWidget(self.openFileBtn)
        self.control_box.addWidget(self.playButton)

        self.layout = QVBoxLayout()
        self.layout.addWidget(self.playerFrame)
        self.layout.addLayout(self.control_box)

        self.setLayout(self.layout)

        self.timer = VideoTimer()
        self.timer.timeSignal.signal[str].connect(self.show_video_images)


        self.playCapture = VideoCapture()
        if self.video_url != "":
            self.playCapture.open(self.video_url)
            fps = self.playCapture.get(CAP_PROP_FPS)
            self.timer.set_fps(fps)
            self.playCapture.release()
            if self.auto_play:
                self.switch_video()

    def reset(self):
        self.timer.stop()
        self.playCapture.release()
        self.status = self.STATUS_INIT
        self.playButton.setIcon(self.style().standardIcon(QStyle.SP_MediaPlay))

    def show_video_images(self):
        if self.playCapture.isOpened():
            success, frame = self.playCapture.read()
            if success:
                height, width = frame.shape[:2]
                if frame.ndim == 3:
                    rgb = cvtColor(frame, COLOR_BGR2RGB)
                elif frame.ndim == 2:
                    rgb = cvtColor(frame, COLOR_GRAY2BGR)

                temp_image = QImage(rgb.flatten(), width, height, QImage.Format_RGB888)
                temp_pixmap = QPixmap.fromImage(temp_image.scaled(800, 450, Qt.IgnoreAspectRatio, Qt.SmoothTransformation))
                self.pictureLabel.setPixmap(temp_pixmap)
                self.pictureLabel.setAlignment(Qt.AlignCenter)
            else:
                print("read failed, no frame data")
                success, frame = self.playCapture.read()
                if not success and self.video_type is self.VIDEO_TYPE_OFFLINE:
                    print("play finished")  # 判断本地文件播放完毕
                    self.reset()
                    self.playButton.setIcon(self.style().standardIcon(QStyle.SP_MediaStop))
                return
        else:
            print("open file or capturing device error, init again")
            self.reset()

    def switch_video(self):
        if self.video_url == "" or self.video_url is None:
            return
        if self.status is self.STATUS_INIT:
            self.playCapture.open(self.video_url)
            self.timer.start()
            self.playButton.setIcon(QIcon('../icons/Pause-icon.png'))
        elif self.status is self.STATUS_PLAYING:
            self.timer.stop()
            if self.video_type is self.VIDEO_TYPE_REAL_TIME:
                self.playCapture.release()
            self.playButton.setIcon(QIcon('../icons/Play-icon.png'))
        elif self.status is self.STATUS_PAUSE:
            if self.video_type is self.VIDEO_TYPE_REAL_TIME:
                self.playCapture.open(self.video_url)
            self.timer.start()
            self.playButton.setIcon(QIcon('../icons/Pause-icon.png'))

        self.status = (self.STATUS_PLAYING,
                       self.STATUS_PAUSE,
                       self.STATUS_PLAYING)[self.status]

    def openFile(self, pressed):
        fileName, _ = QFileDialog.getOpenFileName(self, "Open Movie",
                QDir.homePath())

        self.video_name = fileName.split('/')[-1]

        if fileName != '':
            self.video_url = fileName
            self.playButton.setEnabled(True)

class Communicate(QObject):

    signal = pyqtSignal(str)


class VideoTimer(QThread):

    def __init__(self, frequent=20):
        QThread.__init__(self)
        self.stopped = False
        self.frequent = frequent
        self.timeSignal = Communicate()
        self.mutex = QMutex()

    def run(self):
        with QMutexLocker(self.mutex):
            self.stopped = False
        while True:
            if self.stopped:
                return
            self.timeSignal.signal.emit("1")
            time.sleep(1 / self.frequent)

    def stop(self):
        with QMutexLocker(self.mutex):
            self.stopped = True

    def is_stopped(self):
        with QMutexLocker(self.mutex):
            return self.stopped

    def set_fps(self, fps):
        self.frequent = fps



