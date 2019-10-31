#!/usr/bin/env python3

import sys
import getopt
import socket
import os

from pyvoid.headset import Headset

def exit_help(ret_code = 2):
    print('Usage:  pyvoidd [OPTION] [CMD]')
    print('A simple set of client/daemon scripts to control a Corsair VOID headset.')
    print('\nOptions:')
    print('%-28s specify socket path' % '  -s, --socket')
    print('%-28s print additional information' % '  -v, --verbose')
    print('%-28s display this help and exit' % '  -h, --help')
    print('\nCommands:')
    print('%-28s return the percentage of battery' % '  get_battery_level')
    print('%-28s activate Dolby Surround 7.1' % '  set_dolby_on')
    print('%-28s deactivate Dolby Surround 7.1' % '  set_dolby_off')
    print('%-28s activate the RGB lights' % '  set_light_on')
    print('%-28s deactivate the RGB lights' % '  set_light_off')
    sys.exit(ret_code)

def main():
    argv = sys.argv[1:]
    try:
        opts, args = getopt.getopt(argv,"hvs:",["verbose","socket="])
    except getopt.GetoptError:
        exit_help(2)

    verbose = False
    socket_path = "/tmp/pyvoidd.sock"

    for opt, arg in opts:
        if opt == '-h':
            exit_help(0)

        elif opt in ("-v", "--verbose"):
            verbose = True

        elif opt in ("-s", "--socket"):
            socket_path = arg

    # Find device and start polling
    hs = Headset()
    hs.start()

    if os.path.exists(socket_path):
        os.remove(socket_path)

    server = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
    server.bind(socket_path)
    os.chmod(socket_path, 0o777)
    server.listen(1)

    while True:
        connection, client_address = server.accept()
        while True:
            data, ancdata, msg_flags, address = connection.recvmsg(1024)
            if not data:
                break
            else:
                if b'shutdown_daemon' == data:
                    break

                elif b'get_battery_level' == data:
                    ret = str(hs.battery_level)
                    connection.sendmsg([ret.encode('utf-8')])

                elif b'set_dolby_on' == data:
                    hs.set_dolby(True)
                    connection.sendmsg(["ok".encode('utf-8')])
                elif b'set_dolby_off' == data:
                    hs.set_dolby(False)
                    connection.sendmsg(["ok".encode('utf-8')])

                elif b'set_light_on' == data:
                    hs.set_light(True)
                    connection.sendmsg(["ok".encode('utf-8')])
                elif b'set_light_off' == data:
                    hs.set_light(False)
                    connection.sendmsg(["ok".encode('utf-8')])

    #print('AC', hs.ac_power, '- Battery', hs.battery_level, '%')

if __name__ == "__main__":
    main()
