import time
import random

class SmartMonitoringSystem:
    def __init__(self):
        print("Smart Monitoring System initialized (simulated mode).")

    def get_monitoring_status(self):
        """Simulates getting monitoring data."""
        fall_detected = random.choice([True, False, False, False, False]) # Simulate occasional fall
        activity_pattern = random.choice(["Low Activity", "Normal Activity", "High Activity"])
        
        status = {
            "fall_detected": fall_detected,
            "activity_pattern": activity_pattern,
            "timestamp": time.time()
        }
        return status

if __name__ == "__main__":
    monitor = SmartMonitoringSystem()
    while True:
        status = monitor.get_monitoring_status()
        print(f"Simulated Monitoring Status: {status}")
        time.sleep(5) # Simulate processing every 5 seconds

