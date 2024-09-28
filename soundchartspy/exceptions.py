class SoundChartsError(Exception):

    def __init__(self, http_status, code, msg, reason=None, headers=None):
        self.http_status = http_status
        self.code = code
        self.msg = msg

    def __str__(self):
        return 'http status: {}, code:{} - {}'.format(
            self.http_status, self.code, self.msg)
