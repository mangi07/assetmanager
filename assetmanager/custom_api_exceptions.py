# -*- coding: utf-8 -*-
"""
Created on Wed Nov  7 16:44:41 2018

@author: Ben.Olson
"""

from rest_framework.exceptions import APIException


class BadRequestException(APIException):
    def __init__(self, message):
        self.default_detail = message
        self.status_code = 400
        self.default_code = 'bad_request'
        super().__init__()

        
    
