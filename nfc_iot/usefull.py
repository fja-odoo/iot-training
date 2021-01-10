def action(self, data):
    try:
        nfc = self._get_nfc()
        nfc.SAMConfig()
        success, uid = nfc.readPassiveTargetID(pn532.PN532_MIFARE_ISO14443A_106KBPS, 100)
        if not success:
            _logger.warning("readPassive error")
            return
        keya = bytearray([0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF])
        for currentblock in range(64):
            success = nfc.mifareclassic_AuthenticateBlock(uid, currentblock, 0, keya)
            if not success:
                _logger.warning("Authentication error")
            _logger.info("Block {:d}".format(currentblock))
            success, data = nfc.mifareclassic_ReadDataBlock(currentblock)
            if success:
                _logger.info(binascii.hexlify(data))
            else:
                _logger.info(" unable to read this block")

    except Exception as e:
        _logger.info('Value action: %s' % (e))
        pass
