#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#
import subprocess

def cmd(command_line, shell=False):
    """
    Execute the command using subprocess.

    :param command_line: Full Command line as string
    :param shell: True or False (the same function on
    :return: the return code and the output of command or error
    """

    if shell:

        c = subprocess.Popen(command_line,
                             universal_newlines=True,
                             stdout=subprocess.PIPE,
                             stderr=subprocess.PIPE, shell=True)
    else:

        c = subprocess.Popen(command_line.split(),
                             universal_newlines=True,
                             stdout=subprocess.PIPE,
                             stderr=subprocess.PIPE)

    c_out, c_err = c.communicate()

    if c.returncode == 0:
        return c.returncode, c_out
    else:
        return c.returncode, c_err

