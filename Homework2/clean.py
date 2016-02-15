import sys


def get_professor_course_mapping(dirty_professor_course_data):
    clean_professor_course_data = {}
    for row in dirty_professor_course_data:
        professor_full_name, courses = row.split(' - ')
        professor_full_name = professor_full_name.strip()
        courses = courses.strip()
        course_list = sorted(courses.split('|'))
        if professor_full_name.find(',') != -1:
            professor_name = professor_full_name.split(',')[0]
        else:
            if len(professor_full_name.split()) == 2:
                professor_name = professor_full_name.split()[1]
            elif len(professor_full_name.split()) == 1:
                professor_name = professor_full_name

        if professor_name not in clean_professor_course_data:
            clean_professor_course_data[professor_name] = course_list
        else:
            clean_professor_course_data[professor_name].extend(course_list)
    
    return clean_professor_course_data


def get_unique_course_names(professor_course_mapping):
    course_set = set()
    for course_list in professor_course_mapping.values():
        course_set = course_set.union(set(course_list))
    return course_set


def jaccard_distance(string1, string2):
    pass


def write_to_file(clean_professor_course_data, output_file_name):
    output_lines = []
    for professor_name, course_list in clean_professor_course_data.items():
        output_line = professor_name + ' - ' + '|'.join(course_list) + '\n'
        output_lines.append(output_line)

    with open(output_file_name, 'w') as output_file:
        output_file.writelines(output_lines)


if __name__ == '__main__':
    dirty_file_name = sys.argv[1]

    with open(dirty_file_name) as dirty_file:
        dirty_data = dirty_file.readlines()

    professor_course_mapping = get_professor_course_mapping(dirty_data)
    dirty_course_list = get_unique_course_names(professor_course_mapping)
    # print(dirty_course_list)
    write_to_file(professor_course_mapping, 'cleaned.txt')
    
