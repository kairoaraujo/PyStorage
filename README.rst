=======================================
Python Storage Disk Toolkit (PyStorage)
=======================================

.. image:: https://travis-ci.org/kairoaraujo/PyStorage.svg?branch=master
    :target: https://travis-ci.org/kairoaraujo/PyStorage

:PyStorage:   Python Storage Disk Toolkit
:Copyright:   Copyright (c) 2016  Kairo Araujo <kairo@kairo.eti.br>
:License:     BSD
:Development: https://github.com/kairoaraujo/PyStorage

.. contents::
    :local:
    :depth: 2
    :backlinks: none

Overview
========

This is a collection of storage disk commands.

At the moment, the current version is supporting some commands of EMC VMAX,
EMC VNX and IBM DS8K Storage.

Requirements
============

* Python >=2.7


Install
=======

* Using PIP:

.. code-block:: bash

    $ pip install PyStorage

* Offline install

Download the package on https://pypi.python.org/pypi/PyStorage/

.. code-block:: bash

    $ tar xvzf PyStorage-X.Y.tar.gz
    $ cd PyStorage-X.Y
    $ python setup.py install

Using
=====

* EMC.VMAX_

* EMC.VNX_

* IBM.DS8K_


.. _EMC.VMAX:

EMC.VMAX
--------

Class EMC.VMAX() works with EMC VMAX Storage 1 and 2.

Is necessary a SYMCLI installed and working well with your environment.
For more information consult the EMC documentation.

* Importing and initializing

>>> import pystorage
>>> symcli_path = '/opt/emc/SYMCLI/bin'
>>> my_vmax = pystorage.EMC.VMAX(symcli_path)



* EMC.VMAX.list()

List all Storages Disk available.

returns array [return code, output]

>>> print my_vmax.list()[1]
                                S Y M M E T R I X
                                       Mcode    Cache      Num Phys  Num Symm
    SymmID       Attachment  Model     Version  Size (MB)  Devices   Devices
    000000000100 Local       VMAX-1    5876      114688         5     12361
    000000000101 Local       VMAX-1    5876      300800        10     16190
    000000000102 Local       VMAX20K   5876      421120        10     13957
    000000000103 Local       VMAX20K   5876      360960         5     24325
    000000000104 Local       VMAX40K   5876      368640        12      9249
    000000000105 Local       VMAX200K  5977     3014656         2      2691
    000000000106 Remote      VMAX20K   5876      360960         0      9588
    000000000107 Remote      VMAX20K   5876      240640         0     11360
    000000000108 Remote      VMAX20K   5876      120320         0      4640



* EMC.VMAX.lspools(SID)

List all Pools from specific storage SID.

returns array [return code, output]

>>> print my_vmax.lspools(108)[1]
Symmetrix ID: 000000000108
                       S Y M M E T R I X   P O O L S
---------------------------------------------------------------------------
Pool         Flags  Dev              Usable       Free       Used Full Comp
Name         PTECSL Config           Tracks     Tracks     Tracks  (%)  (%)
------------ ------ ------------ ---------- ---------- ---------- ---- ----
DEFAULT_POOL S-F-D- Unknown               0          0          0    0    0
DEFAULT_POOL S-9-D- Unknown               0          0          0    0    0
DEFAULT_POOL S-8-D- Unknown               0          0          0    0    0
DEFAULT_POOL S-A-D- Unknown               0          0          0    0    0
MYPOOLSAS01  TEFDEI RAID-5(7+1)    84095232   69400896   14694336   17    0
MYPOOLSAS02  TFFDEI RAID-5(7+1)  1215449040  791717292  423731748   34    0
MYPOOLSATA01 TSFDEI RAID-6(6+2)  1081337856  974749776  106588080    9    0
Total                            ---------- ---------- ---------- ---- ----
Tracks                           2380882128 1835867964  545014164   22    0



* EMC.VMAX.ign(SID, WWN)

Get Initial Group Name full output by the WWN.

returns array [return code, output]

>>> print my_vmax.ign('108', '10:23:45:67:89:0A:BC:DE')[1]
Symmetrix ID          : 000000000108
Initiator Group Name
--------------------
IG_LNXDBSRV001



* EMC.VMAX.get_ign(SID, WWN)

Get Initial Group Name, only the Initial Group Name.

returns array [return code, output]

