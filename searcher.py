# -*- coding: utf-8 -*-

from whoosh.qparser import MultifieldParser
from whoosh import scoring
from whoosh.index import open_dir
import sys

def search(query_str):
    ix = open_dir("indexdir")
    # Top 'n' documents as result
    global search_results
    search_results = []
    with ix.searcher(weighting=scoring.BM25F()) as searcher:
        query = MultifieldParser(["title", "content"], ix.schema).parse(query_str)
        results = searcher.search(query,limit=30)

        if len(results) > 0 :
            for i in results:
                result = dict(i)
                with open(i['path'], 'rb') as file:
                    filecontents = file.read().decode(errors='replace')
                result['excerpt'] = i.highlights("content",text=filecontents)
                if result['excerpt'] == "":
                    result['excerpt'] = filecontents.split("\n")
                    if len(result['excerpt']) == 1:
                        result['excerpt'] = result['excerpt'][0]
                    else:
                        result['excerpt'] = result['excerpt'][1]
                else:
                    result['excerpt'] = "..." + result['excerpt'] + "..."
                result['title'] = i['path'].split('\\')[-1].replace(".txt", "")
                search_results.append(result)
    return search_results