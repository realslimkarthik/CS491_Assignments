from math import log
from clean import get_professor_course_data


def q1(cleaned_txt):
    professor_course_data = get_professor_course_data(cleaned_txt.splitlines())
    course_set = set()
    for prof_name, course_list in professor_course_data.items():
        for course in course_list:
            course_set.add(course.lower())
    for course in course_set:
        print(course)


def q2(cleaned_txt):
    professor_course_data = get_professor_course_data(cleaned_txt.splitlines())
    print(professor_course_data['Theys'])


def q3(cleaned_txt):
    # professor_course_data = get_professor_course_data(cleaned_txt.splitlines())
    professor_course_data = get_professor_course_data('cleaned.txt')
    idf = generate_idf(professor_course_data.values())
    prof_names = professor_course_data.keys()
    prof_comparison = []
    for prof1 in prof_names:
        for prof2 in prof_names:
            if prof2 != prof1:
                prof_data = {}
                prof1_courses = get_words_from_courses(professor_course_data[prof1])
                prof2_courses = get_words_from_courses(professor_course_data[prof2])
                jaccard_distance_for_courses = weighted_jaccard_distance(prof1_courses, prof2_courses, idf)
                prof_data['prof1'] = prof1
                prof_data['prof2'] = prof2
                prof_data['jaccard_distance'] = jaccard_distance_for_courses['jaccard_distance']
                prof_comparison.append(prof_data)
    sorted_prof_comparison = sorted([(row['jaccard_distance'], row['prof1'], row['prof2']) for row in prof_comparison])
    print(sorted_prof_comparison[0])


def get_words_from_courses(course_list):
    unique_words = set()
    for course in course_list:
        for word in course.split():
            unique_words.add(word.lower())
    return unique_words


def weighted_jaccard_distance(string1, string2, word_weights):
    all_words = string1.union(string2)
    common_words = string1.intersection(string2)
    unique_words = all_words - common_words
    
    total_weight = 0
    for word in all_words:
        total_weight += word_weights[word.lower()]
    
    unique_weight = 0
    for word in unique_words:
        unique_weight += word_weights[word.lower()]

    jaccard_distance = unique_weight / total_weight
    return {'string1': string1, 'string2': string2, 'jaccard_distance': jaccard_distance}



def generate_idf(list_of_documents):
    idf_values = {}
    term_frequency = {}
    number_of_docs = len(list_of_documents)
    for document in list_of_documents:
        term_set = set()
        for text in document:
            for term in text.split():
                term_set.add(term.lower())
        for term in term_set:
            if term in term_frequency:
                term_frequency[term] += 1
            else:
                term_frequency[term] = 1

    for term, frequency in term_frequency.items():
        idf_values[term] = log(number_of_docs / frequency)
            
    return idf_values


if __name__ == '__main__':
    with open('cleaned.txt') as clean_file:
        clean_data = clean_file.read()
    q3(clean_data)
