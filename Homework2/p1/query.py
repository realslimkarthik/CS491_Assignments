from math import log


def get_professor_course_data(input_data):
    if isinstance(input_data, str) and input_data.find('\n') == -1:
        with open(input_data) as class_data_file:
            class_data = class_data_file.readlines()
    elif input_data.find('\n') != -1:
        class_data = input_data.splitlines()
    else:
        print('''Invalid Input. Please input a valid file name of the correct format 
            or data of type str that matches the required format''')
        return -1

    professor_course_mapping = {}
    for row in class_data:
        prof_name, courses = row.split(' - ')
        prof_name = prof_name.strip()
        courses = courses.strip()
        course_list = courses.split('|')
        professor_course_mapping[prof_name] = course_list
    return professor_course_mapping


def q1(cleaned_txt):
    professor_course_data = get_professor_course_data(cleaned_txt)
    course_set = set()
    for prof_name, course_list in professor_course_data.items():
        for course in course_list:
            course_set.add(course.lower())
    print(len(course_set))
    return list(course_set)


def q2(cleaned_txt):
    professor_course_data = get_professor_course_data(cleaned_txt)

    course_list_string = ''
    for course in sorted(professor_course_data['Theys']):
        course_list_string += course + ', '
    course_list_string.strip(',')
    print(course_list_string)
    return professor_course_data['Theys']


def q3(cleaned_txt):
    professor_course_data = get_professor_course_data(cleaned_txt)
    idf = generate_idf(professor_course_data.values())
    prof_names = professor_course_data.keys()
    prof_comparison = []
    for prof1 in prof_names:
        if len(professor_course_data[prof1]) >= 5:
            for prof2 in prof_names:
                if prof2 != prof1 and len(professor_course_data[prof2]) >= 5:
                    prof_data = {}
                    prof1_courses = get_words_from_courses(professor_course_data[prof1])
                    prof2_courses = get_words_from_courses(professor_course_data[prof2])
                    jaccard_distance_for_courses = weighted_jaccard_distance(prof1_courses, prof2_courses, idf)
                    prof_data['prof1'] = prof1
                    prof_data['prof2'] = prof2
                    prof_data['jaccard_distance'] = jaccard_distance_for_courses['jaccard_distance']
                    prof_comparison.append(prof_data)
    sorted_prof_comparison = sorted([(row['jaccard_distance'], row['prof1'], row['prof2']) for row in prof_comparison])
    print(sorted_prof_comparison[0][1], sorted_prof_comparison[0][2])
    return sorted_prof_comparison[0]


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

