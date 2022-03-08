# Sending Acc and Gyor sensor Data from MetaTracker to RPI and then to MAX78000

This project aims to send and receive data from a wearable device, a host machine and the MAX78000EVKIT. 

Sensor reading is sent as follows:
Acceleration and gyro sensor readings from the [MetaTracker](https://mbientlab.com/metatracker/) will be sent to the [MetaHub](https://mbientlab.com/tutorials/MetaHub.html) via Bluetooth.
Once readings is received on the MetaHub, it is sent via UART to the MAX780000EVKIT.
Data is received by the MAX78000EVKIT through the UART and the values of data will be verfied by sending it back to the MetaHub. 

## Preparing the MAX78000EVKIT board

#### Configure MAX78000EVKIT for running project:

* Turn MAX78000EVKIT off by placing SW1 in the OFF position

* Connect MetaHub to MAX78000EVKIT CN1 using USB Micro-B cable

* Turn MAX78000EVKIT on by placing SW1 in the ON position


## Preparing the host machine
The MetaHub communicates with the MAX78000EVKIT using the USB-to-UART bridge.

The host application only runs in Linux and is written in Python and uses the following packages:

- pyserial -- USB-to-UART communications
- Pillow --  image data access
- metawear -- api library for connection to [MetaTracker](https://mbientlab.com/metatracker/) sensor. GitHub repo for the metawear python sdk: https://github.com/mbientlab/MetaWear-SDK-Python

The host application requires Python 3.7.x or 3.8.x.  Python 2.x and 3.9 are not supported.

* Clone project

* Navigate to project directory

* Create virtual environment: `python -m venv env`

* Activate virtual environment: 
    * Windows: `.\env\Scripts\activate`
    * Linux: `source env/bin/activate`

* Install python modules: `pip install -r requirements.txt`

* Run project: `python stream_acc_gyro_to_chip.py --device <device>` where `--device` specifies the serial port associated with the MAX78000EVKIT USB-to-UART bridge. Default value is `/dev/ttyUSB0` and is dependant on the USB port connected. 

## Preparing the MetaTracker

To check that the battery inserted in the MetaTracker has power, run `sudo python led.py`. If the led on the MetaTracker does not light up, replace the battery in the tracker with a new CR2450 coin cell.

MAC Address of MetaTracker: `C5:DE:74:B6:AC:5F`

## Preparing the MAX78000EVKIT

### Deploy the MAX78000 project in this directory by following the instructions:

For Linux: [Loading and Running Applications on the EV Kit](https://github.com/MaximIntegratedAI/MaximAI_Documentation/blob/master/MAX78000_Evaluation_Kit/README.md#loading-and-running-applications-on-the-ev-kit)

For Windows:

* The [MaximSDK](https://www.maximintegrated.com/en/design/software-description.html/swpart=SFW0010820A) provides a set of tools to easily deploy applciations onto the MAX78000EVKIT using the included Eclipse IDE.

* Refer to this video guide: [A Practical Introduction to the Toolchain and Demos for the MAX78000 AI Microcontroller](https://youtu.be/IBynIlWE8R0?t=1793) for deployment instructions.


## Running the example

With the MAX78000EVKIT connected, powered on and running the 'Add_2' example, run the host application.
