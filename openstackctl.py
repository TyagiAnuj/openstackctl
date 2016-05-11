#! /usr/bin/env python

#This script can be used to create projects, networks and add users to projects.
#The details can be given either directly or can be stored in a file and provided as argument.

#sdc-projects-manage project create -d "Description" project_name
#sdc-projects-manage projects create project_list_file

#sdc-projects-manage network create -s segementation_id -p project_name 
#sdc-projects-manage networks create network_list_file

#sdc-projects-manage user add/rm -u user_name -p proejct_name -r user_role
#sdc-projects-manage user add/rm -u user_name -p proejct_name
#sdc-projects-manage users add/rm user_list_file

#For Projects creation, file should contain project_name : description (optional)
#For network creation, file should contain segmentation_id : project_name
#For adding users, file should contain user_name : project_name

#For network deletion only project name is needed.
#sdc-projects-manage network delete -p project_name
#sdc-projects-manage networks delete file_name (file will contain project names only)

#There are a few assumptions made 
# 1. Network_Name will always be like nw_project_name_vlan_id (ex - vlan_id = 328, project = "Cloud Demo_project"; project_name = cloud_demo_project
#                                                                network_name = nw_cloud_demo_project_328)
# 2. Network Address = 10.41.(vlan_id-300).0/24
# 3. Gateway = 10.41.(vlan_id-300).1
# 4. Allocation_range = start=10.41.(vlan_id-300).11,end=10.41.(vlan_id-300).254



import os
import argparse

from openstackctl.project import *
from openstackctl.user import *
from openstackctl.network import *

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='OpenStack user and project management.')
    subparsers = parser.add_subparsers(dest='command')

    project_parser = subparsers.add_parser('project')
    project_parser.set_defaults(func=project_func)
    projects_parser = subparsers.add_parser('projects')
    projects_parser.set_defaults(func=projects_func)
    user_parser = subparsers.add_parser('user')
    user_parser.set_defaults(func=user_func)
    users_parser = subparsers.add_parser('users')
    users_parser.set_defaults(func=users_func)
    network_parser = subparsers.add_parser('network')
    network_parser.set_defaults(func=network_func)
    networks_parser = subparsers.add_parser('networks')
    networks_parser.set_defaults(func=networks_func)    

    project_subparsers = project_parser.add_subparsers(dest='subcommand')
    projects_subparsers = projects_parser.add_subparsers(dest='subcommand')
    user_subparsers = user_parser.add_subparsers(dest='subcommand')
    users_subparsers = users_parser.add_subparsers(dest='subcommand')
    network_subparsers = network_parser.add_subparsers(dest='subcommand')
    networks_subparsers = networks_parser.add_subparsers(dest='subcommand')

    project_create_parser = project_subparsers.add_parser('create')
    # project_rm_parser = project_subparsers.add_parser('rm')

    projects_create_parser = projects_subparsers.add_parser('create')
    # projects_rm_parser = projects_subparsers.add_parser('rm')

    user_add_parser = user_subparsers.add_parser('add')
    user_rm_parser = user_subparsers.add_parser('rm')

    users_create_parser = users_subparsers.add_parser('add')
    users_rm_parser = users_subparsers.add_parser('rm')

    network_create_parser = network_subparsers.add_parser('create')
    network_delete_parser = network_subparsers.add_parser('delete')

    networks_create_parser = networks_subparsers.add_parser('create')
    networks_delete_parser = networks_subparsers.add_parser('delete')

    project_create_parser.add_argument('-d', '--description', type=str, required=False,
                                       help='Description of the project being created.',
                                       metavar='"Snapdeal OpenStack Project"',
                                       default='""', dest='desc')
    project_create_parser.add_argument('project', type=str,
                                       help='The name of the project to be created.',
                                       metavar='project_name')


    projects_create_parser.add_argument('file', type=str,
                                        help='Filename of file containing list of projects to be created, along with description.',
                                       metavar='projectlist_file')


    user_add_parser.add_argument('-u', '--user', type=str, required=True,
                                 help='The user to be added.',
                                 metavar='firstname.lastname', dest='user')
    user_add_parser.add_argument('-p', '--project', type=str, required=True,
                                 help='The name of the project user is to be added to.',
                                 metavar='project_name', dest='project')
    user_add_parser.add_argument('-r', '--role', type=str, required=False,
                                 help='The role the user is being assigned.',
                                 metavar='user_role', default='user', dest='role')

    users_create_parser.add_argument('file', type=str,
                                     help='Filename of file containing list of users to be added, along with project name.',
                                     metavar='userlist_file')
    users_create_parser.add_argument('-r', '--role', type=str, required=False,
                                     help='The role the users are being assigned.',
                                     metavar='user_role', default='user', dest='role')

    user_rm_parser.add_argument('-u', '--user', type=str, required=True,
                                 help='The user to be removed.',
                                 metavar='firstname.lastname', dest='user')
    user_rm_parser.add_argument('-p', '--project', type=str, required=True,
                                 help='The name of the project user is to be removed from.',
                                 metavar='project_name', dest='project')
    user_rm_parser.add_argument('-r', '--role', type=str, required=False,
                                 help='The role the user is assigned to.',
                                 metavar='user_role', default='user', dest='role')

    users_rm_parser.add_argument('file', type=str,
                                 help='Filename of file containing list of users to be removed, along with project name.',
                                 metavar='userlist_file')
    users_rm_parser.add_argument('-r', '--role', type=str, required=False,
                                 help='The role the users are dissociated with.',
                                 metavar='user_role', default='user', dest='role')

    network_create_parser.add_argument('-s', '--segmentation_id', type=str, required=True,
                                       help='Segmentation_id of the network to be created.',
                                       metavar='segmentation_id', dest='seg_id')
    network_create_parser.add_argument('-p', '--project', type=str, required=True,
                                       help='The name of the Project network is to be added.',
                                       metavar='project_name', dest='project') 
    networks_create_parser.add_argument('file', type=str,
                                        help='Filename of the file containing list of segmentation_id and projects for which network has to be created.',
                                        metavar='networklist_file')

    network_delete_parser.add_argument('-p', '--project', type=str, required=True,
                                       help='The name of the Project network of which is to be deleted.',
                                       metavar='project_name', dest='project')
    networks_delete_parser.add_argument('file', type=str,
                                        help='Filename of the file containing list of projects for which network is to be deleted.',
                                        metavar='networklist_file')
    
    args = parser.parse_args()
    args.func(args)
