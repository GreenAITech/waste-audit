import threading
import queue
import serial
from parser import parse_line
from signals import WeightSignal


# ---------- serial reader thread (owns the serial handle) ----------

class SerialReader(threading.Thread):
    def __init__(self, port, baudrate, signal: WeightSignal):
        super().__init__(daemon=True)
        self.port = port
        self.baud = baudrate
        self.signal = signal
        self.running = True
        self._cmd_q: "queue.Queue[str]" = queue.Queue()
        self._ser = None

    def enqueue_command(self, cmd: str):
        # Queue single-letter commands; reader thread will send them safely.
        try:
            self._cmd_q.put_nowait(cmd)
        except queue.Full:
            pass

    def stop(self):
        self.running = False
        # shorten timeout so the loop exits quickly
        try:
            if self._ser and self._ser.is_open:
                self._ser.timeout = 0.2
        except Exception:
            pass

    def run(self):
        try:
            with serial.Serial(self.port, self.baud, timeout=1) as ser:
                self._ser = ser
                self.signal.status.emit(f"Connected {self.port} @ {self.baud}")
                buffer = bytearray()

                while self.running:
                    # 1) send any queued commands (single letter only!)
                    try:
                        while True:
                            cmd = self._cmd_q.get_nowait()
                            if cmd in ('Z', 'T'):
                                try:
                                    ser.write(cmd.encode('ascii'))  # ← IMPORTANT: no CRLF
                                    self.signal.status.emit(f"Sent command: {cmd}")
                                except Exception as e:
                                    self.signal.status.emit(f"Write error: {e}")
                            else:
                                self.signal.status.emit(f"Ignored unknown cmd: {cmd!r}")
                    except queue.Empty:
                        pass

                    # 2) read incoming
                    b = ser.read(1)
                    if not b:
                        continue
                    buffer.extend(b)
                    if b == b'\n':
                        try:
                            line = buffer.decode('ascii', errors='ignore')
                        finally:
                            buffer.clear()
                        data = parse_line(line)
                        if data:
                            self.signal.data_received.emit(data)
        except serial.SerialException as e:
            self.signal.status.emit(f"Serial error: {e}")
        except Exception as e:
            # Any unexpected exception—report it instead of hard-crashing
            self.signal.status.emit(f"Fatal reader error: {e}")
        finally:
            self.signal.status.emit("Disconnected")
            self._ser = None
