from timestemp import TimeStemp
import time

class LogType():
    INFO = '--Info--'
    WARNING = '--Warning--'
    ERROR = '--Error--'

class _SingleLogger():

    file_name = 'log.txt'
    
    def write_log (self, i_message):
        print(TimeStemp.get_time_stemp() + '\t' + i_message)

        return True
    
    def write_log_with_type (self, i_type_message, i_message):
        """
        Post a log in log file with type of Info, Warning or Error.
        type_message (String): Info, Warning or Error from LogType.
        message (String): Message to write in log file.
        """

        return self.write_log(i_message = str(i_type_message) + ': ' + str(i_message))
    
    def write_info_log (self, i_message):
        return self.write_log_with_type(i_type_message = LogType.INFO, i_message = i_message)
    
    def write_warning_log (self, i_message):
        return self.write_log_with_type(i_type_message = LogType.WARNING, i_message = i_message)
    
    def write_error_log (self, i_message):
        return self.write_log_with_type(i_type_message = LogType.ERROR, i_message = i_message)
    
    def __del__(self):
        pass

class Logger:
    """
    """

    _file_inited = False
    #_logger = None
    _logger = _SingleLogger()

    def __init__(self):
        if (Logger._logger is None):
            Logger._logger = _SingleLogger()
            _file_inited = True
    
    @staticmethod
    def get_logger():
        return Logger._logger


logger = Logger.get_logger()