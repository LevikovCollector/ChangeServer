from PyQt5.QtWidgets import QMainWindow, QMessageBox, QProgressDialog, QMenu, QAction, QTableWidgetItem, QHeaderView,  \
    QApplication, QStyleFactory
from PyQt5 import uic
from PyQt5.QtCore import QThread, pyqtSignal
from PyQt5.Qt import Qt
from PathsForm import PathForm
from FileToCopy import FileToCopy
from EditServerListForm import EditServerList
from win32com.client import Dispatch
from parser_ini_file import  chanche_server
from log_work import log_new_line
import psutil
import time
import os
import shutil
import logging
import sys

from DB.hosts_db import get_all_hosts_name_and_comment_with_id, get_all_info_by_id, delete_host, get_host_link_by_id, add_host
from DB.settings_db import get_settings_by_type
from DB.file_for_copy import get_all_ch_file
from DB.conf import create_DB
import sqlalchemy.sql.default_comparator

LOG_PATH = 'log.log'


class MainForm(QMainWindow):
    def __init__(self):
        super(MainForm, self).__init__()
        uic.loadUi("ui\mainForm.ui", self)

        logging.basicConfig(format=u'%(levelname)s %(message)s', level=logging.INFO,
                            filename=LOG_PATH)

        self.copy_thread = CopyProcess(self)

        self.create_table_host()

        self.path_action.triggered.connect(self.open_path_settings)
        self.copy_file_action.triggered.connect(self.open_copy_files_settings)

        self.table_hosts.cellDoubleClicked.connect(self.edit_server_name)

        self.run_button.clicked.connect(self.run)
        self.clear_log_button.clicked.connect(self.clear_log)
        self.update_files_button.clicked.connect(self.run_copy)
        self.copy_thread.copy_done.connect(self.upd_progress_bar)
        self.copy_thread.finished.connect(self.get_and_set_file_version)
        self.refresh_version_button.clicked.connect(self.get_and_set_file_version)

        self.table_hosts.setContextMenuPolicy(Qt.CustomContextMenu)
        self.table_hosts.customContextMenuRequested.connect(self.open_con_menu)

        self.set_log_info()
        self.get_and_set_file_version()

    def create_table_host(self):
        all_host = get_all_hosts_name_and_comment_with_id()
        self.table_hosts.setRowCount(len(all_host))
        self.table_hosts.setColumnCount(2)
        header = self.table_hosts.horizontalHeader()
        for index in range(0,len(all_host)):
            host = all_host[index]
            self.table_hosts.setItem(index, 0, QTableWidgetItem(str(host[0])))
            if host[2] != '':
                self.table_hosts.setItem(index, 1, QTableWidgetItem('{} ({})'.format(host[1], host[2])))
            else:
                self.table_hosts.setItem(index, 1, QTableWidgetItem('{}'.format(host[1])))
        self.table_hosts.setColumnHidden(0, True)
        header.setSectionResizeMode(1, QHeaderView.Stretch)

    def open_con_menu(self, position):

        if self.table_hosts.itemAt(position):
            con_menu = QMenu()

            add_server = QAction('Добавить', con_menu)
            add_server.triggered.connect(self.add_server_to_list)
            con_menu.addAction(add_server)

            copy_link = QAction('Скопировать ссылку', con_menu)
            copy_link.triggered.connect(self.copy_host_link)
            con_menu.addAction(copy_link)
            if get_host_link_by_id(self.get_current_host_id())[0] != '127.0.0.1':
                del_server = QAction('Удалить', con_menu)
                del_server.triggered.connect(self.ask_question_delete)
                con_menu.addAction(del_server)

            con_menu.exec_(self.table_hosts.viewport().mapToGlobal(position))

    def copy_host_link(self):
        h_link = get_host_link_by_id(self.get_current_host_id())[0]

        QApplication.clipboard().setText(h_link)

    def ask_question_delete(self):

        q_mess = QMessageBox(self)
        q_mess.setIcon(QMessageBox.Question)
        q_mess.setWindowTitle('Вопрос')
        q_mess.setText('Вы уверены что хотите удалить запись?')
        q_mess.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        q_mess.button(QMessageBox.Yes).setText('Да')
        q_mess.button(QMessageBox.No).setText('Нет')
        q_mess.buttonClicked.connect(self.question_button_pressed)
        q_mess.show()

    def get_current_host_id(self):
        return int(self.table_hosts.item(self.table_hosts.currentRow(), 0).text())

    def question_button_pressed(self, button):

        if button.text() == 'Да':
            id_host = self.get_current_host_id()
            delete_host(id_host)
            self.create_table_host()

    def add_server_to_list(self):
        edit_server_form = EditServerList(self)
        edit_server_form.show()

    def edit_server_name(self, row):

        ch_host = get_all_info_by_id(int(self.table_hosts.item(row, 0).text()))
        edit_server_form = EditServerList(self, ch_host)
        edit_server_form.show()

    def open_copy_files_settings(self):
        copy_settings = FileToCopy(self)
        copy_settings.show()

    def open_path_settings(self):
        path_form = PathForm(self)
        path_form.show()

    def clear_log(self):
        try:
            with open(LOG_PATH, 'w') as log_file:
                log_file.write('')
                self.log_text.clear()
        except Exception as e:
            self.error_except(e)

    def error_except(self, error):
        error = 'Возникла ошибка: {}'.format(error.args)
        log_new_line(error, 'warning')
        QMessageBox.warning(self, 'Ошибка', error)
        self.set_log_info()

    def set_log_info(self):
        with open(LOG_PATH, 'r', encoding='cp1251') as log_file:
            self.log_text.setPlainText(log_file.read())

    def run(self):
        try:
            new_server = get_host_link_by_id(self.get_current_host_id())[0]
            for proc in psutil.process_iter():
                name = proc.name()
                if name == "experium.exe":
                    proc.kill()
                    time.sleep(1)
            # Меняем сервер в ini файле программы
            chanche_server(new_server, get_settings_by_type('ini_path'))
            log_new_line('Выбран сервер: {}'.format(new_server))
            # удаляем папку cash
            cash_dir = get_settings_by_type('cash_path')
            if (os.path.exists(cash_dir)):
                shutil.rmtree(cash_dir)
                log_new_line('Папка "{0}"  удалена'.format(cash_dir))
            else:
                log_new_line('Папка "{0}" была удалена ранее'.format(cash_dir))
            # запуск приложения
            exe_path = get_settings_by_type('exe_path')
            if (exe_path != '' or exe_path != None):
                os.startfile(exe_path)
                log_new_line('Приложение запущено')

            self.set_log_info()

        except AttributeError:
            QMessageBox.warning(self, 'Внимание!', 'Выберите сервер из списка')

        except Exception as e:
            print(e)
            self.error_except(e)

    def run_copy(self):
        all_files_for_copy = get_all_ch_file()
        folder_from = get_settings_by_type('edit_from')
        folder_to = get_settings_by_type('edit_to')

        self.progress = QProgressDialog(self)
        self.progress.setWindowTitle('Копирование')
        self.progress.setWindowModality(Qt.WindowModal)
        self.progress.setMaximum(len(all_files_for_copy))
        self.progress.setVisible(True)

        for proc in psutil.process_iter():
            name = proc.name()
            if name == "Experium.exe" or name == "experium.exe":
                proc.kill()
                time.sleep(1)

        if all_files_for_copy != [] and folder_from != '' and folder_to != '':
            try:
                self.copy_thread.start()
            except IOError as e:
                    QMessageBox.information(self, 'Файл', '{} '.format(e))
            except Exception as e:
                    self.error_except(e)
        else:
            QMessageBox.warning(self, 'Внимание', 'Нет данных!')


    def upd_progress_bar(self, val):
        self.progress.setValue(val)
        self.set_log_info()

    def get_and_set_file_version(self):


        path_cnv = get_settings_by_type('cnv_path')
        path_exe = get_settings_by_type('exe_path')
        try:
            ver_parser = Dispatch('Scripting.FileSystemObject')
            if path_cnv != '' and path_cnv is not None:
                cnv_ver = ver_parser.GetFileVersion(path_cnv)
                self.serv_ver_edit.setText(cnv_ver)

            if path_exe != '' and path_exe is not None:
                exe_ver = ver_parser.GetFileVersion(path_exe)
                self.app_ver_edit.setText(exe_ver)
                

        except Exception as e:
            self.error_except(e)


