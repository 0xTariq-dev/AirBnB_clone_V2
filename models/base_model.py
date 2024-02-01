#!/usr/bin/python3
"""This module defines a base class for all models in our hbnb clone"""
import uuid
import models
from datetime import datetime
from sqlalchemy import Integer, String, Column, DateTime, MetaData
from sqlalchemy.ext.declarative import declarative_base
from os import getenv


if getenv('HBNB_TYPE_STORAGE') == 'db':
    Base = declarative_base()
else:
    Base = object


class BaseModel:
    """A base class for all hbnb models"""
    if getenv('HBNB_TYPE_STORAGE') == 'db':
        id = Column(String(60), primary_key=True, nullable=False)
        created_at = Column(DateTime, default=datetime.utcnow(), nullable=False)
        updated_at = Column(DateTime, default=datetime.utcnow(), nullable=False)

    def __init__(self, *args, **kwargs):
        """Instatntiates a new model"""
        if not kwargs:
            self.id = str(uuid.uuid4())
            self.created_at, self.updated_at = datetime.now(), datetime.now()
        else:
            for k, v in kwargs.items():
                if k == 'created_at' or k == 'updated_at':
                    setattr(self, k, datetime.strptime(v,
                                                       '%Y-%m-%dT%H:%M:%S.%f'))
                elif k != '__class__'and k != "_sa_instance_state":
                    setattr(self, k, v)
            if 'id' not in kwargs:
                self.id = str(uuid.uuid4())
            if 'created_at' not in kwargs:
                self.created_at = datetime.now()
            if 'updated_at' not in kwargs:
                self.updated_at = datetime.now()
            self.__dict__.update(kwargs)

    def __str__(self):
        """Returns a string representation of the instance"""
        cls = (str(type(self)).split('.')[-1]).split('\'')[0]
        dict_repr = self.__dict__.copy()  # create a copy of the dictionary
        if '_sa_instance_state' in dict_repr:
            dict_repr.pop('_sa_instance_state')  # remove _sa_instance_state from the dictionary
        dict_repr_str = str(dict_repr)  # convert the dictionary to a string
        dict_repr_str = dict_repr_str.replace('["', '[', 1).replace('"]', ']', 1)  # remove the double quotation between the first two square brackets
        return '[{}] ({}) {}'.format(cls, self.id, dict_repr_str)

    def save(self):
        """Updates updated_at with current time when instance is changed"""
        from models import storage
        self.updated_at = datetime.now()
        storage.new(self)
        storage.save()

    def to_dict(self):
        """Convert instance into dict format"""
        dict = {}
        dict.update(self.__dict__) 
        dict.update(
            {'__class__': (
                str(type(self)).split('.')[-1]
                ).split('\'')[0]})
        if isinstance(self.created_at, datetime):
            dict['created_at'] = self.created_at.isoformat()
        else:
            dict['created_at'] = self.created_at
        if isinstance(self.updated_at, datetime):
            dict['updated_at'] = self.updated_at.isoformat()
        else:
            dict['updated_at'] = self.updated_at
        if '_sa_instance_state' in dict.keys():
            dict.pop('_sa_instance_state')
        return dict

    def delete(self):
        """Delete the current instance from the storage"""
        from models import storage
        storage.delete(self)
