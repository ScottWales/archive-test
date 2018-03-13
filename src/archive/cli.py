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
import archive.db as db
from archive.model import Dataset, File
import sqlalchemy
import click
import os
import argparse

def cli():
    parser = argparse.ArgumentParser()
    parser.add_argument('--database',
            default='sqlite:///%s/archive-test.db'%os.environ['HOME'],
            help='Database URL')
    subparser = parser.add_subparsers(help='Commands')

    init_args = subparser.add_parser('init',
            help='Create a new dataset')
    init_args.add_argument('--dataset',
            required=True,
            help='Dataset ID')
    init_args.add_argument('--project', '-P',
            default=os.environ.get('PROJECT',None),
            help='NCI Project')
    init_args.set_defaults(command=init)

    put_args = subparser.add_parser('put',
            help='Store files')
    put_args.add_argument('--dataset',
            required=True,
            help='Dataset ID')
    put_args.add_argument('filenames',
            nargs='+',
            metavar='file',
            help='File to store')
    put_args.set_defaults(command=put)

    get_args = subparser.add_parser('get',
            help='Retrieve files')
    get_args.add_argument('--dataset',
            required=True,
            help='Dataset ID')
    get_args.add_argument('filenames',
            nargs='+',
            metavar='file',
            help='File to retrieve')
    get_args.set_defaults(command=get)

    list_args = subparser.add_parser('list',
            aliases=['ls'],
            help='List files')
    list_args.set_defaults(command=list_files)

    # Parse the args into a dict
    args = vars(parser.parse_args())

    db.connect(args.pop('database'), init=True)
    session = db.Session()

    args.pop('command')(**args, session=session)


def init(session, dataset, project):
    session.add(Dataset(name=dataset, project=project))
    session.commit()

def dataset_from_name(name, session):
    try:
        return session.query(Dataset).filter_by(name=name).one()
    except sqlalchemy.orm.exc.NoResultFound as e:
        raise LookupError("Dataset '%s' not found") from e

def put(filenames, dataset, session=None):
    dataset = dataset_from_name(dataset, session)
    
    files = [File.from_filename(f, dataset=dataset) for f in filenames]
    session.add_all(files)

    for f in files:
        mdss.put([f.name], 'saw562/archive/object/%s/%s'%(f.sha256[0:2], f.sha256[2:]),
                project=dataset.project)
    session.commit()

def get(filenames, dataset, session=None):
    dataset = dataset_from_name(dataset, session)

    mdss.get(['saw562/archive/%s/%s'%(dataset.name, f) for f in filenames], '.',
            project=dataset.project)
    session.commit()

def list_files(session=None):
    q = session.query(Dataset, File).join(Dataset.files).order_by(Dataset.id)

    current_id = -1
    for d, f in q:
        if d.id != current_id:
            current_id = d.id
            print(d.name)

        print("\t%s\t%s"%(f.name,f.sha256))
