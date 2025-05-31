
## Requirements

### Permissions  
The user running the script must be in the `gpio` group:

```bash
sudo adduser your_username gpio
```

### Libraries  
Install `requests` and the appropriate GPIO library:

```bash
pip3 install requests
```

Only **one** of the following GPIO libraries should be installed, depending on your Raspberry Pi model:

- **Raspberry Pi 2/3/4**:
  ```bash
  pip3 install RPi.GPIO
  ```

- **Raspberry Pi 5**:
  ```bash
  pip3 install rpi-lgpio
  ```

> **Note:** Installing both GPIO libraries may cause conflicts.

---

## Usage

1. **Set password**  
   Create a file named `password` and enter the Connect Box 3 settings password (the one used to log in at [192.168.1.1](http://192.168.1.1)).

2. **Test the script manually**  
   Run the script to verify functionality:

   ```bash
   python3 toggle_wifi.py
   ```

3. **Configure the button script**  
   Set the correct LED and button GPIO pin numbers in `main.py`.

---

## Running with systemd

To keep the script running and responsive to button presses:

1. **Edit `wifi-toggle.service`**  
   Replace the placeholders

2. **Copy and enable the service:**

   ```bash
   sudo cp wifi-toggle.service /etc/systemd/system/
   sudo systemctl daemon-reload
   sudo systemctl enable wifi-toggle.service
   sudo systemctl start wifi-toggle.service
   ```

To view logs in real time:

```bash
journalctl -u wifi-toggle.service -f
```
