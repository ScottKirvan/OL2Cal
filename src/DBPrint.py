
## Usage:
# from DBPrint import DebugPrint 
# import inspect
# frame = inspect.currentframe()
# DebugPrint(__file__, frame.f_lineno, "boowah!  %s, and %d, and %d" % (oneliner, 2, 3))

def _DebugPrint(filename, linenumber, *xargs):
    print('%s(%d): %s' % (filename, linenumber,  "%s" % (xargs)))

DebugPrint = _DebugPrint
