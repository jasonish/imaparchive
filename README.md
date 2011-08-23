WARNING
-------

This script may delete all your email.  That being said, it had yet to
delete my email - at least as far as I know.

Introduction
------------

This script archive a specific IMAP folder into dated folders similar
to the Thunderbird email program.

Configuration Example
---------------------

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

    python /path/to/imap-archive.py -c <config_file>

This will move all the mail in the folder Archive to folders named
Archives/YYYY/MM and purge them from the source folder.
