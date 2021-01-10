odoo.define('nfc_iot.DebugWidget', function (require) {
    'use strict';

    const { useState } = owl.hooks;

    const DebugWidget = require('point_of_sale.DebugWidget');
    const Registries = require('point_of_sale.Registries');

    const NfcIotDebugWidget = DebugWidget =>
        class extends DebugWidget {
            /**
            * @override
            */
            constructor() {
                super(...arguments);
                this.state = useState({
                    nfcInput: '',
                });
            }
            /**
             * @param {Event} ev
             */
            nfcPoll(ev) {
                ev.preventDefault();
                this.scanners = this.env.pos.iot_device_proxies.scanners;
                for (var identifier in this.scanners) {
                    this.scanners[identifier].add_listener(function (barcode) {
                        console.log(barcode.value);
                    });
                    this.scanners[identifier].action({ action: 'nfc_poll' });
                }
            }
            /**
             * @param {Event} ev
             */
            nfcWrite(ev) {
                ev.preventDefault();
                this.scanners = this.env.pos.iot_device_proxies.scanners;
                for (var identifier in this.scanners) {
                    this.scanners[identifier].add_listener(function (barcode) {
                        console.log(barcode.value);
                    });
                    this.scanners[identifier].action({
                        action: 'nfc_write',
                        card_value: this.state.nfcInput,
                    });
                }
            }
        };

    Registries.Component.extend(DebugWidget, NfcIotDebugWidget);

    return DebugWidget;
});
