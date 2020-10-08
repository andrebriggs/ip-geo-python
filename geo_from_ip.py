import pandas
import geoip2.database
import json
import time
from multiprocessing import Pool
import multiprocessing

SOURCES = {
    "ip_data": "query_data.csv",
    "ip_database":"GeoLite2-City.mmdb"
}
DATA = {}

def _dataframe(key):
    return pandas.read_csv(f"./data/{SOURCES[key]}") if key in SOURCES else None

def _ip_database(key):
    return geoip2.database.Reader(f"./data/{SOURCES[key]}")

def _get_dataframe(key):
    if key not in DATA:
        DATA[key] = _dataframe(key)
    return DATA[key]

def get_ip_data():
    return _get_dataframe("ip_data")

def get_ip_database():
    return _ip_database("ip_database")

def ip_geo_lookup(ip):
    response = g_ip_db.city(ip)
    state_name = None
    country_code = response.country.iso_code
    if country_code is not None:
        state_name = response.subdivisions.most_specific.name

    return [ip, country_code, state_name]

if __name__ == "__main__":
    print("Hello")

    dataframe = get_ip_data()
    print(dataframe.size)
    
    list_of_ip = json.loads(dataframe['clientIp_s'].iloc[0])[:1000]
    print("Number of unique ip addresses: ",len(list_of_ip))
    
    global g_ip_db 
    g_ip_db = get_ip_database()
    map_results = []
    ip_db = get_ip_database()

    cpu_count = multiprocessing.cpu_count()
    print("Using {} cores".format(cpu_count))
  
    # Map:  Read the large list of IP addresses using multiple processors
    start = time.time()
    with Pool(cpu_count) as p:
        map_results = p.map(ip_geo_lookup,list_of_ip)
    end = time.time()
    print("Mapping tooks {} seconds".format(round(end - start,2)))
    print("There are {} unique ip addresses".format(len(map_results))) 

    # Filter out ip addresses that couldn't be mapped to locations
    valid_results = list(filter(lambda x: x[1] is not None, map_results))
    print("There are {} valid ip addresses".format(len(valid_results)))    

    idx = 0
    for i in range(10):
        print(map_results[i])

    # Reduce: Aggregate the unique ip address count by country_code and sub_division (state)
    df = pandas.DataFrame(map_results)

    # Add headers to the dataframe
    df.columns =['ip', 'country_code', 'sub_division'] 
    print (df)

    grouped_by_state = df.groupby(['country_code','sub_division']).agg(['count'],)
    print(grouped_by_state)

    # Merge the header names 
    grouped_by_state.columns = ["_".join(x) for x in grouped_by_state.columns.ravel()]

    # Write out to CSV
    grouped_by_state.to_csv('country_state_count-{}.csv'.format(time.strftime("%Y%m%d-%H%M%S")))

    print("Done!")
    
