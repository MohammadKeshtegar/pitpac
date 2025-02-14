from PyQt5.QtWidgets import QMainWindow, QWidget, QPushButton, QLabel, QVBoxLayout, QFileDialog, QComboBox, QHBoxLayout, QScrollArea, QSplitter, QLineEdit, QMessageBox, QProgressBar
from PyQt5.QtGui import QImage, QPixmap, QIntValidator, QIcon
from PyQt5.QtCore import Qt, QProcess
from PIL import Image

from termcolor import colored

from utils.guides import RESOLUTION_GUIDE, VIDEO_CODEC_GUIDE, VIDEO_BITRATE_GUIDE, AUDIO_BITRATE_GUIDE, AUDIO_CODEC_GUIDE
from utils.styles import  button_dark_style, button_light_style
from utils.assets import is_dark_theme, settings, PATH_TO_FILE

import ffmpeg
import io
import os

class VideoSizeReducer(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Decrease video size")
        self.setGeometry(500, 250, 800, 600)
        self.setObjectName("VideoSizeReducer")
        self.is_default_video_bitrate = False

        self.processes = []
        self.total_frames = {}
        self.video_durations = {}
        self.current_video_index = 0
        self.cancel_requested = False

        self.setup_video_decrease_size_page()
        self.set_styles()

    def setup_video_decrease_size_page(self):
        self.main_layout = QSplitter(Qt.Orientation.Horizontal, self)
        self.main_layout.setHandleWidth(10)

        # Left layout for options
        self.left_widget = QWidget()
        self.left_layout = QVBoxLayout(self.left_widget)
        self.left_widget.setMinimumWidth(260)

        # Video resolution
        self.resolution = QWidget()
        self.resolution_layout = QHBoxLayout(self.resolution)
        self.resolution_layout.setContentsMargins(5,5,5,5)

        self.resolution_info_button = QPushButton('!')
        self.resolution_info_button.setFixedWidth(20)
        self.resolution_info_button.clicked.connect(self.show_resolution_info_guide)

        self.resolution_label = QLabel("Resolution", self.resolution)
        self.resolution_combo = QComboBox(self.resolution)
        self.resolution_combo.addItem("1080", "1920:1080")
        self.resolution_combo.addItem("720", "1280:720")
        self.resolution_combo.addItem("480", "854:480")
        self.resolution_combo.addItem("360", "640:360")
        self.resolution_combo.addItem("240", "426:240")
        self.resolution_combo.setCurrentIndex(0)
        self.resolution_combo.setEnabled(False)
        self.resolution_combo.currentIndexChanged.connect(self.handle_resolution)

        self.resolution_layout.addWidget(self.resolution_info_button, alignment=Qt.AlignmentFlag.AlignTop)
        self.resolution_layout.addWidget(self.resolution_label)
        self.resolution_layout.addWidget(self.resolution_combo)

        # Video codec
        self.video_codec = QWidget()
        self.video_codec_layout = QHBoxLayout(self.video_codec)
        self.video_codec_layout.setContentsMargins(5,5,5,5)

        self.video_codec_info_button = QPushButton('!')
        self.video_codec_info_button.setFixedWidth(20)
        self.video_codec_info_button.clicked.connect(self.show_video_codec_info_guide)

        self.video_codec_label = QLabel("Video codec")
        self.video_codec_combo = QComboBox(self.video_codec)
        self.video_codec_combo.addItem("H.264", "libx264")
        self.video_codec_combo.addItem("H.265", "libx265")
        self.video_codec_combo.addItem("VPB/VP9", "libvpx")
        self.video_codec_combo.addItem("AV1", "libaom")
        self.video_codec_combo.addItem("MPEG-2", "mpeg2video")
        self.video_codec_combo.addItem("ProRes", "prores")
        self.video_codec_combo.setCurrentIndex(0)
        self.video_codec_combo.setEnabled(False)
        self.video_codec_combo.currentIndexChanged.connect(self.handle_codec)

        self.video_codec_layout.addWidget(self.video_codec_info_button, alignment=Qt.AlignmentFlag.AlignTop)
        self.video_codec_layout.addWidget(self.video_codec_label)
        self.video_codec_layout.addWidget(self.video_codec_combo)

        # Video bitrate
        self.video_bitrate = QWidget()
        self.video_bitrate_layout = QHBoxLayout(self.video_bitrate)
        self.video_bitrate_layout.setContentsMargins(5,5,5,5)

        self.video_bitrate_info_button = QPushButton('!')
        self.video_bitrate_info_button.setFixedWidth(20)
        self.video_bitrate_info_button.clicked.connect(self.show_video_bitrate_info_guide)

        self.video_bitrate_label = QLabel("Video Bitrate")
        self.video_bitrate_field = QLineEdit()
        self.video_bitrate_field.setEnabled(False)
        self.video_bitrate_field.setStyleSheet("background-color: #424242")
        self.video_bitrate_field.setFixedWidth(40)
        self.video_bitrate_field.textChanged.connect(self.hanlde_video_bitrate)
        self.video_bitrate_field.setValidator(QIntValidator())

        self.increase_video_bitrate_button = QPushButton()
        self.decrease_video_bitrate_button = QPushButton()

        self.increase_video_bitrate_button.setEnabled(False)
        self.decrease_video_bitrate_button.setEnabled(False)

        self.video_bitrate_fields_widget = QWidget() 
        self.video_bitrate_fields_widget.setFixedWidth(120)
        self.video_bitrate_fields_layout = QHBoxLayout(self.video_bitrate_fields_widget)

        self.increase_video_bitrate_button.setFixedWidth(40)
        self.decrease_video_bitrate_button.setFixedWidth(40)

        self.increase_video_bitrate_button.clicked.connect(self.increase_video_bitrate)
        self.decrease_video_bitrate_button.clicked.connect(self.decrease_video_bitrate)

        self.video_bitrate_fields_layout.addWidget(self.decrease_video_bitrate_button) 
        self.video_bitrate_fields_layout.addWidget(self.video_bitrate_field) 
        self.video_bitrate_fields_layout.addWidget(self.increase_video_bitrate_button)

        self.video_bitrate_layout.addWidget(self.video_bitrate_info_button, alignment=Qt.AlignmentFlag.AlignTop)
        self.video_bitrate_layout.addWidget(self.video_bitrate_label)
        self.video_bitrate_layout.addWidget(self.video_bitrate_fields_widget)

        # Audio codec
        self.audio_codec = QWidget()
        self.audio_codec_layout = QHBoxLayout(self.audio_codec)
        self.audio_codec_layout.setContentsMargins(5,5,5,5)

        self.audio_codec_info_button = QPushButton('!')
        self.audio_codec_info_button.setFixedWidth(20)
        self.audio_codec_info_button.clicked.connect(self.show_audio_codec_info_guide)

        self.audio_codec_label = QLabel("Audio Codec")
        self.audio_codec_combo = QComboBox(self.audio_codec)
        self.audio_codec_combo.addItem("AAC", "aac")
        self.audio_codec_combo.addItem("MP3", "libmp3lame")
        self.audio_codec_combo.addItem("Opus", "libopus")
        self.audio_codec_combo.addItem("FLAC", "flac")
        self.audio_codec_combo.addItem("Vorbis", "libvorbis")
        self.audio_codec_combo.addItem("AC3", "ac3")
        self.audio_codec_combo.setEnabled(False)
        self.audio_codec_combo.setCurrentIndex(0)
        self.audio_codec_combo.currentIndexChanged.connect(self.handle_audio_codec)

        self.audio_codec_layout.addWidget(self.audio_codec_info_button, alignment=Qt.AlignmentFlag.AlignTop)
        self.audio_codec_layout.addWidget(self.audio_codec_label)
        self.audio_codec_layout.addWidget(self.audio_codec_combo)

        # Audio Bitrate
        self.audio_bitrate = QWidget()
        self.audio_bitrate_layout = QHBoxLayout(self.audio_bitrate)
        self.audio_bitrate_layout.setContentsMargins(5,5,5,5)

        self.audio_bitrate_info_button = QPushButton('!')
        self.audio_bitrate_info_button.setFixedWidth(20)
        self.audio_bitrate_info_button.clicked.connect(self.show_audio_bitrate_info_guide)

        self.audio_bitrate_label = QLabel("Audio Bitrate")
        self.audio_bitrate_field = QLineEdit()
        self.audio_bitrate_field.setEnabled(False)
        self.audio_bitrate_field.setFixedWidth(40)
        self.audio_bitrate_field.setStyleSheet("background-color: #424242")
        self.audio_bitrate_field.setValidator(QIntValidator())
        self.audio_bitrate_field.textChanged.connect(self.handle_audio_bitrate)

        self.audio_bitrate_layout.addWidget(self.audio_bitrate_info_button, alignment=Qt.AlignmentFlag.AlignTop)
        self.audio_bitrate_layout.addWidget(self.audio_bitrate_label)
        self.audio_bitrate_layout.addWidget(self.audio_bitrate_field)

        self.increase_audio_bitrate_button = QPushButton()
        self.decrease_audio_bitrate_button = QPushButton()

        self.increase_audio_bitrate_button.setEnabled(False)
        self.decrease_audio_bitrate_button.setEnabled(False)
        
        self.audio_bitrate_fields_widget = QWidget()
        self.audio_bitrate_fields_widget.setFixedWidth(120)
        self.audio_bitrate_fields_layout = QHBoxLayout(self.audio_bitrate_fields_widget)

        self.increase_audio_bitrate_button.setFixedWidth(40)
        self.decrease_audio_bitrate_button.setFixedWidth(40)

        self.increase_audio_bitrate_button.clicked.connect(self.increase_audio_bitrate)
        self.decrease_audio_bitrate_button.clicked.connect(self.decrease_audio_bitrate)

        self.audio_bitrate_fields_layout.addWidget(self.decrease_audio_bitrate_button) 
        self.audio_bitrate_fields_layout.addWidget(self.audio_bitrate_field) 
        self.audio_bitrate_fields_layout.addWidget(self.increase_audio_bitrate_button)

        self.audio_bitrate_layout.addWidget(self.audio_bitrate_label)
        self.audio_bitrate_layout.addWidget(self.audio_bitrate_fields_widget)

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
        self.center_bottom_layout = QHBoxLayout(self.center_bottom_widget)
        self.center_bottom_widget.setFixedHeight(200)

        self.buttons_widget = QWidget()
        self.buttons_layout = QVBoxLayout(self.buttons_widget)
        self.buttons_layout.setContentsMargins(0,0,0,0)

        self.select_videos_button = QPushButton("Select Video")
        self.select_videos_button.clicked.connect(self.select_videos)

        self.remove_video_button = QPushButton("Remove Selected Video")
        self.remove_video_button.setEnabled(False)

        self.add_video_button = QPushButton("Add Video")
        self.add_video_button.setEnabled(False)

        self.confirm_reduce_button = QPushButton("Reduce")
        self.confirm_reduce_button.clicked.connect(self.confirm_reduce)
        self.confirm_reduce_button.setEnabled(False)
        
        self.exit_button = QPushButton("Cancel")
        self.exit_button.clicked.connect(self.cancel_reduce)

        self.buttons_layout.addWidget(self.select_videos_button)
        self.buttons_layout.addWidget(self.remove_video_button)
        self.buttons_layout.addWidget(self.add_video_button)
        self.buttons_layout.addWidget(self.confirm_reduce_button)
        self.buttons_layout.addWidget(self.exit_button)
        
        self.center_left = QWidget()
        self.center_left.setFixedWidth(265)
        self.center_left_layout = QVBoxLayout(self.center_left)
        self.center_left_layout.setContentsMargins(0, 0, 0, 0)

        self.general_info = QWidget()
        self.general_info_layout = QVBoxLayout(self.general_info)
        self.general_info.setStyleSheet("background-color: #262626")

        self.selected_videos = QLabel("Selected videos: ")
        self.total_size = QLabel("Total size: ")

        self.general_info_layout.addWidget(self.selected_videos)
        self.general_info_layout.addWidget(self.total_size)

        self.process_info = QWidget()
        self.process_info.setStyleSheet("background-color: #262626")
        self.process_info_layout = QVBoxLayout(self.process_info)

        self.finished_videos = QLabel("Done: ")

        self.progress_bar = QProgressBar()

        self.process_info_layout.addWidget(self.finished_videos)
        self.process_info_layout.addWidget(self.progress_bar)

        self.center_left_layout.addWidget(self.general_info)
        self.center_left_layout.addWidget(self.process_info)

        self.center_bottom_layout.addWidget(self.center_left)
        self.center_bottom_layout.addWidget(self.buttons_widget)

        self.center_layout.addWidget(self.scroll_area)
        self.center_layout.addWidget(self.center_bottom_widget)

        # Right layout for video info
        self.right_widget = QWidget()
        self.right_layout = QVBoxLayout(self.right_widget)
        self.right_widget.setMinimumWidth(250)
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

        self.apply_icon_style()

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
        output_path = QFileDialog.getExistingDirectory(None, "Select folder to save", settings.location)
        self.output_path = output_path
        self.current_video_index = 0
        self.cancel_requested = False
        self.start_processing_next_video()

    def start_processing_next_video(self):
        if self.cancel_requested or self.current_video_index >= len(self.video_files):
            print("All videos processed")
            return
        
        video = self.video_files[self.current_video_index]
        duration = self.get_video_duration(video)
        if duration > 0:
            self.total_frames[video] = self.get_total_frames(video)
            self.video_durations[video] = duration
            output_file = os.path.join(self.output_path, os.path.basename(video))
            
            if os.path.exists(output_file):
                reply = QMessageBox.question(
                    None,
                    "File Exists",
                    f"The file '{os.path.basename(output_file)}' already exists. Do you want to overwrite it?",
                    QMessageBox.Yes | QMessageBox.No,
                    QMessageBox.No
                )

                if reply == QMessageBox.No:
                    print(f"Skipping video {video} due to existing file")
                    self.current_video_index += 1
                    self.start_processing_next_video()
                    return

            self.process_video(video, self.output_path)
        else:
            print(f"Skipping video {video} due to invalid duration")
            self.current_video_index += 1
            self.start_processing_next_video()

    def process_video(self, video, output_path):
        command = [
            "ffmpeg",
            "-i", f'"{video}"',
            "-vf", f"scale={self.resolution_combo.currentData()}",
            "-c:v", self.video_codec_combo.currentData(),
            "-c:a", self.audio_codec_combo.currentData()
        ]
        if self.video_bitrate_field.text() != '':
            command.extend(["-b:v", self.video_bitrate_field.text()])
        if self.audio_bitrate_field.text() != '':
            command.extend(["-b:a", self.audio_bitrate_field.text()])

        output_file = os.path.join(output_path, os.path.basename(video))
        if os.path.exists(output_file):
            command.append('-y')  # Overwrite existing file if user agrees

        command.append(f'"{output_file}"')

        self.run_command(video, command)

    def run_command(self, video, command):
        process = QProcess(self)
        self.processes.append(process)
        process.setProcessChannelMode(QProcess.ProcessChannelMode.MergedChannels)
        process.finished.connect(lambda exit_code, exit_status, v=video, p=process: self.on_process_finished(exit_code, exit_status, v, p))
        process.readyReadStandardOutput.connect(lambda v=video, p=process: self.update_progress(v, p))
        process.start(" ".join(command))

    def update_progress(self, video, process):
        output = str(process.readAllStandardOutput(), "utf-8")

        if "time=" in output:
            time_str = output.split("time=")[-1].split(" ")[0]
            time_parts = time_str.split(':')

            if 'N/A' in time_parts:
                return

            try:
                seconds = int(time_parts[0]) * 3600 + int(time_parts[1]) * 60 + float(time_parts[2])
                if self.video_durations[video] > 0:
                    progress = (seconds / self.video_durations[video]) * 100
                    self.progress_bar.setValue(int(progress))
            except ValueError as e:
                print(f"Error in parsing time: {e}")

    def on_process_finished(self, exit_code, exit_status, video, process):
        self.progress_bar.setValue(100)
        process.terminate()
        process.waitForFinished()
        self.progress_bar.reset()
        self.current_video_index += 1
        self.finished_videos.setText(f"Done: {self.current_video_index}/{len(self.video_files)}")
        self.start_processing_next_video()

    def get_total_frames(self, video_file):
        command = [
            "ffmpeg",
            "-i", video_file,
            "-map", "0:v:0",
            "-c", "copy",
            "-f", "null",
            "-"
        ]
        process = QProcess(self)
        process.start(" ".join(command))
        process.waitForFinished()

        output = str(process.readAllStandardError(), "utf-8")
        for line in output.split('\n'):
            if "frame=" in line:
                return int(line.split('=')[1].strip())

        return 0
    
    def get_video_duration(self, video_file):
        command = [
            "ffprobe",
            "-v", "error",
            "-show_entries", "format=duration",
            "-of", "default=noprint_wrappers=1:nokey=1",
            f'"{video_file}"'
        ]
        process = QProcess(self)
        process.start(" ".join(command))
        process.waitForFinished()

        output = str(process.readAllStandardOutput(), "utf-8").strip()

        if output:
            try:
                return float(output)
            except ValueError as e:
                print(f"Error in parsing video duration: {e}")
                return 0.0
        else:
            print("No duration output from ffprobe")
            return 0.0

    def cancel_reduce(self):
        self.cancel_requested = True
        for process in self.processes:
            if process.state() == QProcess.ProcessState.Running:
                process.terminate()
                process.waitForFinished()
        self.progress_bar.reset()
        self.processes.clear()

    def set_video_bitrate_min_max(self):
        match self.video_codec_combo.currentData():
            case 'libx264':
                self.min_video_bit = 500
                self.max_video_bit = 40000
            case 'libx265':
                self.min_video_bit = 250
                self.max_video_bit = 20000
            case 'libvpx':
                self.min_video_bit = 250
                self.max_video_bit = 6000
            case 'libaom':
                self.min_video_bit = 200
                self.max_video_bit = 16000
            case 'flac':
                self.min_video_bit = 500
                self.max_video_bit = 10000

    def set_audio_bitrate_min_max(self):
        match self.audio_codec_combo.currentData():
            case "aac" | "libmp3lame" | "vorbis":
                self.min_audio_bit = 64
                self.max_audio_bit = 320
            case 'libvpx':
                self.min_audio_bit = 6
                self.max_audio_bit = 128

    def hanlde_video_bitrate(self, text):
        try:
            int_text = int(text)
        except:
            int_text = None

        if int_text is None or int_text > self.max_video_bit or int_text < self.min_video_bit:
            return

        self.handle_increase_decrease_video_bitreate_buttons()

    def increase_video_bitrate(self):
        new_video_bitrate = int(self.video_bitrate_field.text()) + 100
        if new_video_bitrate > self.max_video_bit:
            self.video_bitrate_field.setText(str(self.max_video_bit))
        else:
            self.video_bitrate_field.setText(str(new_video_bitrate))

    def decrease_video_bitrate(self):
        new_video_bitrate = int(self.video_bitrate_field.text()) - 100
        if new_video_bitrate < self.min_video_bit:
            self.video_bitrate_field.setText(str(self.min_video_bit))
        else:
            self.video_bitrate_field.setText(str(new_video_bitrate))

    def handle_audio_codec(self, index):
        self.audio_codec_combo.setCurrentIndex(index)

    def handle_guide(self):
        self.guide = QWidget()

    def handle_audio_bitrate(self, text):
        try:
            int_text = int(text)
        except:
            int_text = None

        if int_text == None or int_text > self.max_audio_bit or int_text < self.min_audio_bit:
            return

        self.handle_increase_decrease_audio_bitreate_buttons()

    def increase_audio_bitrate(self):
        new_audio_bitrate = int(self.audio_bitrate_field.text()) + 100
        if new_audio_bitrate > self.max_audio_bit:
            self.audio_bitrate_field.setText(self.max_audio_bit)
        else:
            self.audio_bitrate_field.setText(new_audio_bitrate)

    def decrease_audio_bitrate(self):
        new_audio_bitrate = int(self.audio_bitrate_field.text()) - 100
        if new_audio_bitrate < self.min_audio_bit:
            self.audio_bitrate_field.setText(self.min_audio_bit)
        else:
            self.audio_bitrate_field.setText(new_audio_bitrate)

    def handle_codec(self, index):
        self.video_codec_combo.setCurrentIndex(index)

    def handle_resolution(self, index):
        self.resolution_combo.setCurrentIndex(index)

    def select_videos(self):
        options = QFileDialog.Options()
        options |= QFileDialog.ReadOnly
        video_files, _ = QFileDialog.getOpenFileNames(self, "Select video File", settings.location, "Video Files (*.mp4 *.avi *.mkv)::All Files (*)", options=options)

        if video_files:
            self.resolution_combo.setEnabled(True)
            self.video_bitrate_field.setEnabled(True)
            self.audio_bitrate_field.setEnabled(True)
            self.video_codec_combo.setEnabled(True)
            self.audio_codec_combo.setEnabled(True)

            self.set_video_bitrate_min_max()
            self.set_audio_bitrate_min_max()

            self.video_bitrate_field.setValidator(QIntValidator(0, self.max_video_bit))
            self.audio_bitrate_field.setValidator(QIntValidator(0, self.max_audio_bit))

            self.handle_increase_decrease_video_bitreate_buttons()
            self.handle_increase_decrease_audio_bitreate_buttons()

            self.video_files = video_files
            self.display_selected_vidoes(self.video_layout)
            total_size, final_unit = self.calculate_videos_size()
            self.total_size.setText(f"Total size:  {str(total_size)} {final_unit}")
            self.selected_videos.setText(f"Selected videos:  {(len(self.video_files))}")
            self.finished_videos.setText(f"Done: {self.current_video_index}/{len(self.video_files)}")

            self.remove_video_button.setEnabled(True)
            self.add_video_button.setEnabled(True)
            self.confirm_reduce_button.setEnabled(True)

            video_info, audio_info = self.get_video_info(video_files[0])
            self.video_name_text.setText(os.path.basename(video_files[0]))
            self.video_info_label.setText(f"Video Info: \n\n{video_info}")
            self.audio_info_label.setText(f"Audio Info: \n\n{audio_info}")

    def handle_increase_decrease_video_bitreate_buttons(self):
        video_bitrate_value = self.video_bitrate_field.text()
        if video_bitrate_value is not None and video_bitrate_value != '':
            self.increase_video_bitrate_button.setEnabled(True)
            self.decrease_video_bitrate_button.setEnabled(True)

    def handle_increase_decrease_audio_bitreate_buttons(self):
        audio_bitrate_value = self.audio_bitrate_field.text()
        if audio_bitrate_value is not None and audio_bitrate_value != '':
            self.increase_audio_bitrate_button.setEnabled(True)
            self.decrease_audio_bitrate_button.setEnabled(True)

    def calculate_videos_size(self):
        total_size = 0.0
        for video in self.video_files:
            probe = ffmpeg.probe(video)
            format_info = probe.get("format", {})
            file_size = format_info.get("size", "N/A")
            file_size, _ = self.calculate_video_size(file_size)
            total_size += float(file_size)

        if total_size > 1000 :
            total_size = round(total_size / 1000, 2)
            final_unit = "GB"
        else:
            total_size = round(total_size, 2)
            final_unit = "MB"

        return total_size, final_unit

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
                row_widget.setStyleSheet("background-color: #d4d4d4; border-radius: 4px")

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

            file_size, file_size_unit = self.calculate_video_size(file_size)

            duration = float(duration)
            self.video_duration = duration
            hours = int(duration // 3600)
            minutes = int((duration % 3600) // 60)
            seconds = int(duration % 60)

            if hours > 0:
                video_duration = f"{hours}:{minutes}:{seconds}"
            else:
                video_duration = f"{minutes}:{seconds}"

            video_metadata = (
                f"Format:          {format}\n"
                f"File Size:       {file_size} {file_size_unit}\n"
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

            self.resolution_combo.setCurrentText(str(height))

            # if video_bitrate == "N/A":
            #     match height:
            #         case 1080:
            #             self.video_bitrate_field.setText("8000")
            #         case 720:
            #             self.video_bitrate_field.setText("3000")
            #         case 480:
            #             self.video_bitrate_field.setText("1500")

            # if audio_bitrate == "N/A":
            #     match audio_codec:
            #         case "aac":
            #             if channels == 2:
            #                 self.audio_bitrate_field.setText("128k")
            #             else:
            #                 self.audio_bitrate_field.setText("384k")
            #         case "libmp3lame" | "libvorbis":
            #             self.audio_bitrate_field.setText("128k")
            #         case "libopus":
            #             self.audio_bitrate_field.setText("48k")
            #         case "flac":
            #             self.audio_bitrate_field.setText("500k")

            return video_metadata, audio_metadata

        except ffmpeg.Error as e:
            print(colored(e, "red"))

    def calculate_video_size(self, file_size):
        file_size_int = int(file_size)
        if file_size_int > 1000000 and file_size_int < 1000000000:
            file_size = round(file_size_int / 1000000, 2)
            file_size_unit = 'MB'

        if file_size_int > 1000000000:
            file_size = round(file_size_int / 1000000000, 2)
            file_size_unit = 'GB'

        return file_size, file_size_unit

    def show_resolution_info_guide(self):
        self.resolution_info_message_box = QMessageBox()
        self.resolution_info_message_box.setText(RESOLUTION_GUIDE)
        self.resolution_info_message_box.exec()

    def show_video_codec_info_guide(self):
        self.video_codec_info_message_box = QMessageBox()
        self.video_codec_info_message_box.setText(VIDEO_CODEC_GUIDE)
        self.video_codec_info_message_box.exec()

    def show_audio_codec_info_guide(self):
        self.audio_codec_info_message_box = QMessageBox()
        self.audio_codec_info_message_box.setText(AUDIO_CODEC_GUIDE)
        self.audio_codec_info_message_box.exec()

    def show_video_bitrate_info_guide(self):
        self.video_bitrate_info_message_box = QMessageBox()
        self.video_bitrate_info_message_box.setText(VIDEO_BITRATE_GUIDE)
        self.video_bitrate_info_message_box.exec()

    def show_audio_bitrate_info_guide(self):
        self.audio_bitrate_info_message_box = QMessageBox()
        self.audio_bitrate_info_message_box.setText(AUDIO_BITRATE_GUIDE)
        self.audio_bitrate_info_message_box.exec()

    def set_styles(self):
        if is_dark_theme():
            self.setStyleSheet("QWidget#VideoSizeReducer { background-color: #262626 } ")
        else:
            self.setStyleSheet("QWidget#VideoSizeReducer { background-color: #f5f5f5 }")

    def apply_icon_style(self):
        if is_dark_theme():
            self.increase_video_bitrate_button.setIcon(QIcon(f"{PATH_TO_FILE}plus-bold-dark.svg"))
            self.decrease_video_bitrate_button.setIcon(QIcon(f"{PATH_TO_FILE}minus-bold-dark.svg"))
            self.increase_audio_bitrate_button.setIcon(QIcon(f"{PATH_TO_FILE}plus-bold-dark.svg"))
            self.decrease_audio_bitrate_button.setIcon(QIcon(f"{PATH_TO_FILE}minus-bold-dark.svg"))
        else:
            self.increase_video_bitrate_button.setIcon(QIcon(f"{PATH_TO_FILE}plus-bold-light.svg"))
            self.decrease_video_bitrate_button.setIcon(QIcon(f"{PATH_TO_FILE}minus-bold-light.svg"))
            self.increase_audio_bitrate_button.setIcon(QIcon(f"{PATH_TO_FILE}plus-bold-light.svg"))
            self.decrease_audio_bitrate_button.setIcon(QIcon(f"{PATH_TO_FILE}minus-bold-light.svg"))

    def apply_video_decrease_size_dark_theme(self):
        self.video_container.setStyleSheet("background-color: #171717")
        self.left_widget.setStyleSheet("background-color: #171717")
        self.center_bottom_widget.setStyleSheet("background-color: #171717")
        self.right_widget.setStyleSheet("background-color: #171717")
        self.progress_bar.setStyleSheet("background-color: #424242")

        self.select_videos_button.setStyleSheet(button_dark_style)
        self.add_video_button.setStyleSheet(button_dark_style)
        self.confirm_reduce_button.setStyleSheet(button_dark_style)
        self.exit_button.setStyleSheet(button_dark_style)
        self.remove_video_button.setStyleSheet(button_dark_style)

        self.resolution_info_button.setStyleSheet(button_dark_style)
        self.video_bitrate_info_button.setStyleSheet(button_dark_style)
        self.video_codec_info_button.setStyleSheet(button_dark_style)
        self.audio_bitrate_info_button.setStyleSheet(button_dark_style)
        self.audio_codec_info_button.setStyleSheet(button_dark_style)

        self.video_name.setStyleSheet("background-color: #262626")
        self.video_info.setStyleSheet("background-color: #262626")
        self.audio_info.setStyleSheet("background-color: #262626")

    def apply_video_decrease_size_light_theme(self):
        self.video_container.setStyleSheet("background-color: #eeeeee")
        self.left_widget.setStyleSheet("background-color: #d4d4d4")
        self.center_bottom_widget.setStyleSheet("background-color: #d4d4d4")
        self.right_widget.setStyleSheet("background-color: #d4d4d4")
        self.progress_bar.setStyleSheet("background-color: #dddddd")
        
        self.general_info.setStyleSheet("background-color: #f5f5f5; color: #000")
        self.buttons_widget.setStyleSheet("background-color: #dddddd")

        self.select_videos_button.setStyleSheet(button_light_style)
        self.add_video_button.setStyleSheet(button_light_style)
        self.confirm_reduce_button.setStyleSheet(button_light_style)
        self.exit_button.setStyleSheet(button_light_style)
        self.remove_video_button.setStyleSheet(button_light_style)

        self.resolution.setStyleSheet("background-color: #f5f5f5; color: #000")
        self.video_codec.setStyleSheet("background-color: #f5f5f5; color: #000")
        self.video_bitrate.setStyleSheet("background-color: #f5f5f5; color: #000")
        self.audio_codec.setStyleSheet("background-color: #f5f5f5; color: #000")
        self.audio_bitrate.setStyleSheet("background-color: #f5f5f5; color: #000")

        self.increase_video_bitrate_button.setStyleSheet("background-color: #d4d4d4")
        self.decrease_video_bitrate_button.setStyleSheet("background-color: #d4d4d4")
        self.increase_audio_bitrate_button.setStyleSheet("background-color: #d4d4d4")
        self.decrease_audio_bitrate_button.setStyleSheet("background-color: #d4d4d4")

        self.video_bitrate_field.setStyleSheet("background-color: #dddddd")
        self.audio_bitrate_field.setStyleSheet("background-color: #dddddd")

        self.resolution_info_button.setStyleSheet(button_light_style)
        self.video_bitrate_info_button.setStyleSheet(button_light_style)
        self.video_codec_info_button.setStyleSheet(button_light_style)
        self.audio_bitrate_info_button.setStyleSheet(button_light_style)
        self.audio_codec_info_button.setStyleSheet(button_light_style)

        self.video_name.setStyleSheet("background-color: #f5f5f5; color: #000")
        self.video_info.setStyleSheet("background-color: #f5f5f5; color: #000")
        self.audio_info.setStyleSheet("background-color: #f5f5f5; color: #000")

# Reduce the size by:
# 1 - CRF Adjustment - from 0 to 50
# 2 - Codec Change - ffmpeg -i input-mp4 -vcodec libx265 -crf 28 output.mpt4
# 3 - Resolution Adjustment
# 4 - Bitrate Control
