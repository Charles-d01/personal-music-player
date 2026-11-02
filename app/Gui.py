import sys
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QLabel,
                             QVBoxLayout, QHBoxLayout, QPushButton, QStyle,
                             QSlider, QFileDialog)
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtCore import Qt
from mutagen import File


def get_music_art(mp3_path):
    audio = File(mp3_path)


    if audio is not None and audio.tags is not None:
        cover_data = audio.tags.getall("APIC")

        if cover_data:
               return cover_data[0].data
    return None

class Mainwind(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Audio Player")
        self.setGeometry(700,300,500,500)
        self.setWindowIcon(QIcon("iconfinder-musicmelodysoundaudio19-4105562_113867.png"))
        self.setStyleSheet("""
            QMainWindow {
                background-color: #171923
            }
        """)
        self.initUI()
        

    def initUI(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        song_title = QLabel("No song selected", central_widget)
        artist_label = QLabel("Choose a song to begin", central_widget)

        song_title.setStyleSheet("""
                                 color: #F7FAFC;
                                 font-size: 24px;
                                 font-weight: bold;
                                 """)
        
        artist_label.setStyleSheet("""
                                   color: #A0AEC0;
                                   font-size: 14px;
                                   """)

        # duration label 
        d_label1 = QLabel("00:00",central_widget)
        d_label2 = QLabel("00:00",central_widget)

        time_style = """
            color: #A0AEC0;
            font-size: 12px;
        
        """
        d_label1.setStyleSheet(time_style)
        d_label2.setStyleSheet(time_style)

        # Playback control
        previous_button = QPushButton()
        pre_icon = self.style().standardIcon(QStyle.SP_MediaSkipBackward)
        previous_button.setIcon(pre_icon)

        play_button = QPushButton()
        play_icon = self.style().standardIcon(QStyle.SP_MediaPlay)
        play_button.setIcon(play_icon)
        
        next_button = QPushButton()
        next_icon = self.style().standardIcon(QStyle.SP_MediaSkipForward)
        next_button.setIcon(next_icon)
        

        play_button.setStyleSheet("""
            QPushButton {
                background-color: #F7FAFC;
                color: #171923;
                border: none;
                border-radius: 25px;
                min-width: 50px;
                min-height: 50px;
                max-width: 50px;
                max-height: 50px;
                font-size: 20px;
                font-weight: bold;
                padding: 0px;
            }

            QPushButton:hover {
                background-color: #CBD5E0;
            }

            QPushButton:pressed {
                background-color: #A0AEC0;
            }
        """)

        control_style = """
            QPushButton {
                background-color: #A8ADD1;
                color: #CBD5E0;
                border: none;
                padding: 10px;
                font-size: 14px;
            }

            QPushButton:hover {
                color: #FFFFFF;
                background-color: #2D3748;
                border-radius: 8px;
            }
        """

        previous_button.setStyleSheet(control_style)
        next_button.setStyleSheet(control_style)

        # slider
        slider = QSlider()
        slider.setOrientation(Qt.Horizontal)
        slider.setRange(0,100)
        slider.setValue(0)

        slider.setStyleSheet("""
            QSlider::groove:horizontal {
                background: #4A5568;
                height: 5px;
                border-radius: 2px;
            }

            QSlider::handle:horizontal {
                background: #F7FAFC;
                width: 14px;
                height: 14px;
                margin: -5px 0;
                border-radius: 7px;
            }

            QSlider::sub-page:horizontal {
                background: #A8ADD1;
                border-radius: 2px;
            }

        """)

        #cover label
        mp3_path = self.select_song()

        
        self.cover_label = QLabel(central_widget)
        self.cover_label.setFixedSize(200,200)
        self.cover_label.setAlignment(Qt.AlignCenter)


        cover_data = get_music_art(mp3_path)
        
        if cover_data:
            pixmap = QPixmap()

            if pixmap.loadFromData(cover_data):
                self.cover_label.setPixmap(
                    pixmap.scaled(
                        200,200,
                        Qt.KeepAspectRatio,
                        Qt.SmoothTransformation
                                  )
                    )
            else:
                self.cover_label.setText("No Cover")

        else:  
            cover = QPixmap("images.jpg")

            if not cover.isNull():
                    self.cover_label.setPixmap(
                    cover.scaled(
                        200, 200,
                        Qt.KeepAspectRatio,
                        Qt.SmoothTransformation
                    )
                )
            else:
                 self.cover_label.setText("No Artwork Available")

        self.cover_label.setStyleSheet("""
            QLabel {
                background-color: #252A3A;
                border-radius: 12px;
                color: #A0AEC0;
            }
        """)
    
        # select file button

        select_button = QPushButton("Select File")
        select_button.clicked.connect(self.select_song)


        song_title.setAlignment(Qt.AlignCenter)
        artist_label.setAlignment(Qt.AlignCenter)

        vbox = QVBoxLayout()
        hbox = QHBoxLayout()
        time_layout = QHBoxLayout()

        vbox.setSpacing(5)
        vbox.setContentsMargins(20, 15, 20, 15)

        vbox.addWidget(self.cover_label, alignment= Qt.AlignCenter)
        vbox.addWidget(song_title)
        vbox.addWidget(artist_label)

        hbox.addStretch()
        hbox.addWidget(previous_button)
        hbox.addWidget(play_button)
        hbox.addWidget(next_button)
        hbox.addStretch()

        
        time_layout.addWidget(d_label1)
        time_layout.addStretch()
        time_layout.addWidget(d_label2)
        
        vbox.addWidget(select_button)
        vbox.addWidget(slider)
        
        vbox.addLayout(time_layout)
        vbox.addLayout(hbox)
    

        central_widget.setLayout(vbox)
    
    def select_song(self):
        file_path, _ = QFileDialog.getOpenFileName(
              self,
              "Select audio file",
              "",
              "Audio Files (*.mp3 *.wav  *.flac *.ogg);;All Files (*)"
         )   
        if file_path:
             return file_path

        #self.update_music_cover(file_path)

        return None
    

    def update_music_cover(self, song_path):
        music_art = get_music_art(song_path)

        pixmap = QPixmap()

        if music_art:
            pixmap.loadFromData(music_art)





def main():
    app = QApplication(sys.argv)
    window = Mainwind()
    window.show()
    sys.exit(app.exec_())
    

if __name__ == "__main__":
    main()