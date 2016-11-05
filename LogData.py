class LogData(object):

    def __init__(self, start_time = 0, stop_time = 0, ip = 0):
        self.start_time = start_time
        self.stop_time = stop_time
        self.ip = ip

    def get_start_time(self):
        return self.start_time

    def get_stop_time(self):
        return self.stop_time

    def get_ip(self):
        return self.ip

    def set_start_time(self, start_time):
        self.start_time = start_time

    def set_stop_time(self, stop_time):
        self.stop_time = stop_time

    def set_ip(self, ip):
        self.ip = ip
