from bs4 import BeautifulSoup


def generate_soup(html_file_name):
    with open(html_file_name) as html_file:
        soup = BeautifulSoup(html_file.read(), 'html.parser')
    return soup



if __name__ == '__main__':
    soup = generate_soup('superbowl.html')
    