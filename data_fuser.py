# usage: python data_fuser.py [mac1] [mac2] ... [mac(n)]
from __future__ import print_function
from ctypes import c_void_p, cast, POINTER
from mbientlab.metawear import MetaWear, libmetawear, parse_value, cbindings
from mbientlab.metawear.cbindings import *
from time import sleep
from threading import Event
from sys import argv

states = []

class State:
    # init
    def __init__(self, device):
        self.device = device
        self.callback = cbindings.FnVoid_VoidP_DataP(self.data_handler)
        self.processor = None
    # download data callback fxn
    def data_handler(self, ctx, data):
        values = parse_value(data, n_elem = 2)
        print("acc: (%.4f,%.4f,%.4f), gyro; (%.4f,%.4f,%.4f)" % (values[0].x, values[0].y, values[0].z, values[1].x, values[1].y, values[1].z))
    # setup
    def setup(self):
        # ble settings
        libmetawear.mbl_mw_settings_set_connection_parameters(self.device.board, 7.5, 7.5, 0, 6000)
        sleep(1.5)
        # events
        e = Event()
        # processor callback fxn
        def processor_created(context, pointer):
            self.processor = pointer
            e.set()
        # processor fxn ptr
        fn_wrapper = cbindings.FnVoid_VoidP_VoidP(processor_created)

        # get acc signal
        libmetawear.mbl_mw_acc_set_odr(self.device.board, 25)
        libmetawear.mbl_mw_acc_set_range(self.device.board, 16.0)
        libmetawear.mbl_mw_acc_write_acceleration_config(self.device.board)
        acc = libmetawear.mbl_mw_acc_get_acceleration_data_signal(self.device.board)

        # get gyro signal
        libmetawear.mbl_mw_gyro_bmi160_set_range(self.device.board, GyroBoschRange._1000dps);
        libmetawear.mbl_mw_gyro_bmi160_set_odr(self.device.board, GyroBoschOdr._25Hz);
        libmetawear.mbl_mw_gyro_bmi160_write_config(self.device.board);
        gyro = libmetawear.mbl_mw_gyro_bmi160_get_rotation_data_signal(self.device.board)

        # create signals variable
        signals = (c_void_p * 1)()
        signals[0] = gyro

        # create acc + gyro signal fuser
        libmetawear.mbl_mw_dataprocessor_fuser_create(acc, signals, 1, None, fn_wrapper)

        # wait for fuser to be created
        e.wait()

        # subscribe to the fused signal
        # segmentation fault here:
        libmetawear.mbl_mw_datasignal_subscribe(self.processor, None, self.callback)

    # start
    def start(self):
        # start gyro
        libmetawear.mbl_mw_gyro_bmi160_enable_rotation_sampling(self.device.board)
        libmetawear.mbl_mw_gyro_bmi160_start(self.device.board)

        # start acc
        libmetawear.mbl_mw_acc_enable_acceleration_sampling(self.device.board)
        libmetawear.mbl_mw_acc_start(self.device.board)
        
# connect
for i in range(len(argv) - 1):
    d = MetaWear(argv[i + 1])
    d.connect()
    print("Connected to " + d.address)
    states.append(State(d))

# configure
for s in states:
    print("Configuring %s" % (s.device.address))
    s.setup()

# start
for s in states:
    s.start()

# wait 10 s
sleep(10.0)

# reset
print("Resetting devices")
events = []
for s in states:
    e = Event()
    events.append(e)

    s.device.on_disconnect = lambda s: e.set()
    libmetawear.mbl_mw_debug_reset(s.device.board)

for e in events:
    e.wait()