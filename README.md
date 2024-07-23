## Raspberry Pico W Project: Controlling Devices with Instant Interrupt Cancel

### Overview
This project uses a Raspberry Pico W to control devices like relays, featuring an instant interrupt cancel mechanism such as an IR beam. It also includes experimental Bluetooth scanning to trigger actions when a device is within a certain range.

### Background
Why did I create this project? Living in rented accommodation without a cat flap made it difficult to let our cat in or out at will. While a cat flap would have been simpler, I decided to challenge myself with the Pico W to create a device that opens and closes a window for the cat.

Three months later, I have a prototype that the cat successfully uses.

### Features
This project, built using a Raspberry Pico W, performs the following tasks:

- **Microdot Webserver:** Uses HTTP calls to control functions.
- **Relay Control:** Manages two relays via GPIO pins.
- **Input Monitoring:** Monitors inputs while relays are actuated. For instance, an IR beam across the window triggers a safety feature to reverse functions if broken, preventing the cat from being crushed.
- **Bluetooth Scanning (Experimental):** Scans for our cat's tracker and activates relays if the signal strength indicates the cat is nearby for a set duration.
- **Asynchronous Operation:** Ensures immediate GPIO output cancellation, allowing the next task to run without waiting for the current function to complete, again to ensure the cat's safety.

### Setting Up the Project on Your Pico W
To set up this project, follow these steps:

1. **Get a Raspberry Pico W:** You will need one Raspberry Pico W.
2. **Install Micropython with Bluetooth Support:** Download it from [Micropython's website](https://micropython.org/download/RPI_PICO_W/). Follow online instructions to install it on your Pico W.

### Configuration
1. **WiFi Configuration:** In `wlan.py`, update the `networkSettings()` function with your WiFi network ID and password:
    ```python
    def networkSettings():
        return {
            'ssid' : '',
            'password' : ''
        }
    ```

2. **Bluetooth Configuration:** In `bleScan.py`, update the following settings:
    ```python
    TARGET_DEVICE_NAME = ''
    RSSI_THRESHOLD = -95
    RSSI_CLOSED_OUTSIDE_THRESHOLD = -95
    RSSI_CLOSED_INSIDE_THRESHOLD = -75
    RSSI_OPENED_THRESHOLD = -75
    DURATION = 10
    ```
   Enter your Bluetooth device's ID in `TARGET_DEVICE_NAME`. Adjust signal strength settings and the duration for activating the relays.

3. **Upload Project Files:** Copy the project files to the Pico W, maintaining the same directory structure as the repository.

### Internet Access
I don't recommend exposing this project directly to the internet due to the lack of security. Instead, I keep it accessible only on my internal network.

For internet control, I use an old Raspberry PI Zero running Apache, NOIP, and LetsEncrypt to create a secure HTTPS service with a free SSL certificate. I will provide more details on this setup in the future.
