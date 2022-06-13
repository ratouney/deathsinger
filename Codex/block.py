from neo4j import GraphDatabase, work
import logging

logging.basicConfig(level=logging.INFO)

class Block:
    '''
        The unitname is the shorthand variable name.
        The blocktype is the full Node type name.
    '''
    def __init__(self, blockType = None, link=None) -> None:
        l = blockType[0].lower()
        logging.info(f'Initializing Block ({l}:{blockType})')
        # Cannot check if it's a Connector so don't use Session
        if link != None:
            self.connector = link
            self.session = link.getSession()
        self.blockType = blockType

        self.unitName = l
    
    def setId(self, id):
        logging.info(f'Setting block {self.blockType}::{id}')
        self.id = id

    def setBlockType(self, name:str):
        self.blocktype = name
        self.unitName = name[0].lower()

    def get(self, **kwargs):
        if self.unitName == None or self.blockType == None:
            raise Exception("blockType not set, use setAttribute")
        q = 'MATCH (' + self.unitName + ':' + self.blockType + ' {'
        prev = False
        for k in kwargs:
            if prev == True:
                q += ","
            q += k + ': "' + kwargs[k] + '"'
            prev = True
        q += "}) RETURN " + self.unitName

        rt = self.connector.query(q)

        print(rt)

        return rt