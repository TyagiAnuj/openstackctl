from subprocess import Popen, PIPE
import argparse

def user_func(args):
    if args.subcommand == 'add':
        command = ['openstack', 'role', 'add', '--user', args.user, '--project', args.project, args.role]
        pipe = Popen(command, stdout = PIPE)
        stdout = pipe.communicate()[0]
        print stdout
        print "User '{}' added to '{}' project in '{}' role.".format(args.user, args.project, args.role)
    
    if args.subcommand == 'rm':
        print args.project
        command = ['openstack', 'role', 'remove', '--user', args.user, '--project', args.project, args.role]
        pipe = Popen(command, stdout=PIPE)
        stdout = pipe.communicate()[0]
        print "'{}' in role '{}' removed.".format(args.user, args.role) 

def users_func(args):
    try:
        if args.subcommand == 'add':
            with open(args.file) as f:
                for line in f:
                    user, project = line.split(':', 1)
                    arg = argparse.Namespace()
                    arg.user = user.strip()
                    arg.project = project.strip()
                    arg.subcommand = 'add'
                    arg.role = args.role
                    user_func(arg)
        if args.subcommand == 'rm':
            with open(args.file) as f:
	        for line in f:
		    user, project = line.split(':', 1)
		    arg = argparse.Namespace()
		    arg.user = user.strip()
		    arg.project = project.strip()
		    arg.subcommand = 'rm'
                    arg.role = args.role
                    user_func(arg)
    except IOError:
        print "No file with filename '{}' found.".format(args.file)
