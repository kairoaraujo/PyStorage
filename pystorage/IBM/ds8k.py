#!/usr/bin/env python
from __future__ import annotations

from typing import List, Tuple
from pystorage import runsub


class DS8K:
    """Class IBM.DS8K() works with IBM DS8000 System Storage family.

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

    def __init__(self, dscli_bin: str, dscli_profile: str) -> None:
        """Required values:

        :param dscli_bin: Path of DSCLI binary
        :param dscli_profile: dscli.profile of storage
        """

        self.dscli_bin = dscli_bin
        self.dscli_profile = dscli_profile
        self.base_cmd = f"{self.dscli_bin} -cfg {self.dscli_profile}"

    def __repr__(self) -> str:
        """Representation

        :return: representation (<DS8K>).
        """

        return "<pystorage.IBM.DS8K>"

    def _check_internal_rc(self, return_internal: List[str]) -> List[str]:
        if "CMUC00234I" in return_internal[1].split("\n")[1]:
            return [3, return_internal[1]]

        else:
            return return_internal

    def lsextpool(self, args: str = "") -> List[str]:
        """Get the available pools on DS.

        :param args: use to pass some arguments such as -l .

        :return: array as [return code, output].
        """

        lsextpool_cmd = f"{self.base_cmd} lsextpool {args}"
        lsextpool_out = runsub.cmd(lsextpool_cmd)

        return lsextpool_out

    def lshostconnect(self, wwpn: str | None = None) -> List[str]:
        """Get the list of hosts.

        If used with WWPN return informations from specified WWPN host.

        :param wwpn: optional.

        :return: array as [return code, output].
        """

        if wwpn is None:
            lshostconnect_cmd = f"{self.base_cmd} lshostconnect"
        else:
            lshostconnect_cmd = f"{self.base_cmd} lshostconnect -wwpn {wwpn}"

        lshostconnect_out = runsub.cmd(lshostconnect_cmd)

        return lshostconnect_out

    def get_hostname(self, wwpn: str = "") -> Tuple[int, str] | List[str]:
        """Get the hostname from host by the WWPN.

        :param wwpn: The WWPN from the host that you want to get the name.

        :return: tuple as (return code, hostname) or List[str] as [return code, error, output].
        """

        hostname_out = self.lshostconnect(wwpn)
        hostname_out = self._check_internal_rc(hostname_out)

        if hostname_out[0] == 0;        if hostname_out[0] == 0:
            hostname_splitted = hostname_out[1].split("\n")[3].split()[0]
            return hostname_out[0], hostname_splitted
        else:
            return hostname_out

    def get_id(self, wwpn: str = "") -> Tuple[int, str] | List[str]:
        """Get the hostname from host by the WWPN.

        :param wwpn: The WWPN from the host that you want to get the name.

        :return: tuple as (return code, ID) or List[str] as [return code, error, output].
        """

        id_out = self.lshostconnect(wwpn)
        id_out = self._check_internal_rc(id_out)

        if id_out[0] == 0:
            id_splitted = id_out[1].split("\n")[3].split()[1]
            return id_out[0], id_splitted
        else:
            return id_out

    def get_volgrpid(self, wwpn: str = "") -> Tuple[int, str] | List[str]:
        """Get the Volume Group ID from host by the WWPN.

        :param wwpn: The WWPN from the host that you want to get the Vol Group
        ID.

        :return: tuple as (return code, volgrpid) or List[str] as [return code, error, output].
        """

        volgrpid_out = self.lshostconnect(wwpn)
        volgrpid_out = self._check_internal_rc(volgrpid_out)

        if volgrpid_out[0] == 0:
            volgrpid_splitted = volgrpid_out[1].split("\n")[3].split()[-2]
            return volgrpid_out[0], volgrpid_splitted
        else:
            return volgrpid_out

    def lsfbvol(self, args: str = "") -> List[str]:
        """List all fixed block volumes in a storage.

        Arguments can be used IBM.DS8K.lsfbvol('args')

        Suggestions:

        - To get all volumes for a specific Volume Group use:
            IBM.DS8K.lsfbvol('-volgrp VOL_GROUP_ID')

        - To get all volumes with IDs that contain the specified logical
        subsystem ID use:
            IBM.DS8K.lsfbvol('-lss LSS_ID'

        :param args: optional parameters could be passed here

        :return: array as [return code, output].
        """

        lsfbvol_cmd = f"{self.base_cmd} lsfbvol {args}"
        lsfbvol_out = runsub.cmd(lsfbvol_cmd)

        return lsfbvol_out

    def mkfbvol(
        self,
        pool: str | None = None,
        size: str | None = None,
        prefix: str | None = None,
        vol_group: str | None = None,
        address: str | None = None,
    ) -> List[str]:
        """Create the fbvol(s) and allocate to the Volume Group.

        :param pool: the extpool option
        :param size: the size in GB (without GB)
        :param prefix: the prefix used for LUN
        :param vol_group: the volume group to be allocated
        :param address: the address for the LUNS (LSS)

        :return: array as [return code, output].
        """

        mkfbvol_cmd = (
            f"{self.base_cmd} mkfbvol -extpool
