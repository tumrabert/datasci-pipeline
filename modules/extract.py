import pandas as pd
import json

def extract_fields(data):
    """Extracts target data from a JSON file and writes it to a feather file."""
    # Access relevant data structures within the JSON
    abstracts_retrieval_response = data.get('abstracts-retrieval-response', {}) if data else {}
    if not abstracts_retrieval_response:
        abstracts_retrieval_response = data
    item = abstracts_retrieval_response.get('item', {}) if abstracts_retrieval_response else {}
    bibrecord = item.get('bibrecord', {}) if item else {}
    head = bibrecord.get('head', {}) if bibrecord else {}
    tail = bibrecord.get('tail', {}) if bibrecord else {}
    coredata = abstracts_retrieval_response.get('coredata', {}) if abstracts_retrieval_response else {}
    sid = coredata.get('dc:identifier', '').replace('SCOPUS_ID:', '', 1)  if coredata.get('dc:identifier', '') else ''
    authors = abstracts_retrieval_response.get('authors', {}).get('author', []) if abstracts_retrieval_response else []
    bibliography = tail.get('bibliography', {}) if tail else {}
    references = tail.get('bibliography', {}).get('reference', []) if tail else []
    
    ref = ''
    if isinstance(references, list):
        for r in references:
            ref += r.get('ref-fulltext', '') + ', '
    else:
        ref = references.get('ref-fulltext', '') + ', '
    
    afflication = abstracts_retrieval_response.get('affiliation', [])
    aff = ''
    if isinstance(afflication, dict):
            afflication_city = afflication.get('affiliation-city', '') if afflication.get('affiliation-city', '')  else ''
            afflication_country = afflication.get('affiliation-country', '') if afflication.get('affiliation-country', '') else ''
            affilname = afflication.get('affilname', '') if afflication.get('affilname', '') else ''
            aff += afflication_city + ' ' + afflication_country + ' ' + affilname + ', '
  
    else:
        for a in afflication:
            afflication_city = a.get('affiliation-city', '') if a.get('affiliation-city', '')  else ''
            afflication_country = a.get('affiliation-country', '') if a.get('affiliation-country', '') else ''
            affilname = a.get('affilname', '') if a.get('affilname', '') else ''
            aff += afflication_city + ' ' + afflication_country + ' ' + affilname + ', '
  
    subject_area = abstracts_retrieval_response.get('subject-areas', {}).get('subject-area', [])
    sub = ''
    for i, s in enumerate(subject_area):
        sub += s.get('$', '')
        if i != len(subject_area) - 1:
            sub += ', '
            
    fullname = ''
    for i, author in enumerate(authors):
        preferred_name = author.get('preferred-name', {})
        fullname += preferred_name.get('ce:indexed-name', '')
        if i != len(authors) - 1:
            fullname += ', '
    
    coredata = abstracts_retrieval_response.get('coredata', {})
    issn_or_isbn = ''
    if 'prism:issn' in coredata:
        issn_or_isbn = coredata.get('prism:issn', '')
    else:
        isbn = coredata.get('prism:isbn', '')
        if isinstance(isbn, list):
            for i, e in enumerate(isbn):
                issn_or_isbn += e.get('$', '')
                if i != len(isbn) - 1:
                    issn_or_isbn += ', '
        else:
            issn_or_isbn = isbn
    
    citation_title = head.get('citation-title', '') if head.get('citation-title', '') else ''
    abstracts = head.get('abstracts', '') if head.get('abstracts', '') else ''
    references = ref
    refcount = bibliography.get('@refcount', '') if bibliography.get('@refcount', '') else 0
    affiliations = aff
    citedby_count = coredata.get('citedby-count', '') if coredata.get('citedby-count', '') else ''
    issn_or_isbn = issn_or_isbn
    eid = coredata.get('eid', '') if coredata.get('eid', '') else ''
    journal_title = coredata.get('dc:title', '') if coredata.get('dc:title', '') else ''
    description = coredata.get('dc:description', '') if coredata.get('dc:description', '') else ''
    publisher = coredata.get('dc:publisher', '') if coredata.get('dc:publisher', '') else ''
    cover_date = coredata.get('prism:coverDate', '') if coredata.get('prism:coverDate', '') else ''
    aggregation_type = coredata.get('prism:aggregationType', '') if coredata.get('prism:aggregationType', '') else ''
    publication_name = coredata.get('prism:publicationName', '') if coredata.get('prism:publicationName', '') else ''
    language = abstracts_retrieval_response.get('language', {}) if abstracts_retrieval_response.get('language', {}) else {}
    language = language.get('@xml:lang', '') if language else ''
    subject_area = sub
    fullname = fullname
    
    data_dict = {
        '_id': sid,
        'citation-title': citation_title,
        'abstracts': abstracts,
        'references': ref,
        'refcount': refcount,
        'affiliations': aff,
        'citedby-count': citedby_count,
        'issn-or-isbn': issn_or_isbn,  
        'journal-title': journal_title,
        'description': description,
        'publisher': publisher,
        'cover-date': cover_date,
        'aggregation-type': aggregation_type,
        'publication-name': publication_name,
        'language': language,
        'subject-area': sub,
        'fullname': fullname
    }
    
    
    return data_dict

import json
import logging

def extract(file_names):
    data_collection = []
    for file_name in file_names:
        try:
            with open(file_name, 'r', encoding='utf-8') as file:
                data = file.read()
            parsed_data = json.loads(data)
            data_dict = extract_fields(parsed_data)
            data_collection.append(data_dict)
        except UnicodeDecodeError:
            logging.error(f'Error reading file with utf-8 encoding: {file_name}')
            continue
        except json.JSONDecodeError:
            logging.error(f'Error parsing JSON from file: {file_name}')
            continue
        except Exception as e:
            logging.error(f'Unexpected error reading file: {file_name}, error: {str(e)}')
            continue
    return data_collection