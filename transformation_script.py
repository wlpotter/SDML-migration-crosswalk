"""
Description: 
Author: Ngozi Harrison
Date Created: July 18, 2024
Version: 1.0
"""

# import the required dependencies
import pandas as pd, json, sys

try:
    csv_file = sys.argv[1]
except:
    print("ERROR: Please enter the path to the CSV you would like to transform")

def transform_input(row):
    template_schema = """{
    "id": ,
    "type": "individual",
    "pref_name": "Abū Qurrah, Thāwdhūrus, approximately 750-825",
    "alt_name": [
        {
            "lang": "English",
            "value": "Theodore Abū Qurrah"
        },
        {
            "lang": "English",
            "value": "Theodore Bishop of Harran"
        },
        {
            "lang": "Arabic",
            "value": "ثاوذورس أبي قرة"
        }
    ],
    "gender": "male",
    "rel_con": [
        {
            "label": "Abū Qurrah, Thāwdhūrus, approximately 750-825",
            "uri": "http://viaf.org/viaf/116159414",
            "source": "VIAF"
        },
        {
            "label": "Abū Qurrah, Thāwdhūrus, approximately 750-825",
            "uri": "http://id.loc.gov/authorities/names/n85000719",
            "source": "LoC"
        },
        {
            "label": "Abū Qurrah, Thāwdhūrus, approximately 750-825",
            "uri": "https://w3id.org/haf/person/515032103483",
            "source": "HAF"
        },
        {
            "label": "Theodore Abu Qurra",
            "uri": "http://syriaca.org/person/782",
            "source": "Syriaca"
        }
    ],
    "assoc_date": [
        {
            "type": "floruit",
            "iso": {
                "not_before": "0725",
                "not_after": "0850"
            },
            "value": "approximately 750-825"
        }
    ]
}"""
    with open(f'agent_transform_{name}', 'w') as f:
        json.dump(data, f)