import sys
import csv
from bs4 import BeautifulSoup

def generate_soup(html_file_name):
    with open(html_file_name) as html_file:
        soup = BeautifulSoup(html_file.read(), 'html.parser')
    return soup


def get_game_number(table_row):
    table_cell = table_row.find_all('td')[0]
    game_number = table_cell.find_all('span')[1].find('a').text
    return game_number


def get_game_year(table_row):
    table_cell = table_row.find_all('td')[1]
    game_date = table_cell.find_all('span')[1].text
    game_year = game_date.split(',')[1].strip()
    return game_year


def get_winning_team(table_row):
    table_cell = table_row.find_all('td')[2]
    winning_team = table_cell.find_all('span')[0].text.strip(' !')
    return winning_team


def get_score(table_row):
    table_cell = table_row.find_all('td')[3]
    score = table_cell.find_all('span')[1].text
    return score


def get_losing_team(table_row):
    table_cell = table_row.find_all('td')[4]
    losing_team = table_cell.find_all('span')[0].text.strip(' !')
    return losing_team


def get_venue(table_row):
    table_cell = table_row.find_all('td')[5]
    venue = table_cell.find_all('span')[0].text.strip(' !')
    return venue


def extract_data_from_table(table):
    data = []
    for row in table.find_all('tr')[1:-2]:
        row_data = {}
        row_data['Game number'] = get_game_number(row)
        row_data['year'] = get_game_year(row)
        row_data['winning team'] = get_winning_team(row)
        row_data['score'] = get_score(row)
        row_data['losing team'] = get_losing_team(row)
        row_data['venue'] = get_venue(row)
        data.append(row_data)
    return data


def write_to_csv(output_data, output_file):
    field_names = ['Game number', 'year', 'winning team', 'score', 'losing team', 'venue']
    with open(output_file, 'w') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=field_names)
        writer.writeheader()
        for row in output_data:
            writer.writerow(row)


if __name__ == '__main__':
    html_file_name = sys.argv[1]
    soup = generate_soup(html_file_name)
    table_data = soup.find_all('table')[1]
    superbowl_data = extract_data_from_table(table_data)
    write_to_csv(superbowl_data, 'result.csv')