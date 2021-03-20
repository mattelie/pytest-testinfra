from testinfra.modules.base import Module
from testinfra.utils.mysql import generate_mysql_command


class MySQLComponent(Module):
    """Test various mysql attributes"""

    def __init__(self, component_urn, login_pass=None, user="root", password=None, host=None, port=3306, socket="/var/lib/mysql/mysql.sock"):

        self.mysqlcomm = generate_mysql_command(login_pass, user, password, host, port, socket)
        self.component_urn = component_urn
        super().__init__()

    @property
    def exists(self):
        return self.check_output(self.mysqlcomm + " -e 'select count(*) from mysql.component where component_urn = \"%s\"'", self.component_urn) == "1"
