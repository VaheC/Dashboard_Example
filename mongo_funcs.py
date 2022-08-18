import pymongo
import pandas as pd
import numpy as np
import re 

def preprocess_data(df_main):
    '''Loads main df_main for the charts

       Params:
       filename: str, the name of the csv file containing df_main

       Returns:
       df_main: df_mainframe
    '''

    # loading df_main
    # df_main = pd.read_csv(filename)
#     df_main['Time'] = pd.to_datetime(df_main['Time'])
#     df_main.sort_values('Time', ascending=True, inplace=True)

    temp_cols = [col for col in df_main.columns if col != 'Time']

    error_values = list(
        set(
            [df_main[col].iloc[i] 
             for col in temp_cols 
             for i in range(df_main.shape[0]) 
             if len(re.findall(r'\d+', str(df_main[col].iloc[i])))==0]
        )
    )

    df_main.replace(error_values, np.nan, inplace=True)
    #df_main.fillna(method='ffill', inplace=True)

    for col in df_main.columns:
        if col == 'Time':
            pass
        elif col == "Frequency; Hz":
            df_main[col] = df_main[col].astype(int)
        else:
            df_main[col] = df_main[col].astype(float)

    df_main['Flow error; %'] = 100 * df_main['Flow error; %']
    df_main['Pump efficiency; %'] = 100 * df_main['Pump efficiency; %']
    df_main['Pump efficiency optimal; %'] = 100 * df_main['Pump efficiency optimal; %']
    df_main['Saving potential; %'] = 100 * df_main['Saving potential; %']

    return df_main

def get_data(user, password, table_name, db_name='enerwise'):
	mongo_login_link = f'mongodb+srv://{user}:{password}@cluster0.baach.mongodb.net/?retryWrites=true&w=majority'
	client_cloud = pymongo.MongoClient(mongo_login_link)

	db = client_cloud[db_name]

	collection = db[table_name]

	data = pd.DataFrame(list(collection.find()))

	client_cloud.close()

	return data

def delete_db(user, password, db_name='enerwise'):
	mongo_login_link = f'mongodb+srv://{user}:{password}@cluster0.baach.mongodb.net/?retryWrites=true&w=majority'
	client_cloud = pymongo.MongoClient(mongo_login_link)

	client_cloud.drop_database(db_name)

	client_cloud.close()

def delete_table(user, password, table_name, db_name='enerwise'):
	mongo_login_link = f'mongodb+srv://{user}:{password}@cluster0.baach.mongodb.net/?retryWrites=true&w=majority'
	client_cloud = pymongo.MongoClient(mongo_login_link)

	db = client_cloud[db_name]

	collection = db[table_name]

	collection.drop()

	client_cloud.close()

def insert_data(user, password, data, table_name, db_name='enerwise'):

	if table_name == 'chart2':
		pass
	else:
		data = preprocess_data(df_main=data)

	mongo_login_link = f'mongodb+srv://{user}:{password}@cluster0.baach.mongodb.net/?retryWrites=true&w=majority'
	client_cloud = pymongo.MongoClient(mongo_login_link)

	db = client_cloud[db_name]

	collection = db[table_name]

	list_records = [
	    {
	        col: int(data[col].iloc[i])
	        if isinstance(data[col].iloc[i], np.int32) or isinstance(data[col].iloc[i], np.int64)
	        else data[col].iloc[i] for col in data.columns
	    }
	    for i in range(data.shape[0])
	]

	collection.insert_many(list_records)

	client_cloud.close()


# myclient = pymongo.MongoClient("mongodb://localhost:27017/")
# mydb = myclient["mydatabase"]
# mycol = mydb["customers"]

# myquery = { "address": "Mountain 21" }

# mycol.delete_one(myquery)


# # Delete all documents were the address starts with the letter S
# myclient = pymongo.MongoClient("mongodb://localhost:27017/")
# mydb = myclient["mydatabase"]
# mycol = mydb["customers"]

# myquery = { "address": {"$regex": "^S"} }

# x = mycol.delete_many(myquery)