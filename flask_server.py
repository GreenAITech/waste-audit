from flask import Flask, request, jsonify
from PyQt5.QtCore import QObject, pyqtSignal, QThread
import base64
import os
from datetime import datetime

class FlaskSignals(QObject):
    item_received = pyqtSignal(dict)
    new_image_received = pyqtSignal(str)

class FlaskServer(QThread):

    def __init__(self, host='127.0.0.1', port=5000):
        super().__init__()
        self.host = host
        self.port = port
        self.signals = FlaskSignals()
        self.app = None
        self._setup_flask()

        self.image_folder = "received_image"
        if not os.path.exists(self.image_folder):
            os.makedirs(self.image_folder)

    def _setup_flask(self):
        self.app = Flask(__name__)

        @self.app.route('/api/throw', methods=['POST'])
        def receive_item():
            data = request.get_json()
            if not data:
                return jsonify({"error": "Invalid JSON"}), 400

            timestamp_str = data.get('timestamp_str')
            class_name = data.get('class_name')
            location = data.get('location')
            confidence = data.get('confidence')
            image_b64 = data.get('image')

            self.signals.item_received.emit(data)
            print(
                f"Received throw detection: timestamp_str={timestamp_str}, class={class_name}, location={location}, confidence={confidence:.2f}")
            if image_b64:
                # Decode and save image (optional)
                image_data = base64.b64decode(image_b64)
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = f"{class_name}_{timestamp}.jpg"
                filepath = os.path.join(self.image_folder, filename)

                with open(filepath, "wb") as f:
                    f.write(image_data)

                path = os.path.abspath(filepath)
                self.signals.new_image_received.emit(path)

            return jsonify({"status": "received"}), 200

    def run(self):
        self.app.run(host=self.host, port=self.port, debug=False, use_reloader=False)
