import logging
import os
import sys
import traceback

from logging.handlers import SysLogHandler
from NVMeshSDK import Consts

_main_logger = logging.getLogger('NVMeshSDK')

_default_format = '%(name)s[{}]: %(levelname)s: %(message)s'.format(os.getpid())
_logging_formatter = None
_log_level = None
_stdoutHandler = None
_stderrHandler = None
_syslogHandler = None

def getMainLogger():
	return _main_logger

def setOptions(logToSysLog=None, logToStdout=None, logToStderr=None, logLevel=None, propagate=None, formatString=None):
	global _main_logger
	global _syslogHandler
	global _stderrHandler
	global _stdoutHandler
	global _logging_formatter
	global _log_level

	logger = getMainLogger()

	if propagate is not None:
		logger.propagate = propagate

	if logLevel is not None:
		logger.setLevel(logLevel)

	if formatString is not None:
		_logging_formatter = logging.Formatter(formatString)

	if logLevel is not None:
		_log_level = logLevel

	logger.handlers = []

	if logToSysLog is None and _syslogHandler:
		logger.addHandler(_syslogHandler)
	elif logToSysLog:
		_syslogHandler = SysLogHandler(address=Consts.SYSLOG_PATH)
		_syslogHandler.setFormatter(_logging_formatter)
		_syslogHandler.setLevel(_log_level)
		logger.addHandler(_syslogHandler)
	else:
		_syslogHandler = None

	if logToStdout is None and _stdoutHandler:
		logger.addHandler(_stdoutHandler)
	elif logToStdout:
		_stdoutHandler = logging.StreamHandler(sys.stdout)
		_stdoutHandler.setFormatter(_logging_formatter)
		_stdoutHandler.setLevel(_log_level)
		logger.addHandler(_stdoutHandler)
	else:
		_stdoutHandler = None

	if logToStderr is None and _stderrHandler:
		logger.addHandler(_stderrHandler)
	elif logToStderr:
		_stderrHandler = logging.StreamHandler(sys.stderr)
		_stderrHandler.setFormatter(_logging_formatter)
		_stderrHandler.setLevel(logging.ERROR)
		logger.addHandler(_stderrHandler)
	else:
		_stderrHandler = None

def setOptionsDefaults():
	setOptions(logToSysLog=True, logToStdout=False, logToStderr=False, logLevel=logging.DEBUG, propagate=True, formatString=_default_format)

def getNVMeshSDKLogger(logger_name):
	name = 'NVMeshSDK.{0}'.format(logger_name)
	return logging.getLogger(name)

def logStackTrace(ex, logger):
	exc_type, exc_value, exc_traceback = sys.exc_info()
	exString = traceback.format_exc()
	errorLines = exString.split('\n')

	for line in errorLines:
		logger.error(line)

setOptionsDefaults()