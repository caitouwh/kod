import os, futures, pandas as pd, datetime
from pymongo import MongoClient
import Quandl

testdb = "fakedb"

def load_data(contract,subdir):
    f = contract.replace("/","-")
    f = "./test/%s/%s.csv" % (subdir,f)
    if not os.path.isfile(f): raise Quandl.Quandl.DatasetNotFound()
    df = pd.read_csv(f)
    df = df.set_index("Date")
    return df
    
def fake_download_1(contract,start,end):
    return load_data(contract, "data_1")

def fake_today_1():
    return datetime.datetime(2016, 5, 1) 

def init():
    c = MongoClient()
    c[testdb].tickers.drop()
    return c[testdb]

def test_simple():
    db = init()
    futures.download_data(downloader=fake_download_1,today=fake_today_1,
                          db=testdb, years=(1984,1985))
    res = futures.get(market="CME", sym="CL", month="F", year=1984, dt=19831205, db=testdb)
    assert res[0]['oi'] == 5027.0
    res = futures.get(market="CME", sym="CL", month="G", year=1984, dt=19830624, db=testdb)
    assert res[0]['oi'] == 5.0
    res = futures.last_contract("CL","CME", db)
    assert res[0]['_id']['month'] == 'G' 
    
if __name__ == "__main__": 
    test_simple()
    
