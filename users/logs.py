from users.modules import db, Log, session

#logging function and storing in Log table
def logging(phone_no, remote_address, attribute, old_value, new_value):
    log = Log(log_user_phone=phone_no, log_ip_address=remote_address, log_attribute=attribute, log_old_value=old_value, log_new_value=new_value)
    db.session.add(log)
    db.session.commit()