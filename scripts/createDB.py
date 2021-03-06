# Janani Kalyanam
# January 10, 2018

# This script was used to create a database on the Mongo server called "IDS"
# In that, I will create a collection called public stream

import os, sys
import pymongo, json
import glob


full_collection_name = 'public_stream_01220123'
hashtag_collection_name = 'collection_hashtag_01220123'

def fulldb():
    '''
    code to create the full database
    '''
    directory = '/Users/jananikalyanam/Documents/insight_application/PROJECT/data/'
    filenames = glob.glob(directory + '*.json')[-15:];
    client = pymongo.MongoClient(); # client is the name of the connection
    db = client.IDS; # database for IDS data
    collection = db[full_collection_name]; # drugs is a collection (like a table)
                        # Change this line for different drugs

    ii =0;    
    for f in filenames:
        ii+=1;
        lines = open(f,'r').readlines(); # open file
        print(str(ii) + ' ' + f);
        for line in lines:

            try:
                JO = json.loads(line);
            except:
                continue;

            collection.insert_one(JO);

    client.close();

def create_collection_hashtag():
    '''
    code to create a collection for: (1) NON-DELETED & (2) HASHTAGGED
    '''
    client = pymongo.MongoClient();
    db = client.IDS;
    collection = db[full_collection_name];
    collection_hashtag = db[hashtag_collection_name];

    ii = 0;
    for document in collection.find():
        K = list(document.keys());
        
        # continue if the tweet has been deleted
        if('delete' in K):
            continue;

        # continue if the user language is not english
        if('entities' in K):
            if('hashtags' in document['entities']):
                if(len(document['entities']['hashtags']) > 0):
                    collection_hashtag.insert_one(document);
                    ii += 1;

    print(ii);
    client.close();

if __name__ == '__main__':

    #fulldb();
    create_collection_hashtag();
