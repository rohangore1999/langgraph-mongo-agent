import pymongo
from pymongo import MongoClient
import os
from dotenv import load_dotenv
import sys
import ssl

# Create a log file for output
log_file = "mongo_connection_log.txt"
with open(log_file, "w") as f:
    f.write("MongoDB Connection Test Log\n")
    f.write("==========================\n\n")

# Function to log both to console and file
def log(message):
    print(message)
    with open(log_file, "a") as f:
        f.write(message + "\n")

# Load environment variables from .env file if you have one
# This is a good practice for sensitive information
load_dotenv()

# Connection string
connection_string = "mongodb+srv://gorerohan15:Rohangore1999@namaste-node.avd97.mongodb.net/?tlsAllowInvalidCertificates=true"

# Connect to MongoDB
try:
    # Create a MongoClient using the connection string
    # Using tlsAllowInvalidCertificates=true in the connection string to bypass SSL certificate validation
    client = MongoClient(
        connection_string,
        connectTimeoutMS=5000,  # 5 seconds
        serverSelectionTimeoutMS=5000  # 5 seconds
    )
    
    # Get the database instance
    db = client.get_database("devTinder")  # You can replace "test" with your actual database name
    
    # Test connection with a simple command
    server_info = client.server_info()
    log("MongoDB connection successful!")
    log(f"Server info: {server_info}")
    
    # List all available databases
    log("\nAvailable databases:")
    for db_name in client.list_database_names():
        log(f"- {db_name}")
    
    # List all collections in the selected database
    log(f"\nCollections in '{db.name}' database:")
    collections = db.list_collection_names()
    if collections:
        for collection_name in collections:
            log(f"- {collection_name}")
            
            # Display sample documents from each collection (limited to 1)
            log(f"  Sample document from {collection_name}:")
            sample = db[collection_name].find_one()
            if sample:
                log(f"  {sample}")
            else:
                log("  No documents found")
    else:
        log("No collections found in this database")
    
    # Test inserting and retrieving data
    log("\nTesting data operations:")
    test_collection = db["test_collection"]
    
    # Insert a test document
    test_doc = {"name": "Test Document", "value": 42, "test": True}
    insert_result = test_collection.insert_one(test_doc)
    log(f"Inserted document ID: {insert_result.inserted_id}")
    
    # Retrieve the document
    retrieved_doc = test_collection.find_one({"_id": insert_result.inserted_id})
    log(f"Retrieved document: {retrieved_doc}")
    
    # Delete the test document
    delete_result = test_collection.delete_one({"_id": insert_result.inserted_id})
    log(f"Deleted {delete_result.deleted_count} document(s)")
    
except pymongo.errors.ConnectionFailure as e:
    error_msg = f"MongoDB connection failed: {e}"
    log(error_msg)
except pymongo.errors.OperationFailure as e:
    error_msg = f"MongoDB authentication failed: {e}"
    log(error_msg)
except pymongo.errors.ServerSelectionTimeoutError as e:
    error_msg = f"MongoDB server selection timeout: {e}"
    log(error_msg)
except Exception as e:
    error_msg = f"An error occurred: {e}"
    log(error_msg)
finally:
    # Close the connection when done
    if 'client' in locals():
        client.close()
        log("MongoDB connection closed")
    
    log(f"\nComplete log saved to {os.path.abspath(log_file)}")

# Note: For production applications, consider storing your connection string in environment variables
# and implementing connection pooling for better performance. 