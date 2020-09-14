from PyQt5.QtWidgets import QWidget, QFileDialog, QMessageBox
from PyQt5.Qt import Qt
from PyQt5 import uic

from DB.settings_db import add_new_settings, upd_settings_by_type, get_settings_by_type


class PathForm(QWidget):
    def __init__(self, parent=None):
        super(PathForm, self).__init__(parent)
        uic.loadUi('ui\paths_form.ui', self)

        self.setWindowFlags(Qt.Dialog | Qt.WindowCloseButtonHint)
        self.setWindowModality(Qt.WindowModal)

        self.dir_url = get_settings_by_type(self.dir_line_edit.property('TypeField'))
        self.ini_url = get_settings_by_type(self.ini_line_edit.property('TypeField'))
        self.exe_url = get_settings_by_type(self.exe_line_edit.property('TypeField'))
        self.cnv_url = get_settings_by_type(self.datacnv_line_edit.property('TypeField'))

        self.dir_line_edit.setText(self.dir_url)
        self.ini_line_edit.setText(self.ini_url)
        self.exe_line_edit.setText(self.exe_url)
        self.datacnv_line_edit.setText(self.cnv_url)

        self.dir_button_dial.clicked.connect(self.open_dial)
        self.ini_button_dial.clicked.connect(self.open_dial)
        self.exe_button_dial.clicked.connect(self.open_dial)
        self.datacnv_button_dial.clicked.connect(self.open_dial)

        self.save_button.clicked.connect(self.save_settings)



    def save_settings(self):
        setting_1 =  get_settings_by_type(self.dir_line_edit.property('TypeField'))
        setting_2 =  get_settings_by_type(self.ini_line_edit.property('TypeField'))
        setting_3 =  get_settings_by_type(self.exe_line_edit.property('TypeField'))
        setting_4 = get_settings_by_type(self.datacnv_line_edit.property('TypeField'))

        if setting_1 == '' and setting_2 == '' and setting_3 == '' and setting_4 == '':
            add_new_settings(self.dir_url, self.dir_line_edit.property('TypeField'))
            add_new_settings(self.ini_url, self.ini_line_edit.property('TypeField'))
            add_new_settings(self.exe_url, self.exe_line_edit.property('TypeField'))
            add_new_settings(self.cnv_url, self.datacnv_line_edit.property('TypeField'))
        else:
            upd_settings_by_type(self.dir_line_edit.text(), self.dir_line_edit.property('TypeField'))
            upd_settings_by_type(self.ini_line_edit.text(), self.ini_line_edit.property('TypeField'))
            upd_settings_by_type(self.exe_line_edit.text(), self.exe_line_edit.property('TypeField'))
            upd_settings_by_type(self.datacnv_line_edit.text(), self.datacnv_line_edit.property('TypeField'))

        QMessageBox.information(self, 'Уведомление', 'Запись завершена')
        self.close()

    def open_dial(self):
        sender = self.sender()
        sender_object_name = sender.objectName()

        if sender_object_name == 'dir_button_dial':
            self.dir_url = QFileDialog.getExistingDirectory(parent=self, caption='Выбериет папку')
            if self.dir_url != '':
                self.dir_line_edit.setText(self.dir_url)

        elif sender_object_name == 'ini_button_dial':
            self.ini_url = QFileDialog.getOpenFileName(parent=self, caption='Выберите ini файл',
                                                       filter='Конфигурационные файлы (*.ini)')[0]
            if self.ini_url != '':
                self.ini_line_edit.setText(self.ini_url)

        elif sender_object_name == 'exe_button_dial':
            self.exe_url = \
            QFileDialog.getOpenFileName(parent=self, caption='Выберите exe файл', filter='Исполняемый файл (*.exe)')[0]
            if self.exe_url != '':
                self.exe_line_edit.setText(self.exe_url)

        elif sender_object_name == 'datacnv_button_dial':
            self.cnv_url = \
            QFileDialog.getOpenFileName(parent=self, caption='Выберите wdatacnv.exe',
                                            filter='sdatacnv, sdatacnv64, wdatacnv (sdatacnv.exe; wdatacnv.exe; sdatacnv64.exe )')[0]
            if self.cnv_url != '':
                self.datacnv_line_edit.setText(self.cnv_url)
