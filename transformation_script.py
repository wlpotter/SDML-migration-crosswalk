"""
Description: 
Author: Ngozi Harrison
Date Created: July 18, 2024
Version: 1.0
"""

# import the required dependencies
import pandas as pd, json, sys, numpy as np, os

# This is the script that transforms each row of the provided csv into a json document formatted accrding to the cross-walk schema
def transform_input_agent(row):
    # First pull out the basic columns associated with the row
    ark = str(row["ARK"])
    type = row["Type"]
    name = row["Name"]
    gender = row["Gender"]
    date_type = row["Dates.type"]
    date = row["Dates"]
    
    #template for building JSON document according to cross-walk schema https://airtable.com/apptwZzt3XnHrd0bv/tblsKf3bUA04XMUhc/viwsPbKs24Fifny8K?blocks=hide
    base_template_schema = f'''{{
    "ark": {ark},
    "type": "{type}",
    "pref_name": "{name}",
    "alt_name": [],
    "gender": "{gender}",
    "rel_con": [],
    "assoc_date": []}}'''
    
    # Load base JSON template into JSON object
    data = json.loads(base_template_schema)
    
    # Check if there are associated alternate names and if so append them to the json object
    if pd.isnull(row["AKA"]) == False:
        alt_names = zip(row["AKA"].split(" ; "), row["Language.AKA"].split(" ; "))
        for (name, lang) in alt_names:
            data["alt_name"].append({"lang": lang.strip(), "value": name.strip()})    
    if pd.isnull(row["NS Name"]) == False:
            alt_names = zip(row["NS Name"].split(" ; "), row["Language.NS Name"].split(" ; "))
            for (name, lang) in alt_names:
                data["alt_name"].append({"lang": lang.strip(), "value": name.strip()})

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
    

    # Check to see if json directory exists if not create it
    if not os.path.exists("json"):
        os.makedirs("json")

    # Export JSON
    with open(f'data/agents/{ark.split("/")[2]}.json', 'w+') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)


# Function to tranform a work
def transform_input_work(row):
    # First pull out the basic columns associated with the row
    ark = str(row["ARK"])
    name = row["Uniform title"]
    creation_date = ""
    normalized_date = ""
    

    

    if pd.isnull(row["Date.creation"]) == False:
        creation_date = row["Date.creation"]
    
    
    if pd.isnull(row["Date.normalized"]) == False:
        normalized_date = row["Date.normalized"]
   

    
    #template for building JSON document according to cross-walk schema https://airtable.com/apptwZzt3XnHrd0bv/tblsKf3bUA04XMUhc/viwsPbKs24Fifny8K?blocks=hide
    base_template_schema = f'''{{
     "ark": {ark},
    "pref_title": "{name}",
    "alt_title": [],
    {'"orig_lang": "",' if pd.isnull(row["Original Language"]) == False else ""}
    {'"orig_lang_title": "",' if pd.isnull(row["Original Language Title"]) == False else ""}
    "genre": [],
    "rel_con": [],
    "bib": [],
    "assoc_date": [],
    "assoc_name": []

     }}''' 

    # Load base JSON template into JSON object
    data = json.loads(base_template_schema)
    
    # Check to see if there is an original lang if so add to object
    if pd.isnull(row["Original Language"]) == False:
         data["orig_lang"] = row["Original Language"]
    
    if pd.isnull(row["Original Language Title"]) == False:
         data["orig_lang_title"] = row["Original Language Title"]
    
    # Grab alternate titles and append
    if pd.isnull(row["AKA"]) == False:
        alt_names = zip(row["AKA"].split(" ; "), row["Language.AKA"].split(" ; "))
        for (name, lang) in alt_names:
            data["alt_title"].append({"lang": lang.strip(), "value": name.strip()})    
    if pd.isnull(row["NS Title"]) == False:
            alt_names = zip(row["NS Title"].split(" ; "), row["Language.NS Title"].split(" ; "))
            for (name, lang) in alt_names:
                data["alt_title"].append({"lang": lang.strip(), "value": name.strip()})

    if pd.isnull(row["Genres"]) == False:
        genres = row["Genres"].split(",")
        for genre in genres:
            data["genre"].append(genre.strip())  
    
    # Check VIAF
    if pd.isnull(row["VIAF"]) == False:
         data["rel_con"].append({"label": row["Title.VIAF"], "uri": row["VIAF"], "source": "VIAF"})
    # Check LOC
    if pd.isnull(row["LOC"]) == False:
         data["rel_con"].append({"label": row["Title.LOC"], "uri": row["LOC"], "source": "LoC"})
    # Check HAF
    if pd.isnull(row["HAF"]) == False:
         data["rel_con"].append({"label": row["Title.HAF"], "uri": row["HAF"], "source": "HAF"})
    # Check Syriaca
    if pd.isnull(row["Syriaca"]) == False:
         data["rel_con"].append({"label": row["Title.Syriaca"], "uri": row["Syriaca"], "source": "Syriaca"})
    # Check Pinakes
    if pd.isnull(row["Pinakes"]) == False:
         data["rel_con"].append({"label": row["Title.Pinakes"], "uri": row["Pinakes"], "source": "Pinakes"})

    # Add CPG fields
    if pd.isnull(row["CPG"]) == False:
         data["bib"].append({"ark": int(row["biblId.CPG"]), "type": "refno", "range": f"s.v. {int(row['CPG'])}, {row['Title.CPG']}", "url": f"https://clavis.brepols.net/clacla/OA/Link.aspx?clavis=cpg&number={int(row['CPG'])}"})

     # Add dates
    if "/" in normalized_date:
        not_before = normalized_date.split("/")[0].rjust(4, "0")
        not_after = normalized_date.split("/")[1].rjust(4, "0")
        data["assoc_date"].append({"type": "creation","iso": {"not_before": not_before, "not_after": not_after},"value": row["Date.creation"]})         
    elif normalized_date:
        not_before = normalized_date.split("/")[0]
        data["assoc_date"].append({"type": "creation","iso": {"not_before": not_before},"value":row["Date.creation"]})   

    # Check author role
    if pd.isnull(row["Author"]) == False:
         data["assoc_name"].append({"ark": int(row["Author"]), "role":"author"})


    # Check to see if json directory exists if not create it
    if not os.path.exists("json"):
        os.makedirs("json")

    # Export JSON
    with open(f'data/works/{ark.split("/")[2]}', 'w+') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
    
# Check to see if user entered path to csv file and valid command line argument
try:
    csv_file = pd.read_csv(sys.argv[1])
    type = sys.argv[2]
    if type not in ["agents", "works"]:
            raise ValueError
except OSError:
    print("ERROR: Incorrect path to csv, the file may not exist in the provided directory")
except IndexError:
     print("Please be sure to enter both command arguments the path to the CSV you would like to transform and the type (agents or works)")
except ValueError:
     print(f"'{type}' is not a valid type, must be 'agents' or 'works'")

# run transformation script

if type == "agents":
    for i, row in csv_file.iterrows():
            transform_input_agent(row)
elif type == "works":
     for i, row in csv_file.iterrows():        
            transform_input_work(row)
            