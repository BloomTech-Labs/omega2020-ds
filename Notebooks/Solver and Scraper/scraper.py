##################################################
## Omega2020 Flask App
##################################################
## MIT License
##################################################
## Authors: Leydy Johana Luna
## References:  Web Scraping with Python: Collecting Data from the Modern Web. 
##.             Book by Ryan Mitchell
## Version: 1.0.0
##################################################


from bs4 import BeautifulSoup
import urllib3
import requests
import datetime
import numpy as np
import pandas as pd
from urllib.request import urlopen
from urllib.error import HTTPError
from urllib.error import URLError
from tqdm import tqdm
import pandas as pd
import numpy as np
import copy
from solver import *
from ai import *

"""
Extract all the HTML code from the web site
in which the daily Sudoku is posted and create a 
CSV file with all the data scraped.
"""


def total_sudoku():
    """
    Extract from the most recent day the total number of puzzles
    posted in the web site.
    """
    r = requests.get("http://www.sudoku.org.uk/Daily.asp")
    soup = BeautifulSoup(r.content, 'html5lib')
    return(soup.find('span', attrs={
                                    'class': 'newtitle'
                                    }).get_text().split(",")[0].replace("#", ""))


def list_dates(total):
    '''
    check if the website is working or not(for each day)
    and save this link in a list.
    Input: total of puzzles posted
    Output: URL list with the websites that are running correctly
    '''
    dates = []
    dates_error = []
    urls = []
    for i in tqdm(range(2, total)):
        d = datetime.date.today() - datetime.timedelta(days=i)
        d_format = (str(d.day) + '/' + str(d.month) + '/' + str(d.year))
        URL = "http://www.sudoku.org.uk/DailySudoku.asp?solution=please&day=" + d_format
        try:
            urlopen(URL)
        except HTTPError as e:
            pass

        except URLError as e:
            pass

        else:
            urls.append(URL)
    return urls


def get_html(url):
    '''
    Extract all the HTML code.
    Input: url list
    Output: html code
    '''
    r = requests.get(url)
    return BeautifulSoup(r.content, 'html.parser')


def consolidate(urls):
    '''
    Extract all the information
    Input: list of urls
    Output: urls, difficulty levels, number of people
    that solved the puzzle, average time solving the puzzle
    in minutes, initial Sudoku and its solution.
    '''
    solution, sudoku, level, people, av_time, unit = ([] for i in range(6))

    for url in tqdm(urls):
        a, b = ([] for i in range(2))
        soup = get_html(url)
        for link in soup.find_all(
                                'td',
                                attrs={'class': ['InnerTDone2',
                                                 'InnerTDone']}
                                ):
            if link.attrs['class'] == ['InnerTDone2']:
                b.append(link.text)
            else:
                b.append('.')
            a.append(link.text)
        sudoku.append(''.join(b))
        solution.append(''.join(a))
        p = list(list(soup.table.td)[2])
        level.append(str(p[1].get_text()).split(", ")[1].split()[0])
        people.append(str(p[3]).split()[0])
        av_time.append(str(p[3]).split()[6])
        unit.append(str(p[3]).split()[7])
    return(urls, level, people, av_time, unit, sudoku, solution)


def scraper():
    """
    Scrape the data automatically
    """
    print('Extracting all the dates when the website has posted a puzzle and its solution')
    urls = list_dates(pd.to_numeric(total_sudoku()))
    index = urls.index([x for x in urls if '=7/3/2006' in x][0])
    new_urls = urls[:index]
    print('Extracting urls, level, people, av_time, unit, sudoku and solution ')
    urls, level, people, av_time, unit, sudoku, solution = consolidate(new_urls)
    df = pd.DataFrame(list(
                    zip(urls, level, people, av_time, unit, sudoku, solution)),
                   columns=['URL', 'Level', 'People',
                            'Average-Time', 'Unit-Time',
                            'Sudoku', 'Solution'])
    df['Id'] = df.index
    df = df[['Id', 'Level', 'Sudoku',
             'Solution', 'People', 'Average-Time',
             'Unit-Time', 'URL']]
    techniques= ['single_position', 'single_candidate', 'naked_twins','naked_triple']
    for technique in techniques:
        df[technique] = df['Sudoku'].apply(lambda x: solve_technique(x, technique)[0])  
    df.to_csv('../Omega2020/data/dataset.csv')
#     df = pd.read_csv('../Omega2020/data/dataset.csv')
    


if __name__ == '__main__':
    scraper()
