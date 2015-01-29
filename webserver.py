# -*- coding: utf-8 -*-
"""
Created on Sat Dec 27 10:14:54 2014

This script will act as an application, user can interact with it via commandline.
This application should provide options to preprocess raw csv to file that can be consume by
UserProdPreference

@author: qingwei
"""
import tornado.ioloop
import tornado.websocket
import tornado.web
import tornado.httpserver

from usrobj import UserProdPreference
from recommender import Recommender
import dataloader as dl
import preprocessor as pp

def preprocess_file(filename):
    headers = ['CustomerID','ProductCode','Quantity']
    df = "a10 a10 a10 a10 a10 a10 a10 f4 a4 f4 a4 a4 a4 a4 a5 a5 a5 i4 a10 a3 a5"
    rawdata = dl.loadDataFromCSV(filename,",",df)
    processed = rawdata[headers]
    processed = pp.removeEntryByConstraint(processed,lambda x:x[headers[2]]<=0)
    dl.saveNumpyAsCSV('processeddata.csv',processed)
    return processed

class RecommendWebSocket(tornado.websocket.WebSocketHandler):    
    def open(self):
        print('Socket opened')
        dataobj = UserProdPreference.initFromSparseDataFile('Hilti_training.npz')
        self.rc = Recommender(dataobj)
        pass
        
    def on_message(self,message):
        try:
            recommendations = self.rc.recommend(message)
        except(ValueError):
            recommendations = "user not in database, cannot make recommendations"
        self.write_message(str(recommendations))
        
    def on_close(self):
        print('Socket closed')

class Application(tornado.web.Application):
    def __init__(self):
        handlers = [(r"/",RecommendWebSocket)]
        tornado.web.Application.__init__(self,handlers)

if __name__ == "__main__":
    print('running server at 8888')
    wsapp = Application()
    server = tornado.httpserver.HTTPServer(wsapp)
    server.listen(8888)
    tornado.ioloop.IOLoop.instance().start()
    
    
