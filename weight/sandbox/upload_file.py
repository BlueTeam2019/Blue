#!/usr/bin/env python3

import requests as req

url = 'http://localhost:5000/upload'

with open('sid.jpg', 'rb') as f:

    files = {'image': f}

    r = req.post(url, files=files)
    print(r.text)
