import logging

from flask import render_template

from lsreport.app import app, VERSION
from lsreport.read_npz import read_json
from lsreport.read_nifti import read_nifti


@app.route('/')
def main():
    """ Renders the initial page. """
    niftis = read_nifti()
    npz_jsons = read_json()

    return render_template('index.html',
                           title='LungStage Report',
                           niftis=niftis,
                           npz_jsons=npz_jsons,
                           version=VERSION
                          )


@app.route('/viewer')
def viewer():
    """ Renders medical image view. """
    return render_template('viewer.html')

