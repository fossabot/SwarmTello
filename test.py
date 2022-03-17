"""
test.py - sunnyqa233

A python to test all modules in package swarm.
"""
from swarm import _public, _log
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
