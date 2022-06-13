from neo4j import GraphDatabase, work
from numpy import block

from .node import Node
from .block import Block
import logging

logging.basicConfig(level=logging.INFO)

class Connector:
    def __init__(self, uri:str, user:str, password:str):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))

    def query(self, query:str, raw:bool = False):
        # Raw keyword is useless for now, but might not be later
        logging.info(f'Running query from Connector --> {query}')
        s = self.driver.session()
        txn = s.begin_transaction()
        result = txn.run(query)

        rt = []
        for k in result:
            rt.append(k)
        print("RECORD : ", rt)
        #results = [record for record in result.data()]

        txn.commit()

        return rt

    def getSession(self):
        return self.driver.session()

    def getBlock(self, blockType:str=None, preload:bool = True):
        return Block(blockType, self)

    def getNode(self, blockType:str, id:int, preload:bool = True):
        n = Node(blockType, id, self)
        n.sync()
        return n

    def createNode(self, blockType:str, id:int, **kwargs):
        unitName = blockType[0].lower()
        q = 'CREATE (' + unitName + ':' + blockType + ' {id:' + str(id) + '})\n'
        q += 'RETURN ' + unitName

        rt = self.query(q)
        print("CreateNodeRT : ", rt)

        if len(rt) > 0:
            n = Node(blockType, id, self)
            for k in kwargs:
                n[k] = kwargs[k]
            n.commit()
            return n
        else:
            return None

    def deleteNode(self, blockType:str, id:int, detach:bool = True):
        unitName = blockType[0].lower()
        q = 'MATCH (' + unitName + ':' + blockType + ' {id:' + str(id) + '})\n'
        if detach:
            q += 'DETACH DELETE {unitName}'
        else:
            q += 'DELETE {unitName}'
        q += 'RETURN ' + unitName

        rt = self.query(q)

    def close(self):
        self.driver.close()