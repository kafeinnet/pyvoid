#!/usr/bin/env python

import sys
import socket

def main():
    argv = sys.argv[1:]
    cmd = argv[0]

    if len(argv) > 0:
        cmd = argv[0]

        client = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        client.connect("/tmp/pyvoidd.sock")
        client.sendmsg([cmd.encode('utf-8')])

        client.settimeout(1)

        data, ancdata, msg_flags, address = client.recvmsg(1024)
        print(data.decode("utf-8"))
        client.close()

if __name__ == "__main__":
    main()
