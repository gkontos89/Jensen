import datetime
import getpass
import logging
import os
import platform
import sys
from time import strftime


class JensenLogger:
    __instance = None
    __logger = None
    __file_handler = None
    __controller = None
    __logger_name = None

    @staticmethod
    def get_instance():
        """ Static access method. """
        if JensenLogger.__instance is None:
            JensenLogger()
        return JensenLogger.__instance

    def __init__(self):
        """ Virtually private constructor. """
        if JensenLogger.__instance is not None:
            raise Exception("This class is a singleton!")
        else:
            JensenLogger.__logger_name = 'JensenLogger'
            JensenLogger.__instance = self

    def configure(self, controller):
        self.__controller = controller
        root = 'C:\\Users' if platform.system() == 'Windows' else '/users/'
        user_name = getpass.getuser()
        log_directory = os.path.join(root, user_name, 'Documents', 'JensenLogs')
        if not os.path.isdir(log_directory):
            os.mkdir(log_directory)

        now = datetime.datetime.now()
        log_file_name = "JensenLog__" + "{:%m}".format(now) + "_" + "{:%d}".format(now) + "_" + "{:%y}".format(now) \
                        + "__" + "{:%H}".format(now) + "_" + "{:%M}".format(now) + "_" + "{:%S}".format(now) + '.log'
        self.__file_handler = logging.FileHandler(os.path.join(log_directory, log_file_name))
        self.__file_handler.setFormatter(logging.Formatter('%(levelname)s --- %(message)s\n'))
        self.__logger = logging.getLogger("Jensen")
        self.__logger.setLevel(logging.INFO)
        self.__logger.addHandler(self.__file_handler)

    def log_exception(self, msg):
        self.__logger.exception(msg)
        self.__controller.report_failure_occurred()

    def log_info(self, msg):
        self.__logger.info(msg)
        self.__controller.set_healthy_status()

    def log_warning(self, msg):
        self.__logger.warning(msg)

    def log_error(self, msg):
        self.__logger.error(msg)
        self.__controller.report_failure_occurred(msg=msg)

    def shutdown_logger(self):
        pass
