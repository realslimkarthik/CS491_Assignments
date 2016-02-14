import sys


def get_professor_course_mapping(dirty_professor_course_data):
    clean_professor_course_data = {}
    for row in dirty_professor_course_data:
        professor_full_name, courses = row.split(' - ')
        courses = courses.strip()
        course_list = courses.split('|')
        if professor_full_name.find(','):
            professor_name = professor_full_name.split(',')[0]
        else:
            professor_name = professor_full_name.split()[1]    
        clean_professor_course_data[professor_name] = course_list
    
    return clean_professor_course_data


if __name__ == '__main__':
    dirty_file_name = sys.argv[1]

    with open(dirty_file_name) as dirty_file:
        dirty_data = dirty_file.readlines()

    professor_course_mapping = get_professor_course_mapping(dirty_data)
    print professor_course_mapping
