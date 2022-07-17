from neo4j import GraphDatabase, work
from numpy import block

from .node import Node, syncTypes
from .block import Block
import logging

logging.basicConfig(level=logging.INFO)

class NotConnected(Exception):
    def __init__(self):
        super().__init__()

class Connector:
    def __init__(self, uri:str, user:str, password:str):
        self.fail = False
        try:
            self.driver = GraphDatabase.driver(uri, auth=(user, password))
        except Exception as e:
            print("Error: ", e)
            self.fail = True

    def query(self, query:str, raw:bool = False):
        # Raw keyword is useless for now, but might not be later
        logging.info(f'Running query from Connector --> {query}')
        if self.fail:
            raise NotConnected()
        s = self.driver.session()
        txn = s.begin_transaction()
        result = txn.run(query)

        rt = []
        for k in result:
            rt.append(k)
        #results = [record for record in result.data()]

        txn.commit()

        return rt

    def getSession(self):
        return self.driver.session()

    def getBlock(self, blockType:str=None, preload:bool = True) -> Block:
        return Block(blockType, self)

    def getNode(self, blockType:str, id:int, preload:bool = True) -> Node:
        n = Node(blockType, id, self)
        if n.sync(syncTypes.ALLOW_EMPTY) == True:
            return n
        else:
            return None
        

    def createNode(self, blockType:str, id:int, **kwargs) -> Node:
        unitName = blockType[0].lower()
        q = 'CREATE (' + unitName + ':' + blockType + ' {id: \'' + str(id) + '\'})\n'
        q += 'RETURN ' + unitName

        rt = self.query(q)
        logging.debug('CreateNodeRT : ', rt)

        if len(rt) > 0:
            n = Node(blockType, id, self)
            for k in kwargs:
                n[k] = kwargs[k]
            n.commit()
            return n
        else:
            return None

    def deleteNode(self, blockType:str, id:int, detach:bool = True) -> None:
        unitName = blockType[0].lower()
        q = f'MATCH ({unitName}:{blockType}' + ' {id: \"' + str(id) + '\"})\n'
        if detach:
            q += f'DETACH DELETE {unitName}\n'
        else:
            q += f'DELETE {unitName}\n'
        q += 'RETURN ' + unitName

        rt = self.query(q)

        print("Deleted ? ", rt)

    def close(self):
        self.driver.close()