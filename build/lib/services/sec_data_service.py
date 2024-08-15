import requests


class SECDataService:

    def __init__(self, user_agent):
        self.base_url = "https://www.sec.gov/Archives/"
        self.api_headers = {
            "User-Agent": user_agent
        }

    def get_filing(self, path):
        full_path = self.base_url + path
        return requests.get(full_path, headers=self.api_headers)

