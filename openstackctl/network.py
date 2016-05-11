from subprocess import Popen, PIPE
import argparse
import re

def network_func(args):
    if args.subcommand == 'create':
        project_name = re.sub('[ -]', '_', args.project).lower()
        network_name = "nw_"+project_name+"_"+args.seg_id
        
        comm1 = ['openstack', 'project', 'list']
        pipe1 = Popen(comm1, stdout=PIPE)
        comm2 = ['grep', '-iw', args.project]
        pipe2 = Popen(comm2, stdin=pipe1.stdout, stdout=PIPE)
        p_id = pipe2.communicate()[0]
        try:
            project_id = p_id.split(" ")[1]
            command = ['neutron', 'net-create', network_name, '--provider:physical_network', 'physnet1', '--provider:network_type', 'vlan', 
                       '--provider:segmentation_id', args.seg_id, '--tenant-id', project_id]
            pipe = Popen(command, stdout = PIPE)
            stdout = pipe.communicate()[0]
            print stdout

            vlan_id = str(int(args.seg_id) - 600)
            subnet_name = "subnet_"+project_name+"_"+args.seg_id
            network_address = "10.42."+vlan_id+".0/24"
            gateway = "10.42."+vlan_id+".1"

            allocation_pool = "start=10.42."+vlan_id+".11,end=10.42."+vlan_id+".254"

            command_subnet = ['neutron', 'subnet-create', network_name, network_address, '--name', subnet_name, '--tenant-id', project_id, '--allocation-pool',
                              allocation_pool, '--enable-dhcp', '--gateway', gateway]
            pipe_subnet = Popen(command_subnet, stdout=PIPE)
            stdout_subnet = pipe_subnet.communicate()[0]
            print stdout_subnet
	except IndexError:
	    print "ERROR: Openstack No tenant with a name or ID of '{}' exists.".format(args.project)
 
    if args.subcommand == 'delete':
        try:
            project_name = re.sub('[ -]', '_', args.project).lower()
            print args.project
            comm1 = ['neutron', 'net-list']
            pipe1 = Popen(comm1, stdout=PIPE)
            comm2 = ['grep', '-i', project_name]
            pipe2 = Popen(comm2, stdin=pipe1.stdout, stdout=PIPE)
            n_id = pipe2.communicate()[0]
            subnet_id = n_id.split()[5]
            net_id = n_id.split()[1]
            command = ['neutron', 'subnet-delete', subnet_id]
            pipe = Popen(command, stdout=PIPE)
            stdout = pipe.communicate()[0]
            print stdout
            command_net = ['neutron', 'net-delete', net_id]
            pipe_net = Popen(command_net, stdout=PIPE)
            stdout_net = pipe_net.communicate()[0]
            print stdout_net
	except IndexError:
	    print "No network found for '{}' project.".format(args.project)
 


def networks_func(args):
    try:
        if args.subcommand == 'create':
            with open(args.file) as f:
                for line in f:
                    segmentation_id, projectname = line.split(':', 1)
                    args = argparse.Namespace()
                    args.seg_id = segmentation_id.strip()
                    args.project = projectname.strip()
                    args.subcommand = 'create'
                    network_func(args)
        if args.subcommand == 'delete':
            with open(args.file) as f:
                for line in f:
                    projectname = line
                    args = argparse.Namespace()
                    args.project = projectname.strip()
                    args.subcommand = 'delete'
                    network_func(args)
    except IOError:
        print "No file with filename '{}' found.".format(args.file)
