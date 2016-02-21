from PySide import QtCore
from PySide import QtGui


class MainWindow(object):
    def setup_ui(self):
        label_kss = self.label('Koordinatensysteme')
        self.list_kss = QtGui.QListWidget()
        
        
        label_cfg_x = self.label('X')
        label_cfg_z = self.label('Z')
        label_cfg_position = self.label('Cfg Position')
        self.label_config_x = self.label_sunken()
        self.label_config_z = self.label_sunken()
        label_cfg_inv = self.label('Cfg Inv.')
        self.check_config_x_inv = QtGui.QCheckBox()
        self.check_config_z_inv = QtGui.QCheckBox()
        self.check_config_x_inv.setDisabled(True)
        self.check_config_z_inv.setDisabled(True)
        label_cfg_position_new = self.label('New Position')
        self.edit_config_x = self.edit('-')
        self.edit_config_z = self.edit('-')
        label_cfg_inv_new = self.label('New Inv.')
        self.check_config_x_inv_new = QtGui.QCheckBox()
        self.check_config_z_inv_new = QtGui.QCheckBox()
        self.button_save_x = self.button('Save X')
        self.button_save_z = self.button('Save Z')
        
        group_config = QtGui.QGroupBox('Config')
        box_config = QtGui.QGridLayout()
        box_config.addWidget(label_cfg_x, 1, 0)
        box_config.addWidget(label_cfg_z, 2, 0)
        box_config.addWidget(label_cfg_position, 0, 1)
        box_config.addWidget(self.label_config_x, 1, 1)
        box_config.addWidget(self.label_config_z, 2, 1)
        box_config.addWidget(label_cfg_inv, 0, 2)
        box_config.addWidget(self.check_config_x_inv, 1, 2)
        box_config.addWidget(self.check_config_z_inv, 2, 2)
        box_config.addWidget(label_cfg_position_new, 0, 3)
        box_config.addWidget(self.edit_config_x, 1, 3)
        box_config.addWidget(self.edit_config_z, 2, 3)
        box_config.addWidget(label_cfg_inv_new, 0, 4)
        box_config.addWidget(self.check_config_x_inv_new, 1, 4)
        box_config.addWidget(self.check_config_z_inv_new, 2, 4)
        box_config.addWidget(self.button_save_x, 1, 5)
        box_config.addWidget(self.button_save_z, 2, 5)
        group_config.setLayout(box_config)
        
        
        label_def_x = self.label('X')
        label_def_z = self.label('Z')
        label_def = self.label('Default')
        self.label_position_x_default = self.label_sunken()
        self.label_position_z_default = self.label_sunken()
        self.button_reset_x = self.button('Reset X')
        self.button_reset_z = self.button('Reset Z')
        self.label_current_ks = self.label('KS')
        self.label_position_x_ks = self.label_sunken()
        self.label_position_z_ks = self.label_sunken()
        self.button_ks_x_plus = self.button('+')
        self.button_ks_x_minus = self.button('-')
        self.button_ks_z_plus = self.button('+')
        self.button_ks_z_minus = self.button('-')
        self.label_distance = self.label('Distance')
        self.edit_distance_x = self.edit('200')
        self.edit_distance_z = self.edit('20')
        self.label_speed = self.label('Speed')
        self.edit_speed_x = self.edit('100')
        self.edit_speed_z = self.edit('10')
        
        group_position = QtGui.QGroupBox('Position')
        box_position = QtGui.QGridLayout()
        box_position.addWidget(label_def_x, 1, 0)
        box_position.addWidget(label_def_z, 2, 0)
        box_position.addWidget(label_def, 0, 1)
        box_position.addWidget(self.label_position_x_default, 1, 1)
        box_position.addWidget(self.label_position_z_default, 2, 1)
        box_position.addWidget(self.button_reset_x, 1, 2)
        box_position.addWidget(self.button_reset_z, 2, 2)
        box_position.addWidget(self.label_current_ks, 0, 3)
        box_position.addWidget(self.label_position_x_ks, 1, 3)
        box_position.addWidget(self.label_position_z_ks, 2, 3)
        box_position.addWidget(self.button_ks_x_plus, 1, 4)
        box_position.addWidget(self.button_ks_z_plus, 2, 4)
        box_position.addWidget(self.button_ks_x_minus, 1, 5)
        box_position.addWidget(self.button_ks_z_minus, 2, 5)
        box_position.addWidget(self.label_distance, 0, 6)
        box_position.addWidget(self.edit_distance_x, 1, 6)
        box_position.addWidget(self.edit_distance_z, 2, 6)
        box_position.addWidget(self.label_speed, 0, 7)
        box_position.addWidget(self.edit_speed_x, 1, 7)
        box_position.addWidget(self.edit_speed_z, 2, 7)
        group_position.setLayout(box_position)
        
        
        self.button_backen = QtGui.QPushButton('Backen oeffnen/schliessen')
        self.button_spindel = QtGui.QPushButton('Spindel starten/stoppen')
        
        group_commands = QtGui.QGroupBox('Befehle')
        box_commands = self.hbox(self.button_backen,
                                 self.button_spindel)
        group_commands.setLayout(box_commands)
        
        
        box_main = self.vbox(label_kss,
                             self.list_kss,
                             group_config,
                             group_position,
                             group_commands)
                             
        self.setLayout(box_main)
        
    def hbox(self, *args):
        hbox = QtGui.QHBoxLayout()
        for object in args:
            if isinstance(object, QtGui.QLayout):
                hbox.addLayout(object)
            else:
                hbox.addWidget(object)
        return hbox
        
    def vbox(self, *args):
        vbox = QtGui.QVBoxLayout()
        for object in args:
            if isinstance(object, QtGui.QLayout):
                vbox.addLayout(object)
            else:
                vbox.addWidget(object)
        return vbox
        
    def button(self, text):
        button = QtGui.QPushButton(text)
        button.setFixedWidth(100)
        return button
        
    def edit(self, text='-'):
        edit = QtGui.QLineEdit(text)
        edit.setAlignment(QtCore.Qt.AlignRight)
        return edit
        
    def label(self, text = ''):
        label = QtGui.QLabel(text)
        return label
        
    def label_sunken(self, text='-'):
        label = QtGui.QLabel(text)
        label.setFrameStyle(QtGui.QFrame.Panel | QtGui.QFrame.Sunken)
        return label
        # label.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)
        # label.setFixedWidth(65)
        