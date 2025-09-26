#!/usr/bin/env python3
"""
Visitor Counter Feeder for Arduino LCD Display
Fetches visitor count from GCP Resume API and sends to Arduino via Serial
"""

import serial
import requests
import time
import sys
import subprocess
import os
from datetime import datetime

# Configuration
API_URL = "https://visitor-counter-uasgf6ueta-uc.a.run.app"
CHECK_INTERVAL = 10  # Seconds between API checks
SERIAL_BAUD = 9600
SERIAL_TIMEOUT = 2

# sound configuration
SOUND_ENABLED = True # set to false to display all sounds
SOUND_FOR_EVERY_VISITOR = True
SOUND_FOR_LOST_CONNECTION = True # play when connection is lost
SOUND_FOR_SUCESSFUL_CONNECTION = True # play sound when connection is restore or when connection happens in anyway

def play_sound(sound_type="default"):
    # play notification sounds using Mac system sounds
    if not SOUND_ENABLED:
        return
    
    sound_files = {
        "new_visitor": "/System/Library/Sounds/Glass.aiff",
        "milestone": "/System/Library/Sounds/Hero.aiff",
        "connection_success": "/System/Library/Sounds/Blow.aiff",
        "connection_lost": "/System/Library/Sounds/Sosumi.aiff",
        "startup": "/System/Library/Sounds/Purr.aiff",
        "default": "/System/Library/Sounds/Pop.aiff"
    }
    
    sound_file = sound_files.get(sound_type, sound_files["default"])
    
    try:
        # use subprocess to play sound in background
        subprocess.Popen(['afplay', sound_file], 
                        stdout=subprocess.DEVNULL, 
                        stderr=subprocess.DEVNULL)
    except Exception as e:
        # silently ignore sound errors to not interrupt the main function
        pass

def find_arduino_port():
    # auto-detect arduino port
    import serial.tools.list_ports
    
    arduino_ports = []
    for port in serial.tools.list_ports.comports():
        if 'Arduino' in port.description or 'USB' in port.description or 'usbmodem' in port.device:
            arduino_ports.append(port.device)
    
    if len(arduino_ports) == 0:
        return None
    elif len(arduino_ports) == 1:
        return arduino_ports[0]
    else:
        print("Multiple Arduino devices found:")
        for i, port in enumerate(arduino_ports):
            print(f"  {i+1}. {port}")
        choice = input("Select port number: ")
        try:
            return arduino_ports[int(choice)-1]
        except:
            return arduino_ports[0]

def connect_arduino(port=None):
    """Connect to Arduino via Serial"""
    if not port:
        port = find_arduino_port()
        if not port:
            # Try the default Arduino port
            port = "/dev/cu.usbmodem21401"
            print(f"⚠️  Using default port: {port}")
    
    try:
        print(f"📡 Connecting to Arduino on {port}...")
        ser = serial.Serial(port, SERIAL_BAUD, timeout=SERIAL_TIMEOUT)
        time.sleep(2)  # Wait for Arduino to reset
        
        # clear any initial data
        ser.flushInput()
        ser.flushOutput()
        
        # wait for READY signal from Arduino
        print("⏳ Waiting for Arduino to be ready...")
        start_time = time.time()
        while time.time() - start_time < 5:
            if ser.in_waiting:
                line = ser.readline().decode('utf-8').strip()
                if line == "READY":
                    print("✅ Arduino is ready!")
                    if SOUND_FOR_SUCESSFUL_CONNECTION:
                        play_sound("connection_success")
                    return ser
        
        print("⚠️  Arduino connected but didn't send READY signal")
        return ser
        
    except Exception as e:
        print(f"❌ Error connecting to Arduino: {e}")
        return None

def get_visitor_count():
    """Fetch current visitor count from API"""
    try:
        response = requests.get(API_URL, timeout=5)
        if response.status_code == 200:
            data = response.json()
            return data.get('count', 0), data.get('new_visitor', False)
        else:
            print(f"⚠️  API returned status code: {response.status_code}")
            return None, None
    except requests.exceptions.RequestException as e:
        print(f"❌ Error fetching visitor count: {e}")
        return None, None
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return None, None

