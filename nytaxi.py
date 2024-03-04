# %%
import csv
import time
import matplotlib.pyplot as plt
import seaborn as sns

# %%
with open('trip_data_8.csv', 'r') as f:
    Taxi = csv.DictReader(f)
    h = 0
    for file in Taxi:
        h += 1
        if h == 1:
            start_date = file[' pickup_datetime']
        else:
            end_date = file[' dropoff_datetime']

# Print the results
print(f'Total rows: {h}')
print(f'Starting Date: {start_date}, Ending Date: {end_date}')

# %%
with open('trip_data_8.csv', 'r') as f:
    Taxi = csv.DictReader(f)
    h = 0
    for i in Taxi:
        h += 1
        if h < 6:
            print(i)
        else:
            break

# %%
pickup_lat_min = 90
pickup_lat_max = -90
pickup_long_min = 180
pickup_long_max = -180
dropoff_lat_min = 90
dropoff_lat_max = -90
dropoff_long_min = 180
dropoff_long_max = -180
i = 0
with open('trip_data_8.csv', 'r') as df:
    h = csv.DictReader(df)
    for row in h:
        if i > 0:
            try:
                pickup_lat = float(row[' pickup_latitude'])
                pickup_long = float(row[' pickup_longitude'])
                dropoff_lat = float(row[' dropoff_latitude'])
                dropoff_long = float(row[' dropoff_longitude'])
                if (-74.4 <= pickup_long <= -72.05 and 40.4 <= pickup_lat<= 41.02):
                    pickup_lat_min = min(pickup_lat_min, pickup_lat)
                    pickup_lat_max = max(pickup_lat_max, pickup_lat)
                    pickup_long_min = min(pickup_long_min, pickup_long)
                    pickup_long_max = max(pickup_long_max, pickup_long)
                if dropoff_long is not None and (-74.5 <= dropoff_long <= -72.02 and 40.75 <= dropoff_lat<= 41):
                    dropoff_lat_min = min(dropoff_lat_min, dropoff_lat)
                    dropoff_lat_max = max(dropoff_lat_max, dropoff_lat)
                    dropoff_long_min = min(dropoff_long_min, dropoff_long)
                    dropoff_long_max = max(dropoff_long_max, dropoff_long)
            except ValueError:
                continue
        i+=1
        if i > 1000000000:
            break
print("pickup_latitude_min: " ,pickup_lat_min)
print("pickup_longitude_min: ",pickup_long_min)

print("pickup_latitude_max: ",pickup_lat_max)
print("pickup_longitude_max: ",pickup_long_max)

print("dropoff_latitude_min: ",dropoff_lat_min)
print("dropoff_longitude_min: ",dropoff_long_min)

print("dropoff_latitude_max: ",dropoff_lat_max)
print("dropoff_longitude_max: ",dropoff_long_max)

# %%
from math import radians, cos, sin, asin, sqrt
def haversine(lon1, lat1, lon2, lat2):
   
    # convert decimal degrees to radians 
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])

    # haversine formula 
    dlon = lon2 - lon1 
    dlat = lat2 - lat1 
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a)) 
    r = 3958.8 # Radius of earth in kilometers. Use 3958.8 for miles.
    return c * r

# %%
import csv
f = open('trip_data_8.csv', 'r') 
data = csv.DictReader(f)
avg_dist = []
for row in data:
    if row[' pickup_longitude'] == '' or row[' pickup_latitude'] == '' or row[' dropoff_longitude']=='' or row[' dropoff_latitude']=='':
        continue
    else:
        d = round(haversine(float(row[' pickup_longitude']),float(row[' pickup_latitude']),float(row[' dropoff_longitude']),float(row[' dropoff_latitude'])),2)
        avg_dist.append(d)


# %%
import matplotlib.pyplot as plt

no_bins = 50  
plt.hist(avg_dist, bins = no_bins, edgecolor = 'k', range = (0.0, 5.02))
plt.xlabel('Average Distance')
plt.ylabel('Frequency')
plt.title('Histogram Plot')
plt.show()

# %%
from collections import defaultdict
import csv
dv = defaultdict(set)

with open('trip_data_8.csv', 'r') as file:
    csv_reader = csv.DictReader(file)
    h = 0
    for i in csv_reader:
        h += 1
        if h < 1000:
            for key, value in i.items():
                dv[key].add(value)
        else:
            break

# Print distinct values for each field
for field, values in dv.items():
    print(f"{field}: {', '.join(values)}")

# %%
nf = [' passenger_count', ' trip_time_in_secs', ' trip_distance']
min_max_values = {}

for f in nf:
    values = [float(row[f]) for i in csv.DictReader(open('trip_data_8.csv', 'r'))]
    min_max_values[f] = {'min': min(values), 'max': max(values)}

# Print min and max values for numeric fields
for f, values in min_max_values.items():
    print(f"{f}: Min - {values['min']}, Max - {values['max']}")

# %%
pph = defaultdict(list)

with open('trip_data_8.csv', 'r') as file:
    csv_reader = csv.DictReader(file)
    
    for i in csv_reader:
        pickup_hour = int(i[' pickup_datetime'].split()[1].split(':')[0])
        pph[pickup_hour].append(int(i[' passenger_count']))

apph = {hour: sum(passengers) / len(passengers) for hour, passengers in pph.items()}

# Create chart
plt.bar(apph.keys(), apph.values())
plt.xlabel('Hour of the Day')
plt.ylabel('Average Number of Passengers')
plt.title('Average Number of Passengers Each Hour of the Day')
plt.xticks(range(24))
plt.show()

# %%
with open('trip_data_8.csv', 'r') as inf, open('reduced_data.csv', 'w', newline='') as of:
    csv_reader = csv.reader(inf)
    csv_writer = csv.writer(of)
    
    for i, r in enumerate(csv_reader):
        if i % 1000 == 0:
            csv_writer.writerow(r)

# %%
pph = defaultdict(list)

with open('reduced_data.csv', 'r') as file:
    csv = csv.DictReader(file)
    
    for i in csv:
        pickup_hour = int(i[' pickup_datetime'].split()[1].split(':')[0])
        pph[pickup_hour].append(int(row[' passenger_count']))

apph = {hour: sum(passengers) / len(passengers) for hour, passengers in pph.items()}

# Create chart
plt.bar(apph.keys(), apph.values())
plt.xlabel('Hour of the Day')
plt.ylabel('Average Number of Passengers')
plt.title('Average Number of Passengers Each Hour of the Day')
plt.xticks(range(24))
plt.show()


