"""
exceptions.py

Custom exceptions used by LogRotator.
"""


class LogRotatorError(Exception):
    """
    Base exception for all LogRotator errors.
    """
    pass


class ConfigError(LogRotatorError):
    """
    Configuration file is invalid.
    """
    pass

class RuntimeValidationError(LogRotatorError):
    """
    Runtime environment validation failed.
    """
    pass


class LockError(LogRotatorError):
    """
    Unable to acquire application lock.
    """
    pass


class RotationError(LogRotatorError):
    """
    Log rotation failed.
    """
    pass


class CompressionError(LogRotatorError):
    """
    ZIP compression failed.
    """
    pass


class ArchiveError(LogRotatorError):
    """
    Archive movement failed.
    """
    pass


class SchedulerError(LogRotatorError):
    """
    Scheduler initialization or execution failed.
    """
    pass