def send_count_to_arduino(ser, count):
    # send visitor count to Arduino
    try:
        ser.write(f"{count}\n".encode())
        time.sleep(0.1)  # small delay for Arduino to process
        
        # check for confirmation
        if ser.in_waiting:
            response = ser.readline().decode('utf-8').strip()
            if response.startswith("OK:"):
                return True
        return True  # assume success even without confirmation
        
    except Exception as e:
        print(f"❌ Error sending to Arduino: {e}")
        return False

def main():
    """Main loop"""
    print("=" * 50)
    print("🖥️  Website Visitor Counter LCD Display")
    print("=" * 50)
    print(f"📊 API Endpoint: {API_URL}")
    print(f"⏱️  Update Interval: {CHECK_INTERVAL} seconds")
    print(f"🔊 Sound Notifications: {'ON' if SOUND_ENABLED else 'OFF'}")
    if SOUND_ENABLED:
        print(f"   • New visitors: {'ON' if SOUND_FOR_EVERY_VISITOR else 'OFF'}")
        print(f"   • Connection events: {'ON' if SOUND_FOR_SUCESSFUL_CONNECTION else 'OFF'}")
    print()
    
    # connect to arduino
    arduino = connect_arduino()
    if not arduino:
        print("❌ Failed to connect to Arduino. Exiting.")
        return 1
    
    last_count = None
    error_count = 0
    max_errors = 3
    
    print("\n📈 Starting visitor count monitoring...")
    print("-" * 50)
    
    try:
        while True:
            # get current visitor count
            count, is_new = get_visitor_count()

            if count is not None:
                error_count = 0  # reset error counter

                # ALWAYS send to arduino, even if count does not change
                if not send_count_to_arduino(arduino, count):
                    print("⚠️  Failed to send count to Arduino")
                    # try to reconnect
                    print("🔄 Attempting to reconnect to Arduino...")
                    try:
                        arduino.close()
                    except:
                        pass
                    time.sleep(2)
                    arduino = connect_arduino()
                    if arduino:
                        print("✅ Reconnected!")
                        send_count_to_arduino(arduino, count)

                # check if count changed for notifications/sounds
                if count != last_count:
                    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    
                    if last_count is not None:
                        change = count - last_count
                        if change > 0:
                            print(f"[{timestamp}] 🆕 New visitor! Count: {count} (+{change})")
                            
                            # play sound for new visitor
                            if SOUND_FOR_EVERY_VISITOR:
                                play_sound("new_visitor")
                            
                            # check for milestones and play special sound
                            if count % 1000 == 0:
                                print(f"[{timestamp}] 🎉 HUGE MILESTONE: {count:,} visitors! 🎆🎊🎆")
                                play_sound("milestone")
                            elif count % 100 == 0:
                                print(f"[{timestamp}] 🎉 MILESTONE: {count:,} visitors! 🎆")
                                play_sound("milestone")
                            elif count % 50 == 0:
                                print(f"[{timestamp}] 🎊 Nice! {count:,} visitors!")
                                play_sound("milestone")
                            elif count % 10 == 0:
                                print(f"[{timestamp}] 🎈 Milestone: {count:,} visitors!")
                                if SOUND_FOR_EVERY_VISITOR:
                                    play_sound("milestone")
                        else:
                            print(f"[{timestamp}] 📊 Count updated: {count}")
                    else:
                        print(f"[{timestamp}] 📊 Initial count: {count}")
                        play_sound("startup")
                    
                    last_count = count  # update last_count after notifications
                        
            else:
                error_count += 1
                if error_count >= max_errors:
                    print(f"❌ Multiple API errors. Check your connection.")
                  
            # simple connection check - just try to stay connected
            # removed PING check as it was causing false positives
            
            # wait before next check
            time.sleep(CHECK_INTERVAL)
            
    except KeyboardInterrupt:
        print("\n\n👋 Shutting down...")
        if arduino and arduino.is_open:
            arduino.write(b"CLEAR\n")
            time.sleep(0.5)
            arduino.close()
        print("✅ Cleanup complete. Goodbye!")
        return 0
        
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        if arduino and arduino.is_open:
            arduino.close()
        return 1

if __name__ == "__main__":
    sys.exit(main())
