from pymongo.errors import PyMongoError
import logging

def find_documents_by_ids(myclient, ids, database='scopus_db', collection_name='scopus_collection'):
    try:
        db = myclient[database]
        collection = db[collection_name]
        # Query for documents where _id is in the list of ids
        cursor = collection.find({"_id": {"$in": ids}})
        return list(cursor)
    except PyMongoError as e:
        logging.error(f'Error fetching documents from MongoDB: {str(e)}')
        return []
    except Exception as e:
        logging.error(f'Unexpected error: {str(e)}')
        return []