import requests
import os
import settings
import sys
import time
import getpass
import os.path
from os.path import join as pjoin

class Client(object):
    def __init__(self):
        self.uid = input("Enter user id: ")
        self.pwd = getpass.getpass("Enter password for user {}: ".format(self.uid))


    def upload(self, file_to_upload, file_path):
        files = {settings.FILE_UPLOAD_FIELD_NAME : open(file_to_upload, 'rb')}
        data  = {"path": file_path}


        r = requests.post(settings.SERVER_UPLOAD_URL, 
                files=files, data=data, auth=(self.uid, self.pwd))

    def mirror_dir_to_server(self, local_dir_path):
        """Make os.walk do the recursing!"""
        for root, dirs, files in os.walk("."):
            # Ignore empty dirs
            if files:
                for _file in files:
                    _rpath = os.path.relpath(root, local_dir_path)
                    if _rpath[0] == '.':
                        rpath = _rpath[1:]
                    else:
                        rpath = _rpath
                    t2 = time.time()
                    self.upload(pjoin(rpath, _file), rpath)

                    t2 = time.time() - t2
                    print("Uploaded {} in {} ms".format(
                        pjoin(rpath, _file), t2 * 100)) 

if __name__ == '__main__':
    client = Client()
    try:
        client.mirror_dir_to_server(sys.argv[1])
    except Exception:
        client.mirror_dir_to_server(os.getcwd())
