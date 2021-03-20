from testinfra.modules.base import Module
from testinfra.utils.mysql import generate_mysql_command


class MySQLLoginPath(Module):
    """Test various mysql attributes"""

    def __init__(self, loginpath):
        self.mysqlcomm = generate_mysql_command(loginpath=loginpath)
        super().__init__()

    @property
    def valid(self):
        return self.run_test(self.mysqlcomm + " -e 'select %s'", "1").rc == 0

    @property
    def user(self):
        ret = self.run(self.mysqlcomm + " -e 'select current_user'").stdout.rstrip("\r\n")
        return ret
