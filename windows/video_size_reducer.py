from PyQt5.QtWidgets import QMainWindow, QWidget, QPushButton, QLabel, QVBoxLayout, QFileDialog, QComboBox, QHBoxLayout, QScrollArea, QSplitter
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtCore import Qt
from PIL import Image

from termcolor import colored

from utils.styles import  button_dark_style, button_light_style
from utils.assets import is_dark_theme, settings

import subprocess
import ffmpeg
import sys
import io
import os

class VideoSizeReducer(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Decrease video size")
        self.setGeometry(500, 250, 800, 600)
        self.setObjectName("VideoSizeReducer")
        self.setup_video_decrease_size_page()
        self.set_styles()

    def setup_video_decrease_size_page(self):
        self.main_layout = QSplitter(Qt.Orientation.Horizontal, self)
        self.main_layout.setHandleWidth(10)

        # Left layout for options
        self.left_widget = QWidget()
        self.left_layout = QVBoxLayout(self.left_widget)
        self.left_widget.setMinimumWidth(200)

        # Video resolution
        self.resolution = QWidget()
        self.resolution_layout = QHBoxLayout(self.resolution)
        self.resolution_label = QLabel("Resolution")
        self.resolution_combo = QComboBox(self)
        self.resolution_combo.addItem("720", "720")
        self.resolution_combo.addItem("480", "480")
        self.resolution_combo.addItem("360", "360")
        self.resolution_combo.addItem("240", "240")
        self.resolution_combo.addItem("144", "144")
        self.resolution_combo.setCurrentIndex(0)
        self.resolution_combo.currentIndexChanged.connect(self.handle_resolution)
        self.resolution_layout.addWidget(self.resolution_label)
        self.resolution_layout.addWidget(self.resolution_combo)

        # Video codec
        self.video_codec = QWidget()
        self.video_codec_layout = QHBoxLayout(self.video_codec)
        self.video_codec_label = QLabel("Video codec")
        self.video_codec_combo = QComboBox(self)
        self.video_codec_combo.addItem("x264", "x264")
        self.video_codec_combo.addItem("x265", "x265")
        self.video_codec_combo.setCurrentIndex(0)
        self.video_codec_combo.currentIndexChanged.connect(self.handle_codec)
        self.video_codec_layout.addWidget(self.video_codec_label)
        self.video_codec_layout.addWidget(self.video_codec_combo)

        # Video bitrate
        self.video_bitrate = QWidget()
        self.video_bitrate_layout = QHBoxLayout(self.video_bitrate)
        self.video_bitrate_label = QLabel("Video Bitrate")
        self.video_bitrate_combo = QComboBox(self)
        self.video_bitrate_combo.addItem("500k", "500k")
        self.video_bitrate_combo.addItem("1M", "1M")
        self.video_bitrate_combo.addItem("2M", "2M")
        self.video_bitrate_combo.addItem("4M", "4M")
        self.video_bitrate_combo.setCurrentIndex(0)
        self.video_bitrate_combo.currentIndexChanged.connect(self.hanlde_video_bitrate)
        self.video_bitrate_layout.addWidget(self.video_bitrate_label)
        self.video_bitrate_layout.addWidget(self.video_bitrate_combo)

        # Audio codec
        self.audio_codec = QWidget()
        self.audio_codec_layout = QHBoxLayout(self.audio_codec)
        self.audio_codec_label = QLabel("Audio Codec")
        self.audio_codec_combo = QComboBox(self)
        self.audio_codec_combo.addItem("acc", "acc")
        self.audio_codec_combo.addItem("mp3", "mp3")
        self.audio_codec_combo.addItem("opus", "opus")
        self.audio_codec_combo.setCurrentIndex(0)
        self.audio_codec_combo.currentIndexChanged.connect(self.handle_audio_codec)
        self.audio_codec_layout.addWidget(self.audio_codec_label)
        self.audio_codec_layout.addWidget(self.audio_codec_combo)

        # Audio Bitrate
        self.audio_bitrate = QWidget()
        self.audio_bitrate_layout = QHBoxLayout(self.audio_bitrate)
        self.audio_bitrate_label = QLabel("Audio Bitrate")
        self.audio_bitrate_combo = QComboBox(self)
        self.audio_bitrate_combo.addItem("96k", "96k")
        self.audio_bitrate_combo.addItem("128k", "128k")
        self.audio_bitrate_combo.addItem("192k", "192k")
        self.audio_bitrate_combo.setCurrentIndex(0)
        self.audio_bitrate_combo.currentIndexChanged.connect(self.handle_audio_bitrate)
        self.audio_bitrate_layout.addWidget(self.audio_bitrate_label)
        self.audio_bitrate_layout.addWidget(self.audio_bitrate_combo)

        self.resolution.setStyleSheet("background-color: #262626")
        self.video_codec.setStyleSheet("background-color: #262626")
        self.video_bitrate.setStyleSheet("background-color: #262626")
        self.audio_codec.setStyleSheet("background-color: #262626")
        self.audio_bitrate.setStyleSheet("background-color: #262626")

        self.left_layout.addWidget(self.resolution)
        self.left_layout.addWidget(self.video_codec)
        self.left_layout.addWidget(self.video_bitrate)
        self.left_layout.addWidget(self.audio_codec)
        self.left_layout.addWidget(self.audio_bitrate)

        # Center layout
        self.center_layout = QSplitter(Qt.Orientation.Vertical)

        # Center top layout for scroll area
        self.video_container = QWidget()
        self.video_layout = QVBoxLayout(self.video_container)

        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setMinimumHeight(400)
        self.scroll_area.setMinimumWidth(560)
        self.scroll_area.setWidget(self.video_container)

        # Center bottom layout for buttons
        self.center_bottom_widget = QWidget()
        center_bottom_layout = QHBoxLayout(self.center_bottom_widget)
        self.center_bottom_widget.setFixedHeight(200)

        self.buttons_widget = QWidget()
        self.buttons_layout = QVBoxLayout(self.buttons_widget)
        self.buttons_layout.setContentsMargins(0,0,0,0)

        self.select_videos_button = QPushButton("Select Video")
        self.select_videos_button.clicked.connect(self.select_videos)

        self.remove_video_button = QPushButton("Remove Selected Video")
        self.remove_video_button.setEnabled(False)

        self.add_video_button = QPushButton("Add Another Video")
        self.add_video_button.setEnabled(False)

        self.confirm_reduce_button = QPushButton("Reduce")
        self.confirm_reduce_button.clicked.connect(self.confirm_reduce)
        self.confirm_reduce_button.setEnabled(False)

        self.output_videos_path_button = QPushButton("Select output path")
        self.output_videos_path_button.clicked.connect(self.handle_output_videos_path)
        self.output_videos_path_button.setEnabled(False)

        self.buttons_layout.addWidget(self.select_videos_button)
        self.buttons_layout.addWidget(self.remove_video_button)
        self.buttons_layout.addWidget(self.add_video_button)
        self.buttons_layout.addWidget(self.confirm_reduce_button)
        self.buttons_layout.addWidget(self.output_videos_path_button)
        
        self.general_info = QWidget()
        self.general_info_layout = QVBoxLayout(self.general_info)
        self.general_info.setStyleSheet("background-color: #262626")
        
        self.selected_videos = QLabel("Selected videos: ")
        self.total_size = QLabel("Total size: ")
        self.new_size = QLabel("New size:")
        self.reduced_size = QLabel("Reduced size: ")

        self.general_info_layout.addWidget(self.selected_videos)
        self.general_info_layout.addWidget(self.total_size)
        self.general_info_layout.addWidget(self.new_size)
        self.general_info_layout.addWidget(self.reduced_size)

        center_bottom_layout.addWidget(self.general_info)
        center_bottom_layout.addWidget(self.buttons_widget)

        self.center_layout.addWidget(self.scroll_area)
        self.center_layout.addWidget(self.center_bottom_widget)

        # Right layout for video info
        self.right_widget = QWidget()
        self.right_layout = QVBoxLayout(self.right_widget)
        self.right_widget.setMinimumWidth(200)
        self.right_widget.setMaximumWidth(500)

        # Video name
        self.video_name = QWidget()
        self.video_name_layout = QVBoxLayout(self.video_name)
        self.video_name_label = QLabel("Video Name: ")
        self.video_name_text = QLabel()
        self.video_name_layout.addWidget(self.video_name_label)
        self.video_name_layout.addWidget(self.video_name_text)

        # Video info
        self.video_info = QWidget()
        self.video_info_layout = QVBoxLayout(self.video_info)        
        self.video_info_label = QLabel("Video Info: ")
        self.video_info_text = QLabel()
        self.video_info_text.setWordWrap(True)
        self.video_info_layout.addWidget(self.video_info_label)
        self.video_info_layout.addWidget(self.video_info_text)

        # Aufio info
        self.audio_info = QWidget()
        self.audio_info_layout = QVBoxLayout(self.audio_info)
        self.audio_info_label = QLabel("Audio Info: ")
        self.audio_info_text = QLabel()
        self.audio_info_layout.addWidget(self.audio_info_label)
        self.audio_info_layout.addWidget(self.audio_info_text)

        self.video_name.setStyleSheet("background-color: #262626")
        self.video_info.setStyleSheet("background-color: #262626")
        self.audio_info.setStyleSheet("background-color: #262626")

        self.right_layout.addWidget(self.video_name)
        self.right_layout.addWidget(self.video_info)
        self.right_layout.addWidget(self.audio_info)

        # Add all layouts to the main layout
        self.main_layout.addWidget(self.left_widget)
        self.main_layout.addWidget(self.center_layout)
        self.main_layout.addWidget(self.right_widget)

        self.setCentralWidget(self.main_layout)

        if is_dark_theme():
            self.apply_video_decrease_size_dark_theme()
        else:
            self.apply_video_decrease_size_light_theme()

        self.video_files = []

    def confirm_reduce(self):
        target_width = ""
        for video in self.video_files:
            command = [
                "ffmpeg",
                "-i", video,
                "-vf", f"scale={target_width}", # Resize the video to target width, maintaining, aspect_ratio
                "-c:v", self.video_codec_combo.currentData(),
                "-b:v", "", # Set the video bitrate
                "-c:a", "", # Set the audio codec
                "-b:a", "", # Set the audio bitrate
            ]
            print(video)

    def hanlde_video_bitrate(self, index):
        self.video_bitrate_combo.setCurrentIndex(index)

    def handle_audio_codec(self, index):
        self.audio_codec_combo.setCurrentIndex(index)

    def handle_audio_bitrate(self, index):
        self.audio_bitrate_combo.setCurrentIndex(index)
    
    def handle_output_videos_path(self):
        output_path = QFileDialog.getExistingDirectory(None, "Select folder to save", settings.location)
        self.save_folder = output_path

    def handle_codec(self, index):
        self.video_codec_combo.setCurrentIndex(index)

    def handle_resolution(self, index):
        self.resolution_combo.setCurrentIndex(index)

    def select_videos(self):
        options = QFileDialog.Options()
        options |= QFileDialog.ReadOnly

        video_files, _ = QFileDialog.getOpenFileNames(self, "Select video File", settings.location, "Video Files (*.mp4 *.avi *.mkv)::All Files (*)", options=options)
        if video_files:
            self.video_files = video_files
            self.display_selected_vidoes(self.video_layout)
            total_size = self.calculate_videos_size()
            self.total_size.setText(f"Total size:  {str(total_size)} {"GB" if total_size > 1000 else " MB"}")
            self.selected_videos.setText(f"Selected videos:  {(len(self.video_files))}")

            self.remove_video_button.setEnabled(True)
            self.add_video_button.setEnabled(True)
            self.confirm_reduce_button.setEnabled(True)
            self.output_videos_path_button.setEnabled(True)

            video_info, audio_info = self.get_video_info(video_files[0])
            self.video_name_text.setText(os.path.basename(video_files[0]))
            self.video_info_label.setText(f"Video Info: \n\n{video_info}")
            self.audio_info_label.setText(f"Audio Info: \n\n{audio_info}")

    def calculate_videos_size(self):
        total_size = 0.0
        for video in self.video_files:
            probe = ffmpeg.probe(video)
            format_info = probe.get("format", {})
            file_size = format_info.get("size", "N/A")
            file_size = self.calculate_video_size(file_size)
            total_size += float(file_size)
        return total_size

    def display_selected_vidoes(self, layout):
        for i in reversed(range(layout.count())):
            widget_to_remove = layout.itemAt(i).widget()
            layout.removeWidget(widget_to_remove)
            widget_to_remove.setParent(None)

        for file in self.video_files:
            row_widget = QWidget()
            row_layout = QHBoxLayout()

            if is_dark_theme():
                row_widget.setStyleSheet("background-color: #202020; border-radius: 4px")
            else:
                row_widget.setStyleSheet("background-color: #f5f5f5; border-radius: 4px")

            row_widget.setLayout(row_layout)

            preview = self.extract_frame(file)

            label = QLabel()
            pixmap = QPixmap(preview)
            label.setPixmap(pixmap)
            row_layout.addWidget(label)

            name_label = QLabel(os.path.basename(file))
            name_label.setWordWrap(True)
            name_label.setFixedWidth(300)

            if is_dark_theme():
                name_label.setStyleSheet("color: #a3a3a3")
            else:
                name_label.setStyleSheet("color: #000000")

            row_layout.addWidget(name_label)

            layout.addWidget(row_widget)
            layout.setAlignment(Qt.AlignmentFlag.AlignTop)

    def extract_frame(self, file_path):
        try:
            process = (
                ffmpeg.input(file_path, ss=5) # capture a frame at 5 seconds
                .output("pipe:", vframes=1, format="image2", vcodec="png")
                .run(capture_stdout=True, capture_stderr=True)
            )

            image_bytes = io.BytesIO(process[0])

            image = Image.open(image_bytes)
            image = image.convert("RGBA") # Ensure image is RGBA format

            max_width, max_height = 200, 120
            image_width, image_height = image.size
            aspect_ratio = image_width / image_height

            if image_width > max_width or image_height > max_height:
                if aspect_ratio > 1:
                    new_width = min(image_width, max_width)
                    new_height = int(new_width / aspect_ratio)
                else:
                    new_height = min(image_height, max_height)
                    new_width = int(new_height * aspect_ratio)
                
                image = image.resize((new_width, new_height), Image.Resampling.LANCZOS)

            image_bytes = io.BytesIO()
            image.save(image_bytes, format="PNG")
            image_bytes.seek(0)

            qimage = QImage()
            qimage.loadFromData(image_bytes.read())

            pixmap = QPixmap.fromImage(qimage)
            return pixmap

        except ffmpeg.Error as e:
            print(colored(f"FFmpeg error: {e}", "red"))

        except Exception as e:
            print(colored(f"An error occurered: {e}", "red"))

    def get_video_info(self, file_path):
        try:
            probe = ffmpeg.probe(file_path)
            format_info = probe.get("format", {})
            video_streams = [ stream for stream in probe["streams"] if stream["codec_type"] == "video" ]
            audio_streams = [ stream for stream in probe["streams"] if stream["codec_type"] == "audio" ]

            format = format_info.get("format_name", "N/A").split(',')[1]
            file_size = format_info.get("size", "N/A")
            duration = format_info.get("duration", "N/A")

            for stream in video_streams:
                video_codec = stream.get("codec_name", "N/A")
                codec_long_name = stream.get("codec_long_name", "N/A")
                width = stream.get("width", "N/A")
                height = stream.get("height", "N/A")
                video_bitrate = stream.get("bit_rate", "N/A")
                frame_rate = stream.get("r_frame_rate", "N/A")
                pixel_format = stream.get("pix_fmt", "N/A")
                aspect_ratio = stream.get("display_aspect_ratio", "N/A")
                frame_count = stream.get("nb_frames", "N/A")

            file_size = self.calculate_video_size(file_size)

            duration = float(duration)
            hours = int(duration // 3600)
            minutes = int((duration % 3600) // 60)
            seconds = int(duration % 60)

            if hours > 0:
                video_duration = f"{hours}:{minutes}:{seconds}"
            else:
                video_duration = f"{minutes}:{seconds}"

            video_metadata = (
                f"Format:          {format}\n"
                f"File Size:       {file_size} MB\n"
                f"Duration:        {video_duration}\n"
                f"Codec:           {video_codec}\n"
                f"Codec Long Name: {codec_long_name}\n"
                f"Resolution:      {width}x{height}\n"
                f"Bitrate:         {video_bitrate}\n"
                f"Frame Rate:      {frame_rate}\n"
                f"Pixel Format:    {pixel_format}\n"
                f"Aspect Ratio:    {aspect_ratio}\n"
                f"Frame Count:     {frame_count}\n"
            )

            if audio_streams:
                for stream in audio_streams:
                    audio_codec = stream.get("codec_name", "N/A")
                    sample_rate = stream.get("sample_rate", "N/A")
                    channels = stream.get("channels", "N/A")
                    audio_bitrate = stream.get("bit_rate", "N/A")
                    audio_language = stream.get("tags", {}).get("language", "N/A")

                audio_metadata = (
                    f"Codec:           {audio_codec}\n"
                    f"Codec Long Name: {codec_long_name}\n"
                    f"Sample Rate:     {sample_rate}\n"
                    f"Channels:        {channels}\n"
                    f"Bitrate:         {audio_bitrate}\n"
                    f"Language:        {audio_language}\n"
                )

            return video_metadata, audio_metadata

        except ffmpeg.Error as e:
            print(colored(e, "red"))

    def calculate_video_size(self, file_size):
        file_size_int = int(file_size)
        if file_size_int > 1000 and file_size_int < 1000000:
            file_size = round(file_size_int / 1000, 2)

        if file_size_int > 1000000:
            file_size = round(file_size_int / 1000000, 2)

        return file_size

    def set_styles(self):
        if is_dark_theme():
            self.setStyleSheet("QWidget#VideoSizeReducer { background-color: #262626 } ")
        else:
            self.setStyleSheet("QWidget#VideoSizeReducer { background-color: #e5e5e5 }")

    def apply_video_decrease_size_dark_theme(self):
        self.video_container.setStyleSheet("background-color: #171717")
        self.left_widget.setStyleSheet("background-color: #171717")
        self.center_bottom_widget.setStyleSheet("background-color: #171717")
        self.right_widget.setStyleSheet("background-color: #171717")
        self.select_videos_button.setStyleSheet(button_dark_style)
        self.add_video_button.setStyleSheet(button_dark_style)
        self.confirm_reduce_button.setStyleSheet(button_dark_style)
        self.output_videos_path_button.setStyleSheet(button_dark_style)
        self.remove_video_button.setStyleSheet(button_dark_style)
        
    def apply_video_decrease_size_light_theme(self):
        self.select_videos_button.setStyleSheet(button_light_style)
        self.add_video_button.setStyleSheet(button_light_style)
        self.remove_video_button.setStyleSheet(button_light_style)
