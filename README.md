# Multithread Serial Logger
The author of this project considers this project is still in development, and is open for further improvement. The aim is to log multiple devices at once. The logger doesn't need to know what kind of device it's handling, it only needs the port the device is connected to, the baudrate, and the logfile name.  
Why use multithreading? It's because the logger continously polls the data from the device, meaning it's always in waiting state.
You won't notice it if the baudrate is set high enough, but imagine working with low clock device like Arduino, which
only has 16MHz clock. The latency would be a problem if we log multiple Arduinos. The main GUI will be forced to wait for
the logger and cannot process incoming events from the user correctly.

nbsp;  
  
Multiprocessing will execute process concurrently, exactly at the same rate, while threads however, is executed one by one,
by switching between threads really fast, creating the 'illusion' of concurrent proccess. Why not use Python multiprocessing module?
Because it's too heavy on resource. I built this project, with the consideration of running it on my Raspberry Pi, which doesn't have
many cores for doing a good multiprocessing.
  
## What it does
1. Able to connect to multiple device. This is done using multithreading.
2. Able to log data concurrently from devices. 1 device = 1 thread.
  
## What it doesn't do
1. Display log information in the console. If what you need is just displaying log information on the console, there are already tons of tools such as `minicom` , `picocom` , or even the Arduino IDE Serial Monitor. The console is used to display information such as connection sources, errors, etc. You don't wanna make it clogged up with +5 device sending data at the same rate right?

## Installation
1. Clone this repository into your directory of choice
```bash
git clone https://github.com/yeyee2901/multithread-serial-logger.git /path/of/your/choice
```
2. Make sure you have python, pip, and pipenv in your system. For Debian based system:
```bash
sudo apt install python3 pipenv python3-pip
```
3. This project dependencies are managed using Pipfile, so install the requirements using pipenv. Main dependencies
are PyQt5 for GUI, and pyserial.
```bash
cd /path/to/your/repo/clone
pipenv install
```
4. To run the program, activate the virtual environment first using `pipenv` and run `main.py`
```bash
pipenv shell
python main.py
```

## Current State of the Project (as of July 2021)
- The app is able to log multiple device concurrently
- Disconnecting a device will not affect the logging thread of other device
- App can exit without error (clean exit) -> disconnect all device, then close the app.
Closing the app while there's still active device logging, will not kill the process.
- Do not forget to set the baudrate, as of now, mismatch of the baudrate can lead to undesired
behaviour. For safety reasons, I always set all of my device baudrates to be the same.

## Tested Platforms
1. Raspberry Pi 4 Model B
2. Pop-OS 21.04
&nbsp;  

## Screenshot
Simple test run using Arduino UNO R3 & NodeMCU v2. Both of the programs are identically the same. Just sending a 
simple hello string.
![image](https://user-images.githubusercontent.com/55247343/127276557-de432ac8-ca9d-41ce-8881-cacc9a2cee6b.png)
![image](https://user-images.githubusercontent.com/55247343/127276618-1e1ecb24-f85f-4a6e-a617-fa7842f529cd.png)
![image](https://user-images.githubusercontent.com/55247343/127276770-f6452c28-8c8a-4f1f-9ebd-0d920ebb0765.png)
