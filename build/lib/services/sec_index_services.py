import json
import os.path
import re

import requests


class SECIndexServices:

    def __init__(self, user_agent):
        self.base_url = "https://www.sec.gov/Archives/edgar/full-index/"
        self.api_headers = {
            "User-Agent": user_agent
        }

    def get_files(self, cik_list, from_date, to_date, qtr_names=None, form_types=None):
        # Getting valid years. This will be used to know if year
        # exits in sec website
        valid_years_path = self._get_full_index_years()
        current_date = from_date

        filings = []

        while current_date <= to_date:
            if str(current_date) in valid_years_path:
                index_json = self._get_year_index(year=current_date)

                # Loop through valid years
                for item in index_json["directory"]["item"]:
                    if qtr_names is None or item["name"] in qtr_names:
                        print(f"Getting files for {item['name']} in year {current_date}")
                        qtr_filings = self._get_qtr_filings(cik=cik_list, year=current_date, qtr_href=item['href'],
                                                            form_types=form_types, qtr_name=item['name'])
                        filings = filings + qtr_filings

                current_date = current_date + 1

        return filings

    def _get_qtr_filings(self, cik, form_types, year, qtr_name, qtr_href, use_cache=True):
        directory_path = f"caches/full_index/{year}/{qtr_href}"
        filename = "master.idx"
        file_path = f"{directory_path}{filename}"
        url = f"{self.base_url}/{year}/{qtr_href}master.idx"
        filings = []

        # if user doesn't want to use cache or if he wants to use cache but cache doesn't exist, then import it
        if not use_cache or (use_cache and not self._cache_file_exists(file_path)):
            self._import_filings(url=url, directory_path=directory_path, filename=filename)

        pattern = r"(?P<cik>\d+)\|(?P<company_name>[^|]+)\|(?P<form_type>[^|]+)\|(?P<date_filled>\d{4}-\d{2}-\d{2})\|(" \
                  r"?P<file_name>[^|]+)"

        with open(file_path, "r") as file:
            for line in file:
                match = re.match(pattern, line.strip())
                if match:
                    result = match.groupdict()
                    if result["cik"] in cik and (form_types is None or result["form_type"] in form_types):
                        result['qtr'] = qtr_name
                        result['year'] = year
                        filings.append(result)
        return filings

    def _import_filings(self, url, directory_path, filename):
        print("Getting from sec website")
        # Get directories from sec websites
        filings = requests.get(url, headers=self.api_headers).content
        if not self._cache_directory_exists(path=directory_path):
            # if year directory doesn't exist, create one
            os.makedirs(directory_path, exist_ok=True)
        # Save master idx to our cache folder
        with open(f"{directory_path}{filename}", "wb") as file:
            file.write(filings)

    def _get_year_index(self, year, use_cache=True):

        base_path = f"caches/full_index/{year}/"
        index_path = f"{base_path}/index.json"

        index_json = None
        # If user wants to use cache file, and it exists we return from it
        if use_cache and self._cache_file_exists(index_path):
            with open(index_path, 'r') as json_file:
                index_json = json.load(json_file)
        else:
            print("Getting from sec website...")
            # Get directories from sec websites
            url = f"{self.base_url}/{year}/index.json"
            index_json = requests.get(url, headers=self.api_headers).json()
            if not self._cache_directory_exists(path=base_path):
                # if year directory doesn't exist, create one
                os.makedirs(base_path, exist_ok=True)

            # Save index to our cache folder
            with open(index_path, "w") as json_file:
                json.dump(index_json, json_file, indent=4)

        return index_json

    def _get_full_index_years(self):
        url = self.base_url + "index.json"
        valid_years = []
        data = requests.get(url, headers=self.api_headers).json()
        for item in data["directory"]["item"]:
            valid_years.append((item["name"]))
        return valid_years

    @staticmethod
    def _cache_directory_exists(path):
        return os.path.isdir(path)

    @staticmethod
    def _cache_file_exists(file_path):
        return os.path.isfile(file_path)
