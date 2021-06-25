# APC Mini Session Overview midi remote script for Ableton Live 9.6
# version 1.0.0
# This program is free software under the terms of the The MIT License (MIT)
# Copyright 2016, midiscripts.net


class Logger(object):
    """
    Utility class, which gives set of logging tools and promotes
    clean logging code.
    """

    def log_start(self):
        """
        It is convinient to use `----` to emphasize script's log
        entries in Live's log file.
        """
        self.log_message(
            '-------- ' + self.script_name + ' log started ----------')

    def log_disconnect(self):
        """
        Disconnect logging gives clean indication when Live was closed.
        """
        self.log_message(
            '-------- ' + self.script_name + ' disconnected ---------')