from services.sec_xbrl_services import SECXBRLServices
from services.sec_index_services import SECIndexServices
from services.sec_data_service import SECDataService
from services.sec_file_downloader import SECFileDownloader

if __name__ == '__main__':
    # xbrl_services = SECXBRLServices("omekus.co@gmail.com")
    # print(xbrl_services.get_submissions(cik="0000320193"))

    index_services = SECIndexServices(user_agent="omekus.co@gmail.com")
    data_services = SECDataService(user_agent="omekus.co@gmail.com")

    sec_file_downloader = SECFileDownloader(user_agent="omekus.co@gmail.com")
    print(sec_file_downloader.download_file("320193", year = 2023, filing_type="DEF 14A"))

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
