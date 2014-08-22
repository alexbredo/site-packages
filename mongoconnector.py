# Copyright (c) 2014 Alexander Bredo
# All rights reserved.
# 
# Redistribution and use in source and binary forms, with or 
# without modification, are permitted provided that the 
# following conditions are met:
# 
# 1. Redistributions of source code must retain the above 
# copyright notice, this list of conditions and the following 
# disclaimer.
# 
# 2. Redistributions in binary form must reproduce the above 
# copyright notice, this list of conditions and the following 
# disclaimer in the documentation and/or other materials 
# provided with the distribution.
# 
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND 
# CONTRIBUTORS "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, 
# INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF 
# MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE 
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR 
# CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, 
# INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES 
# (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE 
# GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR 
# BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF 
# LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT 
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT 
# OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE 
# POSSIBILITY OF SUCH DAMAGE.

# -*- coding: utf-8 -*-
from pymongo import MongoClient

class MongoConnector(object):
    def __init__(self, host, port, database, collection, username=None, password=None):
        self.__client = MongoClient(host, port)
        self.__db = self.__client['alarm-center']
        if username and password:
            self.__db.authenticate(username, password)
        self.__collection = self.__db[collection]

    def count(self):
        return self.getCollection().count()

    def getCollection(self):
        return self.__collection

    def find(self, condition):
        return self.getCollection().find(condition)

    # Group+Count with Map-Reduce
    def getGroupedCollection(self, field, condition={}):
        return self.getCollection().group({field:1}, condition, {"count": 0}, 'function(obj, prev){prev.count++}')

    def getGroupedCollectionCount(self, field, condition={}):
        return len(self.getGroupedCollection(field, condition))

    def CountByField(field, value):
        return self.find({field: re.compile(value, re.IGNORECASE)}).count()

    def insert(self, service, timestamp, ip, port, type, command, successful, session):
        data = dict(service=service, timestamp=timestamp, ip=ip, port=port, type=type, command=command, successful=successful, session=session)
        return self.getCollection().insert(data)
        
# TODO:
# Range Zeit. 1 Tag. Nach 30 Tagen Inhalte löschen
# THRESHOLD PER HOST/SVC

#    def getFieldMaxValue(self, field):
#        return self.getCollection().find_one(cond={"session": ses['session']},sort=[("timestamp", -1)])['timestamp']

#    def getFieldMinValue(self, field):
#        return self.getCollection().find_one(sort=[(field, 1)])[field]

#for ses in self.getGroupedCollection('session'):
#    print ses['session']
#    print ses['count']
#    print "lmax %s" % events.find({"session": ses['session']}).sort([("timestamp", -1)]).limit(1)[0]['timestamp']
#    print "lmin %s" % events.find({"session": ses['session']}).sort([("timestamp", 1)]).limit(1)[0]['timestamp']