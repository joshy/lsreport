import logging

from flask import render_template, jsonify, request, send_from_directory

from lsreport.app import app, VERSION
from lsreport.read_npz import read_json, image_request
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


@app.route('/nifti_viewer')
def nifti_viewer():
    """ Renders medical image view for nifti. """
    return render_template('nifti_viewer.html')


@app.route('/image_data')
def image_data():
    """ Returns the image to the client. """
    acc_number = request.args.get('acc_number', '')
    if not acc_number:
        return jsonify('Error: no accession number given, \
                       use request param "acc_number"')

    image_type = request.args.get('image_type', '')
    if not image_type:
        return jsonify('Error: no image type given, use request param \
                       "image_type". Values are "ct", "pet" or "label"')

    image_path = image_request(acc_number, image_type)
    return send_from_directory(image_path[0], image_path[1],
                               attachment_filename=image_path[1],
                               as_attachment=True,
                               mimetype='application/nifti')
