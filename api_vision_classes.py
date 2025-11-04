import requests
import json
from PyQt5.QtCore import QObject, pyqtSignal, QThread, QTimer
from datetime import datetime

class APIVisionSignals(QObject):
    status_received = pyqtSignal(dict)
    classes_updated = pyqtSignal(list)
    detection_enabled = pyqtSignal(bool)
    error_occurred = pyqtSignal(str)

class APIVisionClient(QThread):
    def __init__(self, host='192.168.1.1',port=3000):
        super().__init__()
        self.host = host
        self.port = port
        self.signals = APIVisionSignals()
        self.base_url = f'http://{host}:{port}'

        self.session = requests.Session()
        self.session.headers.update({'Content-Type': 'application/json'})

    def get_status(self):
        try:
            response = self.session.get(f'{self.base_url}/api/status')
            if response.status_code == 200:
                data = response.json()
                self.signals.status_received.emit(data)
                print(f"Status received: {data}")
                return data
            else:
                print(f"Failed to get status: {response.status_code}")
                self.signals.error_occurred.emit(f"Failed to get status: {response.status_code}")
        except Exception as e:
            print(f"Error getting status: {e}")
            self.signals.error_occurred.emit(f"Error getting status: {e}")
            return None
    
    def update_accepted_classes(self, classes):
        data = {'accepted_classes': classes}
        try:
            response = self.session.post(f'{self.base_url}/api/control', json=data)
            if response.status_code == 200:
                print(f"Accepted classes updated: {classes}")
                self.signals.classes_updated.emit(classes)
                return True
            else:
                print(f"Failed to update classes: {response.status_code}")
                self.signals.error_occurred.emit(f"Failed to update classes: {response.status_code}")
                return False
        except Exception as e:
            print(f"Error updating classes: {e}")
            self.signals.error_occurred.emit(f"Error updating classes: {e}")
            return False
        
    def enable_detection(self):
        data = {'action':'enable'}
        try:
            response = self.session.post(f'{self.base_url}/api/control', json=data)
            if response.status_code == 200:
                print("Detection enabled")
                self.signals.detection_enabled.emit(True)
                return True
            else:
                print(f"Failed to enable detection: {response.status_code}")
                self.signals.error_occurred.emit(f"Failed to enable detection: {response.status_code}")
                return False
        except Exception as e:
            print(f"Error enabling detection: {e}")
            self.signals.error_occurred.emit(f"Error enabling detection: {e}")
            return False
        
    def disable_detection(self):
        data = {'action':'disable'}
        try:
            response = self.session.post(f'{self.base_url}/api/control', json=data)
            if response.status_code == 200:
                print("Detection disabled")
                self.signals.detection_enabled.emit(False)
                return True
            else:
                print(f"Failed to disable detection: {response.status_code}")
                self.signals.error_occurred.emit(f"Failed to disable detection: {response.status_code}")
                return False
        except Exception as e:
            print(f"Error disabling detection: {e}")
            self.signals.error_occurred.emit(f"Error disabling detection: {e}")
            return False


    def close(self):
        self.session.close()