import re

import requests


class SECFileDownloader:

    def __init__(self, user_agent):
        self.base_url = "https://www.sec.gov/Archives/edgar/full-index/"
        self.api_headers = {
            "User-Agent": user_agent
        }

    def download_file(self, cik, year,  filing_type, qtr = None,):
        # Get the filings for a specific CIK, year, and quarter
        if qtr is not None:
            filings = self._get_qtr_filings(cik=cik, filling_type=filing_type, year=year, qtr_name=qtr)
        else:
            filings = []
            for qtr in ['QTR1', 'QTR2', 'QTR3', 'QTR4']:
                try:
                    filings = filings + self._get_qtr_filings(cik=cik, filling_type=filing_type, year=year,
                                                              qtr_name=qtr)
                except:
                    continue
        return filings

    def _get_qtr_filings(self, cik, filling_type, year, qtr_name):
        filename = "master.idx"
        url = f"{self.base_url}{year}/{qtr_name}/{filename}"
        print(f"Fetching data from: {url}")

        # Fetching the index file from the SEC website
        response = requests.get(url, headers=self.api_headers).content

        # Convert the response from bytes to string
        response_str = response.decode('latin-1')  # Using latin-1 encoding to handle special characters

        # Regex pattern to match the CIK and filing information
        pattern = r"(?P<cik>\d+)\|(?P<company_name>[^|]+)\|(?P<form_type>[^|]+)\|(?P<date_filled>\d{4}-\d{2}-\d{2})\|(?P<file_name>[^|]+)"

        fillings = []

        # Processing the response line by line
        for line in response_str.splitlines():
            match = re.match(pattern, line.strip())
            if match:
                result = match.groupdict()
                # Check if the CIK and filing type match
                if result["cik"] == cik and result["form_type"] == filling_type:
                    result['qtr'] = qtr_name
                    result['year'] = year
                    result['full_url'] = f"https://www.sec.gov/Archives/{result['file_name']}"
                    fillings.append(result)

        return fillings
