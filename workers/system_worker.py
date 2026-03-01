from PySide6.QtCore import QThread, Signal
import psutil
import time
import platform


class SystemWorker(QThread):
    system_signal = Signal(dict)

    def __init__(self):
        super().__init__()

    def get_cpu_temperature(self):
        """Get the highest available temperature from GPU or CPU sensors."""
        try:
            # 1. Try pynvml (Best for NVIDIA GPUs on Windows)
            try:
                import pynvml
                pynvml.nvmlInit()
                device_count = pynvml.nvmlDeviceGetCount()
                if device_count > 0:
                    handle = pynvml.nvmlDeviceGetHandleByIndex(0)
                    temp = pynvml.nvmlDeviceGetTemperature(handle, pynvml.NVML_TEMPERATURE_GPU)
                    if temp > 0:
                        pynvml.nvmlShutdown()
                        return temp
                pynvml.nvmlShutdown()
            except:
                pass

            # 2. Try GPUtil as fallback
            try:
                import GPUtil
                gpus = GPUtil.getGPUs()
                for gpu in gpus:
                    if gpu.temperature and gpu.temperature > 0:
                        return gpu.temperature
            except:
                pass
            
            # 3. Fallback for Windows using WMI (CPU Temp)
            if platform.system() == "Windows":
                try:
                    import wmi
                    c = wmi.WMI()
                    temps = []
                    # Try different temperature sensors
                    for sensor_class in [c.Win32_TemperatureProbe, c.MSAcpi_ThermalZoneTemperature]:
                        try:
                            for temperature in sensor_class():
                                if hasattr(temperature, 'CurrentReading') and temperature.CurrentReading:
                                    temp = temperature.CurrentReading
                                    if temp > 1000:  # tenths of Kelvin
                                        temp = (temp / 10) - 273.15
                                    if 0 < temp < 150:
                                        temps.append(temp)
                        except:
                            continue
                    if temps:
                        return sum(temps) / len(temps)
                except:
                    pass
        except Exception as e:
            print(f"Temperature detection error: {e}")
        return 0

    def get_gpu_usage(self):
        """Get GPU usage percentage, prioritizing NVIDIA via pynvml."""
        try:
            # 1. Try pynvml first (NVIDIA specifically)
            try:
                import pynvml
                pynvml.nvmlInit()
                device_count = pynvml.nvmlDeviceGetCount()
                if device_count > 0:
                    handle = pynvml.nvmlDeviceGetHandleByIndex(0)
                    util = pynvml.nvmlDeviceGetUtilizationRates(handle)
                    pynvml.nvmlShutdown()
                    return float(util.gpu)
                pynvml.nvmlShutdown()
            except:
                pass

            # 2. Try GPUtil as fallback
            try:
                import GPUtil
                gpus = GPUtil.getGPUs()
                if gpus:
                    # Prioritize NVIDIA if found
                    nvidia_gpus = [g for g in gpus if any(x in g.name.lower() for x in ['nvidia', 'geforce', 'rtx'])]
                    if nvidia_gpus:
                        gpu = max(nvidia_gpus, key=lambda g: g.memoryTotal)
                        return gpu.load * 100
                    return gpus[0].load * 100
            except:
                pass
        except Exception as e:
            print(f"GPU detection error: {e}")
        return 0

    def get_disk_usage(self):
        try:
            # Get usage for the primary disk (where Windows is installed)
            if platform.system() == "Windows":
                import os
                windows_path = os.environ.get("SystemDrive", "C:")
                usage = psutil.disk_usage(windows_path)
                return (usage.used / usage.total) * 100
            else:
                # For other OS, get root disk usage
                usage = psutil.disk_usage('/')
                return (usage.used / usage.total) * 100
        except:
            return 0

    def run(self):
        while not self.isInterruptionRequested():
            try:
                # Get all system metrics
                data = {
                    "cpu": psutil.cpu_percent(interval=0.5),
                    "ram": psutil.virtual_memory().percent,
                    "temp": self.get_cpu_temperature(),
                    "gpu": self.get_gpu_usage(),
                    "disk": self.get_disk_usage(),
                }
                
                self.system_signal.emit(data)
                
            except Exception as e:
                print(f"System monitoring error: {e}")
            
            # Check for interruption before sleeping
            if self.isInterruptionRequested():
                break
            time.sleep(1)
