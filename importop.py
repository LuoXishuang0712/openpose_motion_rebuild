import sys

class importop:
    def __init__(self, path) -> None:
        self.path = path

    def __call__(self):
        try:
            sys.path.append(self.path)
            from openpose import pyopenpose as op
        except (ImportError, ) as e:
            print(e)
            return None
        return op


# a method required by openpose official
# try:
#     # Change these variables to point to the correct folder (Release/x64 etc.)
#     sys.path.append('../openpose/build/python')
#     # If you run `make install` (default path is `/usr/local/python` for Ubuntu), you can also access the OpenPose/python module from there. This will install OpenPose and the python library at your desired installation path. Ensure that this is in your python path in order to use it.
#     # sys.path.append('/usr/local/python')
#     from openpose import pyopenpose as op
# except ImportError as e:
#     print(
#         'Error: OpenPose library could not be found. Did you enable `BUILD_PYTHON` in CMake and have this Python script in the right folder?')
#     raise e