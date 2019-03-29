'''
Created on 20 Mar 2019

@author: ejimenez-ruiz
'''
from enum import Enum


class KG(Enum):
        DBpedia = 0
        Wikidata = 1
        Google = 2        
        All = 3

class URI_KG(object):
    
    dbpedia_uri_resource = 'http://dbpedia.org/resource/'
    
    dbpedia_uri = 'http://dbpedia.org/ontology/'
    wikidata_uri ='http://www.wikidata.org/entity/'
    schema_uri = 'http://schema.org/' 
    
    uris = list()
    uris.append(dbpedia_uri)
    uris.append(wikidata_uri)
    uris.append(schema_uri)
    
    uris_resource = list()
    uris_resource.append(dbpedia_uri_resource)
    uris_resource.append(wikidata_uri)
    
    
    
    def __init__(self):
        ''''
        '''



class KGEntity(object):
    
    
    def __init__(self, enity_id, label, description, types, source):
        
        self.ident = enity_id
        self.label = label
        self.desc = description #sometimes provides a very concrete type or additional semantics
        self.types = types  #set of semantic types
        self.source = source  #KG of origin: dbpedia, wikidata or google kg
        
    
    def __repr__(self):
        return "<id: %s, label: %s, description: %s, types: %s, source: %s>" % (self.ident, self.label, self.desc, self.types, self.source)

    def __str__(self):
        return "<id: %s, label: %s, description: %s, types: %s, source: %s>" % (self.ident, self.label, self.desc, self.types, self.source)
    
    
    def getId(self):
        return self.ident
    
    '''
    One can retrieve all types or filter by KG: DBpedia, Wikidata and Google (Schema.org)
    '''
    def getTypes(self, kgfilter=KG.All):
        if kgfilter==KG.All:
            return self.types
        else:
            kg_uri = URI_KG.uris[kgfilter.value]
            filtered_types = set()
            for t in self.types:
                if t.startswith(kg_uri):
                    filtered_types.add(t)
            
            return filtered_types 
    
    def getLabel(self):
        return self.label
    
    def getDescription(self):
        return self.desc
    
    def getSource(self):
        return self.sourcec
    
    
    def addType(self, cls):
        self.types.add(cls)
    
    def addTypes(self, types):
        self.types.update(types)
        
        
        
if __name__ == '__main__':
    print(URI_KG.uris[KG.DBpedia.value])
    print(KG.DBpedia.value)
          
    