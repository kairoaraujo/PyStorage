#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#
from pystorage import runsub

class DS8K(object):
    """
    Class IBM.DS8K() works with IBM DS8000 System Storage family.

    Is necessary a DSCLI installed and configured using profile files by
    storage.

    The profile files is usual stored on /opt/ibm/dscli/profile/
    The usual name is dscli.profile_[storage name]

    For more informations check:
    'http://www-01.ibm.com/support/knowledgecenter/#!/STUVMB/
    com.ibm.storage.ssic.help.doc/f2c_cliprofile_1yecd2.html'

    The default return for any command is an array:
    If command is OK:
    [return code, output]
    If command is not OK:
    [return code, error, output]
    """

    def __init__(self, dscli_bin, dscli_profile):
        """
        :param dscli_bin: Path of DSCLI binary
        :param dscli_profile: dscli.profile of storage
        """

        self.dscli_bin = dscli_bin
        self.dscli_profile = dscli_profile
        self.base_cmd = '{0} -cfg {1}'.format(self.dscli_bin,
                                              self.dscli_profile )

    def __repr__(self):
        """
        :return: representation (<DS8K>).
        """

        representation = '<pystorage.IBM.DS8K>'
        return representation

    def _check_internal_rc(self, return_internal):
        if "CMUC00234I" in return_internal[1].split('\n')[1]:
            return [3, return_internal[1]]

        else:
            return return_internal

    def lsextpool(self, args=''):
        """
        Get the available pools on DS.

        :param args: use to pass some arguments such as -l .
        :return: array as [return code, output].
        """

        lsextpool_cmd = '{0} lsextpool {1}'.format(self.base_cmd, args)
        lsextpool_out = runsub.cmd(lsextpool_cmd)

        return lsextpool_out

    def lshostconnect(self, wwpn=None):
        """
        Get the list of hosts. If used with WWPN return informations
        from specified WWPN host.

        :param wwpn: optional
        :return: array as [return code, output].
        """
        if wwpn is None:
            lshostconnect_cmd = '{0} lshostconnect'.format(
                self.base_cmd)

        else:
            lshostconnect_cmd = '{0} lshostconnect -wwpn {1}'.format(
                self.base_cmd, wwpn)

        lshostconnect_out = runsub.cmd(lshostconnect_cmd)

        return lshostconnect_out

    def get_hostname(self, wwpn=''):
        """
        Get the hostname from host by the WWPN.

        :param wwpn: The WWPN from the host that you want to get the name.
        :return: array as [return code, output].
        """

        hostname_out = self.lshostconnect(wwpn)
        hostname_out = self._check_internal_rc(hostname_out)

        if hostname_out[0] == 0:
            hostname_splitted = hostname_out[1].split('\n')[3].split()[0]

            return hostname_out[0], hostname_splitted

        else:

            return hostname_out

    def get_id(self, wwpn=''):
        """
        Get the hostname from host by the WWPN.

        :param wwpn: The WWPN from the host that you want to get the name.
        :return: array as [return code, output].
        """

        id_out = self.lshostconnect(wwpn)
        id_out = self._check_internal_rc(id_out)

        if id_out[0] == 0:
            id_splitted = id_out[1].split('\n')[3].split()[1]

            return id_out[0], id_splitted

        else:
            return id_out


    def get_volgrpid(self, wwpn=''):
        """
        Get the Volume Group ID from host by the WWPN.

        :param wwpn: The WWPN from the host that you want to get the Vol Group
        ID.
        :return: array as [return code, output].
        """

        volgrpid_out = self.lshostconnect(wwpn)
        volgrpid_out = self._check_internal_rc(volgrpid_out)

        if volgrpid_out[0] == 0:
            volgrpid_splitted = volgrpid_out[1].split('\n')[3].split()[-2]

            return volgrpid_out[0], volgrpid_splitted
        else:
            return volgrpid_out


    def lsfbvol(self, args=''):
        """
        List all fixed block volumes in a storage.
        Arguments can be used IBM.DS8K.lsfbvol('args')

        Suggestions:

        - To get all volumes for a specificl Volume Group use:
            IBM.DS8K.lsfbvol('-volgrp VOL_GROUP_ID')

        - To get all  volumes with IDs that contain the specified logical
        subsystem ID use:
            IBM.DS8K.lsfbvol('-lss LSS_ID'


        :param args: optional parameters could be passed here

        :return: array as [return code, output].
        """

        lsfbvol_cmd = '{0} lsfbvol {1}'.format(self.base_cmd, args)
        lsfbvol_out = runsub.cmd(lsfbvol_cmd)

        return lsfbvol_out

    def mkfbvol(self, pool=None, size=None, prefix=None, vol_group=None,
                address=None):
        """
        Create the fbvol(s) and allocate to the Volume Group.

        :param pool: the extpool option
        :param size: the size in GB (without GB)
        :param prefix: the prefix used for LUN
        :param vol_group: the volume group to be allocated
        :param address: the address for the LUNS (LSS)

        :return: array as [return code, output].
        """


        mkfbvol_cmd = '{0} mkfbvol -extpool {1} -cap {2} -name {3}_#h -eam' \
                      ' rotateexts -sam ese -volgrp {4} {5}'\
            .format(self.base_cmd, pool, size, prefix, vol_group, address)

        mkfbvol_out = runsub.cmd(mkfbvol_cmd)

        return mkfbvol_out

    def chvolgrp(self, vol_address, vol_group):
        """
        Add a volume in another volume group.

        :param vol_address: volume addres from the LUN
        :param vol_group: volume group ID

        :return: array as [return code, output].
        """

        chvolgrp_cmd = '{0} chvolgrp -action add -volume {1} {2}'\
            .format(self.base_cmd, vol_address, vol_group)

        chvolgrp_out = runsub.cmd(chvolgrp_cmd)

        return chvolgrp_out

