import sys
import enchant
from Levenshtein import distance
import re

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


def clean_special_symbols(list_of_strings):
    cleaned_list_of_strings = []
    ampersand_regex = re.compile(r'\b(\&)\b')
    roman_numeral_regex = re.compile(r'\b(i+)\b', re.IGNORECASE)
    hyphen_colon_regex = re.compile(r'-|:')
    for string in list_of_strings:
        # cleaned_string = ampersand_regex.sub(' and ', string.lower())
        cleaned_string = string.lower().replace(' & ', ' and ')

        match = roman_numeral_regex.search(cleaned_string)
        if match:
            number = len(match.group(0))
            cleaned_string = roman_numeral_regex.sub(' ' + str(number), cleaned_string)
        cleaned_string = hyphen_colon_regex.sub(' ', cleaned_string)
        cleaned_string = cleaned_string.replace(',', '')
        cleaned_string = cleaned_string.replace('?', '.')

        cleaned_list_of_strings.append(cleaned_string)
    return cleaned_list_of_strings


def clean_abbreviations(list_of_strings):
    cleaned_list_of_strings = []
    intro_regex = re.compile(r'\b(intro)(\.|\b)')
    three_dimensions_regex = re.compile(r'\b(3d)\b', re.IGNORECASE)
    for string in list_of_strings:
        cleaned_string = intro_regex.sub('introduction ', string.lower())
        cleaned_string = three_dimensions_regex.sub('3 dimensional ', cleaned_string)

        cleaned_list_of_strings.append(cleaned_string)
    return cleaned_list_of_strings


def clean_course_titles(professor_course_data):
    for prof_name in professor_course_data.keys():
        course_list = professor_course_data[prof_name]
        cleaned_course_list = clean_special_symbols(course_list)
        cleaned_course_list = clean_abbreviations(cleaned_course_list)
        professor_course_data[prof_name] = cleaned_course_list
    return professor_course_data


def title_case_course_names(professor_course_data):
    for prof_name in professor_course_data:
        cleaned_course_list = []
        for course in professor_course_data[prof_name]:
            cleaned_course_list.append(course.title())
        professor_course_data[prof_name] = cleaned_course_list
    return professor_course_data


def fix_misspelt_course_names(professor_course_data):
    word_dict = enchant.Dict('en_US')
    for prof_name in professor_course_data.keys():
        new_course_list = []
        for course in professor_course_data[prof_name]:
            term_list = course.split()
            new_term_list = []
            for term in term_list:
                new_term = term
                if not word_dict.check(term):
                    suggestions = word_dict.suggest(term)
                    suggestions = filter(lambda x: len(x) == len(term), suggestions)
                    suggestions = list(filter(lambda x: distance(term, x) == 1, suggestions))
                    if len(suggestions) > 0:
                        new_term = suggestions[0]
                new_term_list.append(new_term)
            new_course_list.append(' '.join(new_term_list))
        professor_course_data[prof_name] = new_course_list
    return professor_course_data


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
    professor_course_mapping = clean_course_titles(professor_course_mapping)
    professor_course_mapping = title_case_course_names(professor_course_mapping)
    professor_course_mapping = fix_misspelt_course_names(professor_course_mapping)
    # dirty_course_list = get_unique_course_names(professor_course_mapping)
    # print(dirty_course_list)
    write_to_file(professor_course_mapping, 'cleaned.txt')
    
