import socket
import sys
import os
import optparse
import time
def createServer(port):

    # create a TCP socket
    sck = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # bind the socket to the port
    server_address = ('localhost', port)
    print("starting up on {} port {}".format(*server_address))
    sck.bind(server_address)

    # put the socket into server mode
    sck.listen(5)

    return sck


def runServer(sck, conn, client, logs):

    # server loop
    count=1
    while True:
        print(count)
        count = count +1
        data = conn.recv(1024)
        if not "end_of_data" in data.decode() :
            message = client[0] + ': ' + data.decode() + '\n'
            print(message)
            logs.write(message)
        else:
            time_now = str(time.time())
            conn.sendall(time_now.encode())


def main():

    # option to set port when launching the server
    parser = optparse.OptionParser("Usage: pyhon3 server.py -p <server port>")
    parser.add_option('-p', dest='port', type='int', help="specify target port")
    (options, args) = parser.parse_args()
    port = options.port

    if port == None:
        print(parser.usage)
        exit(0)

    # create server logs
    logs = open('./logs.txt', 'a+')

    # create the socket
    sck = createServer(port)


    # wait for connection and start thread
    conn, client = sck.accept()
    runServer(sck, conn, client, logs)


if __name__ == '__main__':
    main()
