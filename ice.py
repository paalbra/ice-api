import configparser
import copy
import datetime
import re

import bs4
import requests

import utils

class IceAPI():

    def __init__(self, config_path):
        self.config_path = config_path

        self.config = configparser.ConfigParser()
        self.config.read(config_path)
        self.username = self.config["ice"]["username"]
        self.password = self.config["ice"]["password"]
        self.user_agent = self.config["ice"]["user_agent"]

        self.session = requests.session()
        self.session.headers.update({"User-Agent": self.user_agent})

        self.auth = self.do_auth()
        self.subscription_id = self.do_get_subscription_id()

    def do_auth(self):
        url = "https://minside-mbb.ice.no/User/LogIn"
        data = {
            "Username": self.username,
            "Password": self.password,
        }

        return self.do_request(url, data=data)

    def do_request(self, url, data=None, params=None, headers={}):
        if data:
            return self.session.post(url, headers=headers, params=params, json=data)
        else:
            return self.session.get(url, headers=headers, params=params)

    def do_get_subscription_id(self):
        url = "https://minside-mbb.ice.no/Subscription"
        response = self.do_request(url)
        html = response.text
        soup = bs4.BeautifulSoup(html, 'html.parser')
        div = soup.find("div", {"class": "subscription"})
        return int(div["id"][4:])

    def get_daily_usage(self):
        url = "https://minside-mbb.ice.no/Subscription/UsageDetails"
        response = self.do_request(url, params={"sub": self.subscription_id})
        html = response.text
        soup = bs4.BeautifulSoup(html, 'html.parser')
        div = soup.find("div", {"class": "day"})
        rows = div.find("tbody").findChildren("tr")
        data = []
        for row in rows:
            date, download, upload, total = [column.text for column in row.findChildren("td")]
            date = datetime.datetime.strptime(date, "%d.%m.%Y")
            download = utils.human_to_bytes(download)
            upload = utils.human_to_bytes(upload)
            total = utils.human_to_bytes(total)
            data.append([date, download, upload, total])
        return data
