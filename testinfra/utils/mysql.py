def generate_mysql_command(loginpath=None, user=None, password=None, host=None, port=None, socket=None, no_header=True):
    mysqlcomm = "mysql "

    if loginpath is not None:
        mysqlcomm += " --login-path={}".format(loginpath)
    else:
        mysqlcomm += " --user={}".format(user)
        if password is not None:
            mysqlcomm += " --password={}".format(password)
        if host is not None:
            mysqlcomm += " --host={}".format(host)
        else:
            mysqlcomm += " --socket={}".format(socket)
        mysqlcomm += " --port={}".format(port)

    mysqlcomm += " -B"

    if no_header:
        mysqlcomm += " -N"

    return mysqlcomm
