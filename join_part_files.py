#!/usr/bin/env python
#
# Script to join numbered part files.

import sys
import os
import re

drop_dir = '/volume1/Download/NZBGet/dst'

def join_part_files(dir_path):
    all_files = os.listdir(dir_path)
    prefix = os.path.commonprefix(all_files)
    pattern = re.compile('^' + re.escape(prefix) + r'(\.[0-9]{3})?$')
    part_files = sorted(x for x in all_files if pattern.match(x))
    if not part_files:
        print 'No part files found in:', dir_path
        return False
    if prefix in part_files and prefix + '.000' in part_files:
        print 'Error: Ambiguous part files in:', dir_path
        return False
    prefix_path = os.path.join(dir_path, prefix)
    joining_path = prefix_path + '.joining'
    try:
        with open(joining_path, 'wb') as out:
            for part_name in part_files:
                print 'Joining:', part_name
                part_path = os.path.join(dir_path, part_name)
                with open(part_path, 'rb') as part:
                    data = part.read()
                out.write(data)
                try:
                    os.remove(part_path)
                except OSError as e:
                    print 'Error removing part file:', e
    except Exception:
        try:
            os.remove(joining_path)
        except OSError:
            pass
        raise
    os.rename(joining_path, prefix_path)
    return True

def join_part_files_in_dirs(dir_path):
    for filename in sorted(os.listdir(dir_path)):
        path = os.path.join(dir_path, filename)
        if os.path.isdir(path):
            join_part_files(path)

def main():
    if len(sys.argv) == 1:
        join_part_files_in_dirs(drop_dir)
    else:
        for path in sys.argv[1:]:
            join_part_files(path)

if __name__ == "__main__":
    main()
