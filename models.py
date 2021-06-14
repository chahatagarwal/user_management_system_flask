from init import db, app
import datetime
from sqlalchemy import Column, ForeignKey
from sqlalchemy.sql import func

class User(db.Model):
    """ User Model for storing user related details """
    __tablename__ = "User"
    #id autoincrement
    user_phone = db.Column(db.Integer,primary_key=True, nullable=False)
    user_fname = db.Column(db.String(255), nullable=False)
    user_lname = db.Column(db.String(255), nullable=False)
    user_email = db.Column(db.String(255),unique=True,nullable=False)
    user_password = db.Column(db.String(255), nullable=False)
    #Role type: Admin->1 & Agent->0 
    user_role = db.Column(db.Boolean,default=0,nullable=False)
    #is_deleted: Is account deactivated or not -> 1(Yes) & 0(No) 
    is_deleted = db.Column(db.Boolean,default=0,nullable=False)
    #is_activated: Is the account activated by admin? 1(Yes) & 0(No) 
    is_activated = db.Column(db.Boolean,default=0,nullable=False)
    
    def as_dict(self):
       return {c.name: getattr(self, c.name) for c in self.__table__.columns}

#Data model to store logs/action done by admin
class Log(db.Model):
    """Logs to store the actionable points"""
    __tablename__ = "Log"
    log_id = db.Column(db.Integer,primary_key=True, nullable=False,autoincrement=True)
    log_user_phone = db.Column(db.Integer,ForeignKey('User.user_phone'), nullable=False)
    #IP address of the admin taken an action
    log_ip_address = db.Column(db.String(255), nullable=False)
    log_attribute = db.Column(db.String(255), nullable=False)
    log_old_value = db.Column(db.String(255), nullable=False)
    log_new_value = db.Column(db.String(255), nullable=False)
    #date & time when the admin made an action
    log_datetime = db.Column(db.DateTime(timezone=True), default=func.now(), nullable=False)

    def as_dict(self):
       return {c.name: getattr(self, c.name) for c in self.__table__.columns}