import time


#build log message
def log(msg):
    timestamp = time.ctime()
    loggmsg = {'Timestamp': str(timestamp), 'Message': msg}
    return loggmsg
