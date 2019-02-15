#!/usr/bin/env python3

import os
import logging
import subprocess
from git import Repo


def main():
    logging.basicConfig(level=logging.DEBUG)

    repo = Repo(os.path.curdir)
    _git = repo.git

    logging.info('[pre-push] > Saving all local changes in a temporary stash')
    # TODO: This should maybe actually use a uuid or something else unique, I guess...
    _git.stash('save', '-u', '[post-merge] Temporary stash, do not pop or delete')

    xcode_project_name = 'PRODUCTNAME.xcodeproj'

    logging.info('[pre-push] > Running synx')
    synx_cmd_args = ['synx', '--prune', xcode_project_name]
    logging.debug(">>> {}".format(' '.join(synx_cmd_args)))
    synx_proc = subprocess.run(synx_cmd_args, encoding='utf-8', stdout=subprocess.PIPE)
    for line in synx_proc.stdout.split('\n'):
        logging.debug(line)

    logging.info('[pre-push] > Running xunique')


if __name__ == '__main__':
    main()
