from bs4 import BeautifulSoup
from urllib.request import urlopen


def get_abstracts(keywords_to_search: str, output_path: str):
    pubmed_url = 'https://pubmed.ncbi.nlm.nih.gov'
    keywords_to_search = '+'.join(keywords_to_search.split())
    search_url = 'https://pubmed.ncbi.nlm.nih.gov/?term=' + keywords_to_search
    html = urlopen(search_url)
    soup = BeautifulSoup(html, features="html.parser")
    matched_results = soup.find_all('a', class_='docsum-title')
    output_content = ''
    for i, result in enumerate(matched_results):
        print('Processing', i+1, 'out of', len(matched_results), 'URLs...')
        result_url = pubmed_url + result.get('href')
        result_html = urlopen(result_url)
        sub_soup = BeautifulSoup(result_html, features="html.parser")
        title = ' '.join(str(sub_soup.find_all('h1', class_='heading-title')).split()[2:-1])
        abstract = ''
        abstract += sub_soup.find_all('div', class_='abstract-content selected')[0].get_text()
        output_content += title + '\n' + result_url + abstract
        output_content += '----------------------------------------------------------------\n'
    with open(output_path, 'w') as output_file:
        output_file.write(output_content)
        print('Written to ' + output_path)


if __name__ == '__main__':
    get_abstracts('dental implant', 'C:/Users/qiujingye/Desktop/pubmed_abstracts.txt')