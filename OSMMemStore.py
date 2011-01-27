#
#  OSMMemStore.py
#  osm2spatialite
#
#  Created by Daniel Sabo on 1/27/11.
#  Copyright (c) 2011 __MyCompanyName__. All rights reserved.
#

class OSMMemStore:
    def __init__(self):
        self.ways  = {}
        self.nodes = {}
        self.relations = {}
    
    def addNode(self, object):
        self.nodes[object["id"]] = object
    
    def addWay(self, object):
        self.ways[object["id"]] = object
    
    def addRelation(self, object):
        self.relations[object["id"]] = object
    
    def _getSet(self, osm_ids, func):
        result = {}
        for osm_id in osm_ids:
            result[osm_id] = func(id)
        return result
    
    def getNode(self, osm_id):
        try:
            return self.nodes[osm_id]
        except KeyError:
            return None
    
    def getNodes(self, osm_ids):
        return self._getSet(osm_ids, self.getNode)
        
    def getWay(self, osm_id):
        try:
            return self.ways[osm_id]
        except KeyError:
            return None
    
    def getWays(self, osm_ids):
        return self._getSet(osm_ids, self.getWay)
        
    def getRelation(self, osm_id):
        try:
            return self.relations[osm_id]
        except KeyError:
            return None
    
    def getRelations(self, osm_ids):
        return self._getSet(osm_ids, self.getRelation)
        