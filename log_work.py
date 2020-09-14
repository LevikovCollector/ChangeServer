import logging


def log_new_line(p_str, m_type='info'):
    if m_type == 'info':
        logging.info('{}\n {}'.format(p_str, '---'))
    elif m_type == 'warning':
        logging.warning('{}\n {}'.format(p_str, '---'))
