#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# 
import subprocess


class VMAX(object):
    """
    Class VMAX works with EMC VMAX Storage.
    """

    def __init__(self, symcli_path=''):
        """
        :param symcli_path: Path installation of SYMCLI
        """

        self.symcli_path = symcli_path

    def __repr__(self):
        """
        :return: representation (<VMAX>).
        """

        representation = '<VMAX>'
        return representation

    def validate_args(self):
        """ Validate if the required args is declared. """

        if self.symcli_path == '':
            return 'The symcli path is required'

    def list(self):
        """
        Get informations about all available Storages

        :return: the return code and list of storages
        """

        symcfg_list_cmd = '{0}/symcfg list'.format(self.symcli_path)

        c_symcfg_list = subprocess.Popen(symcfg_list_cmd.split(),
                                         stdout=subprocess.PIPE,
                                         stderr=subprocess.PIPE)

        symcfg_list_out, symcfg_list_err = c_symcfg_list.communicate()

        if c_symcfg_list.returncode == 0:
            return c_symcfg_list.returncode, symcfg_list_out
        else:
            return c_symcfg_list.returncode, symcfg_list_err

    def lspools(self,  sid='', args=''):
        """
        List all available pools on VMAX.
         :param: args is optional. You can use parameters such as -thin
         :param: sid Identification of VMAX (SID)
         :return: the return code and pools without legend.
        """

        self.validate_args()

        lspools_cmd = '{0}/symcfg -sid {1} list -pool {2}'.format(
            self.symcli_path, sid, args)

        c_lspools = subprocess.Popen(lspools_cmd.split(),
                                     stdout=subprocess.PIPE,
                                     stderr=subprocess.PIPE)

        lspool_out, lspool_err = c_lspools.communicate()

        if c_lspools.returncode == 0:
            lspool_out = lspool_out.split('Legend:')
            lspool_out = lspool_out[0]  # first part only
            return c_lspools.returncode, lspool_out
        else:
            return c_lspools.returncode, lspool_err

    def get_ign(self, sid='', wwn=''):
        """
        Get the Initiator Group Name by the WWN.

        :param: sid Identification of VMAX (SID)
        :param: wwn of client
        :return: the return code and Initiator Group Name of the client server.
        """

        self.validate_args()

        ign_cmd = "{0}/symaccess -sid {1} -type init list -wwn {2}".format(
            self.symcli_path, sid, wwn)

        c_ign = subprocess.Popen(ign_cmd.split(), stdout=subprocess.PIPE,
                                 stderr=subprocess.PIPE)

        ign_out, ign_err = c_ign.communicate()

        if c_ign.returncode == 0:
            # spliting in lines
            ign_out = ign_out.split('\n')
            # cleaning the empty elements (filter) and removing whitespaces
            # (lstrip)
            ign_out = filter(None, ign_out)[-1].strip()
            return c_ign.returncode, ign_out

        else:
            return c_ign.returncode, ign_err

    def get_mvn(self, sid='', ign=''):
        """
        Get the Mask View Names by Initiator Group Name.

        :param: sid Identification of VMAX (SID)
        :param ign: Initiator Group Name. check init_ign(ign, sid)
        :return: the return code and Mask View Name
        """
        self.validate_args()

        mvn_cmd = "{0}/symaccess -sid {1} -type init show {2}".format(
            self.symcli_path, sid, ign)

        c_mvn = subprocess.Popen(mvn_cmd.split(), stdout=subprocess.PIPE,
                                 stderr=subprocess.PIPE)
        mvn_out, mvn_err = c_mvn.communicate()

        if c_mvn.returncode == 0:
            mvn_out = mvn_out.split('Masking View Names')[1]
            mvn_out = mvn_out.split()[1].lstrip()

            return c_mvn.returncode, mvn_out

        else:
            return c_mvn.returncode, mvn_err

    def get_sgn(self, sid='', mvn=''):
        """
         Get the Storage Group Name by the Mask View Name

         :param: sid Identification of VMAX (SID)
         :param mvn: Mask View Name check init_mvn(mvn, sid)
         :return: the return code and Storage Group Name
         """
        self.validate_args()

        sgn_cmd = '{0}/symaccess -sid {1} show view {2}'.format(
            self.symcli_path, sid, mvn)

        c_sgn = subprocess.Popen(sgn_cmd.split(), stdout=subprocess.PIPE,
                                 stderr=subprocess.PIPE)

        sgn_out, sgn_err = c_sgn.communicate()

        if c_sgn.returncode == 0:
            sgn_out = sgn_out.split('Storage Group Name ')[1]
            sgn_out = sgn_out.split()[1]

            return c_sgn.returncode, sgn_out
        else:
            return c_sgn.returncode, sgn_err

    def create_dev(self, sid='', count=0, lun_size=0, member_size=0,
                   lun_type='', pool='', sgn=''):
        """
        Create device(s) for Storage Group Name.

        :param: sid Identification of VMAX (SID)
        :param count: number of devices
        :param lun_size: the size of LUN (GB) Ex: 100
        :param member_size: Member size (only for lun_type=meta)
        :param lun_type: meta or regular
        :param pool: the pool for allocation (use lspools() to check)
        :param sgn: Storage Group Name
        :return: returns the return code and output of allocation
        """

        # convert size GB to CYL
        lun_size = int(lun_size)
        member_size = int(member_size)
        lun_size *= 1092
        member_size *= 1092

        self.validate_args()

        if lun_type == 'meta':
            create_dev_cmd = 'echo {0}/symconfigure -sid {1} -cmd \" ' \
                             'create dev count= {2}, size= {3} CYL, ' \
                             'emulation=FBA , config=TDEV , ' \
                             'meta_member_size= {4} CYL, ' \
                             'meta_config=striped, binding to pool= {5}, ' \
                             'sg={6} ;\" commit -v -nop' \
                .format(self.symcli_path,
                        sid,
                        count,
                        lun_size,
                        member_size,
                        pool,
                        sgn)

        elif lun_type == 'regular':

            create_dev_cmd = 'echo {0}/symconfigure -sid {1} -cmd \" ' \
                             'create dev count= {2}, size= {3} CYL, ' \
                             'emulation=FBA , config=TDEV , ' \
                             'binding to pool= {4}, sg={5} ;\"commit -v -nop' \
                .format(self.symcli_path,
                        sid,
                        count,
                        lun_size,
                        pool,
                        sgn)

        else:
            return 'argument dev_type is not valid. use: meta or regular'

        c_create_dev = subprocess.Popen(create_dev_cmd.split(),
                                        stdout=subprocess.PIPE,
                                        stderr=subprocess.PIPE)

        create_dev_out, create_dev_err = c_create_dev.communicate()

        if c_create_dev.returncode == 0:
            return c_create_dev.returncode, create_dev_out
        else:
            return c_create_dev.returncode, create_dev_err
