""" Database models """

from exts import db
from datetime import datetime

class Account(db.Model):
    __tablename__="accounts"
    uid = db.Column(db.Integer,  primary_key=True)
    line_id = db.Column(db.String(100), nullable=False)
    line_user_id = db.Column(db.String(100), nullable=False)
    username =  db.Column(db.String(100), nullable=False, unique=True)
    email = db.Column(db.String(100), nullable=False, unique=True)
    password =  db.Column(db.Text(), nullable=False)
    
    def __repr__(self):
        return f'<Account {self.uid}>'

    def save(self):
        db.session.add(self)
        db.session.commit()
        
    def delete(self):
        db.session.delete(self)
        db.session.commit()
    
    """    
    def update(self, username, email, password):
        self.username = username
        self.email = email
        self.password = password
        db.session.commit()
    """    

class Exchange(db.Model):
    __tablename__="exchanges"
    id = db.Column(db.Integer,  primary_key=True)
    receiver_uid = db.Column(db.Integer, db.ForeignKey('accounts.uid'), nullable=False)
    provider_uid = db.Column(db.Integer, db.ForeignKey('accounts.uid'))
    receiver = db.relationship("Account", foreign_keys=receiver_uid)
    provider = db.relationship("Account", foreign_keys=provider_uid)
    
    item = db.Column(db.String(50), nullable=False)
    region = db.Column(db.String(100), nullable=False)
    status = db.Column(db.String(50), nullable=False)
    notes =  db.Column(db.String(200))
    date_added = db.Column(db.DateTime(), default=datetime.now)
    
    def __repr__(self):
        return f'<Exchange {self.id} {self.receiver_uid} {self.item}>'

    def save(self):
        db.session.add(self)
        db.session.commit()
        
    def delete(self):
        db.session.delete(self)
        db.session.commit()
        
    def update_status(self, status):
        self.status = status
        db.session.commit()
    
    def update_provider(self , provider_uid):
        self.provider_uid = provider_uid
        db.session.commit()