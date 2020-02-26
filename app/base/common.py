import math
import sys
import traceback

from PyQt5.QtWidgets import QMessageBox


def try_exec(return_=False, show=False, info_only=False):
    def wrapper(func):
        def _wrapper(*args, **kwargs):
            try:
                result = func(*args, **kwargs)
                if return_:
                    return result
                else:
                    return True
            except Exception as e:
                if show:
                    exc = traceback.format_exc()
                    if info_only:
                        QMessageBox.warning(None, 'Error', '%s' % e)
                    else:
                        print(exc, file=sys.stderr)
                        QMessageBox.warning(None, 'Error', exc)
                return False

        return _wrapper

    return wrapper
