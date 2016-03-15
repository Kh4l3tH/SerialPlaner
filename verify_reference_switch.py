from ParallelPort import ParallelPort
from Schrittmotor import Schrittmotor
from Nanotec import commands
from Nanotec import nanotec
import serial

# Falls alles funzt:

# from fpdm import FPDM
# fpdm = FPDM()
# list_null = []
# for x in range(10):
#     list_null.append(fpdm.X.reference())
# print list_null
# print '='*80
# print 'Max = {0}'.format(max(list_null))
# print 'Min = {0}'.format(min(list_null))
# print 'Delta = \033[92m{0}\033[0m'.format(min(list_null))

com = serial.Serial('/dev/ttyUSB0',
                    115200,
                    timeout = 0.2)

cmd = commands.Commands(nanotec.Nanotec(com))
P = ParallelPort.ParallelPort('/dev/parport1')

#############################
#X:
id = 1
pin = 10
#Z:
#id = 3
#pin = 12
#############################


Axis = Schrittmotor.Schrittmotor(cmd, id, 200, 8, 5, 'SINUS', 4, reference_pin = pin)

def ref(Axis):
    if P.getPin(Axis.reference_pin) == True:
        print 'Achse {0} nicht auf Referenzschalter. Verfahre Achse...'.format(Axis.id)
        Axis.move_rel(1000, 100)
        while P.getPin(Axis.reference_pin) == True:
            pass
        Axis.stop()
        Axis.wait()
    else:
        print 'Achse bereits auf Refenzschalter!'
        Axis.move_rel(-10)
        Axis.wait()
        Axis.move_rel(1000, 100)
        while P.getPin(Axis.reference_pin) == True:
            pass
        Axis.stop()
        Axis.wait()

    print 'Bewege Achse vor den Referenzschalter...'
    # Kompensation um Geschwindigkeit zu erhoehen
    Axis.move_rel(-0.15)
    Axis.wait()
    #print ''
    if P.getPin(Axis.reference_pin) == True:
        raise ValueError('Kompensation zu hoch!')
    while P.getPin(Axis.reference_pin) == False:
        Axis.move_rel(-0.003125, 100)
        Axis.wait()
        print 'Pos: {0:.6f}, Pin {2}: {1}'.format(Axis.get_position(), P.getPin(Axis.reference_pin), Axis.reference_pin)
    return Axis.get_position()

print 'Final Pos: {0}'.format(ref(Axis))

exit()

list_null = []
for x in range(10):
    list_null.append(ref(Axis))
print list_null
print '='*80
print 'Max = {0}'.format(max(list_null))
print 'Min = {0}'.format(min(list_null))
print 'Delta = \033[92m{0}\033[0m'.format(min(list_null))

print '0-Punkt der Achse; {0}'.format(Axis.get_position())
# Und auch testen, ob die Referenzfahrt von LinuxCNC genau ist, bzw wie genau -> Ref -> Home -> Ref*X -> dHome
# An der Stelle testen was passiert wenn du drueber faerst und ob dann der Referenzschalter aus geht!!!
# An der Stelle testen was passiert wenn du drueber faerst und ob dann der Referenzschalter aus geht!!!
# Nix vermutlich
# An der Stelle testen was passiert wenn du drueber faerst und ob dann der Referenzschalter aus geht!!!
# An der Stelle testen was passiert wenn du drueber faerst und ob dann der Referenzschalter aus geht!!!
