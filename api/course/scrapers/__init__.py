# imports all the different scrapers
from .ubc import scrapeCourseInformation as scrapeUbcCourseInformation

courseScrapers = {
    'UBC': scrapeUbcCourseInformation
}