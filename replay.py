#!/usr/bin/env python3
"""
Pymodbus Synchronous Client Examples
--------------------------------------------------------------------------

The following is an example of how to use the synchronous modbus client
implementation from pymodbus.

It should be noted that the client can also be used with
the guard construct that is available in python 2.5 and up::

    with ModbusClient('127.0.0.1') as client:
        result = client.read_coils(1,10)
        print result
"""
# --------------------------------------------------------------------------- #
# import the various client implementations
# --------------------------------------------------------------------------- #
from click import parser
from pymodbus.client.sync import ModbusTcpClient as ModbusClient
# from pymodbus.client.sync import ModbusUdpClient as ModbusClient
# from pymodbus.client.sync import ModbusSerialClient as ModbusClient
from argparse import ArgumentParser
import random

# --------------------------------------------------------------------------- #
# configure the client logging
# --------------------------------------------------------------------------- #
import logging
FORMAT = ('%(asctime)-15s %(threadName)-15s '
          '%(levelname)-8s %(module)-15s:%(lineno)-8s %(message)s')
logging.basicConfig(format=FORMAT)
log = logging.getLogger()
log.setLevel(logging.DEBUG)

UNIT = 0x1


def run_sync_client(destination, port, loops=100):
    # ------------------------------------------------------------------------#
    # choose the client you want
    # ------------------------------------------------------------------------#
    # make sure to start an implementation to hit against. For this
    # you can use an existing device, the reference implementation in the tools
    # directory, or start a pymodbus server.
    #
    # If you use the UDP or TCP clients, you can override the framer being used
    # to use a custom implementation (say RTU over TCP). By default they use
    # the socket framer::
    #
    #    client = ModbusClient('localhost', port=5020, framer=ModbusRtuFramer)
    #
    # It should be noted that you can supply an ipv4 or an ipv6 host address
    # for both the UDP and TCP clients.
    #
    # There are also other options that can be set on the client that controls
    # how transactions are performed. The current ones are:
    #
    # * retries - Specify how many retries to allow per transaction (default=3)
    # * retry_on_empty - Is an empty response a retry (default = False)
    # * source_address - Specifies the TCP source address to bind to
    # * strict - Applicable only for Modbus RTU clients.
    #            Adheres to modbus protocol for timing restrictions
    #            (default = True).
    #            Setting this to False would disable the inter char timeout
    #            restriction (t1.5) for Modbus RTU
    #
    #
    # Here is an example of using these options::
    #
    #    client = ModbusClient('localhost', retries=3, retry_on_empty=True)
    # ------------------------------------------------------------------------#
    client = ModbusClient(destination, port=port)
    # from pymodbus.transaction import ModbusRtuFramer
    # client = ModbusClient('localhost', port=5020, framer=ModbusRtuFramer)
    # client = ModbusClient(method='binary', port='/dev/ptyp0', timeout=1)
    # client = ModbusClient(method='ascii', port='/dev/ptyp0', timeout=1)
    # client = ModbusClient(method='rtu', port='/dev/ptyp0', timeout=1,
    #                       baudrate=9600)
    try:
        client.connect()

        # ------------------------------------------------------------------------#
        # specify slave to query
        # ------------------------------------------------------------------------#
        # The slave to query is specified in an optional parameter for each
        # individual request. This can be done by specifying the `unit` parameter
        # which defaults to `0x00`
        # ----------------------------------------------------------------------- #
        log.debug("Reading Coils")
        rr = client.read_coils(1, 1, unit=UNIT)
        log.debug(rr)


        # ----------------------------------------------------------------------- #
        # example requests
        # ----------------------------------------------------------------------- #
        # simply call the methods that you would like to use. An example session
        # is displayed below along with some assert checks. Note that some modbus
        # implementations differentiate holding/input discrete/coils and as such
        # you will not be able to write to these, therefore the starting values
        # are not known to these tests. Furthermore, some use the same memory
        # blocks for the two sets, so a change to one is a change to the other.
        # Keep both of these cases in mind when testing as the following will
        # _only_ pass with the supplied asynchronous modbus server (script supplied).
        # ----------------------------------------------------------------------- #
        for iteration in range(loops):
            iter_unit = UNIT + random.randint(0, 100)
            rq = client.write_coil(0, True, unit=iter_unit)
            rr = client.read_coils(0, 1, unit=iter_unit)
            log.debug(f'iteration {iteration + 1}: {iter_unit}')

    except:
        pass
    # ----------------------------------------------------------------------- #
    # close the client
    # ----------------------------------------------------------------------- #
    finally:
        client.close()


def get_args():
    parser = ArgumentParser()
    parser.add_argument('destination_server', default='localhost', help='Destination modbus server')
    parser.add_argument('-p', '--port', default=5020, type=int, help='Modbus server port')
    parser.add_argument('-i', '--iterations', default=500, type=int, help='Number of iterations')
    return parser.parse_args()


if __name__ == "__main__":
    args = get_args()
    run_sync_client(destination=args.destination_server, port=args.port, loops=args.iterations)
