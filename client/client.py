#!/usr/bin/env python
import requests
import os
import settings
import sys
import hashlib
import os.path
from os.path import join as pjoin


class Client(object):
    def __init__(self, uid, pwd):
        self.uid = uid
        self.pwd = pwd

    def upload(self, file_to_upload, file_path, s=""):
        files = {settings.FILE_UPLOAD_FIELD_NAME: open(file_to_upload, 'rb')}
        data = {"path": file_path}
        md5_hash = hashlib.md5(open(file_to_upload, 'rb').read()).hexdigest()

        headers = {'Content-MD5': md5_hash}

        try:
            r = requests.post(
                settings.SERVER_UPLOAD_URL,
                headers=headers,
                files=files,
                data=data,
                auth=(self.uid, self.pwd))
            if r.status_code == 200:
                print(s)
            else:
                print("Code {}".format(r.status_code))
        except requests.exceptions.ConnectionError:
            print("Remote connection forcibly closed, "
                  "were your credentials okay?")

    def mirror_dir_to_server(self, local_dir_path):
        """Make os.walk do the recursing!"""
        for root, dirs, files in os.walk(local_dir_path):
            # Ignore empty dirs
            if files:
                for _file in files:
                    _rpath = os.path.relpath(root, local_dir_path)
                    if _rpath[:2] == './':
                        rpath = _rpath[2:]
                        print(rpath)
                    elif _rpath == ".":
                        rpath = ""
                    else:
                        rpath = _rpath
                        print(rpath)
                    s = "Uploaded {}".format(pjoin(rpath, _file))
                    self.upload(pjoin(local_dir_path, rpath, _file), rpath, s)


if __name__ == '__main__':
    client = Client()
    client.mirror_dir_to_server(sys.argv[1])
