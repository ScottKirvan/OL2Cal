
## Usage:
# from DBPrint import DebugPrint 
# import inspect
# frame = inspect.currentframe()
# DebugPrint(__file__, frame.f_lineno, "boowah!  %s, and %d, and %d" % (oneliner, 2, 3))

_enabled = True

def SetEnabled(enableit):
    global _enabled
    _enabled = enableit

def GetEnabled():
    global _enabled
    return _enabled

def _DebugPrint(filename, linenumber, *xargs):
    if (_enabled):
        print('%s(%d): %s' % (filename, linenumber,  "%s" % (xargs)))

DebugPrint = _DebugPrint
