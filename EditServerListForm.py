from PyQt5.QtWidgets import QWidget, QDialogButtonBox, QMessageBox
from PyQt5.Qt import Qt
from PyQt5 import uic
from DB.hosts_db import upd_host, add_host


class EditServerList(QWidget):
    def __init__(self, parent=None, item=None):
        super(EditServerList, self).__init__(parent)
        uic.loadUi('ui\edit_server_list.ui',  self)
        self.ch_item = None
        if item is None:
            self.setWindowTitle('Новый сервер')
            self.id_change_item = ''
        else:
            self.setWindowTitle('Сервер: {}'.format(item[1]))
            self.host_name_edit.setText(item[1])
            self.host_link_edit.setText(item[2])
            self.host_comment_edit.setText(item[3])

            self.id_change_item = int(item[0])
        self.setWindowFlags(Qt.Dialog | Qt.WindowCloseButtonHint)
        self.setWindowModality(Qt.WindowModal)
        self.save_box.button(QDialogButtonBox.Save).setText('Сохранить')
        self.save_box.button(QDialogButtonBox.Cancel).setText('Отменить')

        self.save_box.button(QDialogButtonBox.Save).clicked.connect(self.save_server)
        self.save_box.button(QDialogButtonBox.Cancel).clicked.connect(self.close)

    def save_server(self):

        host_name = self.host_name_edit.text()
        host_link = self.host_link_edit.text()
        host_comment = self.host_comment_edit.text()

        if host_name != '':
            if self.id_change_item == '':
                pass
                add_host(host_name, host_link, host_comment)

                self.close()
            else:

                upd_host(self.id_change_item, host_name, host_link, host_comment)
                self.close()
            self.parent().create_table_host()
        else:
            QMessageBox.warning(self, 'Внимание!', 'Введите данные')




