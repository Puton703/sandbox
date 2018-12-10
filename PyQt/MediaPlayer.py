# coding=utf-8

import os
import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.uic import loadUi
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent, QMediaPlaylist
from PyQt5.QtMultimediaWidgets import QVideoWidget


class MainWindow(QWidget):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)

        self.init_ui()

        self.mediaPlayer = QMediaPlayer(None, QMediaPlayer.VideoSurface)
        #self.mediaPlayer.stateChanged.connect(self.mediaStateChanged)
        self.mediaPlayer.positionChanged.connect(self.positionChanged)
        self.mediaPlayer.durationChanged.connect(self.durationChanged)
        self.mediaPlayer.error.connect(self.handleError)
        
        
        self._playlist = QMediaPlaylist()
        self.addMedia("resources/movie/movie1.wmv")
        self._stopped = True

    def init_ui(self):
        ui_path = "resources/ui/MediaPlayer.ui"
        print ui_path
        self.ui = loadUi(ui_path, self)

        self.ui.playButton.clicked.connect(self.play)

        self.ui.positionSlider.setRange(0, 0)
        self.ui.positionSlider.sliderMoved.connect(self.setPosition)
        #self.videoWidget = QVideoWidget(self)
        #self.ui.formLayout.addWidget(self.videoWidget)


    # プレイリストに動画を追加
    def addMedia(self, media_file):
        media_content = QMediaContent(QUrl.fromLocalFile(media_file))
        self._playlist.addMedia(media_content)

    # クリックでポーズ・再生の切り替え
    def mousePressEvent(self, event):
        if self._stopped:
            self.play()
        else:
            self.mediaPlayer.pause()
            self._stopped = True

    # ダブルクリックで動画を読み込み，再生
    def mouseDoubleClickEvent(self, event):
        self.mediaPlayer.setVideoOutput(self.ui.videoWidget)
        self.mediaPlayer.setPlaylist(self._playlist)
        self.mediaPlayer.play()


    def play(self):
        print "aaaaaaaa"
        self.mediaPlayer.setVideoOutput(self.ui.videoWidget)
        self.mediaPlayer.setPlaylist(self._playlist)

        self.mediaPlayer.play()
        self._stopped = False

    def positionChanged(self, position):
        self.ui.positionSlider.setValue(position)

    def durationChanged(self, duration):
        self.ui.positionSlider.setRange(0, duration)

    def setPosition(self, position):
        self.mediaPlayer.setPosition(position)

    def handleError(self):
        self.playButton.setEnabled(False)
        self.errorLabel.setText("Error: " + self.mediaPlayer.errorString())



if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()

    sys.exit(app.exec_())
