# PyVOID

PyVOID is a simple client/daemon scripts to control a Corsair VOID headset.

## Installation

```
python3 setup.py install
```

## Usage

### Daemon

```
pyvoidd [-h] [-v] [-s path]
```

### Client

```
pyvoidclient cmd
```

Where cmd is one of :
 *  get_battery_level : Return the percentage of battery
 *  set_dolby_on : Activate 7.1 Dolby
 *  set_dolby_off : Deactivate 7.1 Dolby
 *  set_light_on : Activate the RGB lights
 *  set_light_off : Deactivate the RGB lights
