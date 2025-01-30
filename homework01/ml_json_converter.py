import json
import csv
import yaml
import xmltodict

data = {}

with open('Meteorite_Landings.json', 'r') as f:
    data = json.load(f)

# Convert to CSV
with open('Meteorite_Landings.csv', 'w') as o:
    csv_dict_writer = csv.DictWriter(o, data['meteorite_landings'][0].keys())
    csv_dict_writer.writeheader()
    csv_dict_writer.writerows(data['meteorite_landings'])

# Convert to XML
root = {'MeteoriteLandings': {'Meteorite': data['meteorite_landings']}}

with open('Meteorite_Landings.xml', 'w', encoding='utf-8') as o:
    o.write(xmltodict.unparse(root, pretty=True))

# Convert to YAML
with open('Meteorite_Landings.yaml', 'w', encoding='utf-8') as o:
    yaml.dump(data['meteorite_landings'], o, default_flow_style=False)

print("CSV, XML, and YAML files created!")
