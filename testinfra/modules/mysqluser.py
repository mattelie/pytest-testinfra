from testinfra.modules.base import Module
from testinfra.utils.mysql import generate_mysql_command


class MySQLUser(Module):
    """Test various mysql attributes"""

    def __init__(self, login_pass=None, user="root", password=None, host=None, port=3306, socket="/var/lib/mysql/mysql.sock"):

        self.mysqlcomm = generate_mysql_command(login_pass, user, password, host, port, socket)
        super().__init__()

    def exists(self, mysql_user):
        """Test

        >>> host.mysqluser("root@localhost").exists
        True
        >>> host.mysqluser("nosuchuser").exists
        False

        """
        mysql_user_info = mysql_user.split("@")
        if len(mysql_user_info) > 1:
            return self.check_output(self.mysqlcomm + " -e 'select count(*) from mysql.user where user = \"%s\" and host = \"%s\"'", mysql_user_info[0], mysql_user_info[1]) == "1"
        else:
            return self.check_output(self.mysqlcomm + " -e 'select count(*) from mysql.user where user = \"%s\" and host = \"%\"'", mysql_user_info[0]) == "1"

    def grants(self, mysql_user, expect):
        """Test

        >>> host.mysqluser().grants("root@localhost", "GRANT PROXY ON ''@'' TO 'root'@'localhost' WITH GRANT OPTION")
        True
        >>> host.mysqluser().grants("test@localhost", "GRANT SUPER ON *.* TO `test`@`localhost`")
        False

        """
        mysql_user_info = mysql_user.split("@")
        if len(mysql_user_info) > 1:
            grants = self.check_output(self.mysqlcomm + " -e 'show grants for `%s`@`%s`'", mysql_user_info[0], mysql_user_info[1]).splitlines()
        else:
            grants = self.check_output(self.mysqlcomm + " -e 'show grants for `%s`@`%`'", mysql_user_info[0], mysql_user_info[1]).splitlines()

        return expect in grants
