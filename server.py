import socket
import sys
import os
import optparse
import time
import hashlib
import re

def checksum_verification_using_md5(data_recieved, md5_of_data):
    new_md5 = hashlib.md5(data_recieved.encode()).hexdigest()
    if not new_md5 == md5_of_data:
        return False
    else:
        return True

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
    overall_data = ""
    while True:
        count = count +1
        data = conn.recv(1024)
        if not "md5-ends" in data.decode() :
            message = client[0] + ': ' + data.decode() + '\n'
            overall_data = overall_data + data.decode()
        else:
            overall_data = overall_data + data.decode()

            """Regular Expression to extract the md5 data sent alongside payload"""
            data = re.match('(.+)md5-begins:(.+):md5-ends',data.decode())
            md5_string = data.group(2)

            """actual chunk of data extraction"""
            sub_string = 'md5-begins:{}:md5-ends'.format(md5_string)
            actual_data = overall_data.replace(sub_string,'')


            """"Integrity check for each chunk"""
            is_integrity_verified = checksum_verification_using_md5(actual_data,md5_string)
            if is_integrity_verified:
                print("A complete and untampered chunk is recieved")
                """reset overall data for next chunk"""
                overall_data =""
            else:
                print("Data tampered")
                """reset overall data for next chunk"""
                overall_data = ""
                
            time_now = str(time.time())
            conn.sendall(time_now.encode())


def main():

    # option to set port when launching the server
    parser = optparse.OptionParser("Usage: python3 server.py -p <server port>")
    parser.add_option('-p', dest='port', type='int', help="specify target port")
    (options, args) = parser.parse_args()
    port = options.port

    if port == None:
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
