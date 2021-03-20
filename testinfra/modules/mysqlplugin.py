from testinfra.modules.base import Module
from testinfra.utils.mysql import generate_mysql_command


class MySQLPlugin(Module):
    """Test various mysql attributes"""

    def __init__(self, plugin_name, login_pass=None, user="root", password=None, host=None, port=3306, socket="/var/lib/mysql/mysql.sock"):

        self.mysqlcomm = generate_mysql_command(login_pass, user, password, host, port, socket)
        self.plugin_name = plugin_name
        super().__init__()

    @property
    def exists(self):
        return self.check_output(self.mysqlcomm + " -e 'select count(*) from information_schema.plugins where plugin_name = \"%s\"'", self.plugin_name) == "1"

    @property
    def enabled(self):
        return self.check_output(self.mysqlcomm + " -e 'select count(*) from information_schema.plugins where plugin_name = \"%s\" and plugin_status = \"ACTIVE\"'", self.plugin_name) == "1"

    @property
    def version(self):
        return self.check_output(self.mysqlcomm + " -e 'select PLUGIN_VERSION from information_schema.plugins where plugin_name = \"%s\"'", self.plugin_name)
