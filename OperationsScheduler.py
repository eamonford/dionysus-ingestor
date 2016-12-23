import time
import thread
import logging
from datetime import datetime as dt

logging.basicConfig()
Logger = logging.getLogger(__name__)

def __runAtInterval(function, period, args, repeat=False):
    while True:
        time.sleep(float(period))
        try:
            function(args)
        except:
            Logger.exception("Failed to execute interval-scheduled "
                              "operation. It will be reattempted at the " +
                              "next scheduled time.")
        if not repeat:
            break


def __runAtTime(function, hour, minute, args, repeat=False):
    while True:
        now = dt.utcnow()
        if now.hour is hour and now.minute is minute:
            try:
                function(args)
            except:
                Logger.exception("Failed to execute time-scheduled "
                                  "operation. It will be reattempted at the " +
                                  "next scheduled time.")
            if not repeat:
                break
            time.sleep(60)
        else:
            time.sleep(60)

def asyncRunAtInterval(function, period, args, repeat=False):
    """Schedule a function to run after a number of seconds, optionally repeating."""
    thread.start_new_thread(__runAtInterval, (function, period, args, repeat))
