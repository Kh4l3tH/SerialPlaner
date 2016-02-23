from Schrittmotor import Koordinatensystem
from Schrittmotor import Schrittmotor
from ParallelPort import ParallelPort
from Nanotec import commands
from Nanotec import nanotec
from gui import configure_gui
from subprocess import call
from PySide import QtCore
from PySide import QtGui
from time import sleep
import ConfigParser
import serial
import sys



class Configure(QtGui.QWidget, configure_gui.MainWindow):
    def __init__(self):
        super(Configure, self).__init__()
        self.setup_ui()

        self.list_kss.currentItemChanged.connect(self.load_new_ks)

        self.button_reset_x.clicked.connect(self.reference_x)
        self.button_reset_z.clicked.connect(self.reference_z)
        self.button_save_x.clicked.connect(lambda: self.save_ks('X'))
        self.button_save_z.clicked.connect(lambda: self.save_ks('Z'))

        self.button_ks_x_plus.clicked.connect(lambda: self.X.move_rel(  float(self.edit_distance_x.text()), float(self.edit_speed_x.text()), self.ks_current.x_inverted))
        self.button_ks_x_minus.clicked.connect(lambda: self.X.move_rel(-float(self.edit_distance_x.text()), float(self.edit_speed_x.text()), self.ks_current.x_inverted))
        self.button_ks_z_plus.clicked.connect(lambda: self.Z.move_rel(  float(self.edit_distance_z.text()), float(self.edit_speed_z.text()), self.ks_current.z_inverted))
        self.button_ks_z_minus.clicked.connect(lambda: self.Z.move_rel(-float(self.edit_distance_z.text()), float(self.edit_speed_z.text()), self.ks_current.z_inverted))

        self.button_backen.clicked.connect(self.toggle_backen)
        self.button_spindel.clicked.connect(self.toggle_spindel)

        self.timer_position_update = QtCore.QTimer(self)
        self.timer_position_update.timeout.connect(self.position_update)

        self.path_config = 'cfg/FPDM.ini'
        print 'Lade Konfigurationsdatei {0}'.format(self.path_config)
        self.config = ConfigParser.ConfigParser()
        self.config.read(self.path_config)
        self.load_kss_from_ini()

        print 'Verbinde Parallelport {0}'.format(self.config.get('Settings', 'ParallelPort'))
        self.pport = ParallelPort.ParallelPort(self.config.get('Settings', 'ParallelPort'))

        print 'Verbinde Serielle Schnittstelle '.format(self.config.get('Settings', 'SerialPort'))
        cmd = commands.Commands(nanotec.Nanotec(serial.Serial(port = self.config.get('Settings', 'SerialPort'),
                                                              baudrate = self.config.get('Settings', 'Baudrate'),
                                                              timeout = 0.2)))
        print 'Verbinde X-Achse (Motoradresse {0})'.format(self.config.getint('Motor_X', 'ID'))
        self.X = Schrittmotor.Schrittmotor(cmd,
                                           self.config.getint('Motor_X', 'ID'),
                                           self.config.getint('Motor_X', 'Schritte'),
                                           self.config.getint('Motor_X', 'Schrittmodus'),
                                           self.config.getint('Motor_X', 'Steigung'),
                                           self.config.get('Motor_X', 'Rampentyp'),
                                           self.config.getfloat('Motor_X', 'Rampe_Hz_pro_ms'),
                                           reference_pin = self.config.getint('Motor_X', 'reference_pin'))
        print 'Verbinde C-Achse (Motoradresse {0})'.format(self.config.getint('Motor_C', 'ID'))
        self.C = Schrittmotor.Schrittmotor(cmd,
                                           self.config.getint('Motor_C', 'ID'),
                                           self.config.getint('Motor_C', 'Schritte'),
                                           self.config.getint('Motor_C', 'Schrittmodus'),
                                           self.config.getint('Motor_C', 'Steigung'),
                                           self.config.get('Motor_C', 'Rampentyp'),
                                           self.config.getfloat('Motor_C', 'Rampe_Hz_pro_ms'),
                                           umin_default = self.config.getfloat('Motor_C', 'umin_default'))
        print 'Verbinde Z-Achse (Motoradresse {0})'.format(self.config.getint('Motor_Z', 'ID'))
        self.Z = Schrittmotor.Schrittmotor(cmd,
                                           self.config.getint('Motor_Z', 'ID'),
                                           self.config.getint('Motor_Z', 'Schritte'),
                                           self.config.getint('Motor_Z', 'Schrittmodus'),
                                           self.config.getint('Motor_Z', 'Steigung'),
                                           self.config.get('Motor_Z', 'Rampentyp'),
                                           self.config.getfloat('Motor_Z', 'Rampe_Hz_pro_ms'),
                                           reference_pin = self.config.get('Motor_Z', 'reference_pin'))

        self.timer_position_update.start(50)

    def reference_x(self):
        print self.pport.getPin(10) #False -> Home
        self.X.reset_position()

    def reference_z(self):
        print self.pport.getPin(12) #False -> Home
        self.Z.reset_position()

    def toggle_backen(self):
        if self.pport.getPin(9) == True:
            print 'Backen oeffnen'
            self.pport.setPin(9, False)
        else:
            print 'Backen schliessen'
            self.pport.setPin(9, True)

    def toggle_spindel(self):
        if self.C.ready():
            self.C.rotate()
        else:
            self.C.stop()
