#!/usr/bin/env python3

import logging
import os
import subprocess
import sys
from git import Repo


def log_info(msg):
    logging.info('[pre-push] > {}'.format(msg))

def log_debug(msg):
    logging.debug('[pre-push] > {}'.format(msg))    

def log_debug_git_cmd(cmd, cmd_args):
    logging.debug(' >>> {} {}'.format(cmd, ' '.join(cmd_args)))

def log_debug_git_cmd_output(output):
    for line in output:
        logging.debug(line)

def run_cmd_args_in_shell(cmd_args):
    logging.debug(' >>> {}'.format(' '.join(cmd_args)))
    proc = subprocess.run(cmd_args, encoding='utf-8', stdout=subprocess.PIPE)
    for line in proc.stdout.split('\n'):
        logging.debug(line)


def main():
    logging.basicConfig(level=logging.DEBUG)

    curdir = os.path.curdir
    log_debug('Current directory is {}'.format(curdir))
    repo = Repo(curdir)
    _git = repo.git

    changes_stashed = False

    if repo.is_dirty():
        log_info('Saving all local changes in a temporary stash')
        # TODO: This should maybe actually use a uuid or something else unique, I guess...
        git_stash_message = '[pre-push] Temporary stash, do not pop or delete'
        git_stash_cmd_args = ['save', '-u', git_stash_message]
        log_debug_git_cmd('git stash', git_stash_cmd_args)
        log_debug_git_cmd_output(_git.stash(*git_stash_cmd_args))
        changes_stashed = True

    xcode_project_name = 'PRODUCTNAME.xcodeproj'

    log_info('Running synx')
    run_cmd_args_in_shell(['synx', '--prune', xcode_project_name])

    log_info('Running xunique')
    run_cmd_args_in_shell(['xunique', xcode_project_name])

    if not repo.is_dirty():
        log_info('No changes were made')
        sys.exit(0)
    
    log_info('Adding changes made by hook')
    git_add_cmd_args = [curdir]
    log_debug_git_cmd('git add', git_add_cmd_args)
    log_debug_git_cmd_output(git.add(*git_add_cmd_args))

    log_info('Commiting changes made by hook')
    git_commit_cmd_args = ['--no-verify', '-m', '[pre-push] Run synx and xunique']
    log_debug_git_cmd('git commit', git_commit_cmd_args)
    log_debug_git_cmd_output(git.commit(*git_commit_cmd_args))
    
    if changes_stashed:
        log_info('Popping temporary stash')

        git_log_cmd_args = ['-g', 'stash', '--grep={}'.format(stash_message), '--pretty=format:%gd']
        log_debug_git_cmd('git log', git_log_cmd_args)
        stash_ref = _git.log(*git_log_cmd_args)
        log_debug_git_cmd_output(stash_ref)

        git_stash_cmd_args = ['pop', stash_ref]
        log_debug_git_cmd('git stash', git_stash_cmd_args)
        log_debug_git_cmd_output(git.stash(*git_stash_cmd_args))


if __name__ == '__main__':
    main()