class CopyProcess(QThread):
    copy_done = pyqtSignal(int)

    def __init__(self, parent=None):
        super(CopyProcess, self).__init__(parent)
    try:
        def run(self):
            all_files_for_copy = get_all_ch_file()
            folder_from = get_settings_by_type('edit_from')
            folder_to = get_settings_by_type('edit_to')
            progress = 1
            for file in all_files_for_copy:
                full_path_from = '{}/{}'.format(folder_from, file)
                full_path_to = '{}/{}'.format(folder_to, file)
                if os.path.exists(full_path_from):
                    shutil.copy(full_path_from, full_path_to)
                    log_new_line('Файл: {} скопирован'.format(file))
                    self.copy_done.emit(progress)
                    progress += 1
                else:
                    log_new_line('Файл: {} не найден'.format(file), 'warning')
                    self.copy_done.emit(progress)
                    progress += 1

    except Exception as e:
        log_new_line('Ошибка: {}'.format(e[0]))

    except FileNotFoundError as e:
        log_new_line('Ошибка: {}'.format(e[0]))


if __name__ == '__main__':
    if not(os.path.exists('w_db.sqlite')):
        create_DB()
        add_host('localhost', '127.0.0.1','')
    app = QApplication(sys.argv)
    QApplication.setStyle(QStyleFactory.create('Fusion'))
    main_form = MainForm()
    main_form.show()
    sys.exit(app.exec_())