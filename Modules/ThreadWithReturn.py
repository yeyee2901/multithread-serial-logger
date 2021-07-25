import sys
from threading import Thread


# Automatically determine which Python version is running
python_version, *_ = sys.version_info

if python_version >= 3:
    _thread_target, _thread_args, _thread_kwargs = ('_target', '_args', '_kwargs')
else:
    _thread_target, _thread_args, _thread_kwargs = ('_Thread_target', '_Thread_args', '_Thread_kwargs')


class ThreadWithReturn(Thread):

    # Call the parent constructor to initialize
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    # Override the default run() method.
    # This is needed because the default run() method only calls the
    # target function. The return value is discarded.
    def run(self):
        target_function = getattr(self, _thread_target)

        # check to see if target function exists
        # If it exists, run the function using arguments passed in
        if target_function:
            self._return = target_function(*getattr(self,_thread_args), **getattr(self,_thread_kwargs))

    # Call parent .join() method
    def join(self, *args, **kwargs):
        super().join(*args, **kwargs)
        return self._return
