from math import log
from clean import get_professor_course_data


def q1():
    professor_course_data = get_professor_course_data('cleaned.txt')
    course_set = set()
    for prof_name, course_list in professor_course_data.items():
        for course in course_list:
            course_set.add(course.lower())
    return course_set


def q2():
    professor_course_data = get_professor_course_data('cleaned.txt')
    return professor_course_data['Theys']


def q3():
    professor_course_data = get_professor_course_data('cleaned.txt')
    

def weighted_jaccard_distance(string1, weight1, string2, weight2):
    
    pass


def generate_idf(list_of_documents):
    idf_values = {}
    term_frequency = {}
    number_of_docs = len(list_of_documents)
    for document in list_of_documents:
        term_set = set()
        for term in document:
            term_set.add(term.lower())
        for term in term_set:
            if term in term_frequency:
                term_frequency[term] += 1
            else:
                term_frequency[term] = 1

    for term, frequency in term_frequency.items:
        idf_values[term] = log(number_of_docs / frequency)
            
    return idf_values
