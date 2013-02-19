#!/usr/bin/env python
import pexpect
import datetime
import sys
import json
import strjson

def main(inputLine): #since this is called by the couchdbkit.Consumer, it will pass in a line from the db. just ignore it.
    #if inputLine == '': return #quit if nothing was sent.. this is probably a heartbeat
    try:
        creds = strjson.load('localcredentials.json')
        print json.dumps(creds, indent=1)

    except Exception as e:
        print e
        print 'failed to open credentials file'
        sys.exit(1)

    try:

        startTime = datetime.datetime.now()
        print ''
        print startTime
        print json.dumps(inputLine,indent=1)
        shellScript = "source /sps/edelweis/kdata/dataprocessing/schedule/sps2hpssHook.sh"
        p = pexpect.spawn('/usr/bin/ssh %s@ccage.in2p3.fr "%s"' % (creds['sftp_username'], shellScript))
        ssh_newkey = 'Are you sure you want to continue connecting'
        i=p.expect([ssh_newkey,'password:',pexpect.EOF])
        if i==0:
            print 'accepting key'
            p.sendline('yes')
            i=p.expect([ssh_newkey,'password:',pexpect.EOF])
        if i==1:
            print startTime, 'sending password and running "%s" ' % shellScript
            p.sendline(creds['sftp_password'])
            p.expect(pexpect.EOF)
        elif i==2:
            print "I either got key or connection timeout"
            pass
    except Exception as e:
        print >> sys.stderr, '\n\n' + startTime + ':\n'
        traceback.print_exc()
        print e
        raise e
    
if __name__ == '__main__':
    if len(sys.argv) > 1: main(sys.argv[1])
    else: main('')
