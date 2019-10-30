################################################################################################################################
#####                                           Script to Anonymize DataHub Logs                                           #####
##### from https://github.com/berkeley-dsep-infra/datahub-usage-analysis/blob/master/notebooks/01-anonimize-hub-logs.ipynb #####
################################################################################################################################

import hashlib
import hmac
import json
import dateutil
import secrets
import re

# Generate a HMAC key for salting the username
# This is only kept in memory, so we can not reverse this after this process dies
HMAC_KEY = secrets.token_bytes(32)

def parse_activity_line(line):
    """
    Parses a user server start/stop line from JupyterHub logs
    
    Returns a tuple of (timestamp, anonymized_username, action).
    
    timestamp is rounded out to the nearest hour for anonymization purposes.
    """
    lineparts = line.split()
    try:
        # Round all timestamp info to the hour to make it more anonymous
        ts = dateutil.parser.parse('{} {}'.format(lineparts[1], lineparts[2])).replace(minute=0, second=0, microsecond=0)
        user = lineparts[6].strip()
        userhash = hmac.new(HMAC_KEY, user.encode(), hashlib.sha512).hexdigest()

        action = lineparts[-1].strip()
    except IndexError:
        # Poor person's debugger!
        print(lineparts)
        raise
    return (ts, userhash, action)

def parse_puller_line(line):
    """
    Parses a redirect from nbgitpuller
    
    Returns a tuple of (timestamp, anonymized_username, accessed_url).
    
    timestamp is rounded out to the nearest hour for anonymization purposes.
    """
    lineparts = line.split()
    try:
        # Round all timestamp info to the hour to make it more anonymous
        ts = dateutil.parser.parse('{} {}'.format(lineparts[1], lineparts[2])).replace(minute=0, second=0, microsecond=0)
        
        try:
            user = re.search(r"\((\w+)@", lineparts[-2])[1]
            userhash = hmac.new(HMAC_KEY, user.encode(), hashlib.sha512).hexdigest()
        except TypeError:
            try:
                user = re.search(r"\/spawn\/(\w+)\?", lineparts[-3])[1]
                userhash = hmac.new(HMAC_KEY, user.encode(), hashlib.sha512).hexdigest()
            except TypeError:
                # will use NULL for the user if there is no user
                userhash = "NULL"

        url = lineparts[7]
    except IndexError:
        # Poor person's debugger!
        print(lineparts)
        raise
    return (ts, userhash, url)

def generate_session_data(infile_path, outfile_path, min_entries_per_hour=0):
    """
    Generate user session data from JupyterHub logs in infile_path
    
    min_entries_per_hour is the minimum number of activity entries that must
    be present in each hour for the hour to be included in the output.
    """
    with open(infile_path) as infile, open(outfile_path, 'w') as outfile:
        current_hour_entries = []
        last_hour = None
        for l in infile:
            if 'seconds to' in l:
                timestamp, user, action = parse_activity_line(l)
                if last_hour is None:
                    last_hour = timestamp
                if timestamp == last_hour:
                    current_hour_entries.append(json.dumps({'timestamp': timestamp.isoformat(), 'user': user, 'action': action}))
                else:
                    if len(current_hour_entries) >= min_entries_per_hour:
                        outfile.write('\n'.join(current_hour_entries) + '\n')
                    else:
                        print(f'Skipped entry for {timestamp}: had less than {min_entries_per_hour} actions')
                    last_hour = timestamp
                    current_hour_entries = []

def generate_pull_data(infile_path, outfile_path, min_entries_per_hour=0):
    """
    Generate user pull data from JupyterHub logs in infile_path
    
    min_entries_per_hour is the minimum number of activity entries that must
    be present in each hour for the hour to be included in the output.
    """
    with open(infile_path) as infile, open(outfile_path, 'w') as outfile:
        current_hour_entries = []
        last_hour = None
        for l in infile:
            if '302 GET' in l:
                timestamp, user, action = parse_puller_line(l)
                if last_hour is None:
                    last_hour = timestamp
                if timestamp == last_hour:
                    current_hour_entries.append(json.dumps({'timestamp': timestamp.isoformat(), 'user': user, 'url': action}))
                else:
                    if len(current_hour_entries) >= min_entries_per_hour:
                        outfile.write('\n'.join(current_hour_entries) + '\n')
                    else:
                        print(f'Skipped entry for {timestamp}: had less than {min_entries_per_hour} actions')
                    last_hour = timestamp
                    current_hour_entries = []