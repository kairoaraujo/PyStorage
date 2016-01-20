=======================================
Python Storage Disk Toolkit (PyStorage)
=======================================

.. image:: https://travis-ci.org/kairoaraujo/PyStorage.svg?branch=master
    :target: https://travis-ci.org/kairoaraujo/PyStorage

:PyStorage:   Python Storage Disk Toolkit
:Copyright:   Copyright (c) 2016  Kairo Araujo <kairo@kairo.eti.br>
:License:     BSD
:Development: https://github.com/kairoaraujo/PyStorage

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

Using:
======

* EMC.VMAX

It's works with Storage Disk EMC VMAX.

**Importing and initializing**

>>> import pystorage
>>> symcli_path = '/opt/emc/SYMCLI/bin'
>>> my_vmax = pystorage.EMC.VMAX(symcli_path)



**EMC.list()**

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



**EMC.lspools(SID)**

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



**EMC.ign(SID, WWN)**

Get Initial Group Name full output by the WWN.

returns array [return code, output]

>>> print my_vmax.ign('108', '10:23:45:67:89:0A:BC:DE')[1]
Symmetrix ID          : 000000000108
Initiator Group Name
--------------------
IG_LNXDBSRV001



**EMC.get_ign(SID, WWN)**

Get Initial Group Name, only the Initial Group Name.

returns array [return code, output]

>>> print my_vmax.get_ign('108', '10:23:45:67:89:0A:BC:DE')[1]
IG_LNXDBSRV001



**EMC.mvn(SID, 'INITIAL GROUP NAME')**

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



**EMC.get_mvn(SID, 'INITIAL GROUP NAME')**

Get Mask View Name by the Initial Group Name.

returns array [return code, output]

>>> print my_vmax.get_mvn('108', 'IG_DBSERVER_LINUX')[1:]
MV_LNXDBSRV001



**EMC.sgn(SID, 'MASK VIEW NAME')**

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



**EMC.get_sgn(SID, 'MASK VIEW NAME')**

Get the Storage Group Name by the Mask View Name

returns array [return code, output]

>>> print my_vmax.get_sgn('108', 'MV_LNXDBSRV001')[1]
SG_LNXDBSRV001



**EMC.create_dev('168', 2, '50', '0', 'regular','MYPOOLSAS02',**
**'SG_LNXDBSRV001' 'prepare')**

Create and add LUN to Storage Group Name.

return array [return code, output]

>>
    Establishing a configuration change session...............Established.
    Processing symmetrix 000592600168
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

Contributing:
=============

* Make a fork from GitHub ( https://github.com/kairoaraujo/PyStorage ) and send
your improvements.

* Create a new issue https://github.com/kairoaraujo/PyStorage/issues

IMPORTANT:
==========

EMC, SYMCLI and VMAX are trademarks of EMC in the United States, other
countries, or both.

IBM and DS are trademarks of EMC in the United States, other countries, or both.