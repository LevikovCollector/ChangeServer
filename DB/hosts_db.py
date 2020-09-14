from DB.conf import TblHosts, db_session
from sqlalchemy.orm.exc import UnmappedInstanceError


def add_host(name, host, comment):
    n_host = TblHosts(name, host, comment)
    db_session.add(n_host)
    db_session.commit()


def get_all_hosts_name_and_comment_with_id():
    act_data = db_session.query(TblHosts.id, TblHosts.name, TblHosts.host_comment).all()
    return act_data


def get_all_info_by_id(host_id):
   return db_session.query(TblHosts.id, TblHosts.name, TblHosts.host_name,  TblHosts.host_comment).filter(TblHosts.id == host_id).first()


def get_host_link_by_id(host_id):
    return db_session.query(TblHosts.host_name).filter(TblHosts.id == host_id).first()


def upd_host(host_id, name, host, comment):
    up_host = db_session.query(TblHosts).get(host_id)
    up_host.name = name
    up_host.host_name = host
    up_host.host_comment = comment
    db_session.commit()


def delete_host(host_id):
    try:
        host_for_del = db_session.query(TblHosts).get(host_id)
        db_session.delete(host_for_del)
        db_session.commit()
    except UnmappedInstanceError:
        print('Объект удален ранее')

if __name__ == '__main__':
    # add_host('name1','adr1', 'comment1')
    # add_host('name12', 'adr12', 'comment12')
    # add_host('name13', 'adr13', 'comment13')
    # add_host('name14', 'adr14', 'comment14')
    #upd_host(1,'name11', 'ya.ru', 'comment')
    print(get_all_info_by_id(4))
