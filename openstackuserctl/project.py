from subprocess import Popen, PIPE

def project_func(args):
    if args.subcommand == 'create':
        # print "Project Create %s - %s" % (args.project, args.desc)
        command = ['openstack', 'project', 'create', '--description', args.desc, args.project]
        print command
        pipe = Popen(command, stdout = PIPE)
        stdout = pipe.communicate()[0]
        print stdout
    if args.subcommand == 'delete':
        pass
