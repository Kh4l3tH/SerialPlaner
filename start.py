from fpdm import fpdm

q = fpdm()

print '\nX Pos: {}'.format(q.X.get_position())
print 'Z Pos: {}'.format(q.Z.get_position())

if not raw_input('\nX-Achse resetten?') == 'n':
    print 'Resetting X...'
    q.X.reset_position()

if not raw_input('\nX-Achse resetten?') == 'n':
    print 'Resetting Z...'
    q.Z.reset_position()

print '\nX Pos: {}'.format(q.X.get_position())
print 'Z Pos: {}'.format(q.Z.get_position())

while raw_input('Einzelfahrt?') == 'n':
    q.execute('/home/werker/test.ngc')

while True:
    print 'Pin 15: {0}'.format(q.P.getPin(15))
    try:
        if q.P.getPin(15) == False:
            q.execute('/home/werker/test.ngc')
    except:
        break
