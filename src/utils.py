import pymongo

# Mongo db setup (change to use your version)
CONNECTION_STRING = "<MONGODB CONNECTION STRING>"
client = pymongo.MongoClient(CONNECTION_STRING)
db = client['<DATABASE>']
collection = db['<COLLECTION>']

# common functions
def error_catch(error):
    return f'Error Type: {type(error)} | Error: {error}'