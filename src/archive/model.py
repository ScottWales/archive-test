#!/usr/bin/env python
"""
Copyright 2018 Scott Wales

author: Scott Wales <scottwales@outlook.com.au>

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""
from __future__ import print_function
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship
import hashlib
import os

Base = declarative_base()

class Dataset(Base):
    __tablename__ = 'dataset'

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True)
    project = Column(String)

    files = relationship('File', back_populates='dataset')

class File(Base):
    __tablename__ = 'file'

    id = Column(Integer, primary_key=True)
    dataset_id = Column(Integer, ForeignKey('dataset.id'))
    sha256 = Column(String)
    size = Column(Integer)

    dataset = relationship('Dataset', back_populates='files')

    @staticmethod
    def from_filename(filename, dataset):
        f = File()
        f.size = os.path.getsize(filename)
        f.dataset = dataset

        checksum = hashlib.sha256()
        with open(filename, 'rb') as f:
            for chunk in iter(lambda: f.read(4096), b""):
                checksum.update(chunk)
        f.sha256 = checksum.hexdigest()
        return f
