from PyQt5.QtMultimedia import QMediaContent, QMediaPlayer
from PyQt5.QtMultimediaWidgets import QVideoWidget
from PyQt5.QtCore import QDir, QUrl, Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QFileDialog, QWidget, QFrame, QMainWindow, \
    QVBoxLayout, QHBoxLayout, QPushButton, QSlider, QLabel, QSizePolicy
from PyQt5.Qt import QStyle, QSize
import cv2

class VideoDisplay(QWidget):

    def __init__(self):
        super().__init__()

        self.video_name = ''
        self.wholeStyleSheet = '''
        QFrame{
            padding-right:0.5px;
            padding-left:0.5px;
            margin-top:0.5px;
            margin-bottom:0.5px;
            height:450px;
            width:800px;
            border:4px solid rgb(0,0,205);
        }
        '''
        self.sliderSheet = '''
        QSlider::groove:horizontal { 
            height: 10px;
            background: #63B8FF;
            border: 1px solid #3A5FCD;
            border-radius: 1px;
            padding-left: -1px;
            padding-right: -1px;
        }
        
        QSlider::sub-page:horizontal { 
            height: 10px;
            background: 
            qlineargradient(
                x1:0, y1:0, 
                x2:0, y2:1, 
                stop:0 #B1B1B1, 
                stop:1 #c4c4c4
            );
            background: 
            qlineargradient(
            x1:0, y1:0.2, 
            x2:1, y2:1, 
            stop:0 #5DCCFF, 
            stop:1 #1874CD);
            border: 1px solid #4A708B;
            border-radius: 2px;
        }

        QSlider::add-page:horizontal { height: 10px;
            background: #575757;
            border: 0px solid #777;
            border-radius: 2px;
        }
        
        QSlider::handle:horizontal{
            height:14px;
            width:15px;
            background:
            qlineargradient(
                x1:0, y1:0, 
                x2:1, y2:1, 
                stop:0 #104E8B, 
                stop:1 #5CACEE); 
            border: 1px solid #777; 
            margin-top: -3px;
            margin-bottom: -3px;
            border-radius: 5px;
        }
            
        QSlider::handle:horizontal:hover{
            height:14px;
            width:15px;
            background:
            qlineargradient(
                x1:1, y1:0, 
                x2:1, y2:1, 
                stop:0 #B0E2FF, 
                stop:1 #FFE1FF); 
            border: 1px solid #444; 
            margin-top: -3px;
            margin-bottom: -3px;
            border-radius: 5px;
        }
        
        QSlider::sub-page:horizontal:disabled { 
            height: 10px;
            background: #E0EEEE;
            border-color: #838B8B;
        }

        QSlider::add-page:horizontal:disabled { 
            height: 10px;
            background: #C1CDCD;
            border-color: #838B8B;
        }
        
        QSlider::handle:horizontal:disabled { 
            background: #483D8B;
            border: 1px solid #696969;
            margin-top: -3px;
            margin-bottom: -3px;
            border-radius: 4px;
        }
        '''
        self.roundBtnSheet = '''
            QPushButton{
                border-top: 1px transparent;
                border-bottom: 1px transparent;
                border-right: 7px transparent;
                border-left: 7px transparent;
            }
        '''
        self.initUI()

    def get_video_name(self):
        return self.video_name

    def initUI(self):

        self.mediaPlayer = QMediaPlayer(None, QMediaPlayer.VideoSurface)
        self.videoWidget = QVideoWidget()
        self.videoWidget.setFixedSize(800, 450)

        self.playerFrame = QFrame()
        self.playerLayout = QHBoxLayout()
        self.playerLayout.addWidget(self.videoWidget)
        self.playerFrame.setLayout(self.playerLayout)
        self.playerFrame.setStyleSheet(self.wholeStyleSheet)

        self.playerWindow = QMainWindow()

        self.playerWindow.setCentralWidget(self.playerFrame)

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
        self.playButton.clicked.connect(self.play)

        self.positionSlider = QSlider(Qt.Horizontal)
        self.positionSlider.setRange(0, 0)
        self.positionSlider.setStyleSheet(self.sliderSheet)
        self.positionSlider.sliderMoved.connect(self.setPosition)

        self.errorLabel = QLabel()
        self.errorLabel.setSizePolicy(QSizePolicy.Preferred,
                QSizePolicy.Maximum)

        self.controlLayout = QHBoxLayout()
        self.controlLayout.addWidget(self.openFileBtn)
        self.controlLayout.addWidget(self.playButton)
        self.controlLayout.addWidget(self.positionSlider)

        self.mediaPlayer.setVideoOutput(self.videoWidget)
        self.mediaPlayer.stateChanged.connect(self.mediaStateChanged)
        self.mediaPlayer.positionChanged.connect(self.positionChanged)
        self.mediaPlayer.durationChanged.connect(self.durationChanged)
        self.mediaPlayer.error.connect(self.handleError)

        self.wholeLayout = QVBoxLayout()
        self.wholeLayout.addWidget(self.playerWindow)
        self.wholeLayout.addLayout(self.controlLayout)
        #self.wholeLayout.addWidget(self.errorLabel)

        self.setLayout(self.wholeLayout)
        self.setStyleSheet(self.wholeStyleSheet)

    def openFile(self, pressed):
        fileName, _ = QFileDialog.getOpenFileName(self, "Open Movie",
                QDir.homePath())

        self.video_name = fileName.split('/')[-1]

        if fileName != '':
            self.mediaPlayer.setMedia(
                    QMediaContent(QUrl.fromLocalFile(fileName)))
            self.playButton.setEnabled(True)


    def play(self):
        if self.mediaPlayer.state() == QMediaPlayer.PlayingState:
            self.mediaPlayer.pause()
            self.playButton.setIcon(QIcon('../icons/Play-icon.png'))
        else:
            self.mediaPlayer.play()
            self.playButton.setIcon(QIcon('../icons/Pause-icon.png'))

    def mediaStateChanged(self, state):
        if self.mediaPlayer.state() == QMediaPlayer.PlayingState:
            self.playButton.setIcon(
                self.style().standardIcon(QStyle.SP_MediaPause))
        else:
            self.playButton.setIcon(
                self.style().standardIcon(QStyle.SP_MediaPlay))

    def positionChanged(self, position):
        self.positionSlider.setValue(position)

    def durationChanged(self, duration):
        self.positionSlider.setRange(0, duration)

    def setPosition(self, position):
        self.mediaPlayer.setPosition(position)

    def handleError(self):
        self.playButton.setEnabled(False)
        self.errorLabel.setText("Error: " + self.mediaPlayer.errorString())