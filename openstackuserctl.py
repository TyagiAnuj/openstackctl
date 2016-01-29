#! /usr/bin/env python

import os
import argparse

from openstackuserctl.project import *
from openstackuserctl.user import *


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='OpenStack user and project management.')
    subparsers = parser.add_subparsers(dest='command')

    project_parser = subparsers.add_parser('project')
    project_parser.set_defaults(func=project_func)
    user_parser = subparsers.add_parser('user')
    user_parser.set_defaults(func=user_func)

    project_subparsers = project_parser.add_subparsers(dest='subcommand')
    user_subparsers = user_parser.add_subparsers(dest='subcommand')


    project_create_parser = project_subparsers.add_parser('create')
    # project_rm_parser = project_subparsers.add_parser('rm')

    user_add_parser = user_subparsers.add_parser('add')
    # user_rm_parser = key_subparsers.add_parser('rm')


    project_create_parser.add_argument('-d', '--description', type=str, required=False,
                                       help='Description of the project being created.',
                                       metavar='"Snapdeal OpenStack Project"',
                                       default='""', dest='desc')
    project_create_parser.add_argument('project', type=str,
                                       help='The name of the project to be created.',
                                       metavar='project_name')


    user_add_parser.add_argument('-u', '--user', type=str, required=True,
                                 help='The user to be added.',
                                 metavar='jasper.india', dest='user')
    user_add_parser.add_argument('-p', '--project', type=str, required=True,
                                 help='The name of the project user is to be added to.',
                                 metavar='project_name', dest='project')
    user_add_parser.add_argument('-r', '--role', type=str, required=False,
                                 help='The role the user is being assigned.',
                                 metavar='user_role', default='user', dest='role')

    args = parser.parse_args()
    print args
    args.func(args)
