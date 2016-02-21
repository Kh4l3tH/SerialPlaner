motor = 1       #raw_input('Motornummer = ')
satz_nr = 0     #raw_input('Satznummer = ')


from lib import serial
from re import search
print '='*80
com = None
for port in range(0,10):
    try:
        com = serial.Serial('/dev/ttyUSB{0}'.format(port), 115200, timeout  = 0.2)
        print 'Connnected on /dev/ttyUSB{0}'.format(port)
        break
    except:
        print 'Could not connect on /dev/ttyUSB{0}'.format(port)

if not com: exit()

list = [('Positionsmodus', 'p'),
        ('Verfahrweg', 's'),
        ('Anfangschrittfrequenz','u'),
        ('Maximalschrittfrequenz', 'o'),
        ('Zweite Max.schrittfreq.', 'n'),
        ('Beschleunigungsrampe', 'b'),
        ('Bremsrampe', 'B'),
        ('Drehrichtung', 'd'),
        ('Drehrichtungsumkehr', 't'),
        ('Wiederholungen', 'W'),
        ('Pause Wdhlg. / Folgesatz', 'P'),
        ('Satznummer Folgesatz', 'N'),
        ('Max. Ruck Beschl.rampe', ':b'),
        ('Max. Ruck Bremsrampe', ':B')]




com.write('#{0}Z{1}|\r'.format(motor, satz_nr))
satz = com.readline(eol='\r')

print '='*80
print 'Motor 1, Satz 0:\n{0}'.format(satz)
print '='*80
for item in list:
    pattern = '(?<={0})[^a-zA-Z:\s]+'.format(item[1])
    try:
        result = search(pattern, satz).group()
        print '{0:25}{1:>2} {2:>8}'.format(item[0], item[1], result)
    except:
        print '{0:25}{1:>2}        -'.format(item[0], item[1])


print '='*80
com.write('#{0}ZE\r'.format(motor))
code = com.readline(eol='\r').split('+')[1].strip()
print 'Fehlerposition: \033[92m{0}\033[0m'.format(code)

list = []
for n in range(1,33):
    com.write('#{0}Z{1}E\r'.format(motor, n))
    reply = com.readline(eol='\r').split('+')[1].strip()
    list.append(reply)
    
for n in range(0, 8):
    print '{0:2}:\033[91m{4:2}\033[0m {1:2}:\033[91m{5:2}\033[0m {2:2}:\033[91m{6:2}\033[0m {3:2}:\033[91m{7:2}\033[0m '.format(
        n*4+1, n*4+2, n*4+3, n*4+4,
        list[n*4], list[n*4+1], list[n*4+2], list[n*4+3])

print '='*80
print 'FEHLEN NOCH DIE GANZEN EINSTELLUNGEN DER RAMPEN USW.!!!'