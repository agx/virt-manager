#!/usr/bin/python

# virt-manager-tui.py - Copyright (C) 2010 Red Hat, Inc.
# Written by Darryl L. Pierce, <dpierce@redhat.com>.
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
# MA 02110-1301 USA.
#

import logging
import optparse
import os
import sys
import traceback

from newt_syrup.dialogscreen import DialogScreen

from virtcli import cliutils, cliconfig


def parse_commandline():
    optParser = optparse.OptionParser(version=cliconfig.__version__)

    optParser.add_option("-c", "--connect", dest="uri",
        help="Connect to hypervisor at URI", metavar="URI")
    optParser.add_option("--debug", action="store_true", dest="debug",
        help="Print debug output to stdout (implies --no-fork)",
        default=False)

    return optParser.parse_args()

def _show_startup_error(message, details):
    errordlg = DialogScreen("Error Starting Virtual Machine Manager",
                            message + "\n\n" + details)
    errordlg.show()

def main():
    cliutils.setup_i18n()

    (options, ignore) = parse_commandline()
    cliutils.setup_logging("virt-manager-tui", options.debug)

    import virtManager
    logging.debug("Launched as: %s", " ".join(sys.argv[:]))

    cliutils.check_virtinst_version()

    import virtManager.guidiff
    virtManager.guidiff.is_gui(False)

    # Hack in the default URI for this instance of the tui
    if options.uri:
        import virtManagerTui.libvirtworker
        virtManagerTui.libvirtworker.default_url = options.uri

    # start the app
    from virtManagerTui.mainmenu import MainMenu
    MainMenu()

if __name__ == "__main__":
    try:
        main()
    except SystemExit:
        raise
    except Exception, error:
        logging.exception(error)
        _show_startup_error(str(error), "".join(traceback.format_exc()))