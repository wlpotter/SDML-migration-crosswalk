# SDML-migration-crosswalk
Welcome to the code repository of tools for SMDL migration created by the UCLA Digital Library!

Using the [cross-walk documentation](https://airtable.com/apptwZzt3XnHrd0bv/shrb0utxqvcVEStOP), the script  takes a CSV input of SMDL name authority records and transforms them into JSON documents compliant with the Data Portal JSON schema for agents.


### Contents
- [Setup](#setup)
- [Usage](#usage)


# Setup

### Requirements
- python3.6
- pandas
- numpy

**Install dependencies**

```bash
pip3 install pandas numpy
```

# Usage

Enter the following command into the command prompt followed by the name of the csv file
 ```python 
python3 transformation_script.py /path/to/csv/file/file.csv
 ```

after running the finished json files will be generated in a folder called ```json``` and each file will be named after the respective local id from the CSV