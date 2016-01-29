from subprocess import Popen, PIPE
import argparse

def user_func(args):
    if args.subcommand == 'add':
        # print "User Add %s to %s in the %s role" % (args.user, args.project, args.role)
        command = ['openstack', 'role', 'add', '--user', args.user, '--project', args.project, args.role]
        # print command
        pipe = Popen(command, stdout = PIPE)
        stdout = pipe.communicate()[0]
        print stdout

    if args.subcommand == 'rm':
        pass

def users_func(args):
    if args.subcommand == 'add':
        # print "Users add from %s" % (args.users)
        with open(args.file) as f:
            for line in f:
                user, project = line.split(':', 1)
                args = argparse.Namespace()
                args.user = '"' + user.strip() + '"'
                args.project = '"' + project.strip() + '"'
                args.role = 'user'
                args.subcommand = 'add'
                user_func(args)
    if args.subcommand == 'rm':
        pass
