import http.client
import json
import termcolor
from Seq1 import *

SERVER = 'localhost:8080'
def make_request(SERVER, url):
    try:
        conn = http.client.HTTPConnection(SERVER)
        print(f"SERVER: {SERVER}")
        conn.request("GET", url)
        print('URL:', SERVER + url)
    except ConnectionRefusedError:
        print("ERROR! Cannot connect to the Server")
        exit()

    r1 = conn.getresponse()
    print(f"Response received: {r1.status} {r1.reason}\n")

    response_normal = r1.read().decode('utf-8')
    response = json.loads(response_normal)
    return response

def get_url(SERVER, dictionary):
    url_list = []
    for i in range(0, len((dictionary['limit']))):
        url = dictionary['endpoint']
        for param in range(0, len(dictionary['connector'])):
            url += dictionary['connector'][param] + dictionary['limit'][i][param]
        url_list.append(url)

    for u in url_list:
        output = make_request(SERVER, str(u + '&json=on'))
        print(output)
        line = '------------------------------------------------------------------------------------------------------'
        print(line)
    return

list_species = {
        'endpoint': '/listSpecies?',
        'connector': ['limit='],
        'limit': [[''],
                  ['a'],
                  ['10000000'],
                  ['0'],
                  ['-1']]}

karyotype = {
        'endpoint': '/karyotype?',
        'connector': ['specie='],
        'limit': [[''],
                  ['1'],
                  ['.'],
                  ['a'],
                  ['human']]}

chromosomeLength = {
        'endpoint': '/chromosomeLength?',
        'connector': ['specie=', '&min_len='],
        'limit': [
            ['', '1'],
            ['a', '1'],
            ['human', 'a'],
            ['human', '1'],
            ['HUMAN', 'x']]}

geneSeq = {
        'endpoint': '/geneSeq?',
        'connector': ['gene='],
        'limit': [[''],
                  ['1'],
                  ['.'],
                  ['a'],
                  ['frat1']]}

geneInfo = {
        'endpoint': '/geneInfo?',
        'connector': ['gene='],
        'limit': [[''],
                  ['1'],
                  ['.'],
                  ['a'],
                  ['frat1']]}

geneCalc = {
        'endpoint': '/geneCalc?',
        'connector': ['gene='],
        'limit': [[''],
                  ['1'],
                  ['.'],
                  ['a'],
                  ['frat1']]}

geneList = {
        'endpoint': '/geneList?',
        'connector': ['chromo=', '&start=', '&end='],
        'limit': [
            ['9', '', '1'],
            ['9', '10', '1'],
            ['9', 'A', '1'],
            ['y', '1', '1000000'],
            ['9', '10', '10000000'],
            ['9', '10000000', '22125500'],
            ['a', '10000000', '22125500']]}


list_dict = [list_species, karyotype, chromosomeLength, geneSeq, geneInfo, geneCalc, geneList]

try:
    # For trying all:
    for i in range(0, len(list_dict)):
        print(get_url(SERVER, list_dict[i]))
    # For trying only one exercise:
    '''print(get_url(SERVER, list_species))'''

    # For trying something specific:
    '''dict_testing = {
    'endpoint' : '/',
    'connector': ['connector1'],
    'limit': [['limit1']]
    }
    print(get_url(SERVER, dict_testing))
    '''

except Exception as e:
    print('exception:', e)

