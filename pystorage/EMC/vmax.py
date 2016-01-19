#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# 
from pystorage import runsub


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
        symcfg_list_out = runsub.cmd(symcfg_list_cmd)

        return symcfg_list_out

    def lspools(self,  sid='', args=''):
        """
        List all available pools on VMAX.
        :param sid: Identification of VMAX (SID)
        :param args: is optional. You can use parameters such as -thin

        :return: the return code and pools without legend.
        """

        self.validate_args()

        lspools_cmd = '{0}/symcfg -sid {1} list -pool {2}'.format(
            self.symcli_path, sid, args)

        lspools_out = runsub.cmd(lspools_cmd)


        if lspools_out[0] == 0:
            return lspools_out[0], lspools_out[1].split('Legend:')[0]
        else:
            return lspools_out

    def get_ign(self, sid='', wwn=''):
        """
        Get the Initiator Group Name by the WWN.

        :param sid: Identification of VMAX (SID)
        :param wwn: of client

        :return: the return code and Initiator Group Name of the client server.
        """

        self.validate_args()

        ign_cmd = "{0}/symaccess -sid {1} -type init list -wwn {2}".format(
            self.symcli_path, sid, wwn)

        ign_out = runsub.cmd(ign_cmd)

        if ign_out[0] == 0:
            # spliting in lines
            ign_out_splited = ign_out[1].split('\n')
            # cleaning the empty elements (filter) and removing whitespaces
            ign_out_splited = filter(None, ign_out_splited)[-1].split()[0]
            return ign_out[0], ign_out_splited
        else:
            return ign_out

    def get_mvn(self, sid='', ign=''):
        """
        Get the Mask View Names by Initiator Group Name.

        :param sid: Identification of VMAX (SID)
        :param ign: Initiator Group Name. check init_ign(ign, sid)
        :return: the return code and Mask View Name
        """
        self.validate_args()

        mvn_cmd = "{0}/symaccess -sid {1} -type init show {2}".format(
            self.symcli_path, sid, ign)

        mvn_out = runsub.cmd(mvn_cmd)

        if mvn_out[0] == 0:
            mvn_out_splited = mvn_out[1].split('Masking View Names')[1]
            mvn_out_splited = mvn_out_splited.split()[1].lstrip()

            return mvn_out[0], mvn_out_splited

        else:
            return mvn_out

    def get_sgn(self, sid='', mvn=''):
        """
         Get the Storage Group Name by the Mask View Name

         :param sid: Identification of VMAX (SID)
         :param mvn: Mask View Name check init_mvn(mvn, sid)
         :return: the return code and Storage Group Name
         """
        self.validate_args()

        sgn_cmd = '{0}/symaccess -sid {1} show view {2}'.format(
            self.symcli_path, sid, mvn)

        sgn_out = runsub.cmd(sgn_cmd)

        if sgn_out[0] == 0:
            sgn_out_splited = sgn_out[1].split('Storage Group Name ')[1]
            sgn_out_splited = sgn_out_splited.split()[1]

            return sgn_out[0], sgn_out_splited
        else:
            return sgn_out

    def create_dev(self, sid='', count=0, lun_size=0, member_size=0,
                   lun_type='', pool='', sgn=''):
        """
        Create device(s) for Storage Group Name.

        :param sid: Identification of VMAX (SID)
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
            create_dev_cmd = '{0}/symconfigure -sid {1} -cmd \"' \
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

            create_dev_cmd = '{0}/symconfigure -sid {1} -cmd \"' \
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

        create_dev_out = runsub.cmd(create_dev_cmd, True)

        return create_dev_out
