def project_func(args):
    if args.subcommand == 'create':
        print "Project Create %s - %s" % (args.project, args.desc)
    if args.subcommand == 'delete':
        pass
