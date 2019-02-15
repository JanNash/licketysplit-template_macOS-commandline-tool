#!/usr/bin/env python3

import os
import logging
import subprocess
from git import Repo


def main():
    repo = Repo(os.path.curdir)
    _git = repo.git

    logging.info('[pre-push] > Saving all local changes in a temporary stash')
    # TODO: This should maybe actually use a uuid or something else unique, I guess...
    _git.stash('save', '-u', '[post-merge] Temporary stash, do not pop or delete')

    xcode_project_name = 'PRODUCTNAME.xcodeproj'

    logging.info('[pre-push] > Running synx')
    result = subprocess.run(['synx', '--prune', xcode_project_name], stdout=subprocess.PIPE)

    logging.info('[pre-push] > Running xunique')


if __name__ == '__main__':
    main()
