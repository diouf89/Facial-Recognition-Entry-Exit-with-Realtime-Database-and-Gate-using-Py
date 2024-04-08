import serial
import time

# Define the serial port (update 'COMx' with your port)
ser = serial.Serial('COM5', 9600, timeout=1)

def control_servo():
    try:
        # Send command to turn the servo
        ser.write(b'1')
        print("Servo turned 90 degrees")

        # Wait for 5 seconds
        time.sleep(5)

        # Send command to return the servo to the original position
        ser.write(b'1')
        print("Servo returned to the original position")

    except Exception as e:
        print(f"Error: {e}")

    finally:
        ser.close()  # Close the serial connection

if __name__ == "__main__":
    control_servo()
