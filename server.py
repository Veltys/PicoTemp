#!/usr/bin/env python3
# -*- coding: utf-8 -*-


'''!
    server

    @file		: server.py
    @brief		: HTTP server module

    @author		: Veltys
    @date		: 2023-10-29
    @version	: 1.0.0
    @usage		: (imported when needed)
    @note		: ...
'''


import socket																	# Socket functions


class server:
    _bound = False
    _socket = None

    def __init__(self):
        '''!
            Class constructor

            Initializes default values of the class
        '''

        self._socket = socket.socket()


    def accept(self, response):
        '''!
            Socket accepter
        '''

        if(self._bound):
            cl, addr = self._socket.accept()

            request = cl.recv(1024)

            cl.send('HTTP/1.0 200 OK\r\nContent-type: text/plain\r\n\r\n')
            cl.send(str(response))
            cl.close()


    def bind(self, ip = '0.0.0.0', port = 80):
        '''!
            Socket binder

            @param ip					: Socket IP to be bond
            @param port					: Socket port to be bond
        '''

        if(server.valid_ip(ip) and port >= 0 and port <= 65535):
            self._socket.bind(socket.getaddrinfo(ip, port)[0][-1])
            self._socket.listen(1)

            self._bound = True

        return self._bound


    @staticmethod
    def valid_ip(ip):
        try:
            host_bytes = ip.split('.')

            valid = [int(b) for b in host_bytes]
            valid = [b for b in valid if b >= 0 and b<=255]

            return len(host_bytes) == 4 and len(valid) == 4

        except:
            return False