>>> print my_vmax.get_ign('108', '10:23:45:67:89:0A:BC:DE')[1]
IG_LNXDBSRV001



* EMC.VMAX.mvn(SID, 'INITIAL GROUP NAME')

Get the Mask View Names with full informations using the Initiator Group Name.

returns array [return code, output]

>>> print my_vmax.get_mvn('108', 'IG_DBSERVER_LINUX')[1]
Symmetrix ID          : 000000000108
Initiator Group Name    : IG_LNXDBSRV001
Last update time        : 12:46:36 PM on Tue Dec 09,2014
Group last update time  : 12:46:36 PM on Tue Dec 09,2014
   Host Initiators
     {
       WWN  : 10234567890abcde
              [alias: 10234567890abcde/10234567890abcde]
     }
   Masking View Names
     {
       MV_LNXDBSRV001
     }
   Parent Initiator Groups
     {
       None
     }



* EMC.VMAX.get_mvn(SID, 'INITIAL GROUP NAME')

Get Mask View Name by the Initial Group Name.

returns array [return code, output]

>>> print my_vmax.get_mvn('108', 'IG_DBSERVER_LINUX')[1:]
MV_LNXDBSRV001



* EMC.VMAX.sgn(SID, 'MASK VIEW NAME')

Get the full Storage Group Name information by the Mask View Name.

returns array [return code, output]

>>> print my_vmax.sgn('168', 'MV_LNXDBSRV001')[1]
Symmetrix ID                : 000000000108
Masking View Name           : MV_LNXDBSRV001
Last update time            : 05:32:53 PM on Thu Nov 12,2015
View last update time       : 05:32:53 PM on Thu Nov 12,2015
Initiator Group Name        : IG_LNXDBSRV001
   Host Initiators
     {
       WWN  : 10234567890abcde
              [alias: 10234567890abcde/10234567890abcde]
     }
Port Group Name             : PG_LNXDBSRV001_012A
   Director Identification
     {
        Director
      Ident  Port   WWN Port Name / iSCSI Target Name
      ------ ---- -------------------------------------------------------
      01-2A   000 500001234567890a
     }
Storage Group Name          : SG_LNXDBSRV001
   Number of Storage Groups : 0
   Storage Group Names      : None
Sym                                        Host
Dev     Dir:Port  Physical Device Name     Lun   Attr  Cap(MB)
------  --------  -----------------------  ----  ----  -------
00055   09F:000   Not Visible                 1              3
00056   09F:000   Not Visible                 2              3
00057   09F:000   Not Visible                 3              3
00058   09F:000   Not Visible                 4              3
                                                       -------
Total Capacity                                              12



* EMC.VMAX.get_sgn(SID, 'MASK VIEW NAME')

Get the Storage Group Name by the Mask View Name

returns array [return code, output]

>>> print my_vmax.get_sgn('108', 'MV_LNXDBSRV001')[1]
SG_LNXDBSRV001



* EMC.VMAX.create_dev(SID, COUNT, 'LUN SIZE', 'MEMBER SIZE', 'REGULAR or META','POOL', 'STORAGE GROUP NAME' 'PREPARE or COMMIT')

Create and add LUN to Storage Group Name.

return array [return code, output]

>>> my_vmax.create_dev('168', 2, '50', '0', 'regular','MYPOOLSAS02',
'SG_LNXDBSRV001' 'prepare')
    Establishing a configuration change session...............Established.
    Processing symmetrix 000000000108
    {
      create dev count=2, size=54600 cyl, emulation=FBA, config=TDEV,
        mvs_ssid=0, binding to pool MYPOOLSAS02, sg=SG_LNXDBSRV001;
    }
    Performing Access checks..................................Allowed.
    Checking Device Reservations..............................Allowed.
    Initiating COMMIT of configuration changes................Started.
    Committing configuration changes..........................Queued.
    COMMIT requesting required resources......................Obtained.
    Step 002 of 018 steps.....................................Executing.
    Step 011 of 018 steps.....................................Executing.
    Step 016 of 019 steps.....................................Executing.
    Step 016 of 019 steps.....................................Executing.
    Local:  COMMIT............................................Done.
    Adding devices to Storage Group...........................
      New symdevs: 00D28:00D29 [TDEVs]
    Terminating the configuration change session..............Done.


.. _EMC.VNX:

EMC.VNX
-------

Class EMC.VNX() works with EMC VNX.

