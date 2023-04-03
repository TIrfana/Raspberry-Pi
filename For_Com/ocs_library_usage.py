from osc_library import Lecroy

OSC_IP_ADDRESS = '10.97.8.220'
CHANNEL = 'C1'
import numpy
#import sys
#sys.path.append("C:/Users/Work/Documents/Irfana/osc/")
#import osc_library

lecroy_if = Lecroy(ip_address=OSC_IP_ADDRESS)
lecroy_if.prepare_for_trace_capture()
lecroy_if.wait_lecroy()

##### End of the setup ####

##### Collect one trace ####
_, interpreted_format = lecroy_if.get_native_signal_float(CHANNEL)
thisArray = numpy.asarray(interpreted_format[:])
print(thisArray)