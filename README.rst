Python Storage Disk Toolkit (PyStorage)
=======================================

This is a collection of storage disk commands.

At the moment the actual version is supporting some commands of EMC VMAX
Storage.

Installing:
-----------

- Using PIP:

# pip install PyStorage

- Offline install
Download the package on https://pypi.python.org/pypi/PyStorage/
# tar xvzf PyStorage-X.Y.tar.gz
# cd PyStorage-X.Y
# python setup.py install

Using:
------

>>> import pystorage
>>> symcli_path = '/opt/emc/SYMCLI/bin'
>>> my_vmax = pystorage.EMC.VMAX(symcli_path)

Listing pools:

>>> my_vmax.lspools('168')

Getting the Initiator Group Name

>>> print my_vmax.get_ign('168', '10:23:45:67:89:0A:BC:DE')
IG_DBSERVER_LINUX

or
>>> my_vmax.get_ign('168', '10234567890ABCDE')




:PyStorage:   Python Storage Disk Toolkit
:Copyright:   Copyright (c) 2016  Kairo Araujo <kairo@kairo.eti.br
:License:     BSD
:Development: https://github.com/kairoaraujo/PyStorage

IMPORTANT:
EMC, SYMCLI and VMAX are trademarks of EMC in the United States, other
countries, or both.

IBM and DS are trademarks of EMC in the United States, other countries, or both.




