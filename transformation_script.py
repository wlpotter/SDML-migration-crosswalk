"""
Description: 
Author: Ngozi Harrison
Date Created: July 18, 2024
Version: 1.0
"""

# import the required dependencies
import pandas as pd, json, sys, numpy as np, os

# This is the script that transforms each row of the provided csv into a json document formatted accrding to the cross-walk schema
def transform_input(row):
    # First pull out the basic columns associated with the row
    local_id = str(row["local ID"])
    type = row["Type"]
    name = row["Name"]
    gender = row["Gender"]
    date_type = row["Dates.type"]
    date = row["Dates"]
    
    #template for building JSON document according to cross-walk schema https://airtable.com/apptwZzt3XnHrd0bv/tblsKf3bUA04XMUhc/viwsPbKs24Fifny8K?blocks=hide
    base_template_schema = f'''{{
    "id": {local_id},
    "type": "{type}",
    "pref_name": "{name}",
    "alt_name": [],
    "gender": "{gender}",
    "rel_con": [],
    "assoc_date": [],
    "note": []}}'''
    
    # Load base JSON template into JSON object
    data = json.loads(base_template_schema)
    
    # Check if there are associated alternate names and if so append them to the json object
    if pd.isnull(row["AKA"]) == False:
        alt_names = zip(row["AKA"].split(" ; "), row["Language.AKA"].split(" ; "))
        for (name, lang) in alt_names:
            data["alt_name"].append({"lang": lang, "value": name})    
    if pd.isnull(row["NS Name"]) == False:
            alt_names = zip(row["NS Name"].split(" ; "), row["Language.NS Name"].split(" ; "))
            for (name, lang) in alt_names:
                data["alt_name"].append({"lang": lang, "value": name})

    # Check to see if there is a date normalized with before and after
    if "/" in row["Dates.normalized"]:
        not_before = row["Dates.normalized"].split("/")[0].rjust(4, "0")
        not_after = row["Dates.normalized"].split("/")[1].rjust(4, "0")
        data["assoc_date"].append({"type": date_type,"iso": {"not_before": not_before, "not_after": not_after},"value": date})         
    else:
        not_before = row["Dates.normalized"].split("/")[0]
        data["assoc_date"].append({"type": date_type,"iso": {"not_before": not_before},"value": date})         

    # Check VIAF
    if pd.isnull(row["VIAF"]) == False:
         data["rel_con"].append({"label": row["Name.VIAF"], "uri": row["VIAF"], "source": "VIAF"})
    # Check LOC
    if pd.isnull(row["LOC"]) == False:
         data["rel_con"].append({"label": row["Name.LOC"], "uri": row["LOC"], "source": "LoC"})
    # Check HAF
    if pd.isnull(row["HAF"]) == False:
         data["rel_con"].append({"label": row["Name.HAF"], "uri": row["HAF"], "source": "HAF"})
    # Check Syriaca
    if pd.isnull(row["Syriaca"]) == False:
         data["rel_con"].append({"label": row["Name.Syriaca"], "uri": row["Syriaca"], "source": "Syriaca"})
    # Check Pinakes
    if pd.isnull(row["Pinakes"]) == False:
         data["rel_con"].append({"label": row["Name.Pinakes"], "uri": row["Pinakes"], "source": "Pinakes"})
    # Check Notes
    if pd.isnull(row["Notes"]) == False:
         data["note"].append({"type": "admin", "value": row["Notes"]})

    # Check to see if json directory exists if not create it
    if not os.path.exists("json"):
        os.makedirs("json")

    # Export JSON
    with open(f'json/{local_id}.json', 'w+') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
    
# Check to see if user entered path to csv file
try:
    csv_file = pd.read_csv(sys.argv[1])    
except Exception as e:
    print("ERROR: Please enter the path to the CSV you would like to transform", str(e))

# run transformation script
for i, row in csv_file.iterrows():
        transform_input(row)