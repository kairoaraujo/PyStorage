=======================================
Python Storage Disk Toolkit (PyStorage)
=======================================

:PyStorage:   Python Storage Disk Toolkit
:Copyright:   Copyright (c) 2016  Kairo Araujo <kairo@kairo.eti.br>
:License:     BSD
:Development: https://github.com/kairoaraujo/PyStorage

Overview
========

This is a collection of storage disk commands.

At the moment the actual version is supporting some commands of EMC VMAX
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
    # python setup.py install

Using:
======

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

IMPORTANT:
==========

EMC, SYMCLI and VMAX are trademarks of EMC in the United States, other
countries, or both.

IBM and DS are trademarks of EMC in the United States, other countries, or both.