"""Convert elections_metadata.json to CSV, and back"""

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


def json_to_csv(filepath, outfilepath):
    infile = open(filepath)
    metadata = json.load(infile)
    outfile = open(outfilepath, 'w')
    writer = csv.DictWriter(outfile, fieldnames, extrasaction='ignore')
    writer.writeheader()
    elections = metadata['objects']
    for election in elections:
        election['state'] = election['state']['postal']
        election['direct_links'] = ', \n'.join(election['direct_links'])
        writer.writerow(election)


def csv_to_json(filepath, outfilepath):
    infile = open(filepath)
    elections = []
    for election in csv.DictReader(infile):
        election['state'] = {'postal': election['state']}
        direct_links = election['direct_links'].split(', \n')
        election['direct_links'] = direct_links
        convert_bools(election)
        elections.append(election)
    data = {'objects': elections}
    outfile = open(outfilepath, 'w')
    json.dump(data, outfile, sort_keys=True, indent=4)


def convert_bools(election):
    """Restore string values for booleans to boolean. Modifies parameter."""
    for key, value in election.items():
        if isinstance(value, basestring):
            value = value.lower()
            if value in ('true', '1'):
                election[key] = True
            elif value in ('false', '0'):
                election[key] = False


def print_usage_message(cmd):
    msg = """\nUsage: {} <filepath>\n
        Convert JSON metadata to CSV, or vice versa.
        If filepath ends in .json, write CSV metadata file.
        If filepath ends in .csv, write JSON metadata file.
    """.format(cmd)
    print(msg)


if __name__ == "__main__":
    cmd = sys.argv[0]
    if len(sys.argv) != 2:
        print_usage_message(cmd)
        sys.exit()
    
    filepath = sys.argv[1]
    path, ext = os.path.splitext(filepath)
    ext = ext.lower()
    if ext == '.json':
        outfilepath = path + '.csv'
        json_to_csv(filepath, outfilepath)
    elif ext == '.csv':
        outfilepath = path + '.json'
        csv_to_json(filepath, outfilepath)
    else:
        print_usage_message(cmd)
    
    