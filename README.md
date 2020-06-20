# ice-mbb-api

## About

Simple module that tries to get information from "My Page" at the [Ice Mobile Broadband page](https://minside-mbb.ice.no/).

## Setup

```
cp config.sample.ini config.ini
vim config.ini # And modify with your details
python3 -m venv venv
. venv/bin/activate
pip install requests beautifulsoup4
```

## Example

```
import pprint

import ice

api = ice.IceAPI("config.ini")

pprint.pprint(api.get_daily_usage())
```
