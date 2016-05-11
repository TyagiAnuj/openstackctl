from subprocess import Popen, PIPE
import argparse

def project_func(args):
    if args.subcommand == 'create':
        command = ['openstack', 'project', 'create', '--description', args.desc, args.project]
        pipe = Popen(command, stdout = PIPE)
        stdout = pipe.communicate()[0]
        print stdout
    if args.subcommand == 'delete':
        pass


def projects_func(args):
    try:
        if args.subcommand == 'create':
            with open(args.file) as f:
                for line in f:
                    projectname, description = line.split(':', 1)
                    args = argparse.Namespace()
                    args.project = projectname.strip()
                    args.desc = description.strip()
                    args.subcommand = 'create'
                    project_func(args)
        if args.subcommand == 'delete':
            pass
    except IOError:
	print "NO file with filename '{}' found.".format(args.file)
