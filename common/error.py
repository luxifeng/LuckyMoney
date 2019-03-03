#-*- coding:utf-8 -*-
"""
Handle errors

@author: Lucy
@file: error.py
@time: 2019/03/01
"""

class Error(Exception):
    """
    Base exception class for errors.
    """

class ConfigParseError(Error):
    """
    Error thrown when failed to parse a config yaml files.
    """

    def __init__(self, file_path):
        self.file_path = file_path
        super(ConfigParseError, self).__init__()

    def __str__(self):
        return 'Failed to parse config file %s.' % self.file_path