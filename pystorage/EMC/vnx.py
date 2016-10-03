#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#
from pystorage import runsub


class VNX(object):
    """
    Class EMC.VNX() works with EMC VNX


    The default return for any command is an array:
    If command is OK:
    [return code, output]
    If command is not OK:
    [return code, error, output]
    """

    def __init__(self, naviseccli_path='', fst_address='', sec_address='',
                 user='admin', password='password', scope='0'):
        """
        :param naviseccli_path: Path installation of NAVISECCLI
        """

        self.naviseccli_path = naviseccli_path
        self.fst_address = fst_address
        self.sec_address = sec_address
        self.user = user
        self.password = password
        self.scope = scope

    def __repr__(self):
        """
        :return: representation (<VNX>).
        """

        representation = '<pystorage.EMC.VNX>'
        return representation

    def _init_vnx(self):
        """
        Initialize the VNX session adding user security scope auth
        for the shell session/user.

        """

        init_1ip_cmd = '{0} -h {1} -addusersecurity -user {2} ' \
                       '-password {3} -scope {4}'.format(self.naviseccli_path,
                                                         self.fst_address,
                                                         self.user,
                                                         self.password,
                                                         self.scope)

        init_2ip_cmd = '{0} -h {1} -addusersecurity -user {2} ' \
                       '-password {3} -scope {4}'.format(self.naviseccli_path,
                                                         self.sec_address,
                                                         self.user,
                                                         self.password,
                                                         self.scope)
        runsub.cmd(init_1ip_cmd)
        runsub.cmd(init_2ip_cmd)

    def _validate_wwn(self, wwn='None'):
        """
        Validate and format the WWN.

        :param wwn: the wwn information
        :return: default return
                 If command is OK:
                 [return code, output]
                 If command is not OK:
                 [return code, error, output]
        """

        # adjust any WWN
        wwn = wwn.replace(':', '')
        wwn = ':'.join(s.encode('hex') for s in wwn.decode('hex'))
        wwn = wwn.upper()

        if len(wwn) == 23:
            return 0, wwn

        else:
            return 1, 'Invalid WWN: {0}'.format(wwn)

    def pools(self):
        """
        List all storage pools from VNX

        :return: default return
                 If command is OK:
                 [return code, output]
                 If command is not OK:
                 [return code, error, output]
        """

        self._init_vnx()
        pools_cmd = '{0} -h {1} storagepool -list'.format(
            self.naviseccli_path,
            self.fst_address
        )
        pools_out = runsub.cmd(pools_cmd)

        return pools_out

    def pool_list(self):
        """
        List the pool list names in one array.

        :return: default return
                 If command is OK:
                 [return code, output]
                 If command is not OK:
                 [return code, error, output]
        """

        list_pool = []
        pools_out = self.pools()

        if pools_out[0] != 0:
            return pools_out

        else:
            for pool_name in pools_out[1].split('\n'):
                if pool_name.startswith('Pool Name:'):
                    list_pool.append(pool_name.split(': ')[1].strip())

        return 0, list_pool

    def port_list_all(self):
        """
        List all port (servers/hosts) from VNX configured.

        :return: default return
                 If command is OK:
                 [return code, output]
                 If command is not OK:
                 [return code, error, output]
        """
        port_list_cmd = '{0} -h {1} port -list'.format(
            self.naviseccli_path,
            self.fst_address
        )
        port_list_out = runsub.cmd(port_list_cmd)

        return port_list_out

    def get_luns(self, pool_name='None'):
        """
        Get all LUNs IDs used by pool sorted.

        :param pool_name: the pool name see pool_list()
        :return: default return
                 If command is OK:
                 [return code, output]
                 If command is not OK:
                 [return code, error, output]
        """

        list_luns_cmd = "{0} -h {1} storagepool -list -name \'{2}\'".format(
            self.naviseccli_path,
            self.fst_address,
            pool_name)

        list_luns_out = runsub.cmd(list_luns_cmd, shell=True)

        luns_ids =[]
        if list_luns_out[0] == 0:
            for line in list_luns_out[1].split('\n'):
                if line.startswith('LUNs:'):
                    luns_id_nf = line.split('LUNs: ')[1].strip()
                    for id_lines in luns_id_nf.split(','):
                        luns_ids.append(id_lines.strip())

        luns_ids.sort(key=int)

        if len(luns_ids) == 0:
            return 1, 'No LUNs founds in Storage Pool \'{0}\''.format(pool_name)

        else:
            return 0, luns_ids

    def show_lun(self, lun_id):
        """
        Get information about specific LUN ID.

        :param lun_id: LUN ID (string)
        :return: default return
                 If command is OK:
                 [return code, output]
                 If command is not OK:
                 [return code, error, output]
        """

        show_lun_cmd = "{0} -h {1} lun -list -l {2}".format(
            self.naviseccli_path,
            self.fst_address,
            lun_id

        )

        show_lun_out = runsub.cmd(show_lun_cmd)

        return show_lun_out

    def get_hostname(self, wwn=''):
        """
        Get the Hostname on storage by host WWN address.

        :param wwn: WWN Address
        :return: default return
                 [return code, output]
        """

        check_wwn = self._validate_wwn(wwn)
        if check_wwn[0] == 1:
            return check_wwn

        else:
            wwn = check_wwn[1]

        hostname = ''
        port_list_out = self.port_list_all()

        if port_list_out[0] != 0:
            return port_list_out

        else:
            wwn_found = False
            for port_line in port_list_out[1].split('\n'):

                if wwn in port_line:
                    wwn_found = True

                if wwn_found is True:
                    if 'Server Name:' in port_line:
                        hostname = port_line.split(':')[1].strip()

                if 'Information about each HBA:' in port_line:
                    wwn_found = False

        if hostname == '':
            return 1, 'WWN {0} not found.'.format(wwn)

        else:
            return 0, hostname

    def get_stggroup(self, wwn=''):
        """
        Get the Storage Group Name on storage used by host WWN address.

        :param wwn: WWN address
        :return: default return
                 [return code, output]
        """

        check_wwn = self._validate_wwn(wwn)
        if check_wwn[0] == 1:
            return check_wwn

        else:
            wwn = check_wwn[1]

        stggroup = ''
        port_list_out = self.port_list_all()

        if port_list_out[0] != 0:
            return port_list_out

        else:
            wwn_found = False
            for port_line in port_list_out[1].split('\n'):

                if wwn in port_line:
                    wwn_found = True

                if wwn_found is True:
                    if 'StorageGroup Name:' in port_line:
                        stggroup = port_line.split(':')[1].strip()

                if 'Information about each HBA:' in port_line:
                    wwn_found = False

        if stggroup == '':
            return 1, 'WWN {0} not found.'.format(wwn)

        else:
            return 0, stggroup


    def show_stggroup(self, stggroup_name):
        """
        Get all informations about the specific storage group name.

        :param stggroup_name: Storage Group Name
        :return: default return
                 If command is OK:
                 [return code, output]
                 If command is not OK:
                 [return code, error, output]
        """

        show_stggroup_cmd = "{0} -h {1} storagegroup " \
                            "-list -gname \'{2}\'".format(self.naviseccli_path,
                                                          self.fst_address,
                                                          stggroup_name)

        show_stggroup_out = runsub.cmd(show_stggroup_cmd, shell=True)

        return show_stggroup_out


    def get_hlu_stggroup(self, stggroup_name):
        """
        Get all the HLU IDs in use on the Storage Group Name

        :param stggroup_name: Storage Group Name
        :return: default return
                 If command is OK:
                 [return code, output]
                 If command is not OK:
                 [return code, error, output]
        """

        show_stggroup = self.show_stggroup(stggroup_name)

        if show_stggroup[0] != 0:
            return 0

        start_line = "----------     ----------\n"
        hlu_list = []
        try:
            for hlu_line in show_stggroup[1].split(start_line)[1].split('\n'):
                try:
                    hlu_id = hlu_line.split('   ')[1].strip()
                    if hlu_id != '':
                        hlu_list.append(hlu_id)
                except IndexError:
                    break

            if len(hlu_list) < 1:
                return 1, hlu_list

            else:
                return 0, hlu_list

        except IndexError:
            return 0, hlu_list

    def create_dev(self, address=None, lun_size=None, pool_name=None,
                   lu=None, lun_name=None, lun_type="NonThin"):
        """
        Create LUN on specific pool

        :param address: address of storage
        :param lun_size:  size of lun in GB (ex: 50GB)
        :param pool_name: pool name
        :param lu: LUN ID on pool
        :param lun_name: Name of LUN
        :param lun_type: Type of LUN (Default: NonThin)
        :return: default return
                 If command is OK:
                 [return code, output]
                 If command is not OK:
                 [return code, error, output]
        """

        create_dev_cmd = "{0} -h {1} lun -create -type {6} -capacity {2} " \
                         "-sq gb -poolName \'{3}\' -aa 1 -l \'{4}\' " \
                         "-name \'{5}\'".format(
            self.naviseccli_path,
            address,
            lun_size,
            pool_name,
            lu,
            lun_name,
            lun_type
        )

        create_dev_cmd_out = runsub.cmd(create_dev_cmd, shell=True)
        return create_dev_cmd_out

    def mapping_dev(self, stggroup='None', hlu='None', alu='None'):
        """
        Add (Mapping) of LUN to Storage Group Name

        :param stggroup: Storage Group Name
        :param hlu: HLU to be used on Storage Group Name
        :param alu: LUN ID (lu)
        :return: default return
                 If command is OK:
                 [return code, output]
                 If command is not OK:
                 [return code, error, output]
        """

        mapping_dev_cmd = "{0} -h {1} -user {2} -password {3} -scope {4} " \
                          "storagegroup -addhlu -gname \'{5}\' -hlu {6} " \
                          "-alu {7}" \
            .format(
            self.naviseccli_path,
            self.fst_address,
            self.user,
            self.password,
            self.scope,
            stggroup,
            hlu,
            alu)

        mapping_dev_cmd_out = runsub.cmd(mapping_dev_cmd, shell=True)
        return mapping_dev_cmd_out
