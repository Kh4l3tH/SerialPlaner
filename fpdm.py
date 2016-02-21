from traceback import format_exc
from lib.log import log
from util import ParallelPort
from util import Schrittmotor
from util import Interpreter
from lib import commands
from lib import nanotec
from lib import serial
import ConfigParser



class FPDM():
    def __init__(self):
        path_config = 'cfg/FPDM.ini'
        log('Lade Config: {0}'.format(path_config))
        config = ConfigParser.ConfigParser()
        config.read(path_config)

        path_kss = 'cfg/Koordinatensysteme.ini'
        log('Lade Koordinatensysteme: {0}'.format(path_kss))
        config_kss = ConfigParser.ConfigParser()
        config_kss.read(path_kss)
        kss = {}
        for ks in config_kss.sections():
            kss[ks] = Schrittmotor.Koordinatensystem(config_kss, ks)

        log('Verbinde Parallel Port: {0}'.format(config.get('Settings', 'ParallelPort')))
        self.P = ParallelPort.ParallelPort(config.get('Settings', 'ParallelPort'))

        log('Verbinde Serielle Schnittstelle: {0}'.format(config.get('Settings', 'SerialPort')))
        self.com = serial.Serial(port = config.get('Settings', 'SerialPort'),
                            baudrate = config.get('Settings', 'Baudrate'),
                            timeout = 0.2)
        self.cmd = commands.Commands(nanotec.Nanotec(self.com))

        log('Verbinde X-Achse (Motoradresse: {0})'.format(config.getint('Motor_X', 'ID')))
        self.X = Schrittmotor.Schrittmotor(self.cmd,
                                           config.getint('Motor_X', 'ID'),
                                           config.getint('Motor_X', 'Schritte'),
                                           config.getint('Motor_X', 'Schrittmodus'),
                                           config.getint('Motor_X', 'Steigung'),
                                           config.get('Motor_X', 'Rampentyp'),
                                           config.getfloat('Motor_X', 'Rampe_Hz_pro_ms'),
                                           reference_pin = config.getint('Motor_X', 'reference_pin'))
        '''log('Verbinde C-Achse (Motoradresse: {0})'.format(config.getint('Motor_C', 'ID')))
        self.C = Schrittmotor.Schrittmotor(cmd,
                                           config.getint('Motor_C', 'ID'),
                                           config.getint('Motor_C', 'Schritte'),
                                           config.getint('Motor_C', 'Schrittmodus'),
                                           config.getint('Motor_C', 'Steigung'),
                                           config.get('Motor_C', 'Rampentyp'),
                                           config.getfloat('Motor_C', 'Rampe_Hz_pro_ms'),
                                           umin_default = config.getfloat('Motor_C', 'umin_default'))'''
        log('Verbinde Z-Achse (Motoradresse: {0})'.format(config.getint('Motor_Z', 'ID')))
        self.Z = Schrittmotor.Schrittmotor(self.cmd,
                                           config.getint('Motor_Z', 'ID'),
                                           config.getint('Motor_Z', 'Schritte'),
                                           config.getint('Motor_Z', 'Schrittmodus'),
                                           config.getint('Motor_Z', 'Steigung'),
                                           config.get('Motor_Z', 'Rampentyp'),
                                           config.getfloat('Motor_Z', 'Rampe_Hz_pro_ms'),
                                           reference_pin = config.get('Motor_Z', 'reference_pin'))

        log('Lade Interpreter')
        self.interpreter = Interpreter.Interpreter(self.X, 'self.C', self.Z, self.P, kss)
        log('Initialisierung abgeschlossen')

    def reference(axis):
        if self.P.getPin(axis.reference_pin) == False:
            log('Achse {0} nicht auf Referenzschalter. Verfahre Achse...'.format(axis.id))
            axis.move_rel(1000, inverted=False)
            while self.P.getPin(axis.reference_pin) == False:
                pass
            Axis.stop()
            Axis.wait()
        else:
            print 'Achse bereits auf Refenzschalter!'

        print 'Bewege Achse vor den Referenzschalter...'
        while P.getPin(axis.reference_pin) == True:
            Axis.move_rel(-0.003125, inverted=False)
            Axis.wait()
            print 'Pos: {0:.6f}, Pin {2}: {1}'.format(Axis.get_position(), P.getPin(axis.reference_pin), axis.reference_pin)
        return axis.get_position()

    def execute(self, path_gcode_file):
        # /home/werker/emc2/nc_files/TB526.ngc
        with open(path_gcode_file) as file:
            gcode = file.readlines()

        log('Starte Interpreter')
        try:
            self.interpreter.process(gcode)
        except ValueError as error:
            log(error)
            log('Programm nach Fehler beendet!')
            return error
        except BaseException:
            log(format_exc())
            log('Programm nach Fehler beendet!')
            return format_exc()
        finally:
            self.X.stop()
            self.Z.stop()
            # self.C.stop()

        return 0


def main():
    log('Programm gestartet')
    FPDM()

if __name__ == '__main__':
    main()
