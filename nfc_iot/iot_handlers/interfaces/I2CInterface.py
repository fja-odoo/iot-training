# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

import logging

from smbus2 import SMBus

from odoo.addons.hw_drivers.interface import Interface

_logger = logging.getLogger(__name__)

class I2CInterface(Interface):
    connection_type = 'i2c'

    def get_devices(self):
        i2c_devices = {}

        with SMBus(1) as bus:
            for device in range(3, 128):
                try:
                    bus.read_byte_data(device, 0)
                    identifier = hex(device)
                    i2c_devices[identifier] = {
                        'identifier': identifier
                    }
                except Exception as e:
                    pass
        return i2c_devices
