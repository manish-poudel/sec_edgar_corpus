import requests


class SECXBRLServices:

    def __init__(self, user_agent):
        self._base_url = "https://data.sec.gov/"
        self._api_headers = {
            "User-Agent": user_agent
        }

    def get_submissions(self, cik):
        url = f"{self._base_url}submissions/CIK{cik}.json"
        data = requests.get(url, headers=self._api_headers)
        return data

    def get_company_facts(self, cik):
        url = f"{self._base_url}/api/xbrl/companyfacts/CIK{cik}.json"
        data = requests.get(url, headers=self._api_headers)
        return data


