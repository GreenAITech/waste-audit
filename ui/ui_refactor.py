from datetime import datetime
import os
from PyQt5.QtWidgets import QWidget, QHBoxLayout, QFrame, QMessageBox
from PyQt5.QtCore import QTimer

from signals import WeightSignal
from serial_reader import SerialReader
from flask_server import FlaskServer
from api_vision_classes import APIVisionClient
from csv_settings import create_combined_csv_header, write_combined_data
from .camera_panel import CameraPanel
from .right_panel import RightPanel


class WeightUI(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Green AI Waste Audit")
        self._init_counter()
        self._init_components()
        self._setup_layout()
        self._init_serial()
        self._init_flask_server()
        self._init_api_client()
        self._init_csv_folder()
        self._connect_signals()
        self._setup_timer()
        self._init_label_timer()
        self._setup_vision_reconnect_timer()
        self.resize(1280, 720)

    def _setup_timer(self):
        self.update_timer = QTimer(self)
        self.update_timer.timeout.connect(self._refresh_ui)
        self.update_timer.start(1000)  

    def _setup_vision_reconnect_timer(self):
        self.vision_reconnect_timer = QTimer(self)
        self.vision_reconnect_timer.timeout.connect(self._try_reconnect_vision)
        self.vision_reconnect_timer.setSingleShot(False)
        self._try_reconnect_vision()

    def _try_reconnect_vision(self):
        try:
            status = self.api_client.get_status()
            if status and not self.vision_connected:
                self.vision_connected = True
                self.vision_reconnect_timer.stop()
                print("Vision connected successfully")
                self.right_panel.update_status("Vision connected")
                self._on_vision_status_received(status)
            elif not status and self.vision_connected:
                self.vision_connected = False
                print("Vision disconnected")
                self.right_panel.update_status("Vision disconnected")
                self._start_reconnect_timer()
        except Exception as e:
            if self.vision_connected:
                self.vision_connected = False
                print(f"Vision connection lost: {e}")
                self.right_panel.update_status("Vision connection lost")
            self._start_reconnect_timer()
            
    def _start_reconnect_timer(self):
        if not self.vision_reconnect_timer.isActive():
            self.vision_reconnect_timer.start(5000) 

    def _init_components(self):
        self.camera_panel = CameraPanel()
        self.right_panel = RightPanel()

    def _init_counter(self):
        self._total_count = 0
        self._last_data = None

    def _init_label_timer(self):
        self.label_timer = QTimer(self)
        self.label_timer.timeout.connect(self.camera_panel.set_alert_normal)
        self.label_timer.setSingleShot(True)

    def _setup_layout(self):
        right_container = QFrame()
        right_container.setLayout(self.right_panel.layout())
        right_container.setMinimumWidth(720)

        main_layout = QHBoxLayout(self)
        main_layout.addWidget(self.camera_panel, stretch=3)
        main_layout.addWidget(right_container, stretch=2)

    def _init_serial(self):
        self.signal = WeightSignal()
        self.reader = None

    def _init_flask_server(self):
        self.flask_server = FlaskServer(host='192.168.1.2', port=5000)
        self.flask_server.start()
        print("Flask server started on http://192.168.1.2:5000")

    def _init_api_client(self):
        self.vision_connected = False
        self.api_client = APIVisionClient(host='192.168.1.1', port=3000)
        print("API Client started to connect to http://192.168.1.1:3000")


    def _init_csv_folder(self):
        self.csv_folder = "waste_info"
        current_dir = os.path.dirname(os.path.abspath(__file__))
        parent_dir = os.path.dirname(current_dir)
        self.folder_path = os.path.join(parent_dir, self.csv_folder)
        if not os.path.exists(self.folder_path):
            os.makedirs(self.folder_path)

        self.csv_filepath = None
        self.round_num = 0
        self.category = "Unknown"
    def _init_csv_files(self):

        today_time = datetime.now().strftime("%Y%m%d_%H%M")
        self.csv_filename = f"round_{self.round_num}_{self.category}_{today_time}.csv"
        self.csv_filepath = os.path.join(self.folder_path, self.csv_filename)

        if not os.path.exists(self.csv_filepath):
            create_combined_csv_header(self.csv_filepath)

    def _connect_signals(self):
        self.signal.data_received.connect(self._on_data)
        self.signal.status.connect(self.right_panel.update_status)

        self.right_panel.serial_connect_requested.connect(self._connect_serial)
        self.right_panel.serial_disconnect_requested.connect(self._disconnect_serial)
        self.right_panel.command_requested.connect(self._enqueue_cmd)

        self.right_panel.recognition_panel.category_selected.connect(self._on_category_changed)
        self.right_panel.recognition_panel.start_clicked.connect(self._on_recognition_started)
        self.right_panel.recognition_panel.done_clicked.connect(self._on_recognition_done)
        self.right_panel.recognition_panel.pause_clicked.connect(self._on_recognition_paused)
        self.right_panel.recognition_panel.resume_clicked.connect(self._on_recognition_resumed)
        self.right_panel.recognition_panel.reset_clicked.connect(self._on_reset_clicked)


        self.camera_panel.camera_connected.connect(lambda: print("Camera connected"))
        self.camera_panel.camera_disconnected.connect(lambda: print("Camera disconnected"))

        self.flask_server.signals.item_received.connect(self._on_item_detected)
        self.flask_server.signals.new_image_received.connect(self._on_new_image)

        self.api_client.signals.status_received.connect(self._on_vision_status_received)
        self.api_client.signals.classes_updated.connect(self._on_vision_classes_updated)
        self.api_client.signals.detection_enabled.connect(self._on_vision_detection_changed)
        self.api_client.signals.error_occurred.connect(self._on_vision_error)

    def _on_vision_status_received(self, status: dict):
        print(f"Vision Status: {status}")
        accepted_classes = status.get('accepted_classes', [])
        if accepted_classes:
            display_classes = [cls.replace('_', ' ').capitalize() for cls in accepted_classes]
            self.right_panel.update_category_options(display_classes)
    

    def _on_vision_classes_updated(self, classes: list):
        print(f"Vision Accepted Classes Updated: {classes}")

    def _on_vision_detection_changed(self, enabled: bool):
        state = "enabled" if enabled else "disabled"
        print(f"Vision Detection {state}")

    def _on_vision_error(self, error_msg: str):
        print(f"Vision API Error: {error_msg}")

    def _on_recognition_started(self):
        self.category = self.right_panel.get_current_category()
        self.round_num = self.right_panel.get_current_recognition_round()

        print(f"Recognition started for Round {self.round_num}, Category: {self.category}")
        self._init_csv_files()
        api_classes = [self.category.lower().replace(' ', '_')]
        self.api_client.update_accepted_classes(api_classes)
        self.api_client.enable_detection()
        if self.reader:
            self._enqueue_cmd('T')

    def _on_recognition_paused(self):
        success = self.api_client.disable_detection()
        if success:
            print("Recognition paused")
        else:
            print("Failed to pause recognition")
        

    def _on_recognition_resumed(self):
        success = self.api_client.enable_detection()
        if success:
            print("Recognition resumed")
        else:
            print("Failed to resume recognition")


    def _on_recognition_done(self):
        round_number = self.right_panel.get_current_recognition_round() - 1
        
        current_weight = 0.0
        if self._last_data:
            current_weight = round(self._last_data.get('NetWeight', 0.0), 3)

        if hasattr(self.right_panel.recognition_panel, 'current_round_data'):
            self.right_panel.recognition_panel.update_current_round_data(
                amount=self._total_count,
                weight=current_weight
            )
            
        success = self.api_client.disable_detection()
        if success:
            print(f"Recognition completed for Round {round_number}")
        else:
            print("Failed to complete recognition")
        if self.csv_filepath:
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            write_combined_data(
                self.csv_filepath, 
                timestamp, 
                current_weight, 
                self._total_count, 
                "ROUND_COMPLETED",
                1.0
            )
        self._total_count = 0
        self.right_panel.update_count(self._total_count)
        if self.reader:
            self._enqueue_cmd('T')
            
    def _connect_serial(self, port: str):
        if self.reader:
            self._disconnect_serial()

        self.reader = SerialReader(port=port, baudrate=9600, signal=self.signal)
        self.reader.start()

        self.right_panel.set_serial_connected(True)
        self.right_panel.update_status(f"Connecting {port}...")

    def _disconnect_serial(self):
        if self.reader:
            self.reader.stop()
            self.reader.join(timeout=1.5)
            self.reader = None

        self.right_panel.set_serial_connected(False)
        self.right_panel.update_status("Disconnected")

    def _enqueue_cmd(self, cmd: str):
        if self.reader:
            self.reader.enqueue_command(cmd)
        else:
            QMessageBox.information(self, "Info", "Not connected.")

    def _on_data(self, data: dict):

        self._last_data = data
    
    def _refresh_ui(self):
        if self._last_data:
            self.right_panel.update_weight_data(self._last_data)

    def _on_category_changed(self, category: str):
        count = self._total_count
        self.right_panel.update_count(count)
        print(f"Category changed to: {category}, count: {count}")

    def _on_reset_clicked(self):
        self._total_count = 0
        if self.reader:
            self._enqueue_cmd('T')

    def _on_item_detected(self, data: dict):
        class_name = data.get('class_name', 'Unknown')
        confidence = data.get('confidence', 0.0)
        timestamp = data.get('timestamp_str', datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        print(f"Item detected: {class_name} (confidence: {confidence:.2f})")

        category = class_name.replace('_', ' ').capitalize()
        current_category = self.right_panel.get_current_category()
        if category == current_category and self.right_panel.recognition_panel.is_recognition_running():
            self.camera_panel.set_alert_normal()
            self.label_timer.stop()

            self._total_count += 1

            self.right_panel.update_count(self._total_count)

            if self.csv_filepath:
                current_weight = 0.0
                if self._last_data:
                    current_weight = round(self._last_data.get('NetWeight', 0.0), 3)
                
                write_combined_data(
                    self.csv_filepath, 
                    timestamp, 
                    current_weight, 
                    self._total_count, 
                    class_name, 
                    confidence
                )

            print(f"Current category: {current_category}")
            print(f"Total: {self._total_count}")

        elif category != current_category and self.right_panel.recognition_panel.is_recognition_running():
            self.camera_panel.set_alert_warning()
            self.label_timer.start(5000)

    def _on_new_image(self, image_path: str):
        self.camera_panel.display_image_from_path(image_path)

    def closeEvent(self, event):

        self._disconnect_serial()
        event.accept()