Is necessary a NAVISECCLI installed and working well with your environment.
For more information consult the EMC documentation.

All returns are:

If return code is 0: [return code, data]

If return code is different of 0: [return code, 'data error', 'data'

* Importing and initializing

>>> import pystorage
>>> vnx = pystorage.VNX('naviseccli', '10.0.0.1')

* EMC.VNX.pools()

List all pools informations.


>>> print vnx.pools()[1]
Pool Name:  P1SAS600K15
Pool ID:  0
Raid Type:  r_5
Percent Full Threshold:  70
Description:
Disk Type:  SAS
State:  Ready
Status:  OK(0x0)
Current Operation:  None
Current Operation State:  N/A
Current Operation Status:  N/A
Current Operation Percent Completed:  0
Raw Capacity (Blocks):  236411400960
Raw Capacity (GBs):  112729.741
User Capacity (Blocks):  188771917824
User Capacity (GBs):  90013.465
Consumed Capacity (Blocks):  187616231424
Consumed Capacity (GBs):  89462.391
Available Capacity (Blocks):  1155686400
Available Capacity (GBs):  551.074
Percent Full:  99.388
Total Subscribed Capacity (Blocks):  189324546048
Total Subscribed Capacity (GBs):  90276.979
Percent Subscribed:  100.293
Oversubscribed by (Blocks):  552628224
Oversubscribed by (GBs):  263.514
(...)
Disks:
Bus 2 Enclosure 2 Disk 10
Bus 2 Enclosure 2 Disk 12
Bus 2 Enclosure 2 Disk 14
Bus 3 Enclosure 3 Disk
LUNs:  806, 677, 198, 896, 479, 768, 620, 708, (...)
(... End of Example ...)

* EMC.VNX.pool_list()

Return array with pool names

>>> vnx.pool_list()[1]
['P1SAS600K15']


* EMC.VNX.port_list_all()

Return all data about port list from storage


>>> print vnx.port_list_all()[1]
Information about each HBA:
HBA UID:                 C0:50:76:05:17:AA:00:2C:C0:50:76:05:17:AA:00:2C
Server Name:             MYSERVER01
Server IP Address:       10.10.10.10
HBA Model Description:
HBA Vendor Description:
HBA Device Driver Name:   N/A
Information about each port of this HBA:
    SP Name:               SP A
    SP Port ID:            4
    HBA Devicename:        N/A
    Trusted:               NO
    Logged In:             YES
    Source ID:             3943170
    Defined:               YES
    Initiator Type:           3
    StorageGroup Name:     SG_MYSERVER01
.
    SP Name:               SP B
    SP Port ID:            4
    HBA Devicename:        N/A
    Trusted:               NO
    Logged In:             YES
    Source ID:             3943170
    Defined:               YES
    Initiator Type:           3
    StorageGroup Name:     SG_MYSERVER01
.
Information about each HBA:
HBA UID:                 C0:50:76:05:17:AA:00:2E:C0:50:76:05:17:AA:00:2E
Server Name:             MYSERVER02
Server IP Address:       10.10.10.11
HBA Model Description:
HBA Vendor Description:
HBA Device Driver Name:   N/A
Information about each port of this HBA:
(...end of example...)


* EMC.VNX.get_luns('POOL')

Get all LUNs IDs used in the pool sorted.

>>> print vnx.get_luns('P1SAS600K15')[1]
['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11' ...]


* EMC.VNX.show_lun('ID')

Get information about specific LUN ID.


>>> print vnx.show_lun('3')[1]
LOGICAL UNIT NUMBER 3
Name:  DB_LUN_3
UID:  60:06:01:60:20:A0:2D:00:36:1B:B4:88:A3:A9:E1:11
Current Owner:  SP B
Default Owner:  SP B
Allocation Owner:  SP B
User Capacity (Blocks):  943718400
User Capacity (GBs):  450.000
Consumed Capacity (Blocks):  972877824
Consumed Capacity (GBs):  463.904
Pool Name:  P1SAS600K15
Raid Type:  r_5
Offset:  0
Auto-Assign Enabled:  DISABLED
Auto-Trespass Enabled:  DISABLED
Current State:  Ready
Status:  OK(0x0)
Is Faulted:  false
Is Transitioning:  false
Current Operation:  None
Current Operation State:  N/A
Current Operation Status:  N/A
Current Operation Percent Completed:  0
Is Pool LUN:  Yes
Is Thin LUN:  No
Is Private:  No
Is Compressed:  No
Tiering Policy:  No Movement
Initial Tier:  Optimize Pool
Tier Distribution:
Performance:  100.00


* EMC.VNX.get_hostname('WWN')

Get the Hostname on storage by host WWN address.

>>> print vnx.get_hostname('C0:50:76:05:14:5F:00:30')[1]
SERVER_DB02


* EMC.VNX.get_stggroup('WWN')

Get the Storage Group Name on storage used by host WWN address.

>>> print vnx.get_stggroup('C0:50:76:05:14:5F:00:30')[1]
SG_SERVER_DB2


* EMC.VNX.show_stggroup('STORAGE GROUP NAME')

Get all informations about the specific storage group name.

>>> print vnx.show_stggroup('SG_SERVER_DB2')[1]
Storage Group Name:    SG_SERVER_DB2
Storage Group UID:     D2:F2:E2:05:89:2F:E3:11:B6:12:00:60:16:38:6D:4F
HBA/SP Pairs:
.
  HBA UID                                          SP Name     SPPort
  -------                                          -------     ------
  20:00:00:24:FF:40:1B:3F:21:00:00:24:FF:40:1B:3F   SP A         7
  20:00:00:24:FF:40:35:C1:21:00:00:24:FF:40:35:C1   SP A         7
  20:00:00:24:FF:40:1B:3F:21:00:00:24:FF:40:1B:3F   SP B         7
  20:00:00:24:FF:40:35:C1:21:00:00:24:FF:40:35:C1   SP B         7
  20:00:00:24:FF:40:1B:4F:21:00:00:24:FF:40:1B:4F   SP A         7
  20:00:00:24:FF:40:1B:4F:21:00:00:24:FF:40:1B:4F   SP B         7
  20:00:00:24:FF:40:1A:3E:21:00:00:24:FF:40:1A:3E   SP A         3
  20:00:00:24:FF:40:1A:3E:21:00:00:24:FF:40:1A:3E   SP B         3
  20:00:00:24:FF:40:35:C0:21:00:00:24:FF:40:35:C0   SP A         3
  20:00:00:24:FF:40:1B:4E:21:00:00:24:FF:40:1B:4E   SP A         3
  20:00:00:24:FF:40:35:C0:21:00:00:24:FF:40:35:C0   SP B         3
  20:00:00:24:FF:40:1B:4E:21:00:00:24:FF:40:1B:4E   SP B         3
  20:00:00:24:FF:40:1A:3F:21:00:00:24:FF:40:1A:3F   SP A         7
  20:00:00:24:FF:40:1A:3F:21:00:00:24:FF:40:1A:3F   SP B         7
.
HLU/ALU Pairs:
.
  HLU Number     ALU Number
  ----------     ----------
    0               923
    1               920
    2               925
    3               922
    4               1040
    5               1041
    6               1042
Shareable:             YES


* EMC.VNX.get_hlu_stggroup('STORAGE GROUP NAME')

Get all the HLU IDs in use on the Storage Group Name

>>> print vnx.get_hlu_stggroup('ALE_CLUSTER_ALELOESXRJ01-02-03-04')[1]
['0', '1', '2', '3', '4', '5', '6']


* EMC.VNX.create_dev('address', 'lun_size', 'pool_name', 'LUN ID', 'LUN', lun_type="NonThin")

Create LUN on specific pool

>>> vnx.create_dev('10.0.0.1', 50, 'P1SAS600K15', '103' 'DB2_LUN_103', lun_type="NonThin"):


* EMC.VNX.mapping_dev('STORAGR GROUP NAME', 'HLU ID', 'LUN ID'):

Add (Mapping) of LUN to Storage Group Name

>>> vnx.mapping_dev('SG_SERVER_DB2', '7', '103')


.. _IBM.DS8K:

IBM.DSK8K
---------

Class IBM.DS8K() works with IBM DS8000 System Storage family.

Is necessary a DSCLI installed and configured using profile files by
storage.

The profile files is usual stored on /opt/ibm/dscli/profile/

The usual name is dscli.profile_[storage name]

For more informations check:
http://www-01.ibm.com/support/knowledgecenter/#!/STUVMB/com.ibm.storage.ssic.help.doc/f2c_cliprofile_1yecd2.html

* Importing and initializing

>>> import pystorage
>>> dscli_path = '/opt/ibm/dscli'
>>> dscli_profile_path = '/opt/ibm/dscli/profile/'
>>> my_ds8k = pystorage.IBM.DS8K(dscli_path, dscli_profile_path+'dscli.profile_wxyz')

* IBM.lsextpool()

List all available pools, full output.

return [return code, output]

>>> print my_ds8k.lsextpool()[1]
Date/Time: January 21, 2016 10:34:07 AM BRST IBM DSCLI Version: 7.7.5.61 DS: IBM.2107-82BWXYZ
Name ID stgtype rankgrp status availstor (2^30B) %allocated available reserved numvols
======================================================================================
P0   P0 fb            0  below             14285         96     14285        0    2948
P1   P1 fb            1  below             11737         96     11737        0    2878
P2   P2 fb            0  below             11995         66     11995        0     341
P3   P3 fb            1  below             12123         65     12123        0     422


* IBM.lshostconnect('WWPN')

Get the list of hosts. If used with WWPN (optional) returns informations from
specified WWPN host.

>>> print my_ds8k.lshostconnect('10234567890abcde')[1]
Date/Time: January 21, 2016 10:36:55 AM BRST IBM DSCLI Version: 7.7.5.61 DS: IBM.2107-82BWXYZ
Name                 ID   WWPN             HostType  Profile            portgrp volgrpID ESSIOport
==================================================================================================
LNXDBSRV001_TESTS    03DB 10234567890ABCDE LinuxRHEL Intel - Linux RHEL       0 V334     all




* IBM.get_hostname('WWPN')

Get the hostname from host by the WWPN.

>>> print my_ds8k.get_hostname('10234567890abcde')[1]
LNXDBSRV001_TESTS



* IBM.get_id('WWPN')

Get the id from host by the WWPN.

>>> print my_ds8k.get_hostname('10234567890abcde')[1]
03DB



* IBM.get_volgrpid('WWPN')

Get the Volume Group ID from host by the WWPN.

>>> print my_ds8k.get_volgrpid('10234567890abcde')[1]
V334


* IBM.lsfbvol()

List all fixed block volumes in a storage.
Arguments can be used IBM.DS8K.lsfbvol('args')

Suggestions:

To get all volumes for a specific Volume Group use:

IBM.DS8K.lsfbvol('-volgrp VOL_GROUP_ID')

To get all  volumes with IDs that contain the specified logical subsystem
ID use:

IBM.DS8K.lsfbvol('-lss LSS_ID')

>>> print my_ds8k.lsfbvol('-lss 01')
Date/Time: January 21, 2016 11:55:35 AM BRST IBM DSCLI Version: 7.7.5.61 DS: IBM.2107-82BWXYZ
Name        ID   accstate datastate configstate deviceMTM datatype extpool cap (2^30B) cap (10^9B) cap (blocks)
===================================================================================================================
LUN_0100    0000 Online   Normal    Normal      2107-900  FB 512   P1             50.0           -    104857600
LUN_0101    0001 Online   Normal    Normal      2107-900  FB 512   P1             50.0           -    104857600
LUN_0102    0002 Online   Normal    Normal      2107-900  FB 512   P1             50.0           -    104857600
(...)



* IBM.DS8K.mkfbvol(pool, size, prefix, vol_group, address)

Create the fbvol(s) and allocate to the Volume Group.

>>> print my_ds8k.mkfbvol('P1', 50, 'LUN_', 'V334', '0100 0101 0102 0103')
FB volume 0100 successfully created.
FB volume 0101 successfully created.
FB volume 0102 successfully created.
FB volume 0103 successfully created.


* IBM.DSK8K.chvolgrp(vol_address, vol_group):

Add a volume in another volume group.

>>> my_ds8k.chvolgrp('0101-0103', 'V335')
Volume group V335 successfully modified.



Contributing
============

* Coding

1. Create your account on GitHub
2. Make a fork from GitHub (https://github.com/kairoaraujo/PyStorage)
3. Sign in on GerritHub.io (http://review.gerrithub.io) using your account from GitHub
4. Submit you review =)

* Reporting Issue or suggestions

1. Create a new issue https://github.com/kairoaraujo/PyStorage/issues

Important
=========

EMC, SYMCLI and VMAX are trademarks of EMC in the United States, other
countries, or both.

IBM and DS are trademarks of EMC in the United States, other countries, or both.