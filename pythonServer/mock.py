import serial
import time

arduino = serial.Serial('/dev/ttyACM0', 9600)
time.sleep(2)

def send_received():
    arduino.write(b"received\n")

def main():
    arduino.write(b"start\n")
    
    data = []
    while len(data) < 3:
        if arduino.in_waiting > 0:
            received_data = arduino.readline().decode('utf-8').strip()
            
            if received_data and received_data not in ["start", "received", "finish", 0, ""]:
                print(f"Received: {received_data}")
                data.append(float(received_data))
                send_received()
            
            if received_data == "finish":
                print("All data received.")
                break

    print("Final data array:", data)
    arduino.close()

if __name__ == "__main__":
    main()
