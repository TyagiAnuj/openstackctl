from subprocess import Popen, PIPE

def user_func(args):
    if args.subcommand == 'add':
        # print "User Add %s to %s in the %s role" % (args.user, args.project, args.role)
        command = ['openstack', 'role', 'add', '--user', args.user, '--project', args.project, args.role]
        pipe = Popen(command, stdout = PIPE)
        stdout = pipe.communicate()[0]
        print stdout

    if args.subcommand == 'rm':
        pass
