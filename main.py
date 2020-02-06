import os
import re
import nltk
# trying to import few modules
# if not found, then they are installed using pip

try:
    from termcolor import colored
except:
    os.system('pip3 install termcolor')
try:
    from nltk.corpus import stopwords
except:
    os.system('pip3 install nltk')

try:
    import requests
except:
    os.system('pip3 install requests')

try:
    from bs4 import BeautifulSoup
except:
    os.system('pip3 install bs4')

try:
    from googlesearch import search
except:
    os.system('pip3 install google')


def scrap_stackoverflow_question(url):
    # search for question section for a particular id of a tag
    page = requests.get(url, headers=headers, timeout=2)
    soup = BeautifulSoup(page.content, 'html.parser')
    question = soup.find(
        attrs={'class': 'postcell post-layout--right'}).get_text(strip=True)
    question = question.strip()
    return question


def scrap_stackoverflow(url):
    # search for answer section for a particular id of a tag
    page = requests.get(url, headers=headers, timeout=2)
    soup = BeautifulSoup(page.content, 'html.parser')
    upvote = soup.find(
        attrs={'class': 'votecell post-layout--left'}).get_text()
    upvote = str(upvote).strip()
    upvote = upvote.replace('\n', ' ')
    up = upvote.split(' ')
    answer = soup.find(
        attrs={'class': 'answercell post-layout--right'}).get_text()

    return up[0], answer.rstrip('\n')

filename = input('Enter the filename that you want to compile: ')
if not re.search(r'(.*)\.py', filename):
    print('File not found!!\nTry giving the entire path of the file.')
    exit(0)
os.system('python3 ' + filename + ' 2> ./FileResults/error_file')
fileHandle = open('./FileResults/error_file', "r")
lineList = fileHandle.readlines()
fileHandle.close()
keyword = ''
if len(lineList) == 0:
    exit(0)
detailed_query = lineList[-1]
query = detailed_query[:detailed_query.index(':')] + ' in python 3'
# to be given by the user
headers = {
    "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:70.0) Gecko/20100101 Firefox/70.0"}
q_answers = []
s_o_answers = []
for url in search(query, tld='com', num=10, stop=6, pause=2):
    if re.search(r'(.*)https://stackoverflow.com/(.*)', url):
        # all the answers are stored in answers list
        q_answers.append(scrap_stackoverflow_question(url))
        s_o_answers.append(scrap_stackoverflow(url))

i = 0

for u, a in s_o_answers:
    # calculating on what topic the answer is based on
    tokens = [t for t in a.split()]
    clean_tokens = tokens[:]
    sr = stopwords.words('english')
    for token in tokens:
        if token in stopwords.words('english'):
            clean_tokens.remove(token)
    freq = nltk.FreqDist(clean_tokens)
    keyword = tuple(freq.most_common(1))
    print(
        colored(f'We found a question with most occurances of word: {keyword[0][0]}', 'yellow'))
    q_answers[i] = q_answers[i][:q_answers[i].index('share')]
    print(colored('Question: \n', 'red', attrs=[
          'underline']), colored(q_answers[i], 'magenta'))
    i += 1
    a = a[:a.index('share')]
    print(colored(u+': upvotes', 'blue'))
    print(colored('Answer: \n', 'red', attrs=[
          'underline']), colored(a, 'cyan'))

    if i == len(s_o_answers)-1 or input('\nShall I display another result:(y/n) ') == 'n':
        print('We hope you will solve the error')
        try:
            exit(0)
        except:
            quit()
