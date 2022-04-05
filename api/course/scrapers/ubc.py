# sample links
# https://courses.students.ubc.ca/cs/courseschedule?pname=subjarea&tname=subj-all-departments
# https://courses.students.ubc.ca/cs/courseschedule?pname=subjarea&tname=subj-department&dept=AANB
# https://courses.students.ubc.ca/cs/courseschedule?pname=subjarea&tname=subj-course&dept=AANB&course=530A

# TODO: If error detected during scraping, don't save into redis

import re
import json
import traceback
from bs4 import BeautifulSoup

from api.redis.constants.datatypes import COURSE_DATA_TYPE
from api.redis.utils import getOne
from api.selenium import driver

from api.utils.exceptions import PageError
from api.utils.regex import isStringACourse
from api.utils.url import generateUbcUrl

RE_STRING_PREREQ = re.compile("^(?:Pre-reqs).*$")
RE_STRING_COREQ = re.compile("^(Co-req).*$")
RE_STRING_NOOFFER = re.compile("no longer offered")

RE_STRING_REQUIRED_COURSES = [
    [0, re.compile("(?:All of|all of)")],
    [1, re.compile("(?:One of|one of)")],
    [2, re.compile("(?:Two of|two of)")],
    [3, re.compile("(?:Three of|three of)")],
    [4, re.compile("(?:Four of|four of)")],
    [5, re.compile("(?:Five of|five of)")],
]

def filterPrereqContainer(tag):
    return tag.name == "p" and len(tag.contents) and RE_STRING_PREREQ.match(tag.contents[0].get_text())

def filterCoreqContainer(tag):
    return tag.name == "p" and len(tag.contents) and RE_STRING_COREQ.match(tag.contents[0].get_text())

def checkCourseNotOffered(container):
    try:
        return any(RE_STRING_NOOFFER.search(content.get_text()) for content in container.contents)
    except:
        print("ERROR ->>> page layout unrecognized")
        raise

def checkNumberOfCoursesRequired(line):
    for NUM_CRIT in RE_STRING_REQUIRED_COURSES:
        if NUM_CRIT[1].search(line): return NUM_CRIT[0]
    return -1 # if no match, this line is not a prereq indicator

def getCoursePrereqs(container):
    prereqs = [] # collect prereqs
    requiredCourses = 0 # number of courses required in the group
    prereqGroupCounter = -1

    for currLine in container:
        # get number of courses required for this prereq group
        coursesRequired = checkNumberOfCoursesRequired(currLine.get_text())

        # add to prereq list as necessary
        if coursesRequired != -1: # if an indicator is given
            requiredCourses = coursesRequired # save the number of required corses
            prereqGroupCounter += 1 # increment the group number
            continue
        elif prereqGroupCounter == -1: # if no indicator but its the first line
            requiredCourses = 0
            prereqGroupCounter += 1
            continue

        # if its not a link or no indicator yet (weird use case)
        if prereqGroupCounter == -1 or currLine.name != "a": continue
        # add as a prereq
        name = currLine.get_text().strip().upper()
        if not isStringACourse(name): continue # validation check if string is a course

        splitted = name.split(" ")
        prereqs.append({
            "dept": splitted[0],
            "courseNum": splitted[1],
            "extraAttribs": {
                "type": "prereq",
                "group": prereqGroupCounter,
                "numRequired": requiredCourses,
            }
        })

    return prereqs

def getCourseCoreqs(container):
    coreqs = [] # collect coreqs
    requiredCourses = 0 # number of courses required in the group
    coreqGroupCounter = -1

    for currLine in container:
        # get number of courses required for this prereq group
        coursesRequired = checkNumberOfCoursesRequired(currLine.get_text())

        # add to prereq list as necessary
        if coursesRequired != -1: # if an indicator is given
            requiredCourses = coursesRequired # save the number of required corses
            coreqGroupCounter += 1 # increment the group number
            continue
        elif coreqGroupCounter == -1: # if no indicator but its the first line
            requiredCourses = 0
            coreqGroupCounter += 1
            continue

        # if its not a link or no indicator yet (weird use case)
        if coreqGroupCounter == -1 or currLine.name != "a": continue
        # add as a prereq
        name = currLine.get_text().strip().upper()
        if not isStringACourse(name): continue # validation check if string is a course

        splitted = name.split(" ")
        coreqs.append({
            "key": name.replace(" ", "-"),
            "name": name,
            "attributes": {
                "type": "coreq",
                "institution": "UBC",
                "department": splitted[0],
                "courseNum": splitted[1],
                "group": coreqGroupCounter,
                "numRequired": requiredCourses,
            },
            "children": []
        })

    return coreqs

