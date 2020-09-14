from DB.conf import TblSettings, db_session
from DB.program_exception import CreateDataExc


def add_new_settings(path, settings_type):
        if get_settings_by_type(settings_type) == '':
            n_settings = TblSettings(path, settings_type)
            db_session.add(n_settings)
            db_session.commit()
        else:
            raise CreateDataExc('This type path was create before: {}'.format(settings_type))


def get_settings_by_type(settings_type):
    try:
        setting_path = (db_session.query(TblSettings.path_to).filter(TblSettings.type_path == settings_type).all())[0][0]
        return setting_path
    except IndexError:
        return ''


def upd_settings_by_type(new_path, settings_type):
    old_setting_path = db_session.query(TblSettings).filter(TblSettings.type_path == settings_type).first()
    old_setting_path.path_to = new_path
    db_session.commit()

if __name__ == '__main__':
    print(add_new_settings('22222','type2'))
    pass