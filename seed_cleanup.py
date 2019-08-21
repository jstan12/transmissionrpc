#!/usr/bin/python

## Remove old seeds from Transmission and delete files from the seed location

import time
import os, sys
import datetime
import os.path as path
import transmissionrpc

# Transmission client
client = transmissionrpc.Client(
    address='127.0.0.1',
    port='9091',
    user='',
    password=''
    )
# Seed directory
seed_download_dir = '/media/1TBWDD/completed/'

script_dir = os.path.dirname(__file__)
# Current time epoch
now = time.time()
# List of all torrents in transmission
torrent_list = client.get_torrents()
# Single torrent
torrent = client.get_torrent
# Begin logging
log_file = os.path.join(script_dir,'cleanup.log')
log = open(log_file, 'a')
timestamp = '[{:%Y-%m-%d %H:%M:%S}]'.format(datetime.datetime.now())
print >> log, timestamp +  ': ' + 'Checking torrents for cleanup'
log.close()

for t in torrent_list:
# Get torrent by ID in transmission

    # Torrent attributes
    done_date = torrent(t.id).doneDate
    seed_time = now - done_date
    ratio = torrent(t.id).ratio
    seed_files_dict = torrent(t.id).files() 
    
    # 30 days seed time
    if seed_time >= 2592000: 
        # Log removed torrent
        log = open(log_file, 'a')
        timestamp = '[{:%Y-%m-%d %H:%M:%S}]'.format(datetime.datetime.now())
        print >> log, timestamp + ': Removed ' + torrent(t.id).name
        log.close()
        # Get file name
        for y in seed_files_dict:
            fname = (seed_files_dict[y]['name']) 
            # Verify file exists in directory 
            seed_file = os.path.isfile(seed_download_dir + fname) 
            # Delete file
            if seed_file == 1:
                print fname
                os.remove(seed_download_dir + fname)

        # Remove the torrent from transmission
        client.remove_torrent(t.id)

# Clean up empty dirs/subdirs
empty_dirs = 1
while (empty_dirs > 0): 
    empty_dirs = 0
    for dirpath, dirnames, files in os.walk(seed_download_dir):
        if not (files or dirnames):
            empty_dirs = empty_dirs + 1
            os.rmdir(dirpath)
            # Log removed folder
            log = open(log_file, 'a')
            timestamp = '[{:%Y-%m-%d %H:%M:%S}]'.format(datetime.datetime.now())
            print >> log, timestamp + ': Removed ' + dirpath
            log.close()
