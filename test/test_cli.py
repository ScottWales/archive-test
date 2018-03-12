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
from archive.cli import *
import archive
import pytest
import unittest.mock as mock

@pytest.fixture
def mock_mdss():
    """
    Mock out MDSS commands
    """
    with mock.patch('archive.cli.mdss.put') as mdss_put:
        with mock.patch('archive.cli.mdss.get') as mdss_get:
            yield {'put': mdss_put, 'get': mdss_get}

@pytest.fixture
def mock_file():
    """
    Dummy file constructor that doesn't touch the filesystem
    """
    with mock.patch('archive.cli.File.from_filename') as mock_file:
        def from_filename(filename, dataset):
            return archive.model.File(dataset=dataset, size=500000,
                    sha256='abcdef123456')
        mock_file.side_effect = from_filename
        yield mock_file

def test_cli(session, mock_mdss, mock_file):
    """
    Make sure the general workflow works
    """
    init(dataset='sample_dataset', project='a12', session=session)
    put(['sample_file'], dataset='sample_dataset', session=session)
    get(['sample_file'], dataset='sample_dataset', session=session)

@pytest.fixture
def dataset(session, mock_mdss, mock_file):
    """
    Test dataset to modify
    """
    init(dataset='sample_dataset', project='a12', session=session)
    put(['sample_file'], dataset='sample_dataset', session=session)

def test_put(dataset, session):
    """
    'put'ing a file should create it on MDSS
    """
    with mock.patch('archive.cli.mdss.put') as mdss_put:
        put(['sample_file'], dataset='sample_dataset', session=session)
        mdss_put.assert_called_once_with(
                ['sample_file'],
                'archive/sample_dataset',
                project='a12')

def test_get(dataset, session):
    """
    'get'ing a file should retrieve it from MDSS
    """
    with mock.patch('archive.cli.mdss.get') as mdss_get:
        get(['sample_file'], dataset='sample_dataset', session=session)
        mdss_get.assert_called_once_with(
                ['archive/sample_dataset/sample_file'],
                '.',
                project='a12')

def test_put_wrong_dataset(dataset, session):
    with pytest.raises(LookupError):
        put(['sample_file'], dataset='wrong_dataset', session=session)

def test_get_wrong_dataset(dataset, session):
    with pytest.raises(LookupError):
        get(['sample_file'], dataset='wrong_dataset', session=session)

