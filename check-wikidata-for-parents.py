#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__description__ = "retrieve information on historical persons from wikidata; " \
                  "step 1: retrieve Q-ID (intern Wikidata ID)" \
                  "step 2: retrieve name and Q-IDs of mother, father and children"
__author__ = "Eva Seidlmayer <seidlmayer@zbmed.de>"
__copyright__ = "2021 by Eva Seidlmayer"
__license__ = "ISC license"
__email__ = "seidlmayer@zbmed.de"
__version__ = "1 "



from SPARQLWrapper import SPARQLWrapper, JSON
import csv

user_agent = "Eva Seidlmayer, ZB MED Informationszentrum Lebenswissenschaften, seidlmayer@zbmed.de"
wd_url = SPARQLWrapper("https://query.wikidata.org/sparql", agent=user_agent)


def main():

    names = ['Bertha Krupp', 'Tilo Wilmowsky', 'Bertha Benz', 'Ferdinand Redtenbacher', 'Werner von Siemens', 'Käthe Pietschker']
    with open('results-from-WD.csv', 'w') as csvfile:
        csv_writer = csv.writer(csvfile)
        csv_writer.writerow(['name','QID', 'mother', 'mother-QID', 'father', 'father-QID', 'child', 'child-QID'])

        try:
             for name in names:
                query_1 = f''' SELECT ?item WHERE {{ ?item rdfs:label '{name}'@en }}'''
                wd_url.setQuery(query_1)
                wd_url.setReturnFormat(JSON)
                results = wd_url.query().convert()
                if (len(results['results']['bindings'])) > 0:
                    for res in results['results']['bindings']:
                        QID = res['item']['value'].rsplit('/', 1)[1]

                        query_2 = f''' SELECT ?personLabel ?motherLabel ?mother ?fatherLabel ?father ?childLabel ?child 
                                    WHERE {{ VALUES ?person {{ wd:{QID} }} 
                                    OPTIONAL {{ ?person wdt:P22 ?father . }} 
                                    OPTIONAL {{ ?person wdt:P25 ?mother . }}
                                    OPTIONAL {{ ?person wdt:P40 ?child . }}
                                    SERVICE wikibase:label {{ bd:serviceParam wikibase:language "[AUTO_LANGUAGE],de" }}
                                    }}'''
                        wd_url.setQuery(query_2)
                        wd_url.setReturnFormat(JSON)
                        results_2 = wd_url.query().convert()
                        try:
                            if (len(results_2['results']['bindings'])) > 0:
                                for res_2 in results_2['results']['bindings']:
                                    print(res_2)
                                    try:
                                        mother_QID = res_2['mother']['value'].rsplit('/', 1)[1]
                                    except:
                                        mother_QID = ''
                                    try:
                                        mother_label = res_2['motherLabel']['value']
                                    except:
                                        mother_label =''
                                    try:
                                        father_QID = res_2['father']['value'].rsplit('/', 1)[1]
                                    except:
                                        father_QID = ''
                                    try:
                                        father_label = res_2['fatherLabel']['value']
                                    except:
                                        father_label = ''
                                    try:
                                        child_QID = res_2['child']['value'].rsplit('/', 1)[1]
                                    except:
                                        child_QID = ''
                                    try:
                                        child_label = res_2['childLabel']['value']
                                    except:
                                        child_label = ''

                                    infos = [name, QID, mother_label, mother_QID, father_label, father_QID, child_label,
                                             child_QID]

                                    print(','.join(infos))
                                    csv_writer.writerow(infos)
                        except:
                            continue


        except:
            pass

if __name__ == '__main__':
    main()
