import re
import traceback
from bs4 import BeautifulSoup

from api.redis.constants.datatypes import DEPARTMENT_DATA_TYPE
from api.selenium import driver

from api.utils.url import generateUbcUrl

RE_STRING_HEADER_CLASS = re.compile('listHeader')
RE_STRING_ALLOWED_CHARACTERS = r'[^a-zA-Z0-9 ]'

def scrapeDepartmentInformation():
    departmentInfo = []
    try:
        # do this initially to test connection
        driver.get(generateUbcUrl('DEPARTMENTS'))
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        main_table = soup.find('table', id='mainTable')
        main_table = main_table.find('tbody')

        rows = main_table.find_all('tr')
        
        for row in rows:
            key = re.sub(RE_STRING_ALLOWED_CHARACTERS, '', row.contents[0].get_text()).strip()
            departmentInfo.append({
                'rkey': f'{DEPARTMENT_DATA_TYPE}:{key}',
                'key': key.upper(),
                'name': re.sub(RE_STRING_ALLOWED_CHARACTERS, '', row.contents[1].get_text()).strip(),
                'faculty': re.sub(RE_STRING_ALLOWED_CHARACTERS, '', row.contents[2].get_text()).strip(),
            })

    except Exception as e:
        print('ERROR ->>> could not get department info.',  '{}'.format(e))
        traceback.print_exc()
        raise
    finally:
        print(departmentInfo)
        return departmentInfo
