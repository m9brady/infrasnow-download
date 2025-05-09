from datetime import datetime
from pathlib import Path
from time import sleep

import serial
from serial.tools.list_ports import comports

MAX_ATTEMPTS = 10  # tries
SLEEP_DURATION = 5  # seconds


def detect_port():
    # will appear when the device is turned on and TX to USB is active
    port_found = False
    attempts = 0
    while not port_found:
        ports = comports()
        # Ideal case, only 1 USB comm port in-use
        if len(ports) == 1:
            port, desc, hwid = ports[0]
            # test and see if it's the expected device
            if desc.startswith("USB Serial Device"):
                print(f"Detected device {desc!r} on port {port}")
                port_found = True
            else:
                print(
                    f"Detected device connected on COM port: {port}: {desc!r} ({hwid})"
                )
                choice = input(
                    "Does the displayed device appear to be the SLF InfraSnow device? y/N"
                )
                if choice.upper() in ["Y", "YES"]:
                    port_found = True
        # Less-ideal case, more than 1 USB comm port in-use
        elif len(ports) > 1:
            print("Detected multiple devices connected on COM ports")
            for idx, (device_port, device_desc, device_hwid) in enumerate(
                ports, start=1
            ):
                print(f"#{idx}  |  {device_port}: {device_desc!r} ({device_hwid})")
            try:
                choice = int(input("Select the device number to monitor: "))
                port, desc, _ = ports[choice - 1]
                port_found = True
            except ValueError:
                print("Invalid choice")
        if port_found:
            break
        # Even less-ideal case, no active comm ports detected. May indicate a problem with the host hardware
        print(f"No ports detected. Sleeping for {SLEEP_DURATION} seconds")
        attempts += 1
        if attempts == MAX_ATTEMPTS:
            print(f"Maximum attempts ({MAX_ATTEMPTS}) reached. Aborting...")
            sleep(SLEEP_DURATION)
            exit()
        sleep(SLEEP_DURATION)
    return port, desc


if __name__ == "__main__":
    # first, detect COM port to monitor
    port, desc = detect_port()
    # establish connection to device
    try:
        with serial.Serial(
            port=port,
            baudrate=9600,
            parity=serial.PARITY_NONE,
            stopbits=serial.STOPBITS_ONE,
            bytesize=serial.EIGHTBITS,
            timeout=0,
        ) as connection:
            print(f"Connection established with {port} device {desc!r}")
            buffer = connection.read_all()
            data_attempts = 1
            while len(buffer) == 0:
                print(f"No data stream detected. Sleeping for {SLEEP_DURATION} seconds")
                sleep(SLEEP_DURATION)
                buffer = connection.read_all()
                data_attempts += 1
                if data_attempts == MAX_ATTEMPTS:
                    print(f"Maximum attempts ({MAX_ATTEMPTS}) reached. Aborting...")
                    sleep(SLEEP_DURATION)
                    exit(1)
    except serial.SerialException as e:
        print(f"Serial connection failed: {e}")
        exit(1)
    # convert bytes to string
    buffer_as_str = buffer.decode("utf-8").replace("\r", "")
    print(buffer_as_str)
    # save to current working directory (i.e. where the binary/script was run from)
    txt_file = (
        Path.cwd() / f"InfraSnow_Data_{datetime.now().strftime('%Y%m%dT%H%M%S')}.txt"
    )
    save_to_txt = input("Would you like to save to text file? [y/N]: ")
    if save_to_txt.upper() in ["Y", "YES"]:
        with txt_file.open("w") as f:
            f.write(buffer_as_str)
        print(f"Saved to {txt_file}")
    print("Execution complete. This message will self-destruct in 10 seconds...")
    sleep(10)
