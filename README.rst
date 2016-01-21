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

At the moment, the current version is supporting some commands of EMC VMAX
Storage.

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



* EMC.list()

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



* EMC.lspools(SID)

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



* EMC.ign(SID, WWN)

Get Initial Group Name full output by the WWN.

returns array [return code, output]

>>> print my_vmax.ign('108', '10:23:45:67:89:0A:BC:DE')[1]
Symmetrix ID          : 000000000108
Initiator Group Name
--------------------
IG_LNXDBSRV001



* EMC.get_ign(SID, WWN)

Get Initial Group Name, only the Initial Group Name.

returns array [return code, output]

>>> print my_vmax.get_ign('108', '10:23:45:67:89:0A:BC:DE')[1]
IG_LNXDBSRV001



* EMC.mvn(SID, 'INITIAL GROUP NAME')

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



* EMC.get_mvn(SID, 'INITIAL GROUP NAME')

Get Mask View Name by the Initial Group Name.

returns array [return code, output]

>>> print my_vmax.get_mvn('108', 'IG_DBSERVER_LINUX')[1:]
MV_LNXDBSRV001



* EMC.sgn(SID, 'MASK VIEW NAME')

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



* EMC.get_sgn(SID, 'MASK VIEW NAME')

Get the Storage Group Name by the Mask View Name

returns array [return code, output]

>>> print my_vmax.get_sgn('108', 'MV_LNXDBSRV001')[1]
SG_LNXDBSRV001



* EMC.create_dev(SID, COUNT, 'LUN SIZE', 'MEMBER SIZE', 'REGULAR or META','POOL', 'STORAGE GROUP NAME' 'PREPARE or COMMIT')

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
Date/Time: January 21, 2016 10:34:07 AM BRST IBM DSCLI Version: 7.7.5.61 DS: IBM.2107-82BCN51
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

To get all volumes for a specificl Volume Group use:

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

Make a fork from GitHub ( https://github.com/kairoaraujo/PyStorage ) and send
your improvements.

Create a new issue https://github.com/kairoaraujo/PyStorage/issues

Important
=========

EMC, SYMCLI and VMAX are trademarks of EMC in the United States, other
countries, or both.

IBM and DS are trademarks of EMC in the United States, other countries, or both.