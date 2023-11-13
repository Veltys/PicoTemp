#!/usr/bin/env python3
# -*- coding: utf-8 -*-


'''!
    server

    @file		: server.py
    @brief		: HTTP server module

    @author		: Veltys
    @date		: 2023-11-11
    @version	: 1.1.0
    @usage		: (imported when needed)
    @note		: ...
'''


import socket																	# Socket functions


SOCKET_TIMEOUT = 30


class server:
    _bound = False
    _socket = None

    def __init__(self):
        '''!
            Class constructor

            Initializes default values of the class
        '''

        self._socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        self._socket.settimeout(SOCKET_TIMEOUT)


    def accept(self, response):
        '''!
            Socket accepter
            
            @param response             : Plain text response
        '''

        res = None

        if(self._bound):
            try:
                cl, _ = self._socket.accept()

            except OSError:
                res = False

            else:
                _ = cl.recv(1024)

                cl.send("HTTP/1.0 200 OK\r\nContent-type: text/plain\r\n\r\n")
                cl.send(str(response))
                cl.close()

                res = True

        else:
            res = False

        return res


    def bind(self, ip = '0.0.0.0', port = 80):
        '''!
            Socket binder

            @param ip					: Socket IP to be bond
            @param port					: Socket port to be bond
        '''

        if(server.valid_ip(ip) and port >= 0 and port <= 65535):
            try:
                self._socket.bind(socket.getaddrinfo(ip, port)[0][-1])

            except OSError:
                self._bound = False

            else:
                self._socket.listen(1)

                self._bound = True

        return self._bound


    def close(self):
        '''!
            Socket closer
        '''

        self._socket.close()


    @staticmethod
    def valid_ip(ip):
        try:
            host_bytes = ip.split('.')

            valid = [int(b) for b in host_bytes]
            valid = [b for b in valid if b >= 0 and b<=255]

            return len(host_bytes) == 4 and len(valid) == 4

        except Exception:
            return False
