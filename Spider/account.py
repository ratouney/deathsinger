import logging
from .regions import Region

class Account:
    def __init__(self, params, link = None, givenRegion:Region = Region.EUW) -> None:
        print(params)
        if "status" in params:
            if 'status_code' in params['status'] != 200:
                msg = params['status']['message']
                raise Exception(f'AccountCreation : {msg}')
        self.name = params['name']
        logging.info(f'Creating account for {givenRegion.value}:{self.name}')
        self.api = link
        self.region = givenRegion
        self.id = params['id']
        self.accountId = params['accountId']
        self.puuid = params['puuid']
        #self.name = params['name']
        self.profileIconId = params['profileIconId']
        self.summonerLevel = params['summonerLevel']

    def __repr__(self) -> str:
        return f'[{self.region}:{self.name}]'

    def getLastMatchIds(self, link = None):
        out = None
        if self.api == None:
            logging.info(f'No linked api')
            if link == None:
                logging.error(f'No linked api and none provided. Fuck')
                return None
            else:
                out = link
        else:
            out = self.api

        return out.getLastMatchIds(self)