def findCourseDependencies(courseCache, newCourses, dept: str, courseNum: str, extraAttribs: dict = {}):
    # if already cached, don"t repeat the computation
    courseKey = (f"{dept}-{courseNum}").upper()
    if courseKey in courseCache: return courseCache[courseKey]

    # rKey is the key used for redis
    rKey = f"UBC:{COURSE_DATA_TYPE}:{courseKey}"
    courseInfo = None
    isCourseInredis = False

    try:
        # first, search for the course in redis
        existing = getOne("UBC", COURSE_DATA_TYPE, courseKey)
        if existing["data"]: # return if course found in redis
            isCourseInredis = True
            courseInfo = json.loads(existing["data"])
            return courseInfo

        # if the course was not found in redis, we have to scrape its data
        courseInfo = {
            "key": courseKey,
            "name": f"{dept} {courseNum}",
            "attributes": {
                # "type": "prereq/coreq",
                "institution": "UBC",
                "department": dept.upper(),
                "courseNum": courseNum,
                # "group": prereq_group_num
                # "numRequired": prereq_num_required
                "status": "OFFERED",
                **extraAttribs
            },
            "children": [],
        }

        # scrape for course info
        driver.get(generateUbcUrl("COURSES", dept, courseNum))
        soup = BeautifulSoup(driver.page_source, "html.parser")
        content_container = soup.find("div", class_=re.compile("content expand"))

        if not content_container: # means something is wrong with the page
            raise PageError("Page layout unrecognized")

        # check if the course is offered, 
        if checkCourseNotOffered(content_container): # return if course is not offered
            courseInfo["attributes"]["status"] = "NOT_OFFERED"
            print(f"DEBUG (scrape_course): {dept} {courseNum} not offered")
            return courseInfo

        # if offered, get prereq containers and coreq containers
        prereqContainer = content_container.find_all(filterPrereqContainer)
        coreqContainer = content_container.find_all(filterCoreqContainer)

        # get list of prereqs and coreqs, if any
        prereqs = [] if not len(prereqContainer) else getCoursePrereqs(prereqContainer[0]) 
        coreqs = [] if not len(coreqContainer) else getCourseCoreqs(coreqContainer[0]) 

        # recurse here for each prereq
        if len(prereqs):
            for idx, p in enumerate(prereqs):
                prInfo = findCourseDependencies(courseCache, newCourses, p["dept"], p["courseNum"], p["extraAttribs"])
                prereqs[idx] = prInfo
        else:
            print(f"DEBUG (scrape_course): no prereqs found for {dept} {courseNum}")

        # don"t need to recurse for coreqs
        courseInfo["children"] = [*prereqs, *coreqs]

    except Exception as e:
        traceback.print_exc()
        raise

    finally:
        courseCache[courseKey] = courseInfo # save the course in cache
        if not isCourseInredis: newCourses[rKey] = json.dumps(courseInfo) # indicate as new if not already in redis
        return courseInfo

def scrapeCourseInformation(courseKey: str):
    courseCache = {} # memoization for if recursive scraping sees the same node
    newCourses = {} # new courses to save into redis
    mainCourseInfo = {} # the main course being queried

    courseKeySplit = courseKey.split("-")
    dept = courseKeySplit[0]
    courseNum = courseKeySplit[1]

    try:
        # do this initially to test connection
        driver.get(generateUbcUrl("COURSES", dept, courseNum))
        # start finding dependencies
        mainCourseInfo = findCourseDependencies(courseCache, newCourses, dept, courseNum)

    except PageError as e:
        print("ERROR ->>> cannot find page layout. {}".format(e))
        traceback.print_exc()
        raise e

    except Exception as e:
        print("ERROR ->>> could not scrape course page. {}".format(e))
        traceback.print_exc()
        raise

    finally:
        print(mainCourseInfo)
        return mainCourseInfo, newCourses
