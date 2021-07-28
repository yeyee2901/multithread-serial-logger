# Multithread Serial Logger
This project is still in development, and is open for further improvement. The aim is to log multiple devices at once. The logger doesn't need to know what kind of device it's handling, it only needs the port the device is connected to, the baudrate, and the logfile name.  
  
## What it does
1. Able to connect to multiple device
2. Able to log data concurrently from devices. 1 device = 1 thread.
  
## What it doesn't do
1. Display log information in the console. If what you need is just displaying log information on the console, there are already tons of tools such as `minicom` , `picocom` , or even the Arduino IDE Serial Monitor. The console is used to display information such as connection sources, errors, etc. You don't wanna make it clogged up with +5 device sending data at the same rate right?

## Installation
1. Clone this repository into your directory of choice
```bash
git clone https://github.com/yeyee2901/multithread-serial-logger.git
```
2. Make sure you have python, pip, and pipenv. For Debian based system:
```bash
sudo apt install python3 pipenv python3-pip
```
3. This project is managed using Pipfile, so install the requirements using pipenv:
```bash
cd multithread-serial-logger/
pipenv install
```
4. To run the program, activate the virtual environment and run `main.py`
```bash
pipenv shell
python main.py
```

## Current State of the Project (as of July 2021)
- The app is able to log multiple device concurrently
- Disconnecting a device will not affect the logging thread of other device
- App can exit without error (clean exit) -> disconnect all device then close the app.
- Make sure to set the baudrate into 9600.

## Planned improvement
- Adjustable baudrate
