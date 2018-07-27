# FoodTruckFinder
Command line tool to find food trucks in SF at the current time and day

## Install Dependencies
This project should be run with Python 3. You can get Python3 using [homebrew](https://brew.sh/):<br />
`brew install python`

Use [pip](https://pypi.org/project/pip/) to install dependencies to your Python interpreter from the requirements.txt file:<br />
`cd` into cloned project directory and run `pip install -r requirements.txt`

## How to Run
1) `cd` into cloned project directory
2) Generate an app token [here](https://data.sfgov.org/profile/app_tokens)
3) Run the following command in your terminal to set app_token in your environment variables:<br />
`export SODAPY_APPTOKEN=<your_app_token>`
4) Run `python food_truck_finder.py`

## Scaling to Webapp
In order to expand this project to a webapp, we will need to account for caching returned results for a given time to minimize the latency of calling the underlying API.  Since it is unlikely that a given user would submit a request at the exact same time on a given day, we need to take into account the time frame of when the user submits the request.  We can make an assumption that if someone makes a request at 7:33pm on a given day, the results should be the same as someone who makes a request at 7:36pm or 7:38pm on that same day.  From inspection of the data source, start and end times seem to always be on the hour mark.  Thus in our cache, we can store that if someone makes a request at 7:33pm on Saturday, we can store the results of that request to correlate to a 7-8pm time frame.  When any subsequent requests come through, we can first check if the cache has a corresponding result stored for the hour time frame surrounding the current time and directly return the result from cache if there is.  To ensure that the cache does not contain stale data, we can configure a TTL (Time to Live) variable to the cache data.
