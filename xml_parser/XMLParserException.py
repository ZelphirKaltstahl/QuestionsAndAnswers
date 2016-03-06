# -*- coding: utf-8 -*-
__author__ = 'xiaolong'


class XMLParserException(BaseException):
    def __init__(self, message):
        super(XMLParserException, self).__init__(message)