#        if self.pport.getPin(5) == True:
#            print 'Spindel aus'
#            self.pport.setPin(4, True)
#            self.pport.setPin(5, True)
#            sleep(1.5)
#            self.pport.setPin(4, False)
#            self.pport.setPin(5, False)
#            self.pport.setPin(5, False)
#        else:
#            print 'Spindel ein'
#            self.pport.setPin(5, True)


    def save_ks(self, mode):
        with open(self.path_kss, 'w') as file:
            if mode == 'X':
                self.config_kss.set(self.ks_current.name, 'x_offset', self.edit_config_x.text())
                self.config_kss.set(self.ks_current.name, 'x_inverted', self.check_config_x_inv_new.isChecked())
            elif mode == 'Z':
                self.config_kss.set(self.ks_current.name, 'z_offset', self.edit_config_z.text())
                self.config_kss.set(self.ks_current.name, 'z_inverted', self.check_config_z_inv_new.isChecked())
            self.config_kss.write(file)
        self.load_kss_from_ini()
        self.load_new_ks()


    def load_kss_from_ini(self):
        update_list_kss = False
        if self.list_kss.count() == 0:
            self.path_kss = 'cfg/Koordinatensysteme.ini'
            print 'Lade Koordinatensysteme: {0}'.format(self.path_kss)
            self.config_kss = ConfigParser.ConfigParser()
            update_list_kss = True
        self.config_kss.read(self.path_kss)
        self.ks = {}
        for ks in self.config_kss.sections():
            self.ks[ks] = Koordinatensystem.Koordinatensystem(self.config_kss, ks)
            if update_list_kss == True:
                self.list_kss.addItem(ks)
        if update_list_kss == True:
            self.list_kss.setCurrentItem(self.list_kss.item(0))

    def load_new_ks(self):
        self.ks_current = self.ks[self.list_kss.currentItem().text()]
        self.label_config_x.setText(str(self.ks_current.x_offset))
        self.label_config_z.setText(str(self.ks_current.z_offset))
        self.label_current_ks.setText(self.ks_current.name)
        if self.ks_current.x_inverted:
            self.check_config_x_inv.setChecked(True)
            self.check_config_x_inv_new.setChecked(True)
        else:
            self.check_config_x_inv.setChecked(False)
            self.check_config_x_inv_new.setChecked(False)
        if self.ks_current.z_inverted:
            self.check_config_z_inv.setChecked(True)
            self.check_config_z_inv_new.setChecked(True)
        else:
            self.check_config_z_inv.setChecked(False)
            self.check_config_z_inv_new.setChecked(False)

    def position_update(self):
        # if self.edit_config_x.hasFocus():
        pos_x = '{0:.6f}'.format(self.X.get_position())
        pos_z = '{0:.6f}'.format(self.Z.get_position())
        pos_x_ks = '{0:.6f}'.format(self.X.get_position(self.ks_current.x_offset, self.ks_current.x_inverted))
        pos_z_ks = '{0:.6f}'.format(self.Z.get_position(self.ks_current.z_offset, self.ks_current.z_inverted))
        self.label_position_x_ks.setText(pos_x_ks)
        self.label_position_z_ks.setText(pos_z_ks)
        self.label_position_x_default.setText(pos_x)
        self.label_position_z_default.setText(pos_z)
        self.edit_config_x.setText(pos_x)
        self.edit_config_z.setText(pos_z)
        print 'Pin 10: {0}'.format(self.pport.getPin(10))
        print 'Pin 12: {0}'.format(self.pport.getPin(12))


def main():
    app = QtGui.QApplication(sys.argv)
    configure = Configure()
    configure.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
