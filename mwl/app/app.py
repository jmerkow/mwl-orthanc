import json

import pandas as pd
import requests
from flask import Flask, render_template, Markup
from flask_table import Table, Col

app = Flask(__name__)


# Declare your table
class RISTable(Table):
    classes = ["table", 'table-striped', "table-sm", 'display']

    sortable=True

    @property
    def table_id(self):
        if self.sortable:
            return 'tab-sort'
        else:
            return 'table-normal'

    # table_id = "example"
    StudyDateTime = Col('Exam Date', column_html_attrs={'class': 'text-center'})
    PatientMainDicomTagsPatientName = Col('Patient Name', column_html_attrs={'class': 'text-center'})
    Study = Col('Study', column_html_attrs={'class': 'text-center'})
    MainDicomTagsAccessionNumber = Col('Accession', column_html_attrs={'class': 'text-center'})
    PatientMainDicomTagsPatientSex = Col('Patient Sex', column_html_attrs={'class': 'text-center'})
    MainDicomTagsInstitutionName = Col('Facility', column_html_attrs={'class': 'text-center'})
    PatientMainDicomTagsPatientBirthDate = Col('Patient DOB', column_html_attrs={'class': 'text-center'})
    Comments = Col('DeepCTHead', column_html_attrs={'class': 'text-center'})


def curl(url):
    resp = requests.get(url)
    result = json.loads(resp.text)
    return result


def get_results(uid, analysis='CT-HEAD_ICH_v20.03', base="172.21.142.16"):
    resp = requests.get('http://{base}/api/v1/outcomes/{analysis}/{uid}/'.format(base=base, analysis=analysis, uid=uid))
    return json.loads(resp.text)


# def get_result(uid):
#     res = get_results(uid)
#
#     output = {
#         'FLAG': "<span class='text-danger font-weight-bold'>Suspected ICH</span>",
#         'OK': "<span class='text-success font-weight-bold'>No Suspected ICH</span>",
#         'PENDING': "<span class='text-info font-weight-bold'>Not Available: Pending</span>",
#         'FAILURE': "<span class='text-secondary font-weight-bold'>Not Available: Failure</span>",
#         'ERROR': "<span class='text-secondary font-weight-bold'>Not Available: Error</span>",
#         'UNKNOWN': "<span class='text-secondary font-weight-bold'>Not Available: Unknown</span>",
#
#     }
#     return Markup(output[res['outcome']])

def get_result(uid):
    res = get_results(uid)

    output = {
        'FLAG': "<span class='text-danger font-weight-bold'>Suspected ICH</span>",
        'OK': "",
        'PENDING': "<span class='text-info font-weight-bold'>Pending</span>",
        'FAILURE': "<span class='text-secondary font-weight-bold'>Not Available</span>",
        'ERROR': "<span class='text-secondary font-weight-bold'>Not Available</span>",
        'UNKNOWN': "<span class='text-secondary font-weight-bold'>Not Available</span>",

    }
    return Markup(output[res['outcome']])


@app.route('/')
def hello_world():
    studies = curl("http://orthanc:8042/studies")
    studies = [curl("http://orthanc:8042/studies/" + id) for id in studies]
    studies = pd.io.json.json_normalize(studies, sep='')

    studies['Comments'] = studies['MainDicomTagsStudyInstanceUID'].apply(get_result)
    studies.fillna('', inplace=True)

    studies = studies.set_index('MainDicomTagsStudyInstanceUID')
    studies['Study'] = 'CT HEAD'
    studies['StudyDateTime'] = pd.to_datetime(
        studies['MainDicomTagsStudyDate'] + ' ' + studies['MainDicomTagsStudyTime'])
    studies['PatientMainDicomTagsPatientBirthDate'] = studies['PatientMainDicomTagsPatientBirthDate'].apply(
        pd.to_datetime).apply(
        lambda t: t.date)

    uids = sorted(studies.index.tolist())

    x = [studies.loc[u].to_dict() for u in uids]

    table = RISTable(x)

    return render_template('index.html', table=table)
    # return table.__html__()


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
