# python script to upload via FTP

import os
import sys
import ftplib
import logging
from RMS.Logger import initLogging
from importlib import import_module as impmod
import RMS.ConfigReader as cr
import paramiko


def uploadviaFTP(arch_dir, ftpdets, log, checkfortest=''):
    _, mp4name = os.path.split(arch_dir)
    mp4name = mp4name + '.mp4'
    fullname = os.path.join(arch_dir, mp4name)
    targpth = ftpdets[3]
    if len(targpth) > 0: 
        targpth = targpth +'/'

    # rename the file to UKxxxx_latest.mp4. 
    newfile =mp4name[:7] + 'latest.mp4'

    if checkfortest == 'test':
        fullname = 'README.md'
        newfile = 'README.md.new'

    log.info(f'uploading {mp4name} to {ftpdets[1]}@{ftpdets[0]}:{targpth}{newfile}')

    proto='ftp'
    if len(ftpdets) == 5:
        proto = ftpdets[4].lower()

    log.info(f'using protocol {proto}')

    if proto == 'ftp': 
        session = ftplib.FTP(ftpdets[0],ftpdets[1],ftpdets[2])
        if ftpdets[3] != '':
            session.cwd(ftpdets[3])
        with open(fullname,'rb') as uplf:                   # file to send
            session.storbinary(f'STOR {newfile}', uplf)     # send the file
        session.quit()    

    elif proto == 'ftps':
        session = ftplib.FTP_TLS(ftpdets[0], ftpdets[1],ftpdets[2])
        session.prot_p()
        if ftpdets[3] != '':
            session.cwd(ftpdets[3])
        with open(fullname,'rb') as uplf:                   # file to send
            session.storbinary(f'STOR {newfile}', uplf)     # send the file
        session.quit()    

    elif proto == 'sftp':
        ssh_client = paramiko.SSHClient()
        ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh_client.connect(ftpdets[0], username=ftpdets[1], password=ftpdets[2])
        ftp_client = ssh_client.open_sftp()
        if ftpdets[3] != '':
            newfile = ftpdets[3] + '/' + newfile
        ftp_client.put(fullname, newfile)
        ftp_client.close()
        pass
    else:
        log.info(f'Unknown protocol {proto} - must be one of ftp, sftp or ftps')
    return 


def rmsExternal(cap_dir, arch_dir, config):

    # clear existing log handlers
    log = logging.getLogger("logger")
    while len(log.handlers) > 0:
        log.removeHandler(log.handlers[0])
        
    initLogging(config, 'ftpu_')
    log.info('mp4toftp external script started')
    
    rebootlockfile = os.path.join(config.data_dir, config.reboot_lock_file)
    with open(rebootlockfile, 'w') as f:
        f.write('1')

    myloc = os.path.split(os.path.abspath(__file__))[0]
    log.info('app home is {}'.format(myloc))

    _, checkfortest = os.path.split(cap_dir)
    if checkfortest == 'test':
        inifname = 'mp4toftp.ini.test'        
    else:
        inifname = 'mp4toftp.ini'

    if not os.path.isfile(os.path.join(myloc, inifname)):
        log.info('mp4toftp config file missing, cannot upload')
    else:
        with open (os.path.join(myloc, inifname), 'r') as inf:
            lis = inf.readlines()
        ftpdets = []
        for li in lis:
            if li[0] == '#':
                continue
            ftpdets.append(li.split(':')[1].strip())
        uploadviaFTP(arch_dir, ftpdets, log, checkfortest)

    log.info('about to test for extra script')
    try:
        with open(os.path.join(myloc, 'extrascript'),'r') as extraf:
            extrascript=extraf.readline().strip()

        log.info(f'running additional script {extrascript}')
        sloc, sname = os.path.split(extrascript)
        sys.path.append(sloc)
        scrname, _ = os.path.splitext(sname)
        nextscr=impmod(scrname)
        nextscr.rmsExternal(cap_dir, arch_dir, config)
    except (IOError,OSError):
        log.info('additional script not called')
        try:
            os.remove(rebootlockfile)
        except:
            log.info('unable to remove reboot lock file, pi may not reboot')
            pass

    while len(log.handlers) > 0:
        log.removeHandler(log.handlers[0])
    return


if __name__ == '__main__':
    dated_dir = sys.argv[1]
    try:
        config = cr.parse(os.path.expanduser('~/source/RMS/.config'))
    except:
        config = cr.parse(os.path.expanduser(sys.argv[2]))

    cap_dir = os.path.join(config.data_dir, 'CapturedFiles', dated_dir)
    arch_dir = os.path.join(config.data_dir, 'ArchivedFiles', dated_dir)
    rmsExternal(cap_dir, arch_dir, config)
