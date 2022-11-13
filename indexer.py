# -*- coding: utf-8 -*-

import os
from whoosh.index import create_in
from whoosh.fields import Schema, TEXT, ID

def indexer(root, writer):
    filepaths = [os.path.join(root,i) for i in os.listdir(root)]
    for path in filepaths:
        if os.path.isdir(path):
            indexer(path, writer)
            continue
        fp = open(path,'rb')
        text = fp.read().decode(errors='replace')
        writer.add_document(title=path.split("\\")[-1].replace(".txt", ""), path=path,\
          content=text)
        fp.close()
 
def createSearchableData(root):   

    schema = Schema(title=TEXT(field_boost=2.0),path=ID(stored=True, unique=True),\
              content=TEXT)
    if not os.path.exists("indexdir"):
        os.mkdir("indexdir")
 
    # Creating a index writer to add document as per schema
    ix = create_in("indexdir",schema)
    writer = ix.writer()
 
    indexer(root, writer)

    writer.commit()
 
root = "corpus"
createSearchableData(root)