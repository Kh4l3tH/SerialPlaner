import ConfigParser
import serial


config = ConfigParser.ConfigParser()
config.read('cfg/FPDM.ini')
try:
    com = serial.Serial(port     = config.get('Settings', 'SerialPort'),
                        baudrate = config.getint('Settings', 'Baudrate'),
                        timeout  = 0.2)
except:
    print 'Could not connect to serial port {0}'.format(config.get('Settings', 'SerialPort'))
    exit()

def get_motor():
    com.write('#*Zm\r')
    reply = com.readline()
    return reply.split('+')[-1].strip()

def set_motor(address):
    current_motor = get_motor()
    com.write('#{0}m{1}\r'.format(current_motor, address))
    reply = com.readline()
    return get_motor()

def get_state(motor):
    com.write('#{0}$\r'.format(motor))
    state = com.readline()
    if state:
        return '\033[92m{0}\033[0m'.format(state.split('$')[1].strip())
    return '\033[91mNicht erreichbar\033[0m'



X = config.getint('Motor_X', 'ID')
C = config.getint('Motor_C', 'ID')
Z = config.getint('Motor_Z', 'ID')

print 'Motor X: {0}'.format(get_state(X))
print 'Motor C: {0}'.format(get_state(C))
print 'Motor Z: {0}'.format(get_state(Z))

if not raw_input('\nSteuerkarte der X-Achse anschliessen'):
    print 'Alte Motoradresse: {0}'.format(get_motor())
    print 'Neue Motoradresse: {0}'.format(set_motor(X))

if not raw_input('\nSteuerkarte der C-Achse anschliessen'):
    print 'Alte Motoradresse: {0}'.format(get_motor())
    print 'Neue Motoradresse: {0}'.format(set_motor(C))

if not raw_input('\nSteuerkarte der Z-Achse anschliessen'):
    print 'Alte Motoradresse: {0}'.format(get_motor())
    print 'Neue Motoradresse: {0}'.format(set_motor(Z))


raw_input('\nAlle Steuerkarten anschliessen')
print '\nPruefe Status der Steuerkarten:'
print 'Motor X: {0}'.format(get_state(X))
print 'Motor C: {0}'.format(get_state(C))
print 'Motor Z: {0}'.format(get_state(Z))
