__author__ = 'xfu'
#!/usr/bin/env python
#Filename:BDEException.py
class BDEException(Exception):
    def __init__(self,response,msg):
        self.response = response
        self.msg = msg
    def _read_(self):
        return self.msg
    def _getStatus_(self):
        return self.response.status
    def _getReason(self):
        return self.response.reason