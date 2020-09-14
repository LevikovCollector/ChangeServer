from PyQt5.QtWidgets import QWidget, QFileDialog,  QTableWidgetItem, QHeaderView, QMessageBox
from PyQt5.Qt import Qt
from PyQt5.QtCore import QDir
from PyQt5 import uic


from DB.settings_db import add_new_settings, get_settings_by_type, upd_settings_by_type
from DB.file_for_copy import get_all_files_with_id, upd_status, add_file, del_file


class FileToCopy(QWidget):
    def __init__(self, parent=None):
        super(FileToCopy, self).__init__(parent)
        uic.loadUi('ui\\file_to_copy.ui', self)
        self.setWindowFlags(Qt.Dialog | Qt.WindowCloseButtonHint)
        self.setWindowModality(Qt.WindowModal)

        self.dir_line_edit_from.setText(get_settings_by_type(self.dir_line_edit_from.property('TypeField')))
        self.dir_line_edit_to.setText(get_settings_by_type(self.dir_line_edit_to.property('TypeField')))

        self.dir_button_dial_to.clicked.connect(self.open_dial)
        self.dir_button_dial_from.clicked.connect(self.open_dial)
        self.add_files_name_button.clicked.connect(self.open_dial)
        self.delete_file_name_button.clicked.connect(self.remove_file_name)

        self.table_files.itemClicked.connect(self.up_file_state)

        self.create_table_files()

    def up_file_state(self, item):
        file_id = int(self.table_files.item(item.row(), 0).text())
        if item.checkState() == Qt.Checked:
            upd_status(file_id, 1)
        else:
            upd_status(file_id, 0)

    def create_table_files(self):
        all_files = get_all_files_with_id()
        self.table_files.setRowCount(len(all_files))
        self.table_files.setColumnCount(2)
        header = self.table_files.horizontalHeader()
        for index in range(0, len(all_files)):
            file = all_files[index]

            self.table_files.setItem(index, 0, QTableWidgetItem(str(file[0])))
            item = QTableWidgetItem('{}'.format(file[1]))
            item.setFlags(Qt.ItemIsUserCheckable | Qt.ItemIsEnabled)
            if file[2]:
                item.setCheckState(Qt.Checked)
            else:
                item.setCheckState(Qt.Unchecked)

            self.table_files.setItem(index, 1, item)
        self.table_files.setColumnHidden(0, True)
        header.setSectionResizeMode(1, QHeaderView.Stretch)

    def remove_file_name(self):
        try:
           file_id = int(self.table_files.item(self.table_files.currentRow(), 0).text())
           del_file(file_id)
           self.create_table_files()

        except Exception:
            QMessageBox.warning(self, 'Ошибка', 'Выберите строку')

    def open_dial(self):
        sender = self.sender()
        sender_object_name = sender.objectName()

        if sender_object_name in['dir_button_dial_from', 'dir_button_dial_to']:
            dir_url = QFileDialog.getExistingDirectory(parent=self, caption='Выбериет папку')
            if dir_url != '':
                if sender_object_name == 'dir_button_dial_from':
                    if get_settings_by_type('edit_from') == '':
                        add_new_settings(dir_url, self.dir_line_edit_from.property('TypeField'))

                    else:
                        upd_settings_by_type(dir_url, self.dir_line_edit_from.property('TypeField'))
                    self.dir_line_edit_from.setText(dir_url)

                if sender_object_name == 'dir_button_dial_to':
                    if get_settings_by_type('edit_to') == '':
                        add_new_settings(dir_url, self.dir_line_edit_to.property('TypeField'))
                    else:
                        upd_settings_by_type(dir_url, self.dir_line_edit_to.property('TypeField'))
                    self.dir_line_edit_to.setText(dir_url)

        elif sender_object_name == 'add_files_name_button':
            dlg_chosen_files = QFileDialog(self)
            dlg_chosen_files.setFileMode(QFileDialog.ExistingFiles)
            dlg_chosen_files.setWindowTitle('Выберите файлы')
            dlg_chosen_files.setFilter(QDir.Files)
            if dlg_chosen_files.exec_():
                raw_chosen_files = dlg_chosen_files.selectedFiles()
                for file in raw_chosen_files:
                    f_name = file.split('/')[-1]
                    add_file(f_name, 1)
            self.create_table_files()





