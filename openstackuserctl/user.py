def user_func(args):
    if args.subcommand == 'add':
        print "User Add %s to %s in the %s role" % (args.user, args.project, args.role)
    if args.subcommand == 'rm':
        pass
