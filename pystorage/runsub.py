#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#
import subprocess

def cmd(command_line):
    """
    Execute the command using subprocess.

    :param command_line: Full Command line as string
    :return: the return code and the output of command or error
    """

    c = subprocess.Popen(command_line.split(),
                         stdout=subprocess.PIPE,
                         stderr=subprocess.PIPE)

    c_out, c_err = c.communicate()

    if c.returncode == 0:
        return c.returncode, c_out
    else:
        return c.returncode, c_err

