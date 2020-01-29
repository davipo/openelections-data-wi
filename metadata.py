"""Convert elections_metadata.json to CSV"""

import csv
import json
import os
import sys


fieldnames = [
    'id', 'state', 'start_date', 'end_date', 
    'race_type', 'special', 'primary_type', 'primary_note',
    
    'prez', 'senate', 'house', 'gov', 'state_officers', 'state_leg', 
    
    'portal_link', 'direct_links',
    
    'county_level', 'county_level_status',
    'precinct_level', 'precinct_level_status',
    'cong_dist_level', 'cong_dist_level_status',
    'state_leg_level', 'state_leg_level_status',
    'state_level', 'state_level_status',     
    
    'result_type',
    'absentee_and_provisional', 
    'user_fullname',
]



if __name__ == "__main__":
    json_filepath = sys.argv[1]
    
    path, ext = os.path.splitext(json_filepath)
    csvfilepath = path + '.csv'
    outfile = open(csvfilepath, 'w')
    writer = csv.DictWriter(outfile, fieldnames, extrasaction='ignore')
    writer.writeheader()
    
    with open(json_filepath) as metadata_file:
        metadata = json.load(metadata_file)
    elections = metadata['objects']

### Getting the fieldnames
#     for field in elections[0]:
#         print("'" + field + "', ", end='')
    
    for election in elections:
        election['state'] = election['state']['postal']
        election['direct_links'] = ', \n'.join(election['direct_links'])
        writer.writerow(election)

