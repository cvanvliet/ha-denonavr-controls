# Denon AVR Controls

A Home Assistant enhancement layer for Denon and Marantz receivers. It runs alongside Home Assistant's official Denon AVR integration and adds controls that are supported by the receiver library but are not exposed as normal Home Assistant entities.

## First release

- Dynamic EQ switch
- Dynamic Volume select
- Reference Level Offset select
- MultiEQ select
- Refresh Audyssey button
- Recover Audio button

The Recover Audio button performs a soft receiver power cycle, waits for the receiver to restart, and restores the previously selected input. It does not cut electrical power.

## Manual installation

Copy `custom_components/denonavr_controls` into Home Assistant's `/config/custom_components` directory. Restart Home Assistant, then go to **Settings → Devices & services → Add integration** and search for **Denon AVR Controls**.

Enter the same receiver address used by the official Denon integration. Do not remove the official integration.

## HACS installation

1. Open HACS in Home Assistant.
2. Open the three-dot menu and select **Custom repositories**.
3. Add `https://github.com/cvanvliet/ha-denonavr-controls` as an **Integration**.
4. Find **Denon AVR Controls** in HACS and install it.
5. Restart Home Assistant.
6. Go to **Settings → Devices & services → Add integration** and search for **Denon AVR Controls**.

## Safety

Receiver models vary. Controls may be unavailable when the current sound mode, input, or receiver model does not support them. Recover Audio turns the receiver off and back on; do not use it while firmware is being updated.
