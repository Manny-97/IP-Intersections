import math
import re
import os
from enum import Enum


PI = math.pi


class MsgType(Enum):
    INFO = 1
    WARNING = 2
    ERROR = 3

# Convert real and imaginary parts of complex number
# to magnitude and phase. Phase is within [-0.5pi, 1.5pi).
def complex2mag(re, im):
    mag = math.sqrt(re * re + im * im)
    phase = math.atan2(im, re)

    if re < 0.0:
        phase += PI

    return mag, phase

# Map an angle to the range [0, 2pi) radians.
def wrapAngle(angle):
    twoPi = 2.0 * PI
    return angle - twoPi * math.floor(angle / twoPi)

class Log:
    @staticmethod
    def log(str, type):
        if type == MsgType.INFO:
            print("Info: ", str)
        elif type == MsgType.WARNING:
            print("Warning: ", str)
        elif type == MsgType.ERROR:
            print("Error: ", str)

    @staticmethod
    def info(str):
        Log.log(str, MsgType.INFO)

    @staticmethod
    def warning(str):
        Log.log(str, MsgType.WARNING)

    @staticmethod
    def error(str):
        Log.log(str, MsgType.ERROR)

# if path doesn't exist, return False
# if path is a zero-length file, return False
# if path is a directory, return False
def fileexists(path):
    if not os.path.exists(path):
        return False

    if os.path.isdir(path):
        return False

    if os.path.getsize(path) == 0:
        return False

    return True

# Check if the extension of a filename matches a given extension
def extensionIs(filename, ext):
    return filename.endswith(ext)

# if path is a file, return its parent directory.
# if path is a directory, return itself.
# if neither, throw a runtime_error.
def getDirectory(path):
    if os.path.isfile(path):
        return os.path.dirname(path)
    elif os.path.isdir(path):
        return path
    else:
        raise RuntimeError(f"getDirectory(): '{path}' is neither a file nor a directory.")

# Check the syntax of a regular expression
def checkregex(regex):
    try:
        re.compile(regex)
    except re.error as ex:
        error_codes = {
            re.error: "Unknown error in regex.",
            re.error: "The expression contained an invalid collating element name.",
            re.error: "The expression contained an invalid character class name.",
            re.error: "The expression contained an invalid escaped character, or a trailing escape.",
            re.error: "The expression contained an invalid back reference.",
            re.error: "The expression contained mismatched brackets [ and ].",
            re.error: "The expression contained mismatched parentheses ( and ).",
            re.error: "The expression contained mismatched braces { and }.",
            re.error: "The expression contained an invalid range between braces { and }.",
            re.error: "The expression contained an invalid character range.",
            re.error: "There was insufficient memory to convert the expression into a finite state machine.",
            re.error: "The expression contained a repeat specifier (one of *?+{) that was not preceded by a valid regular expression.",
            re.error: "The complexity of an attempted match against a regular expression exceeded a pre-set level.",
            re.error: "There was insufficient memory to determine whether the regular expression could match the specified character sequence."
        }
        return False, error_codes[ex.__class__]
    return True, ""



import math
import re
import sys
from enum import Enum
from typing import Tuple
import os

PI = 3.14159265358979323846


class MsgType(Enum):
    INFO = "Info"
    WARNING = "Warning"
    ERROR = "Error"


class Log:
    os = sys.stderr

    @staticmethod
    def log(msg: str, msg_type: MsgType) -> None:
        prefix = msg_type.value + ": "
        Log.os.write(prefix + msg + '\n')

    @staticmethod
    def info(msg: str) -> None:
        Log.log(msg, MsgType.INFO)

    @staticmethod
    def warning(msg: str) -> None:
        Log.log(msg, MsgType.WARNING)

    @staticmethod
    def error(msg: str) -> None:
        Log.log(msg, MsgType.ERROR)


def complex2mag(re: float, im: float) -> Tuple[float, float]:
    mag = math.sqrt(re * re + im * im)
    phase = math.atan2(im, re)

    if re < 0.0:
        phase += PI

    return mag, phase


def wrap_angle(angle: float) -> float:
    two_pi = 2.0 * PI
    return angle - two_pi * math.floor(angle / two_pi)


def file_exists(path: str) -> bool:
    return os.path.exists(path) and os.path.isfile(path) and os.path.getsize(path) != 0


def extension_is(filename: str, ext: str) -> bool:
    return filename.endswith(ext)


def get_directory(path: str) -> str:
    return os.path.dirname(path)


def check_regex(regex: str) -> bool:
    try:
        re.compile(regex)
        return True
    except re.error as e:
        Log.error(str(e))
        return False