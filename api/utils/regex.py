import re

RE_COURSE_FORMAT = r"^[a-zA-Z]{2,6} \d{1,4}([a-zA-Z]{0,2})$"
# 2-6 letters
# 1 whitespace
# 1-4 numbers
# optional 0-2 letters

def isStringACourse(subj: str):
    return re.match(RE_COURSE_FORMAT, subj)
