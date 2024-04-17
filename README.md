# Nomad

Nomad is a simple python script to update windows' timezone from a GPS antenna connected to the computer.

The timezone is calculated by geolocating the coordinates from the NMEA string generated from the GPS antenna.

## Dependencies
To run this script you need python 3.11+ and this `pip` packages:
- `pytz`
- `timezonefinder`

To install them you just need to run:
```powershell
pip install -r requirements.txt
```

> [!TIP]
> It's suggested to use a venv for developing purposes, so you should first of all install `venv` and then create a virtual environment:
> ```powershell
> python3 -m pip install venv
> python3 -m venv .venv
> ```
> If you have multiple versions of python installed, be sure to use the correct version.

## Usage
```powershell
usage: change_time.py [-h] (--nmea NMEA | --coordinates LATITUDE LONGITUDE)

Change system time to the one received from GPS

options:
  -h, --help            show this help message and exit
  --nmea NMEA           NMEA position string
  --coordinates LATITUDE LONGITUDE
                        Latitude and longitude coordinates in decimal format
```
