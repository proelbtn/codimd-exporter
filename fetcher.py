import logging
import os
import sys

import requests
from bs4 import BeautifulSoup



class CodiMDClient:
    def _get(self, endpoint, **kwargs) -> requests.Response:
        return self.sess.get(f"{self.baseurl}{endpoint}", **kwargs)
    
    def _post(self, endpoint, data, **kwargs) -> requests.Response:
        return self.sess.post(f"{self.baseurl}{endpoint}", data, **kwargs)

    def __init__(self, baseurl, email, password):
        if baseurl == None or baseurl == "":
            raise Exception("baseurl must not be empty.")

        if email == None or email == "": 
            raise Exception("email must not be empty.")

        if password == None or password == "": 
            raise Exception("password must not be empty.")

        self.sess = requests.Session()
        self.baseurl = baseurl

        if self.baseurl == "https://hackmd.io":
            res = self._get("/login")
            if 400 <= res.status_code < 500:
                raise Exception(f"fetch csrf token failed with status {res.status_code}.")

            soup = BeautifulSoup(res.content, features="lxml")
            csrf_token = soup.select("head > meta[name=csrf-token]")[0]["content"]

            res = self._post("/login", data={"email": email, "password": password, "_csrf": csrf_token})
            if 400 <= res.status_code < 500:
                raise Exception(f"login failed with status {res.status_code}.")
            if "Forgot password" in res.content.decode():
                raise Exception(f"login failed.")
        else:
            res = self._post("/login", data={"email": email, "password": password})
            if 400 <= res.status_code < 500:
                raise Exception(f"login failed with status {res.status_code}.")


    def export_data(self) -> bytes:
        if self.baseurl == "https://hackmd.io":
            endpoint = "/exportAllNotes"
        else:
            endpoint = "/me/export"

        res = self._get(endpoint)
        return res.content



CODIMD_BASEURL = os.getenv("CODIMD_BASEURL")
CODIMD_EMAIL = os.getenv("CODIMD_EMAIL")
CODIMD_PASSWORD = os.getenv("CODIMD_PASSWORD")

CODIMD_DEBUG = os.getenv("CODIMD_DEBUG")

if CODIMD_DEBUG:
    logging.basicConfig(level=logging.DEBUG)

cli = CodiMDClient(CODIMD_BASEURL, CODIMD_EMAIL, CODIMD_PASSWORD)

res = cli.export_data()
sys.stdout.buffer.write(res)
