import http.server
import socketserver
import termcolor
from urllib.parse import parse_qs, urlparse
from pathlib import Path
import http.client
import json
from Seq1 import *
import utils_server as us

PORT = 8080
socketserver.TCPServer.allow_reuse_address = True

json_no_input = {"error": 'Please, insert information'}
class TestHandler(http.server.BaseHTTPRequestHandler):

    def do_GET(self):
        termcolor.cprint(self.requestline, 'green')
        url_path = urlparse(self.path)
        path = url_path.path
        arguments = parse_qs(url_path.query)
        self.send_response(200)
        if path == '/favicon.ico':
            contents = ''
        else:
            #  #######################   MAIN MENU   ##################################################################
            if path == '/':
                contents = Path('html/0main-menu.html').read_text()
            #  EXAM CHANGE ------------------------------------------------------------------------
            elif path == "/sequence":
                if 'specie' in arguments and 'id' in arguments:
                    msg_specie = arguments['specie'][0].strip().replace(' ', '_')
                    msg_id = arguments['id'][0].replace(' ', '_')
                    response = us.get_gene_exam(msg_specie, msg_id)
                    if 'error' in response:
                        json_dict = {"error": 'Could not find any data for the value inserted.'}
                        contents = us.read_html_file("specific_error.html").render(context=json_dict)
                    else:
                        try:
                            seq = str(Seq(response['seq']))
                            length = len(str(Seq(response['seq'])).replace(' ','').replace('\n', ''))
                            base_type = 'odd'
                            if 'even' in arguments:
                                if length % 2:
                                    base_type = 'Its even'
                                else:
                                    base_type = 'Its not even'
                            else:
                                if length % 2:
                                    base_type = 'Its not odd'
                                else:
                                    base_type = 'Its odd'
                            json_dict = {"id_given": msg_id, 'specie': msg_specie, "sequence": seq,
                                         'length': length, 'type' : base_type}
                            contents = us.read_html_file("exam.html").render(context=json_dict)
                        except TypeError:
                            json_dict = {"error": 'Could not find any data for the value inserted.'}
                            contents = us.read_html_file("specific_error.html").render(context=json_dict)
                else:
                    json_dict = json_no_input
                    contents = us.read_html_file("specific_error.html").render(context=json_dict)




            #  ####################### 1 ALL SPECIES   ################################################################
            elif path == "/listSpecies":
                response = us.server_connection('info/species')
                if 'limit' in arguments:
                    try:
                        msg = int(str(arguments['limit'][0]).strip().replace(' ', '_'))
                        if 0 <= msg <= len(response['species']):
                            pass
                        else:
                            msg = len(response['species'])
                        list_response = [response['species'][i]['display_name'] for i in range(msg)]
                        json_dict = {"total_species": len(response['species']), "limit": msg, "list_species": list_response}
                        contents = us.read_html_file("1species.html").render(context=json_dict)
                    except ValueError:
                        json_dict = {"error": 'The limit should be a number. Please, insert a number'}
                        contents = us.read_html_file("specific_error.html").render(context=json_dict)
                else:
                    list_response = [response['species'][i]['display_name'] for i in range(len(response['species']))]
                    json_dict = {
                            "total_species": len(response['species']),
                            "limit": len(response['species']),
                            "list_species": list_response
                        }
                    contents = us.read_html_file("1species.html").render(context=json_dict)
            #  ####################### 2 CHROMOSOME NAMES   ##########################################################
            elif path == "/karyotype":
                if 'specie' in arguments:
                    try:
                        msg = arguments['specie'][0].strip().replace(' ', '_')
                        response = us.server_connection('info/assembly/' + str(msg))
                        if 'error' in response:
                            json_dict = {"error": 'The specie is not in the database.'}
                            contents = us.read_html_file("specific_error.html").render(context=json_dict)
                        elif 'empty' in response:
                            json_dict = {"error": 'The source is empty when requested to Ensembl.'}
                            contents = us.read_html_file("specific_error.html").render(context=json_dict)
                        else:
                            if not response['karyotype']:
                                response['karyotype'] = ['Sorry, the chromosomes are not available', '']
                            json_dict = {"list_chromosomes": response['karyotype']}
                            contents = us.read_html_file("2karyotype.html").render(context=json_dict)
                    except TypeError:
                        json_dict = {"error": 'There was an error.'}
                        contents = us.read_html_file("specific_error.html").render(context=json_dict)
                else:
                    json_dict = json_no_input
                    contents = us.read_html_file("specific_error.html").render(context=json_dict)
            #  ####################### 3 CHROMOSOME LENGTH   ##########################################################
            elif path == '/chromosomeLength':
                if 'specie' in arguments and 'min_len' in arguments:
                    try:
                        msg_species = str(arguments['specie'][0]).strip().replace(' ', '_')
                        msg_chromosome = str(arguments['min_len'][0]).upper().strip().replace(' ', '_')
                        response = us.server_connection('info/assembly/' + msg_species)
                        if 'error' in response:
                            json_dict = {"error": 'Could not find any data for the value inserted.'}
                            contents = us.read_html_file("specific_error.html").render(context=json_dict)
                        else:
                            length = 'uwu'
                            for i in response['top_level_region']:
                                if msg_chromosome == i['name']:
                                    length = i['length']
                            if length == 'uwu':
                                json_dict = {"error": 'The chromosome inserted is not correct.'}
                                contents = us.read_html_file("specific_error.html").render(context=json_dict)
                            else:
                                json_dict = {"len_chromosomes": length}
                                contents = us.read_html_file("3chromosome.html").render(context=json_dict)
                    except KeyError:
                        json_dict = {"error": 'Could not find any data for the value inserted.'}
                        contents = us.read_html_file("specific_error.html").render(context=json_dict)
                else:
                    json_dict = json_no_input
                    contents = us.read_html_file("specific_error.html").render(context=json_dict)
            #  #######################  4 SEQUENCE FROM GENE NAME   ###################################################
            elif path == '/geneSeq':
                if 'gene' in arguments:
                    msg = arguments['gene'][0].strip().replace(' ', '_')
                    if msg.startswith(' '):
                        json_dict = {"error": 'The character " " (space) is not recognised.'}
                        contents = us.read_html_file("specific_error.html").render(context=json_dict)
                    else:
                        id_gotten, response = us.get_gene(msg)
                        if 'error' in response:
                            json_dict = {"error": 'Could not find any data for the value inserted.'}
                            contents = us.read_html_file("specific_error.html").render(context=json_dict)
                        else:
                            if 'error' in id_gotten:
                                json_dict = {"error": 'Could not find any data for the value inserted.'}
                                contents = us.read_html_file("specific_error.html").render(context=json_dict)
                            else:
                                try:
                                    json_dict = {"sequence_given": msg, "sequence": str(Seq(response['seq'])),
                                                 'sequence_id': id_gotten}
                                    contents = us.read_html_file("4geneseq.html").render(context=json_dict)
                                except TypeError:
                                    json_dict = {"error": 'Could not find any data for the value inserted.'}
                                    contents = us.read_html_file("specific_error.html").render(context=json_dict)
                else:
                    json_dict = json_no_input
                    contents = us.read_html_file("specific_error.html").render(context=json_dict)
            #  ####################### 5 LENGTH, START, END, CHROMOSOME   ############################################
            elif path == '/geneInfo':
                if 'gene' in arguments:
                    msg = arguments['gene'][0].strip().replace(' ', '_')
                    try:
                        id_gotten, response = us.get_gene(msg)
                        if 'error' in response or 'error' in id_gotten:
                            json_dict = {"error": 'Could not find any data for the value inserted.'}
                            contents = us.read_html_file("specific_error.html").render(context=json_dict)
                        else:
                            lookup_response = us.get_data_gene(id_gotten)
                            json_dict = {
                                "sequence_given": msg,
                                "length": str(int(lookup_response['start']) - int(lookup_response['end']) + 1),
                                'start': lookup_response['start'],
                                'end': lookup_response['end'],
                                'display_name': lookup_response['display_name'],
                                'sequence_id': id_gotten,
                                'chromosome': lookup_response['seq_region_name']}
                            contents = us.read_html_file("5geneinfo.html").render(context=json_dict)
                    except TypeError:
                        json_dict = {"error": 'Start and end values should be numbers.'}
                        contents = us.read_html_file("specific_error.html").render(context=json_dict)
                    except KeyError:
                        json_dict = {"error": 'Could not find any data for the value inserted.'}
                        contents = us.read_html_file("specific_error.html").render(context=json_dict)
                else:
                    json_dict = json_no_input
                    contents = us.read_html_file("specific_error.html").render(context=json_dict)
            #  ####################### 6 CALCULATIONS  ###############################################################
            elif path == '/geneCalc':
                if 'gene' in arguments:
                    msg = arguments['gene'][0].strip().replace(' ', '_')
                    try:
                        id_gotten, response = us.get_gene(msg)
                        if 'error' in response or 'error' in id_gotten:
                            json_dict = {"error": 'Could not find any data for the value inserted.'}
                            contents = us.read_html_file("specific_error.html").render(context=json_dict)
                        else:
                            s = Seq(response['seq'])
                            json_dict = {
                                "sequence_given": msg, 'sequence_id': id_gotten, "total_length": s.len(),
                                "percentage": [k + ': ' + v for k, v in s.percentage().items()]}
                            contents = us.read_html_file("6genecalc.html").render(context=json_dict)
                    except TypeError:
                        json_dict = {"error": 'The gene should be a correct one.'}
                        contents = us.read_html_file("specific_error.html").render(context=json_dict)
                else:
                    json_dict = json_no_input
                    contents = us.read_html_file("specific_error.html").render(context=json_dict)
            #  ####################### 7 GENES IN CHROMOSOMES UNTIL SOME LENGTH   ####################################
            elif path == '/geneList':
                if 'chromo' in arguments and 'start' in arguments and 'end' in arguments:
                    chromosome = arguments['chromo'][0].upper().strip().replace(' ', '_')
                    start = arguments['start'][0].strip().replace(' ', '_')
                    end = arguments['end'][0].strip().replace(' ', '_')
                    if chromosome in us.server_connection('info/assembly/homo_sapiens')['karyotype']:
                        try:
                            if int(start) <= int(end):
                                response = us.get_chromosome(chromosome, start, end)
                                if 'error' in response or response == []:
                                    json_dict = {"error": 'We could not find information for the data introduced.'}
                                    contents = us.read_html_file("specific_error.html").render(context=json_dict)
                                else:
                                    list_names = []
                                    list_id = []
                                    for i in response:
                                        if 'phenotype_associations' in i:
                                            if 'attributes' in i['phenotype_associations'][0]:
                                                if 'associated_gene' in i['phenotype_associations'][0]['attributes']:
                                                    list_names.append(i['phenotype_associations'][0]['attributes']['associated_gene'])
                                                    list_id.append(i['id'])
                                    dict_names = dict(zip(list_names, list_id))
                                    list_printed = [i + ' (id:' + a + ')' for i, a in dict_names.items()]
                                    json_dict = {"chromosome": chromosome, 'start': start, 'end': end, 'list_names': list_printed}
                                    contents = us.read_html_file("7genelist.html").render(context=json_dict)
                            else:
                                json_dict = {"error": 'Start should be smaller than end.'}
                                contents = us.read_html_file("specific_error.html").render(context=json_dict)
                        except ValueError:
                            json_dict = {"error": 'The values inserted for start and end should be numbers.'}
                            contents = us.read_html_file("specific_error.html").render(context=json_dict)
                    else:
                        json_dict = {"error": 'The chromosome inserted is not a human chromosome.'}
                        contents = us.read_html_file("specific_error.html").render(context=json_dict)
                else:
                    json_dict = json_no_input
                    contents = us.read_html_file("specific_error.html").render(context=json_dict)
            #  #######################   OTHER ACTION   ##############################################################
            else:
                contents = Path('html/error.html').read_text()
        #  #######################   MAIN PROGRAM   ##################################################################
        try:
            if 'json' in arguments:
                try:
                    contents = json.dumps(json_dict)
                    self.send_header('Content-Type', 'application/json')
                except Exception as e:
                    print(e)
            else:
                self.send_header('Content-Type', 'text/html')
            self.send_header('Content-Length', len(str.encode(contents)))
            self.end_headers()
            self.wfile.write(str.encode(contents))
        except UnboundLocalError:
            contents = Path('html/error.html').read_text()
            self.send_header('Content-Type', 'text/html')
            self.send_header('Content-Length', len(str.encode(contents)))
            self.end_headers()
            self.wfile.write(str.encode(contents))
        return


Handler = TestHandler

with socketserver.TCPServer(("", PORT), Handler) as httpd:
    print("Serving at PORT", PORT)
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("")
        print("Stopped by the user")
        httpd.server_close()

