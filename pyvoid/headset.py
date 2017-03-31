import threading

import usb.core
import usb.util

class Headset():
    def __init__(self):
        self._dev = None
        self._thread = None

        self._battery_level = None
        self._power_button = None
        self._vol_up_button = None
        self._vol_down_button = None
        self._power_state = None
        self._ac_power = None

        self._find_device()

    @property
    def battery_level(self):
        return self._battery_level

    @property
    def power_button(self):
        return self._power_button

    @property
    def vol_up_button(self):
        return self._vol_up_button

    @property
    def vol_down_button(self):
        return self._vol_down_button

    @property
    def power_state(self):
        return self._power_state

    @property
    def ac_power(self):
        return self._ac_power

    def _find_device(self):
        self._dev = usb.core.find(idVendor=0x1b1c, idProduct=0x1b27)
        if self._dev is None:
            raise ValueError('Our device is not connected')

        if self._dev.is_kernel_driver_active(3):
            self._dev.detach_kernel_driver(3)

        return self._dev

    def start(self):
        self._thread = threading.Thread(target=self._loop)
        self._thread.start()

    def _loop(self):
        while True:
            self._read_message()

    def _read_message(self):
        val = None
        try:
            val = self._dev.read(0x83, 40)
        except usb.core.USBError:
            pass

        if val is not None:
            self._parse_message(val)

    def _parse_message(self, msg):
        if msg[0] == 0x64:
            # Power message

            if msg[1] == 0x80:
                # Power button down
                self._power_button = True
            else:
                # Power button up
                self._power_button = False

            # Battery level (0->100)
            self._battery_level = msg[2]

            if msg[3] == 0xb1:
                # Power on
                self._power_state = 'on'
            elif msg[3] == 0x31:
                # Powering down
                self._power_state = 'down'
            elif msg[3] == 0x33:
                # Power off
                self._power_state = 'off'

            if msg[4] == 0x05:
                # On AC power
                self._ac_power = True
            elif msg[4] == 0x01:
                # On battery power
                self._ac_power = False
            elif msg[4] == 0x00:
                self._ac_power = None

        elif msg[0] == 0x01:
            # Buttons
            pass

    def set_dolby(self, state):
        if state:
            return self._dev.ctrl_transfer(0x21, 0x09, 0x02CA, 0x0003, [0xCA, 0x02, 0x01, 0X00, 0x00])
        else:
            return self._dev.ctrl_transfer(0x21, 0x09, 0x02CA, 0x0003, [0xCA, 0x02, 0x00, 0X00, 0x00])

    def set_light(self, state):
        if state:
            self._dev.ctrl_transfer(0x21, 0x09, 0x02CB, 0x0003, [0xCB, 0x06, 0x2C, 0XAF, 0x26, 0xAF, 0x27, 0xAF, 0x2d, 0xAF, 0x28, 0xAF, 0x29, 0xAF, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00])
            self._dev.ctrl_transfer(0x21, 0x09, 0x02CB, 0x0003, [0xCB, 0x01, 0x01, 0X2A, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00])
        else:
            self._dev.ctrl_transfer(0x21, 0x09, 0x02CB, 0x0003, [0xCB, 0x06, 0x2C, 0X00, 0x26, 0x00, 0x27, 0x00, 0x2d, 0x00, 0x28, 0x00, 0x29, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00])
            self._dev.ctrl_transfer(0x21, 0x09, 0x02CB, 0x0003, [0xCB, 0x09, 0x1C, 0X00, 0x16, 0x00, 0x17, 0x00, 0x1d, 0x00, 0x18, 0x00, 0x19, 0x00, 0x1B, 0x00, 0x1A, 0x00, 0x1E, 0x00])
            self._dev.ctrl_transfer(0x21, 0x09, 0x02CB, 0x0003, [0xCB, 0x01, 0x01, 0X00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00])

