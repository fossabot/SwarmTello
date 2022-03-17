"""
test.py - sunnyqa233

A python to test all modules in package swarm.
"""
import socket

from swarm import _public, _log, _udp
import threading
import time

print("----------")
print("File: _public.py", end="\n\n")

print("Func: colourful_text()")
print(_public.colourful_text("r", "Red Text"))
print(_public.colourful_text("g", "Green Text"))
print(_public.colourful_text("b", "Blue Text"))
print(_public.colourful_text("y", "Yellow Text"))
print(_public.colourful_text("c", "Cyan Text"), end="\n\n")

print("Func: sleep()")
duration = 0.5
start = time.time()
_public.sleep(duration)
end = time.time()
print(f"Error is about {end - start - duration}s.", end="\n\n")

print("----------")
print("File: _log.py", end="\n\n")

print("Func: get_logger()")
print("Creating Logfile: logs/test.log")

log = _log.get_logger("test", level=10)
log.debug("This is a debug info.")
log.info("This is a normal info.")
log.warning("This is a warning info.")
log.error("This is an error info.")
log.critical("This is a critical info.")
try:
    raise OSError
except OSError:
    log.exception("This is a msg created by logging module capturing exception.")

print(
    """
    *****Expected Output
    2022-03-17 17:33:28,246 - DEBUG - <module> - This is a debug info.
    2022-03-17 17:33:28,247 - INFO - <module> - This is a normal info.
    2022-03-17 17:33:28,247 - WARNING - <module> - This is a warning info.
    2022-03-17 17:33:28,247 - ERROR - <module> - This is an error info.
    2022-03-17 17:33:28,247 - CRITICAL - <module> - This is a critical info.
    2022-03-17 17:33:28,247 - ERROR - <module> - This is a msg created by logging module capturing exception.
    Traceback (most recent call last):
    File "D:\\Projects\\SwarmTello\\test.py", line 39, in <module>
        raise OSError
    OSError
    *****
    """, end="\n\n"
)

print("----------")
print("File: _udp.py", end="\n\n")

sample_size = 10000
server_a = _udp.Server(8890, filtrate=False)
server_b = _udp.Server(8895, filtrate=False)
a2b_start = 0
b2a_start = 0
a2b_end = 0
b2a_end = 0


def a2b():
    global a2b_start
    global a2b_end
    a2b_start = time.time()
    for i in range(sample_size):
        server_a.send(f"{time.time()}", socket.gethostbyname(socket.gethostname()), 8895)
    a2b_end = time.time()


def b2a():
    global b2a_start
    global b2a_end
    b2a_start = time.time()
    for i in range(sample_size):
        server_b.send(f"{time.time()}", socket.gethostbyname(socket.gethostname()), 8890)
    b2a_end = time.time()


thread_a2b = threading.Thread(target=a2b, daemon=True)
thread_b2a = threading.Thread(target=b2a, daemon=True)
thread_a2b.start()
thread_b2a.start()
thread_a2b.join()
thread_b2a.join()

t_list = []

a2b_amount = len(server_b.data[socket.gethostbyname(socket.gethostname())])
a2b_latency = 0.0
for item in server_b.data[socket.gethostbyname(socket.gethostname())]:
    a2b_latency += item.timestamp - float(item.text)
    t_list.append(item.text)
a2b_latency = a2b_latency / a2b_amount

b2a_amount = len(server_b.data[socket.gethostbyname(socket.gethostname())])
b2a_latency = 0.0
for item in server_a.data[socket.gethostbyname(socket.gethostname())]:
    b2a_latency += item.timestamp - float(item.text)
    t_list.append(item.text)
b2a_latency = b2a_latency / b2a_amount

print(f"Server A --> Server B. Sample size: {sample_size} Drop: {(1-(a2b_amount/sample_size))*100}% "
      f"Duration: {a2b_end - a2b_start}s")
print(f"Avg latency: {a2b_latency}s")
print(f"Server B --> Server A. Sample size: {sample_size} Drop: {(1-(b2a_amount/sample_size))*100}% "
      f"Duration: {b2a_end - b2a_start}s")
print(f"Avg latency: {b2a_latency}s", end="\n\n")
print(f"Total number of datagram received: {len(t_list)}")

print("----------")
