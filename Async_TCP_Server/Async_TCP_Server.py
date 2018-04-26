# ==========================================================
#   File: Async_TCP_Server.py
#   Author: Arkadiusz Wadowski
#   Email: wadowski.arkadiusz@gmail.com
#   Created: 20.03.2018
# ==========================================================

'''
 *  Copyright (c) 2018, Arkadiusz Wadowski
 *  All rights reserved.
 *
 *  Redistribution and use in source and binary forms, with or without
 *  modification, are permitted provided that the following conditions are met:
 *  1. Redistributions of source code must retain the above copyright
 *     notice, this list of conditions and the following disclaimer.
 *  2. Redistributions in binary form must reproduce the above copyright
 *     notice, this list of conditions and the following disclaimer in the
 *     documentation and/or other materials provided with the distribution.
 *  3. Neither the name of the copyright holder nor the
 *     names of its contributors may be used to endorse or promote products
 *     derived from this software without specific prior written permission.
 *
 *  THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
 *  AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
 *  IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
 *  ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE
 *  LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
 *  CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
 *  SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
 *  INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
 *  CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
 *  ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
 *  POSSIBILITY OF SUCH DAMAGE.
'''

import asyncore
import socket
import logging
import commands
from HTTP_Client.HTTP_Client import *

MAX_NUM_OF_CONNECTIONS = 10

class Async_TCP_Server( asyncore.dispatcher ):
    # a list of clients that are connected to our server
    clients = []
    http_server_ip = ""
    
    def __init__(self, my_ip_and_port, http_server_ip):
        #init parrent class
        asyncore.dispatcher.__init__(self)
        # create TCP socket
        self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
        self.set_reuse_addr()
        # bind server socket with given ip and port
        self.bind(my_ip_and_port)
        self.address = self.socket.getsockname()
        self.listen(5)
        self.http_server_ip = http_server_ip
        # run console logger
        self.logger = logging.getLogger('ServerClass')
        self.logger.debug('Socket is binded to %s', self.address)
        self.logger.debug('Server started to listen...')
    
    # callback called when an client is trying to connect
    def handle_accept(self):
        # accept incoming connection and get information about client
        client_socket, client_ip = self.accept()
        # check if client info is valid
        if (client_ip is not None) and (client_ip is not None):
            self.logger.debug('handle_accept() called for client: %s', client_ip)
            if len(self.clients) >= MAX_NUM_OF_CONNECTIONS:
                self.logger.debug('Cant add new client! No space available!')
            else:
                self.clients.append(Client_Instance(client_socket, client_ip, self.http_server_ip))

    def handle_close(self):
        self.logger.debug('server_handle_close() called')
        self.close()

class Client_Instance( asyncore.dispatcher ):
    http_client = None
    # constructor
    def __init__(self, sock, address, http_server_ip):
        asyncore.dispatcher.__init__(self, sock)
        # set up http client
        self.http_client = HTTP_Client(http_server_ip);
        # run console logger for every client instance
        self.logger = logging.getLogger('ClientInstance: ' + str(address))
        # default output data buffer
        self.data_to_write = []
    
    # method that checks if something is waiting to be sent
    def writable(self):
        return (len(self.data_to_write) > 0)
    
    # method that is called when some data is appeared in data output buffer
    def handle_write(self):
        data = self.data_to_write.pop()
        sent = self.send(data[:1024])
        if sent < len(data):
            remaining = data[sent:]
            self.data.to_write.append(remaining)
            self.logger.debug('handle_write() called! Data length: (%d)  Data: "%s"',
                              sent,
                              data[:sent].rstrip())
            
    # method that is called when some data arrived from client
    def handle_read(self):
        data = self.recv(1024)
        self.http_client.post(':5000/measurements', data)
        self.logger.debug('handle_read() called! Data length: (%d)  Data: "%s"', len(data), data.rstrip())
        # trigger write back action - here data from client will be parsed and post to http server
        #self.data_to_write.insert(0, data)

    # method handles close of object
    def handle_close(self):
        self.logger.debug('handle_close()')
        self.close()

def main():
    try:
        logging.basicConfig(level=logging.DEBUG, format='%(name)s:[%(levelname)s]: %(message)s')
        ip = commands.getstatusoutput('ifconfig wlan0 | grep "inet\ addr" | cut -d: -f2 | cut -d" " -f1')[1]
        port = 1234
        server = Async_TCP_Server((ip, port), '192.168.1.1')
        asyncore.loop()
    except KeyboardInterrupt:
        print ("see you!")

if __name__ == '__main__':
    main()
