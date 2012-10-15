imaparchive
===========

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
imaparchive will look for a file named imaparchive.conf in the current
directory.

### Configuration Example

    [general]
    accounts = some-account

    [Account some-account]
    remotehost = imap.example.com
    remoteuser = username
    remotepass = password
    ssl = yes
    source-folder = Archive
    mark-read = yes

Usage
-----

Run the script like:

    python /path/to/imaparchive [-c <config_file>]

This will move all the mail in the folder Archive to folders named
Archives/YYYY/MM and purge them from the source folder.
