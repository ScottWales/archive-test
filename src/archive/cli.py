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
import archive.mdss as mdss
from archive.model import Dataset, File
import sqlalchemy

def init(dataset, project, session=None):
    session.add(Dataset(name=dataset, project=project))

def dataset_from_name(name, session):
    try:
        return session.query(Dataset).filter_by(name=name).one()
    except sqlalchemy.orm.exc.NoResultFound as e:
        raise LookupError("Dataset '%s' not found") from e

def put(filenames, dataset, session=None):
    dataset = dataset_from_name(dataset, session)
    
    files = [File.from_filename(f, dataset=dataset) for f in filenames]
    session.add_all(files)

    mdss.put(filenames, 'archive/%s'%dataset.name, project=dataset.project)

def get(filenames, dataset, session=None):
    dataset = dataset_from_name(dataset, session)

    mdss.get(['archive/%s/%s'%(dataset.name, f) for f in filenames], '.',
            project=dataset.project)
