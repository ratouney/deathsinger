from distutils.log import debug
import logging
from enum import Enum

from numpy import block

class syncTypes(Enum):
    ALLOW_EMPTY = True
    NO_EMPTY = False

class IDNotFound(Exception):
    def __init__(self, blockType:str, id:str):
        self.blockType = blockType
        self.id = id
        super().__init__(blockType, id)

class Node:
    def __init__(self, blockType:str, id:str = None, link = None) -> None:
        self.isNodeClass = True
        self.blockType = blockType
        # Cannot check if it's a Connector so don't use Session
        if link != None:
            self.connector = link
            self.session = link.getSession()
        self.unitName = blockType[0].lower()
        self.id = id
        self.rawData = {}
    
    def __getitem__(self, key:str):
        return self.rawData[key]

    def __setitem__(self, key:str, value):
        self.rawData[key] = value
    
    def setType(self, type:str):
        self.blockType = type
        self.unitName = type[0].lower()

    def setId(self, id:int):
        self.id = id

    def sync(self, allowEmpty:syncTypes = syncTypes.ALLOW_EMPTY) -> bool:
        if self.connector == None or self.session == None:
            raise Exception("Node not connected")
        if self.id == None:
            raise Exception("No ID to sync to")
        if self.blockType == None:
            raise Exception("No type set on Node")

        l = self.blockType[0].lower()
        q = f'MATCH ({l}:{self.blockType} {{id: \'{self.id}\'}}) RETURN {l}'

        rt = self.connector.query(q)
        if len(rt) == 0:
            logging.debug(f'Node {self.blockType}:{self.id} is empty.')
            if allowEmpty == syncTypes.NO_EMPTY:
                raise IDNotFound(self.blockType, self.id)
            else:
                return False

        # if len(rt) == 0:
                # raise Exception("No corresponding node found {self.blockType}:{self.id}")
        self.data = rt[0][l]
        self.rawData = {}
        for k in self.data:
            self.rawData[k] = self.data[k]

        return True
        
    def commit(self, overwrite:bool = True):
        if overwrite:
            print("Commit local copy")
            self.set(**self.rawData)
        return True

    def set(self, **kwargs):
        if self.unitName == None or self.blockType == None:
            raise Exception("Block.name or Block.unitName not set, use setAttribute")
        q = 'MATCH (' + self.unitName + ':' + self.blockType + ' {id: \'' + str(self.id) + '\'})\n'
        prev = False
        for k in kwargs:
            if k == "id":
                # Skipping ID so it doesn't change to a string
                continue
            s = f'SET {self.unitName}.{k} = "{kwargs[k]}"\n'
            q += s
        q += f"RETURN {self.unitName}"

        logging.debug("Setting Node --> ", q)
        txn = self.session.begin_transaction()
        result = txn.run(q)

        txn.commit()

        rt = []
        for k in result:
            rt.append(k)

        print(rt)

        return True

    def linkMatch(self, otherType:str, otherId:int, label:str):
        n = self.connector.getNode(otherType, otherId)
        return self.link(n, label)

    def link(self, otherNode, label:str):
        if not otherNode.isNodeClass:
            raise Exception("Given link has to be a node")

        debugLine = self.blockType + ':' + str(self.id)
        debugLine += '-[' + label + ']->'
        debugLine += otherNode.blockType + ':' + str(otherNode.id)
        print("Linking ==>", debugLine)
        # Using First and Second as unitname to avoid duplicates
        f = 'MATCH (f:' + self.blockType + ' {id: \'' + str(self.id) + '\'})\n'
        s = 'MATCH (s:' + otherNode.blockType + ' {id: \'' + str(otherNode.id) + '\'})\n'

        lName = label[0].lower()
        lseg = f'CREATE (f)-[{lName}:{label}]->(s)\n'

        q = f + s + lseg + f'RETURN f,{lName},s'

        txn = self.session.begin_transaction()
        result = txn.run(q)

        txn.commit()

        rt = []
        for k in result:
            rt.append(k)

        print(rt)

        return True

    def unlink(self, otherNode, label:str):
        if not otherNode.isNodeClass:
            raise Exception("Given link has to be a node")

        debugLine = self.blockType + ':' + str(self.id)
        debugLine += '-[' + label + ']->'
        debugLine += otherNode.blockType + ':' + str(otherNode.id)
        print("Linking ==>", debugLine)
        # Using First and Second as unitname to avoid duplicates
        f = 'MATCH (f:' + self.blockType + ' {id: \'' + str(self.id) + '\'})\n'
        s = 'MATCH (s:' + otherNode.blockType + ' {id: \'' + str(otherNode.id) + '\'})\n'
        ulName = label[0].lower()
        lFind = f'MATCH (f)-[{ulName}:{label}]->(s)\n'

        ulseg = f'DELETE {ulName}\n'

        q = f + s + lFind + ulseg + f'RETURN f,{ulName},s'

        txn = self.session.begin_transaction()
        result = txn.run(q)

        txn.commit()

        rt = []
        for k in result:
            rt.append(k)

        print(rt)

        return True
