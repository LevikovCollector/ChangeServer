from DB.conf import  TblFilesForCopy, db_session
from sqlalchemy.orm.exc import UnmappedInstanceError



def add_file (file_name, file_status=0):
    n_file = TblFilesForCopy(files_nam=file_name, status_copy = file_status)
    db_session.add(n_file)
    db_session.commit()


def get_all_files_with_id():
    return db_session.query(TblFilesForCopy.id, TblFilesForCopy.files_nam, TblFilesForCopy.status_copy).all()


def get_all_ch_file():
    raw_data = db_session.query(TblFilesForCopy.files_nam).filter(TblFilesForCopy.status_copy==True).all()
    data = []
    for file in raw_data:
        data.append(file[0])
    return data


def del_file(file_id):
    try:
        file_for_del = db_session.query(TblFilesForCopy).get(file_id)
        db_session.delete(file_for_del)
        db_session.commit()
    except UnmappedInstanceError:
        print('Объект удален ранее')


def upd_status(file_id, new_status):
    up_file = db_session.query(TblFilesForCopy).get(file_id)
    up_file.status_copy = new_status
    db_session.commit()


if __name__ == '__main__':
    #upd_status(2, 1)
    print(get_all_ch_file())