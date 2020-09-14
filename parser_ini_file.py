from configobj import ConfigObj, ConfigObjError
from log_work import log_new_line


def chanche_server(server, programm_ini):
    try:
        pr_ini = ConfigObj(infile = programm_ini, encoding = 'utf-8', write_empty_values = True)
        pr_ini['Main']['Server'] = server
        pr_ini.write()
    except ConfigObjError:
        log_new_line('Ошибка при изменении сервера', 'warning')

if __name__ == '__main__':
    pass