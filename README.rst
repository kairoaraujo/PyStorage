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

* Python 2.7


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

List all Storages

returns array [return code, output]

Sample:

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

List all Pools

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

Getting the Initiator Group Name

**EMC.get_ign(SID, WWN)**

Get Initial Group Name.

returns array [return code, output]

>>> print my_vmax.get_ign('108', '10:23:45:67:89:0A:BC:DE')[1]
IG_LNXDBSRV001

**EMC.get_mvn(SID, 'INITIAL GROUP NAME')**

Get Mask View Name by the Initial Group Name.

returns array [return code, output]

>>> print my_vmax.get_mvn('108', 'IG_DBSERVER_LINUX')[1]
MV_DSM_LNXDBSRV001

**EMC.get_sgn(SID, 'MASK VIEW NAME')**

Get the Storage Group Name by the Mask View Name

returns array [return code, output]

>>> print my_vmax.get_sgn(168, 'MV_DSM_TVT_TIVIT0070')[1]
SG_LNXDBSRV001

**EMC.create_dev(SID, COUNT, 'LUN SIZE', 'MEMBER SIZE', 'REGULAR or META',**
**'POOL', 'STORAGE GROUP NAME' 'PREPARE or COMMIT')**

Create and add LUN to Storage Group Name.

return array [return code, output]

IMPORTANT:
==========

EMC, SYMCLI and VMAX are trademarks of EMC in the United States, other
countries, or both.

IBM and DS are trademarks of EMC in the United States, other countries, or both.