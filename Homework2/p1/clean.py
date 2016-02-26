import sys
import re
import roman
import enchant
from Levenshtein import distance

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
            professor_name = professor_full_name.split('.')[-1]
            if len(professor_name.split()) > 1:
                professor_name = professor_name.split()[-1]
        else:
            if len(professor_full_name.split()) == 1:
                professor_name = professor_full_name
            elif len(professor_full_name.split()) > 1:
                professor_name = professor_full_name.split()[-1]

        professor_name = professor_name.strip().title()
        if professor_name not in clean_professor_course_data:
            clean_professor_course_data[professor_name] = course_list
        else:
            clean_professor_course_data[professor_name].extend(course_list)
    
    return clean_professor_course_data


def sort_courses_alphabetically(professor_course_data):
    for professor_name in professor_course_data.keys():
        course_list = professor_course_data[professor_name]
        professor_course_data[professor_name] = sorted(course_list, key=str.lower)
    return professor_course_data


def clean_special_symbols(list_of_strings):
    cleaned_list_of_strings = []
    roman_numeral_regex = re.compile(r'\b(i+)\b', re.IGNORECASE)
    roman_numeral_regex = re.compile(r'\b(ix|iv|v|v?i{1,3})\b')
    hyphen_colon_regex = re.compile(r'-|:')
    for string in list_of_strings:
        cleaned_string = string.lower().replace(' & ', ' and ')

        match = roman_numeral_regex.search(cleaned_string)
        if match:
            number = roman.fromRoman(match.group(0).upper())
            cleaned_string = roman_numeral_regex.sub(' ' + str(number), cleaned_string)
        cleaned_string = hyphen_colon_regex.sub(' ', cleaned_string)
        cleaned_string = cleaned_string.replace(',', '')
        cleaned_string = cleaned_string.replace('?', '.')

        cleaned_list_of_strings.append(cleaned_string)
    return cleaned_list_of_strings


def clean_abbreviations(list_of_strings):
    cleaned_list_of_strings = []
    intro_regex = re.compile(r'\b(intro)(\.|\b)')
    n_dimensions_regex = re.compile(r'\b((\d+)d)\b', re.IGNORECASE)
    for string in list_of_strings:
        cleaned_string = intro_regex.sub('introduction ', string.lower())
        match = n_dimensions_regex.search(cleaned_string)
        if match:
            n = str(match.group(0)[:-1])
            cleaned_string = n_dimensions_regex.sub(n + ' dimensional ', cleaned_string)

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


def edit_distance_for_equal_length_strings(string1, string2):
    if len(string1) != len(string2):
        return -1

    string_length = len(string1)
    edit_distances = [[0 for j in range(string_length)] for i in range(string_length)]

    for i in range(string_length):
        for j in range(string_length):
            if i == 0:
                edit_distances[i][j] = j
            elif j == 0:
                edit_distances[i][j] = i
            elif string1[i-1] == string2[j-1]:
                edit_distances[i][j] = edit_distances[i-1][j-1]
            else:
                edit_distances[i][j] = 1 + min(edit_distances[i-1][j], edit_distances[i][j-1], edit_distances[i-1][j-1])
    return edit_distances[string_length-1][string_length-1]


def fix_misspelt_course_names(professor_course_data):
    word_dict = enchant.Dict('en')
    # word_dict = enchant.Dict('en_US')
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
                    # suggestions = list(filter(lambda x: distance(term, x) == 1, suggestions))
                    suggestions = list(filter(lambda x: edit_distance_for_equal_length_strings(term, x) == 1, suggestions))
                    if len(suggestions) > 0:
                        print(suggestions)
                        print(term)
                        print(prof_name)
                        new_term = suggestions[0]
                        # sys.exit(1)
                    else:
                        word_dict.add(term)
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


if __name__ == '__main__':
    dirty_file_name = sys.argv[1]
    with open(dirty_file_name) as dirty_file:
        dirty_data = dirty_file.readlines()

    professor_course_mapping = get_professor_course_mapping(dirty_data)
    professor_course_mapping = sort_courses_alphabetically(professor_course_mapping)
    professor_course_mapping = clean_course_titles(professor_course_mapping)
    professor_course_mapping = fix_misspelt_course_names(professor_course_mapping)
    professor_course_mapping = title_case_course_names(professor_course_mapping)
    write_to_file(professor_course_mapping, 'cleaned.txt')
    
