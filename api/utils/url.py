from datetime import datetime

def generateUbcUrl(type: str, dept: str = "", courseNum: str = "", session: str = "W"):
    BASE_URL = "https://courses.students.ubc.ca"
    PAGE_NAME = "subjarea"
    TABLE_NAME = {
        "DEPARTMENTS": "subj-all-departments",
        "SUBJECTS_IN_DEPARTMENT": "subj-department",
        "COURSE": "subj-course"
    }

    url = BASE_URL + "/cs/courseschedule?pname=" + PAGE_NAME
    if type == "DEPARTMENTS":
        url += "&tname=" + TABLE_NAME["DEPARTMENTS"]
    elif type == "SUBJECTS":
        url += "&tname=" + TABLE_NAME["SUBJECTS_IN_DEPARTMENT"]
        url += "&dept=" + dept
    else:
        url += "&tname=" + TABLE_NAME["COURSE"]
        url += "&dept=" + dept + "&course=" + courseNum

    url += "&sessyr=" + str(datetime.now().year)
    url += "&sesscd=" + session

    return url
