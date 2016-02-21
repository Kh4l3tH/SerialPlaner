def ok(msg):
    print '[ \033[92m\033[1mok\033[0m ] {0}'.format(msg)
def fail(msg):
    print '[\033[91m\033[1mFAIL\033[0m] \033[1m{0}\033[0m'.format(msg)
def info(msg):
    print '[\033[96m\033[1minfo\033[0m] {0}'.format(msg)


import os

if os.getuid() != 0:
    info('Restarting installer as root')
    os.system('echo turbo | sudo -S python {0}'.format(__file__))
    print ''
    exit()

def blacklist():
    if os.path.isfile('/etc/modprobe.d/lp-blacklist.conf'):
        info('Kernel module \'lp\' already blacklisted')
    else:
        ok('Blacklisting kernel module \'lp\'')
        with open('/etc/modprobe.d/lp-blacklist.conf', 'w') as f:
            f.write('blacklist lp\n')


import grp
if not [group for group in grp.getgrall() if 'werker' in group.gr_mem and group.gr_name=='lp']:
    ok('Adding \'werker\' to group \'lp\'')
    if os.system('usermod -a -G lp werker') != 0:
        fail('\'werker\' could not be added to group \'lp\'')
    ok('Removing kernel module \'lp\'')
#    if os.system('rmmod lp') != 0:
#        fail('INSTALLATION NOT SUCCESSFUL')
    blacklist()
else:
    info('\'werker\' already in group \'lp\'')
    blacklist()





#COOOPPPPPYYY STUFFF





ok('\033[1mInstallation successful!\033[0m')
