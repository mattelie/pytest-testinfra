from testinfra.modules.base import Module
from testinfra.utils.mysql import generate_mysql_command
import csv
from io import StringIO


class MySQLReplication(Module):
    """Test various mysql attributes"""

    def _show_slave_status(self, field):
        show_slave_status_tsv = self.check_output(self.mysqlcomm + " -e 'show slave status'")

        f = StringIO(show_slave_status_tsv)
        reader = csv.DictReader(f, delimiter='\t')
        for row in reader:
            if row["Channel_Name"] == self.channel:
                return row[field]
        return None

    def __init__(self, channel="", login_pass=None, user="root", password=None, host=None, port=3306, socket="/var/lib/mysql/mysql.sock"):

        self.mysqlcomm = generate_mysql_command(login_pass, user, password, host, port, socket, no_header=False)
        self.channel = channel
        super().__init__()

    @property
    def exists(self):
        return self._show_slave_status("Channel_Name") is not None

    @property
    def master_port(self):
        return self._show_slave_status("Master_Port")

    @property
    def master_host(self):
        return self._show_slave_status("Master_Host")

    @property
    def master_user(self):
        return self._show_slave_status("Master_User")

    @property
    def io_running(self):
        return self._show_slave_status("Slave_IO_Running") == "Yes"

    @property
    def sql_running(self):
        return self._show_slave_status("Slave_SQL_Running") == "Yes"

    @property
    def master_uuid(self):
        return self._show_slave_status("Master_UUID")

    @property
    def autoposition(self):
        return self._show_slave_status("Auto_Position") == "1"

    @property
    def sql_delay(self):
        return self._show_slave_status("SQL_Delay")

    @property
    def ssl_allowed(self):
        return self._show_slave_status("Master_SSL_Allowed")

    @property
    def ssl_ca_file(self):
        return self._show_slave_status("Master_SSL_CA_File")

    @property
    def ssl_cert(self):
        return self._show_slave_status("Master_SSL_Cert")

    @property
    def ssl_key(self):
        return self._show_slave_status("Master_SSL_Key")

    @property
    def retrycount(self):
        return self._show_slave_status("Master_Retry_Count")

    @property
    def heartbeat(self):
        return self.check_output(self.mysqlcomm + " -N -e 'select Heartbeat from mysql.slave_master_info where Channel_name = \"%s\"'", self.channel)
