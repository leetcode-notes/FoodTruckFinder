# FoodTruckFinder
Command line tool to find food trucks in SF at the current time and day

## Install Dependencies
This project should be run with Python 3. You can get Python3 using [homebrew](https://brew.sh/): 
`brew install python`

Use [pip](https://pypi.org/project/pip/) to install dependencies to your Python interpreter:
`pip install -r requirements.txt`

## How to Run
1) Generate an app token [here](https://data.sfgov.org/profile/app_tokens)
2) Run the following command in your terminal to set app_token in your environment variables:
`export SODAPY_APPTOKEN=<your_app_token>`
3) Run `python food_truck_finder.py`

## Scaling to Webapp
TODO
