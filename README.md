# MAX78000 Add 2 Example

This project aims to explore the UART connection between a host machine and MAX78000EVKIT. A range of values will be sent from the host machine to the MAX78000EVKIT. Once data is received by the MAX78000EVKIT through the UART, the values of data will be augmented by adding 2 to it and then sent back to the host machine.

## Preparing the MAX78000EVKIT board

#### Configure MAX78000EVKIT for running Add-2 demo:

* Turn MAX78000EVKIT off by placing SW1 in the OFF position

* Connect host to MAX78000EVKIT CN1 using USB Micro-B cable

* Turn MAX78000EVKIT on by placing SW1 in the ON position


## Preparing the host machine
The host application communicates with the MAX78000EVKIT using the USB-to-UART bridge, by sending a range of integers from the host machine to the MAX78000EVKIT.

The host application is written in Python and uses the following packages:

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

* Run project: `python host_main.py --device <device>` where `--device` specifies the serial port associated with the MAX78000EVKIT USB-to-UART bridge

## Preparing the MAX78000EVKIT

### Deploy the MAX78000 project in this directory by following the instructions:

For Linux: [Loading and Running Applications on the EV Kit](https://github.com/MaximIntegratedAI/MaximAI_Documentation/blob/master/MAX78000_Evaluation_Kit/README.md#loading-and-running-applications-on-the-ev-kit)

For Windows:

* The [MaximSDK](https://www.maximintegrated.com/en/design/software-description.html/swpart=SFW0010820A) provides a set of tools to easily deploy applciations onto the MAX78000EVKIT using the included Eclipse IDE.

* Refer to this video guide: [A Practical Introduction to the Toolchain and Demos for the MAX78000 AI Microcontroller](https://youtu.be/IBynIlWE8R0?t=1793) for deployment instructions.


## Running the example

With the MAX78000EVKIT connected, powered on and running the 'Add_2' example, run the host application.

The expected output is shown in the Add_2_Demo.mp4 video
