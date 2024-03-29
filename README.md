# Walks-Selenium-Tests
Automated tests that simulate the checkout process for https://www.takewalks.com and https://www.walksofitaly.com


## Dependencies

#### Python
- `brew install python` to install Python
- `python3 --version` to check version and confirm a successful installation

#### Selenium
- `pip install selenium` to install the Selenium package for Python

#### ChromeDriver
- Download [ChromeDriver](https://sites.google.com/a/chromium.org/chromedriver/downloads) according to your system's version of Google Chrome (find your Chrome version through Help -> About Google Chrome)
- Move the extracted chromedriver file to `/usr/local/bin`

#### Additional Information
- Reference the [Selenium with Python Documentation](https://selenium-python.readthedocs.io/installation.html) for more information on how to install the Selenium package for Python


## Setup

#### Configuration
- Make a copy of `config.ini.example` as `config.ini`
- Fill out `config.ini` in a text editor

#### Run
- `python3 run.py` in the root directory to load the interactive runner
