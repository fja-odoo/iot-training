# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

import logging
import time

from pn532pi import Pn532, pn532
from pn532pi import Pn532I2c

from odoo import _
from odoo.addons.hw_drivers.event_manager import event_manager
from odoo.addons.hw_drivers.driver import Driver

_logger = logging.getLogger(__name__)


class I2CDriver(Driver):
    connection_type = 'i2c'

    def __init__(self, identifier, device):
        super().__init__(identifier, device)
        self.device_type = 'scanner'
        self.device_connection = 'direct'
        self.device_name = 'PN532 NFC Reader/Writer'
        self.scanning = False

    @staticmethod
    def _get_nfc():
        PN532_I2C = Pn532I2c(1)
        nfc = Pn532(PN532_I2C)
        nfc.begin()
        return nfc

    @classmethod
    def supported(cls, device):
        if device.get('identifier', False) != '0x24':
            return False
        try:
            nfc = cls._get_nfc()
            versiondata = nfc.getFirmwareVersion()
            _logger.info('supported: %s' % (versiondata))
            return bool(versiondata)
        except Exception as e:
            _logger.warning('Error supported: %s' % (e))
            return False

    def _nfc_authenticate(self, nfc):
        _logger.info('nfc_authenticate')
        success, uid = nfc.readPassiveTargetID(pn532.PN532_MIFARE_ISO14443A_106KBPS, 100) # 100 tries then scan again
        if success:
            keya = bytearray([0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF])
            success = nfc.mifareclassic_AuthenticateBlock(uid, 4, 0, keya)
        return success

    def action(self, data):
        if self.scanning:
            _logger.warning('Already scanning')
            return
        self.scanning = True
        action = data.get('action', False)
        elapsed = 0
        success = False
        try:
            nfc = self._get_nfc()
            nfc.SAMConfig()
            start = time.time()
            while elapsed < 10:
                success = self._nfc_authenticate(nfc)
                if success:
                    if action == 'nfc_write':
                        buffer = bytearray([0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00])
                        card_value = bytearray(data.get('card_value', ''), 'utf8')
                        card_value = card_value[:16] + buffer[len(card_value) - 16:]
                        _logger.info('card_value: %s' % (card_value.decode().rstrip('\x00')))
                        success = nfc.mifareclassic_WriteDataBlock(4, card_value)
                        if success:
                            self.data['value'] = 'success'
                    elif action == 'nfc_poll':
                        success, card_value = nfc.mifareclassic_ReadDataBlock(4)
                    if success:
                        self.data['value'] = card_value.decode().rstrip('\x00') # Javascript does not handle \x00
                        break
                elapsed = time.time() - start
        except Exception as e:
            _logger.info('Value action: %s' % (e))
            pass

        self.scanning = False
        if elapsed >= 10:
            _logger.warning('timeout')
        elif not success:
            _logger.warning('error')
        else:
            _logger.info('Value action: %s' % (self.data['value']))
            event_manager.device_changed(self)
