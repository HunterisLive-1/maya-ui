from PySide6.QtCore import QThread, Signal
import numpy as np
import sounddevice as sd


class MicWorker(QThread):
    mic_signal = Signal(float)

    def __init__(self):
        super().__init__()
        self.smooth_level = 0

    def run(self):
        try:
            device_index = sd.default.device[0]  # Default input

            device_info = sd.query_devices(device_index)
            samplerate = int(device_info['default_samplerate'])

            stream = None
            try:
                stream = sd.InputStream(
                    samplerate=samplerate,
                    device=device_index,
                    channels=1,
                    dtype='float32',
                    callback=self.callback,
                    blocksize=512
                )
                stream.start()
                
                while not self.isInterruptionRequested():
                    sd.sleep(30)
                    
            except Exception as e:
                print(f"Mic stream error: {e}")
            finally:
                if stream:
                    try:
                        stream.stop()
                        stream.close()
                    except:
                        pass

        except Exception as e:
            print("Mic capture error:", e)

    def callback(self, indata, frames, time, status):
        # RMS calculation
        volume_norm = np.sqrt(np.mean(indata**2))

        # 🔥 HIGH SENSITIVITY GAIN
        gain = 40  # increase this if needed
        amplitude = volume_norm * gain

        # 🔥 Noise Gate (ignore very low noise)
        if amplitude < 0.02:
            amplitude = 0

        # 🔥 Clamp
        amplitude = min(amplitude, 1.0)

        # 🔥 Smooth transition (avoid jitter)
        self.smooth_level += (amplitude - self.smooth_level) * 0.5

        self.mic_signal.emit(self.smooth_level)
