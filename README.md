# Diawi upload script for Android Projects
This is a simple script to upload builds to Diawi. You can use it locally in your machine, or in a CI/CD environment.

## Requirements
* Python 3
* PycURL, libcurl

## Setup
* Clone the repo to the root directory of your Android project.
* Obtain a Diawi token from (here)[https://dashboard.diawi.com/profile/api] and add it to `diawi_token` in `diawi_metadata.json`.
* Optionally, describe your build artifacts in the `artifacts` section.

```json
{
  "diawi_token": "xxxxxxxxxxxxxxxxxxxxxx",
  "artifacts": {
    "app-googleplay-debug.apk": "Google Play version debug",
    "app-fdroid-debug.apk": "Fdroid version debug"
  }
}
```

* Build Android Project
```bash
$ gradle clean assembleDebug
```
* Upload build artifacts
```bash
$ python3 diawi_upload.py
Uploading 2/2
Checking 2/2
Done
Google Play version debug - app-googleplay.debug.apk - https://i.diawi.com/aBcD3f
Fdroid version debug - app-fdroid-debug.apk - https://i.diawi.com/kLmN0p
```
## License
```
MIT License

Copyright (c) 2020 Anand Bose

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```
