imap-archive.py
===============

WARNING
-------

This script may delete all your email.  That being said, it has yet to
delete my email - at least as far as I know.

Introduction
------------

This script archives a specific IMAP folder into dated folders similar
to the Thunderbird email program.

Configuration
-------------

If a configuration file is not specified on the command with -c
imap-archive will first check the current directory for
imap-archive.conf and then for ~/.imap-archive.conf.

### Configuration Example

    [general]
    accounts = some-account

    [Account some-account]
    remotehost = imap.example.com
    remoteuser = username
    remotepass = password
    ssl = yes
    source-folder = Archive

Usage
-----

Run the script like:

    python /path/to/imap-archive.py [-c <config_file>]

This will move all the mail in the folder Archive to folders named
Archives/YYYY/MM and purge them from the source folder.
