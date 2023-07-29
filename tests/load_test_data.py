"""Get course url response and dump to a pickle file for testing."""
from pickle import dump

from bcitflex.modules.extract_course_data import collect_response

if __name__ == "__main__":
    base_url = "https://www.bcit.ca"
    course_url = r"/courses/business-analysis-and-systems-design-comp-2831/"
    url = base_url + course_url

    # get response
    response = collect_response(url)
    dump(response, open("./test_data/course_response.pkl", "wb"))
