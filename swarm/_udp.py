"""
_udp.py - sunnyqa233

A simple udp server.
"""
from swarm import _log, _public
import threading
import select
import socket
import time


class Datagram:
    def __init__(self, datagram: tuple[bin, tuple[str, int]], decode: bool):
        """
        Simple datagram object.
        """
        self.raw = datagram
        # Data
        self.content = datagram[0]
        self.text = "None"
        if decode:
            self.text = self.content.decode("utf-8", errors="ignore")
        # Address
        self.ip = datagram[1][0]
        self.port = datagram[1][1]
        # Additional Info
        self.timestamp = time.time()


class Server:
    def __init__(
            self,
            port: int = 8889,
            decode: bool = True,
            filtrate: bool = True,
            debug: bool = False
    ):
        """
        A simple udp server class.

        :param port: Port to listen.
        :param decode: Decode received message using UTF-8 encoding.
        :param filtrate: Drop package from localhost.
        :param debug: Enable detailed log.
        """
        # Setup log
        if debug:
            self.__log = _log.get_logger(f"UDP_{port}", level=10, unique=True)
        else:
            self.__log = _log.get_logger(f"UDP_{port}")
        # Server options
        self.__port = port
        self.__decode = decode
        self.__filtrate = filtrate
        # Server info
        self.__ip = socket.gethostbyname(socket.gethostname())
        # Server indicator
        self.new = {}
        # Data storage
        self.data = {}
        # Setup socket
        self.__sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # IPV4, UDP
        self.__sock.setblocking(False)  # Timeout = 0
        self.__sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, True)  # Allow broadcast
        self.__sock.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, 4194304)  # 4MB Receive Buffer(Unit: B)
        self.__sock.bind(
            ("0.0.0.0", port)
        )
        self.__log.info(f"Socket initiated.")
        # Setup recv thread
        self.__recv_thread = threading.Thread(target=self.__recv, daemon=True)
        self.__recv_thread.start()
        self.__log.info(f"Receiving thread initiated.")
        # Done
        self.__log.warning(f"Server initiated. [{port}, {decode}, {filtrate}, {debug}]")

    def __recv(self):
        """
        Internal thread to read datagram from socket.
        """
        while True:
            if select.select([self.__sock], [], []):
                try:
                    datagram = self.__sock.recvfrom(4096)
                except (socket.herror, socket.gaierror):
                    self.__log.exception(
                        "Socket address error."
                    )
                except socket.timeout:
                    self.__log.exception(
                        "Socket timeout. Probably datagram didn't arrive."
                    )
                except OSError:
                    self.__log.exception(
                        "OSError. Probably due to ICMP response."
                    )
                else:
                    self.__log.info(f"Received Datagram. '{datagram}'")
                    # Filter
                    if not self.__filtrate:
                        ip = datagram[1][0]
                        self.new[ip] = True
                        # Initiate storage for ip if necessary
                        if ip not in self.data.keys():
                            self.data[ip] = []
                        # Save datagram
                        self.data[ip].append(
                            Datagram(datagram, self.__decode)
                        )
                    else:
                        if datagram[1][0] == self.__ip:
                            self.__log.warning(f"Dropped Datagram. Reason:'From Local' Raw:'{datagram}'")
                        elif len(datagram[0]) == 0:
                            self.__log.warning(f"Dropped Datagram. Reason:'Blank Datagram' Raw:'{datagram}'")
                        else:
                            ip = datagram[1][0]
                            self.new[ip] = True
                            # Initiate storage for ip if necessary
                            if ip not in self.data.keys():
                                self.data[ip] = []
                            # Save datagram
                            self.data[ip].append(
                                Datagram(datagram, self.__decode)
                            )

    def read(self, ip: str) -> Datagram:
        """
        Read the datagram that sent from specific ip, will block until datagram arrive.
        """
        while True:
            try:
                if len(self.data[ip]) == 1:  # Reset indicator
                    self.new[ip] = False
                return self.data[ip].pop()
            except (KeyError, IndexError):
                _public.sleep(0.2)

    def send(self, text: str, ip: str, port: int, internal: bool = False) -> None:
        try:
            self.__sock.sendto(
                text.encode('utf-8', errors="ignore"),
                (ip, port)
            )
        except (socket.herror, socket.gaierror, OSError):
            self.__log.exception(
                f"Error occurs when trying to send datagram. [{text}, {ip}, {port}, {internal}]"
            )
            print(_public.colourful_text("r", f"UDP_{self.__port} - Error occurs when trying to send datagram."))
        else:
            self.__log.info(f"Datagram sent. [{text}, {ip}, {port}, {internal}]")

    def broadcast(self, text: str, port: int) -> None:
        broadcast_ip = self.__ip.split('.')
        broadcast_ip[3] = "255"
        self.send(
            text,
            f"{broadcast_ip[0]}.{broadcast_ip[1]}.{broadcast_ip[2]}.{broadcast_ip[3]}",
            port,
            internal=True
        )
        self.__log.info(f"Datagram broadcast. [{text}, {port}]")

    def dumb_broadcast(self, text: str, port: int) -> None:
        broadcast_ip = self.__ip.split('.')
        ip_list = [f"{broadcast_ip[0]}.{broadcast_ip[1]}.{broadcast_ip[2]}.{x}" for x in range(1, 255)]
        for ip in ip_list:
            self.send(
                text,
                ip,
                port,
                internal=True
            )
        self.__log.info(f"Datagram broadcast. [{text}, {port}]")
