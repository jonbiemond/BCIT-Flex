"""Get course url response and dump to a pickle file for testing."""
from pickle import dump

from bcitflex.modules.extract_course_data import collect_response

if __name__ == "__main__":
    base_url = "https://www.bcit.ca"
    course_url = "/courses/business-analysis-and-systems-design-comp-2831/"
    course_list_url = "/wp-json/bcit/ptscc/v1/list-active-urls"

    # get course response
    response = collect_response(base_url + course_url)
    dump(response, open("./test_data/course_response.pkl", "wb"))

    # get course list response
    response = collect_response(base_url + course_list_url)
    dump(response, open("./test_data/course_list_response.pkl", "wb"))
