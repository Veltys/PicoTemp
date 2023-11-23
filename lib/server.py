#!/usr/bin/env python3
# -*- coding: utf-8 -*-


'''!
    server

    @file       : server.py
    @brief      : HTTP server module

    @author     : Veltys
    @date       : 2023-11-25
    @version    : 1.2.0
    @usage      : (imported when needed)
    @note       : ...
'''


from re import match                                                            # match function for regular expressions
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


    def accept(self, response, ip):
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
                request = str(cl.recv(1024).decode()).splitlines()[0]           # Decode, convert to str, split in lines and take the first one

                matched = match(r".* HTTP/(\d+\.?\d*)", request)

                if(matched):
                    http_version = matched.group(1)

                    if(match(r"GET /(?:\?.*)? HTTP/(?:\d+\.?\d*)", request)):
                        request = request[4:]                                   # Trim the "GET " initial part

                        matched = match(r"/\?.*sensor=(\d)", request)

                        if(matched) and 0 <= int(matched.group(1)) < len(response):
                            index = int(matched.group(1))

                            cl.send(f"HTTP/{ http_version } 200 OK\r\nContent-type: text/plain\r\n\r\n")
                            cl.send(str(response[index]) if response[index] is not None else '??')

                        else:
                            index = 0

                            cl.send(f"HTTP/{ http_version } 307 Temporary Redirect\r\nLocation: http://{ ip }/?sensor=0\r\n\r\n")
                            cl.send(str(response[index]) if response[index] is not None else '??')

                    else:
                        cl.send(f"HTTP/{ http_version } 404 Not Found\r\nContent-type: text/plain\r\n\r\n")
                        cl.send('404 Error: Not Found')

                else:
                    pass

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
