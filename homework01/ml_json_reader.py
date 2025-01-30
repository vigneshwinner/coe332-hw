import json

def compute_average_mass(a_list_of_dicts, a_key_string):
    total_mass = 0.
    for i in range(len(a_list_of_dicts)):
        total_mass += float(a_list_of_dicts[i][a_key_string])
    return (total_mass / len(a_list_of_dicts))

def check_hemisphere(latitude: float, longitude: float) -> str:    # type hints
    location = ''
    if (latitude > 0):
        location = 'Northern'
    else:
        location = 'Southern'
    if (longitude > 0):
        location = f'{location} & Eastern'
    else:
        location = f'{location} & Western'
    return(location)

def count_meteorite_classes(meteorites):
    class_counts = {}

    for meteorite in meteorites:
        m_class = meteorite['recclass']
        if m_class in class_counts:
            class_counts[m_class] += 1
        else:
            class_counts[m_class] = 1 

    return class_counts  

with open('Meteorite_Landings.json', 'r') as f:
    ml_data = json.load(f)

print("Average Mass:", compute_average_mass(ml_data['meteorite_landings'], 'mass (g)'), "grams")

neCount = 0
nwCount = 0
seCount = 0
swCount = 0
for row in ml_data['meteorite_landings']:
    if (check_hemisphere(float(row['reclat']), float(row['reclong']))) == "Northern & Eastern":
        neCount+= 1
    if (check_hemisphere(float(row['reclat']), float(row['reclong']))) == "Northern & Western":
        nwCount+= 1
    if (check_hemisphere(float(row['reclat']), float(row['reclong']))) == "Southern & Eastern":
        seCount+= 1
    if (check_hemisphere(float(row['reclat']), float(row['reclong']))) == "Southern & Western":
        swCount+= 1
print("\nLanding Site Location Count")
print("Northern & Eastern:", neCount)
print("Northern & Western:", nwCount)
print("Southern & Eastern:", seCount)
print("Southern & Western:", swCount)

meteorite_class_counts = count_meteorite_classes(ml_data['meteorite_landings'])
print("\nMeteorite Classes/Count (Type, Number)")
for meteorite_type, count in meteorite_class_counts.items():
    print(f"{meteorite_type}, {count}")
