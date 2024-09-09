"""
Description: 
Author: Ngozi Harrison
Date Created: July 18, 2024
Version: 1.0
"""

# import the required dependencies
import pandas as pd, json, sys, numpy as np, os

works_directory = "data/works"
agents_directory = "data/agents"
if not os.path.exists(works_directory):
    os.makedirs(works_directory)

if not os.path.exists(agents_directory):
    os.makedirs(agents_directory)

# This is the script that transforms each row of the provided csv into a json document formatted accrding to the cross-walk schema
def transform_input_agent(row):
    # First pull out the basic columns associated with the row
    ark = str(row["ARK"])
    type = row["Type"]
    name = row["Name"]
    gender = row["Gender"]
    date = row["Dates"]
    
    #template for building JSON document according to cross-walk schema https://airtable.com/apptwZzt3XnHrd0bv/tblsKf3bUA04XMUhc/viwsPbKs24Fifny8K?blocks=hide
    base_template_schema = f'''{{
    "ark": "{ark}",
    "type": "{type}",
    "pref_name": "{name}",
    "alt_name": [],
    {'"gender": "",' if pd.isnull(row["Gender"]) == False else ""}
    {'"birth": "",' if pd.isnull(row["Dates.type"]) == False and row["Dates.type"] == "birth" else ""}
    {'"death": "",' if pd.isnull(row["Dates.type"]) == False and row["Dates.type"] == "death" else ""}
    {'"floruit": "",' if pd.isnull(row["Dates.type"]) == False and row["Dates.type"] == "floruit" else ""}
    "rel_con": []}}'''
    
    # Load base JSON template into JSON object
    data = json.loads(base_template_schema)
    
    # Grab alternate names and append
    alt_names = []
    if pd.isnull(row["AKA"]) == False:
         alt_names = row["AKA"].split(";")
    if pd.isnull(row["NS Name"]) == False:
         alt_names = alt_names + row["NS Name"].split(";")
    data["alt_name"] = [x.strip() for x in alt_names]

    # Append gender if it exists

    if pd.isnull(row["Gender"]) == False:
         data["gender"] = gender
 
    # Check to see if there is a date normalized with before and after
    if "/" in str(row["Dates.normalized"]):
        not_before = str(row["Dates.normalized"]).split("/")[0].rjust(4, "0")
        not_after = str(row["Dates.normalized"]).split("/")[1].rjust(4, "0")
        if pd.isnull(row["Dates.type"]) == False and row["Dates.type"] == "floruit":
             data["floruit"] = {"value": date, "iso": {"not_before": not_before, "not_after": not_after}}         
        if pd.isnull(row["Dates.type"]) == False and row["Dates.type"] == "birth":
             data["birth"] = {"value": date, "iso": {"not_before": not_before, "not_after": not_after}}
        if pd.isnull(row["Dates.type"]) == False and row["Dates.type"] == "death":
             data["death"] = {"value": date, "iso": {"not_before": not_before, "not_after": not_after}}        
    else:
        not_before = str(row["Dates.normalized"]).split("/")[0].rjust(4, "0")
        if pd.isnull(row["Dates.type"]) == False and row["Dates.type"] == "floruit":
             data["floruit"] = {"value": date, "iso": {"not_before": not_before}}         
        if pd.isnull(row["Dates.type"]) == False and row["Dates.type"] == "birth":
             data["birth"] = {"value": date, "iso": {"not_before": not_before}}
        if pd.isnull(row["Dates.type"]) == False and row["Dates.type"] == "death":
             data["death"] = {"value": date, "iso": {"not_before": not_before}}     

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
    


    # Export JSON
    with open(f'{agents_directory}/{ark.split("/")[2]}.json', 'w+') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)


# Function to tranform a work
def transform_input_work(row):
    # First pull out the basic columns associated with the row
    ark = str(row["ARK"])
    name = row["Uniform title"]
    normalized_date = ""
    

    
    
    if pd.isnull(row["Date.normalized"]) == False:
        normalized_date = str(row["Date.normalized"])
   

    
    #template for building JSON document according to cross-walk schema https://airtable.com/apptwZzt3XnHrd0bv/tblsKf3bUA04XMUhc/viwsPbKs24Fifny8K?blocks=hide
    base_template_schema = f'''{{
    "ark": "{ark}",
    "pref_title": "{name}",
    {'"orig_lang": "",' if pd.isnull(row["Original Language"]) == False else ""}
    {'"orig_lang_title": "",' if pd.isnull(row["Original Language Title"]) == False else ""}
    "alt_title": [],
    "genre": [],
    {'"creator": [],' if pd.isnull(row["Author"]) == False else ""}
    {'"creation": [],' if pd.isnull(row["Date.normalized"]) == False else ""}
    "rel_con": [],
    "refno": [],
    "bib": []

     }}''' 

    # Load base JSON template into JSON object
    data = json.loads(base_template_schema)
    
    # Check to see if there is an original lang if so add to object
    if pd.isnull(row["Original Language"]) == False:
         data["orig_lang"] = {"id": row["Original Language"], "label": row["Original Language Label"]}
    
    if pd.isnull(row["Original Language Title"]) == False:
         data["orig_lang_title"] = row["Original Language Title"]
    
    
    # Grab alternate titles and append
    alt_titles = []
    if pd.isnull(row["AKA"]) == False:
         alt_titles = row["AKA"].split(";") 
    if pd.isnull(row["NS Title"]) == False:
         alt_titles = alt_titles + row["NS Title"].split(";")
    data["alt_title"] = [x.strip() for x in alt_titles]
        
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
         data["refno"] = [{"label": row['Title.CPG'], "idno": row["CPG"], "source": "CPG"}]
         
         
     # Add dates
    if "/" in normalized_date:
        not_before = normalized_date.split("/")[0].rjust(4, "0")
        not_after = normalized_date.split("/")[1].rjust(4, "0")
        data["creation"] = {"value": row["Date.creation"], "iso": {"not_before": not_before, "not_after": not_after}}         
    elif normalized_date:
        not_before = normalized_date.split("/")[0].rjust(4, "0")
        data["creation"] = {"value": row["Date.creation"], "iso": {"not_before": not_before}}   

    # Check author role
    if pd.isnull(row["Author"]) == False:
         data["creator"].append({"id": row["Author"], "role":"author"})


    # Check to see if json directory exists if not create it
 

    # Export JSON
    with open(f'{works_directory}/{ark.split("/")[2]}.json', 'w+') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
    
# Check to see if user entered path to csv file and valid command line argument
try:
    csv_file = pd.read_csv(sys.argv[1], dtype={'CPG': 'string'}) # explicitly declaring CPG as string data to avoid handling as a number
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
            