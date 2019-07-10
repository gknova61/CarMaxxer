#!/usr/bin/env python3

"""ioHandler.py: General lib for handling varying file I/O behavior across operating systems"""

__author__      = "Keanu Kauhi-Correia"
__version__ = "1.0"
__maintainer__ = "Keanu Kauhi-Correia"
__email__ = "keanu.kkc@gmail.com"

import os

def rename(oldFile,newFile,overwrite=True):
    if not os.path.exists(oldFile):
        return False

    if os.path.exists(newFile):
        if overwrite:
            os.remove(newFile)
        else:
            return False
    os.rename(oldFile, newFile)
    return True