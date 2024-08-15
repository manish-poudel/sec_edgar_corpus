from services.sec_xbrl_services import SECXBRLServices
from services.sec_index_services import SECIndexServices
from services.sec_data_service import SECDataService

if __name__ == '__main__':
    # xbrl_services = SECXBRLServices("omekus.co@gmail.com")
    # print(xbrl_services.get_submissions(cik="0000320193"))

    index_services = SECIndexServices(user_agent="omekus.co@gmail.com")
    data_services = SECDataService(user_agent="omekus.co@gmail.com")

    files = index_services.get_files(cik_list=["320193", "51143"], from_date=2013, to_date=2013, form_types=["10-Q", "10-K"],
                                     )
    print(files)

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
