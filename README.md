# Auto_Py
An automation script

## Pre-requisites

1. Download [ChromeDriver](https://chromedriver.storage.googleapis.com/index.html?path=79.0.3945.36/). Unzip the download and place `chromedriver.exe` in `./driver/`

Note: Use ChromeDriver 79.0.3945.36 if you are seeing compatibility issues with Chrome or update Chrome to the latest stable version.

2. Install pip for python:

`python -m install pip`

3. Install Python Pip dependencies:

`pip install -r /requirements.txt`

4. Place files that need to be converted in `/input`

5. Run the script.

`python auto_convert.py /input /output`
