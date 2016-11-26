#!/usr/bin/env python
import requests
import os
import settings
import sys
import hashlib
import os.path
from os.path import join as pjoin


class Client(object):
    def __init__(self, uid, pwd, parent_dialog, server=None):
        self.uid = uid
        self.pwd = pwd
        if server:
            self.upload_url = "http://" + server + "/upload"
        else:
            self.upload_url = settings.SERVER_UPLOAD_URL
        self.parent_dialog = parent_dialog

    def upload(self, file_to_upload, file_path, s=""):
        files = {settings.FILE_UPLOAD_FIELD_NAME: open(file_to_upload, 'rb')}
        data = {"path": file_path}
        md5_hash = hashlib.md5(open(file_to_upload, 'rb').read()).hexdigest()

        headers = {'Content-MD5': md5_hash}

        try:
            r = requests.post(
                self.upload_url,
                headers=headers,
                files=files,
                data=data,
                auth=(self.uid, self.pwd))
            if r.status_code == 200:
                self._print(s)
            else:
                self._print("Code {}".format(r.status_code))
        except requests.exceptions.ConnectionError:
            self._print("Remote connection forcibly closed, "
                        "were your credentials okay?")

    def mirror_dir_to_server(self, local_dir_path):
        """Make os.walk do the recursing!"""
        total_num_files = sum(
            len(files) for _, _, files in os.walk(local_dir_path))
        count = 1
        for root, dirs, files in os.walk(local_dir_path):
            # Ignore empty dirs
            if files:
                for _file in files:
                    _rpath = os.path.relpath(root, local_dir_path)
                    if _rpath[:2] == './':
                        rpath = _rpath[2:]
                    elif _rpath == ".":
                        rpath = ""
                    else:
                        rpath = _rpath
                    s = "uploaded {} ({} of {})".format(
                        pjoin(rpath, _file), count, total_num_files)
                    count += 1
                    self.upload(pjoin(local_dir_path, rpath, _file), rpath, s)

    def _print(self, s):
        self.parent_dialog.set_info_label(s)


if __name__ == '__main__':
    client = Client()
    client.mirror_dir_to_server(sys.argv[1])
