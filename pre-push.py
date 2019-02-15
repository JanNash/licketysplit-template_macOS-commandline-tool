#!/usr/bin/env python3

import logging
import os
import subprocess
import sys
from git import Repo


def log_info(msg):
    logging.info('[pre-push] > {}'.format(msg))

def run_cmd_args(cmd_args):
    logging.debug(' >>> {}'.format(' '.join(cmd_args)))
    proc = subprocess.run(cmd_args, encoding='utf-8', stdout=subprocess.PIPE)
    for line in proc.stdout.split('\n'):
        logging.debug(line)


def main():
    logging.basicConfig(level=logging.INFO)
    logging.getLogger('git').setLevel(logging.WARNING)

    curdir = os.path.curdir
    repo = Repo(curdir)
    _git = repo.git

    changes_stashed = False

    if repo.is_dirty():
        log_info('Saving all local changes in a temporary stash')
        # TODO: This should maybe actually use a uuid or something else unique, I guess...
        git_stash_message = '[pre-push] Temporary stash, do not pop or delete'
        _git.stash('save', '-u', git_stash_message)
        changes_stashed = True

    xcode_project_name = 'PRODUCTNAME.xcodeproj'

    log_info('Running synx')
    run_cmd_args(['synx', '--prune', xcode_project_name])

    log_info('Running xunique')
    run_cmd_args(['xunique', xcode_project_name])

    if not repo.is_dirty():
        log_info('No changes were made')
        sys.exit(0)
    
    log_info('Adding changes made by hook')
    git.add(curdir)

    log_info('Committing changes made by hook')
    git.commit('--no-verify', '-m', '[pre-push] Run synx and xunique')
    
    if changes_stashed:
        log_info('Popping temporary stash')

        stash_ref = _git.log('-g', 'stash', '--grep={}'.format(stash_message), '--pretty=format:%gd')
        git.stash('pop', stash_ref)


if __name__ == '__main__':
    main()
