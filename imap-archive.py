#! /usr/bin/env python
#
# The MIT License
#
# Copyright (c) Jason Ish
#
# Permission is hereby granted, free of charge, to any person
# obtaining a copy of this software and associated documentation files
# (the "Software"), to deal in the Software without restriction,
# including without limitation the rights to use, copy, modify, merge,
# publish, distribute, sublicense, and/or sell copies of the Software,
# and to permit persons to whom the Software is furnished to do so,
# subject to the following conditions:
#
# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS
# BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN
# ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN
# CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import sys
import os
import re
import pprint
import email
import rfc822
import time
import string
import imaplib
from ConfigParser import ConfigParser
from imaplib import IMAP4_SSL, IMAP4
from datetime import datetime
from optparse import OptionParser

folders = []

def buildFolderCache(imapConn):
    global folders
    _folders = []
    for f in imapConn.list("Archives/")[1]:
        m = re.search(".*\"?(Archives\/.*)\"?", f)
        if m:
            _folders.append(m.group(1))
    folders = _folders

def createFolder(imapConn, folder):
    """ Create folder if it does not already exist. """
    if folder not in folders:
        print("Creating folder %s" % folder)
        print(imapConn.create(folder))
        buildFolderCache(imapConn)

def parseUid(buf):
    """ Extract the IMAP UID from buf. """
    m = re.search("UID (\d+)", buf)
    return int(m.group(1))

def getMsgLocaltime(date):
    """ Return the date of the message in local time. """
    return datetime.fromtimestamp(rfc822.mktime_tz(rfc822.parsedate_tz(date)))

def processAccount(config, account):

    section = "Account %s" % account

    try:
        sourceFolder = config.get(section, "source-folder")
    except:
        sourceFolder = None
    if not sourceFolder:
        print("ERROR: Source folder for account %s not specified." % (
                account))
        return

    remoteHost = config.get(section, "remotehost")
    remoteUser = config.get(section, "remoteuser")
    remotePass = config.get(section, "remotepass")

    useSsl = False
    if config.has_option(section, "ssl"):
        useSsl = config.getboolean(section, "ssl")

    if useSsl:
        m = IMAP4_SSL(remoteHost)
    else:
        m = IMAP4(remoteHost)
    print("Logging in.")
    try:
        print(m.login(remoteUser, remotePass))
    except Exception, err:
        print("Failed to login: %s" % str(err))
        sys.exit(1)
    buildFolderCache(m)
    print(m.select(sourceFolder))
    m.expunge()
    status, data = m.search(None, 'ALL')
    msgSet = data[0].split()
    if not msgSet:
        print("Archive folder is empty, exiting...")
        return 0
    print("Found %d messages in %s." % (len(msgSet), sourceFolder))

    print("Marking all messages read...")
    res = m.store("%s:%s" % (msgSet[0], msgSet[-1]), '+FLAGS', '\\Seen')
    print(res)
    print("Done.")

    status, data = m.fetch(
        ",".join(msgSet), '(UID BODY.PEEK[HEADER.FIELDS (DATE)])')
    for response_part in data:
        if isinstance(response_part, tuple):
            uid = parseUid(response_part[0])
            try:
                msg = email.message_from_string(response_part[1])
                ts = getMsgLocaltime(msg['DATE'])
                dstFolder = "Archives/%s/%s" % (
                    ts.strftime("%Y"), ts.strftime("%Y-%m"))
                print "Moving Archive/%s to %s." % (uid, dstFolder)
                createFolder(m, dstFolder)
                print(m.uid('COPY', uid, dstFolder))
                print(m.uid('STORE', uid, '+FLAGS', '\\Deleted'))
            except Exception, e:
                print("Failed to move UID %d: %s" % (uid, e))
                raise

    print("Expunging folder Archive...")
    m.expunge()
    print("\tDone.")

def main():
    parser = OptionParser()
    parser.add_option("-c", "--config", help="config file")
    opts, args = parser.parse_args()

    if opts.config == None:
        print("ERROR: No configuration file specified.")
        return 1
    elif not os.path.exists(opts.config):
        print("ERROR: Specified configuration file does not exist.")
        return 1
    config = ConfigParser()
    config.read(opts.config)
    accounts = config.get("general", "accounts").split(",")
    accounts = [a.strip() for a in accounts]
    if not accounts:
        print("ERROR: No accounts specified.")
        return 1
    for account in accounts:
        print("Processing account %s." % account)
        processAccount(config, account)

sys.exit(main())
