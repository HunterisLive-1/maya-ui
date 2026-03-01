from PySide6.QtCore import QThread, Signal
import numpy as np
import pyaudiowpatch as pyaudio
import time

class AudioWorker(QThread):
    amplitude_signal = Signal(float)

    def run(self):
        p = pyaudio.PyAudio()
        stream = None
        
        try:
            while not self.isInterruptionRequested():
                try:
                    # Get default WASAPI info
                    wasapi_info = p.get_host_api_info_by_type(pyaudio.paWASAPI)
                    default_speakers = p.get_device_info_by_index(wasapi_info["defaultOutputDevice"])
                    
                    # Find loopback device
                    loopback_device = None
                    if not default_speakers["isLoopbackDevice"]:
                        for loopback in p.get_loopback_device_info_generator():
                            if default_speakers["name"] in loopback["name"]:
                                loopback_device = loopback
                                break
                        else:
                            loopback_device = p.get_default_wasapi_loopback()
                    else:
                        loopback_device = default_speakers
                        
                    if loopback_device is None:
                        print("No loopback device found")
                        time.sleep(1)
                        continue

                    def callback(in_data, frame_count, time_info, status):
                        try:
                            # Convert to float32
                            audio_data = np.frombuffer(in_data, dtype=np.float32)
                            # Calculate RMS volume
                            volume_norm = np.sqrt(np.mean(audio_data**2))
                            # Increase sensitivity
                            amplitude = min(volume_norm * 50, 1.0)
                            
                            self.amplitude_signal.emit(float(amplitude))
                        except Exception as e:
                            print(f"Audio processing error: {e}")
                        
                        return (in_data, pyaudio.paContinue)

                    stream = p.open(
                        format=pyaudio.paFloat32,
                        channels=loopback_device["maxInputChannels"],
                        rate=int(loopback_device["defaultSampleRate"]),
                        frames_per_buffer=1024,
                        input=True,
                        input_device_index=loopback_device["index"],
                        stream_callback=callback
                    )
                    
                    print(f"Successfully started audio capture on: {loopback_device['name']}")
                    
                    # Watchdog loop
                    start_time = time.time()
                    while not self.isInterruptionRequested() and stream.is_active():
                        time.sleep(0.1)
                        
                        # Every 5 seconds, check if default device changed
                        if time.time() - start_time > 5:
                            current_default = p.get_device_info_by_index(
                                p.get_host_api_info_by_type(pyaudio.paWASAPI)["defaultOutputDevice"]
                            )
                            if default_speakers["name"] != current_default["name"]:
                                print("Default output device changed, restarting capture...")
                                break
                            start_time = time.time()
                            
                except Exception as e:
                    print(f"Audio device error: {e}")
                    time.sleep(2)
                finally:
                    if stream is not None:
                        stream.stop_stream()
                        stream.close()
                        stream = None
                        
        except Exception as e:
            print(f"Audio worker error: {e}")
        finally:
            p.terminate()
