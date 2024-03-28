import sys
import os
import pytube
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.url_input = QLineEdit()
        self.search_button = QPushButton("Search")
        self.format_combobox = QComboBox()
        self.save_location_input = QLineEdit()
        self.download_button = QPushButton("Download")

        self.status_label = QLabel()

        self.layout = QVBoxLayout()
        self.layout.addWidget(QLabel("YouTube Video Downloader"))
        self.layout.addWidget(QLabel("YouTube Video URL:"))
        self.layout.addWidget(self.url_input)
        self.layout.addWidget(self.search_button)
        self.layout.addWidget(QLabel("Available Formats:"))
        self.layout.addWidget(self.format_combobox)
        self.layout.addWidget(QLabel("Save Location:"))
        self.layout.addWidget(self.save_location_input)
        self.layout.addWidget(self.download_button)
        self.layout.addWidget(self.status_label)

        self.central_widget = QWidget()
        self.central_widget.setLayout(self.layout)
        self.setCentralWidget(self.central_widget)

        self.search_button.clicked.connect(self.search_for_formats)
        self.download_button.clicked.connect(self.download_video)

        self.show()

    def search_for_formats(self):
        video_url = self.url_input.text()
        if not video_url:
            self.status_label.setText("Please enter a YouTube video URL.")
            return

        try:
            video = pytube.YouTube(video_url)
        except pytube.exceptions.VideoUnavailable:
            self.status_label.setText("The video is unavailable.")
            return

        self.format_combobox.clear()
        for format in video.streams:
            self.format_combobox.addItem(format.resolution)

    def download_video(self):
        video_url = self.url_input.text()
        if not video_url:
            self.status_label.setText("Please enter a YouTube video URL.")
            return

        format = self.format_combobox.currentText()
        if not format:
            self.status_label.setText("Please select a format.")
            return

        save_location = self.save_location_input.text()
        if not save_location:
            self.status_label.setText("Please enter a save location.")
            return

        try:
            video = pytube.YouTube(video_url)
        except pytube.exceptions.VideoUnavailable:
            self.status_label.setText("The video is unavailable.")
            return

        video.streams.filter(resolution=format).first().download(save_location)
        self.status_label.setText("The video has been downloaded.")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = MainWindow()
    sys.exit(app.exec_())
