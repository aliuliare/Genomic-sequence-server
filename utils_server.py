import http.server
import jinja2 as j
from pathlib import Path
import http.client
import json

def read_html_file(filename):
    contents = Path("html/" + filename).read_text()
    contents = j.Template(contents)
    return contents

def server_connection(parameter):
    server = 'rest.ensembl.org'
    endpoint = '/' + str(parameter) + '?'
    parameters = 'content-type=application/json'
    url = str(endpoint) + str(parameters)

    print(f"\nSERVER: {server}")
    print('URL: ' + server + url)

    conn = http.client.HTTPConnection(server)
    try:
        conn.request("GET", url)
    except ConnectionRefusedError:
        print("ERROR! Cannot connect to the Server")
        exit()
    r1 = conn.getresponse()
    print(f"Response received: {r1.status} {r1.reason}\n")
    if r1.reason == 'Not Found':
        response = 'error'
    else:
        response = json.loads(r1.read().decode("utf-8"))
    return response

def get_gene(msg):
    try:
        lookup_response = server_connection('xrefs/symbol/' + 'homo_sapiens/' + str(msg))
        if len(lookup_response) >= 1:
            id_got = lookup_response[0]['id']
            response_server = server_connection('sequence/id/' + id_got)
        else:
            id_got = 'empty'
            response_server = 'empty'
    except UnboundLocalError:
        response_server = 'error'
        id_got = 'error'
    except:
        response_server = 'error'
        id_got = 'error'
    return id_got, response_server

def server_connection_exam(parameter):
    server = 'rest.ensembl.org'
    endpoint = '/' + str(parameter)
    parameters = 'content-type=application/json'
    url = str(endpoint) + str(parameters)

    print(f"\nSERVER: {server}")
    print('URL: ' + server + url)

    conn = http.client.HTTPConnection(server)
    try:
        conn.request("GET", url)
    except ConnectionRefusedError:
        print("ERROR! Cannot connect to the Server")
        exit()
    r1 = conn.getresponse()
    print(f"Response received: {r1.status} {r1.reason}\n")
    if r1.reason == 'Not Found':
        response = 'error'
    else:
        response = json.loads(r1.read().decode("utf-8"))
    return response
def get_gene_exam(specie, id):
    try:
        response_server = server_connection_exam('sequence/id/' + id + '?' + 'species=' + str(specie) + ';')
    except UnboundLocalError:
        response_server = 'error'
    except:
        response_server = 'error'
    return response_server

def get_data_gene(id_got):
    try:
        lookup_response = server_connection('lookup/id/' + str(id_got))
        if len(lookup_response) >= 1:
            '''response = server_connection('sequence/id/' + str(id_got))'''
    except UnboundLocalError:
        lookup_response = 'error'
    return lookup_response

def get_chromosome(chromosome, start, end):
    server = 'rest.ensembl.org'
    endpoint = '/' + 'phenotype/region/' + 'homo_sapiens/' + chromosome + ':' + start + '-' + end
    parameters = '?content-type=application/json;feature_type=Variation'

    url = str(endpoint) + str(parameters)

    print(f"\nSERVER: {server}")
    print('URL: ' + server + url)

    conn = http.client.HTTPConnection(server)
    try:
        conn.request("GET", url)
    except ConnectionRefusedError:
        print("ERROR! Cannot connect to the Server")
        exit()
    try:
        r1 = conn.getresponse()
        print(f"Response received: {r1.status} {r1.reason}\n")
        response = json.loads(r1.read().decode("utf-8"))

    except UnboundLocalError:
        response = 'error'
    return response
