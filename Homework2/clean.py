import sys


def get_professor_course_mapping(dirty_professor_course_data):
    clean_professor_course_data = {}
    for row in dirty_professor_course_data:
        professor_full_name, courses = row.split(' - ')
        professor_full_name = professor_full_name.strip()
        courses = courses.strip()
        course_list = courses.split('|')
        if professor_full_name.find(',') != -1:
            professor_name = professor_full_name.split(',')[0]
        elif professor_full_name.find('.') != -1:
            professor_name = professor_full_name.split('.')[1]
        else:
            if len(professor_full_name.split()) == 2:
                professor_name = professor_full_name.split()[1]
            elif len(professor_full_name.split()) == 1:
                professor_name = professor_full_name

        professor_name = professor_name.strip().title()
        if professor_name not in clean_professor_course_data:
            clean_professor_course_data[professor_name] = course_list
        else:
            clean_professor_course_data[professor_name].extend(course_list)
    
    return clean_professor_course_data


def sort_courses_alphabetically(professor_course_data):
    """
        This function sorts the list of courses alphabetically for each professor.
    """
    for professor_name in professor_course_data.keys():
        course_list = professor_course_data[professor_name]
        professor_course_data[professor_name] = sorted(course_list, key=str.lower)
    return professor_course_data


def get_unique_course_names(professor_course_mapping):
    course_set = set()
    for course_list in professor_course_mapping.values():
        course_set = course_set.union(set(course_list))
    return course_set


def write_to_file(clean_professor_course_data, output_file_name):
    output_lines = []
    prof_names = sorted(clean_professor_course_data.keys())
    for professor_name in prof_names:
        course_list = clean_professor_course_data[professor_name]
        output_line = output_line = professor_name + ' - ' + '|'.join(course_list) + '\n'
        output_lines.append(output_line)

    with open(output_file_name, 'w') as output_file:
        output_file.writelines(output_lines)


def get_professor_course_data(input_file):
    with open(input_file) as class_data_file:
        class_data = class_data_file.readlines()

    professor_course_mapping = {}
    for row in class_data:
        prof_name, courses = row.split(' - ')
        prof_name = prof_name.strip()
        courses = courses.strip()
        course_list = courses.split('|')
        professor_course_mapping[prof_name] = course_list
    return professor_course_mapping


if __name__ == '__main__':
    dirty_file_name = sys.argv[1]

    with open(dirty_file_name) as dirty_file:
        dirty_data = dirty_file.readlines()

    professor_course_mapping = get_professor_course_mapping(dirty_data)
    professor_course_mapping = sort_courses_alphabetically(professor_course_mapping)
    dirty_course_list = get_unique_course_names(professor_course_mapping)
    # print(dirty_course_list)
    write_to_file(professor_course_mapping, 'cleaned.txt')
    
