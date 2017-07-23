# https://stackoverflow.com/questions/37345215/retrieve-text-from-textarea-in-flask

import os
import json
import myWit
import myLUIS
import myAPI
from flask import Flask, request

htmlHeader = 'Eric Gregori OMSCS Advisor NLU Testing - egregori3@gatech.edu<br>Ask me about OMSCS admissions or curriculum<br>'

formStart = '<form action="submit" id="textform" method="post">'
formTextArea = '<textarea name="text" cols="40"></textarea>'
formInput = '<input type="submit" value="Submit">'
formEnd = '</form>'

htmlWitRespStart = 'Wit.ai response<br><textarea cols="40" rows="10">'
htmlWitRespEnd   = '</textarea>'

htmlLUISRespStart = 'LUIS response<br><textarea cols="40" rows="10">'
htmlLUISRespEnd   = '</textarea>'

htmlAPIRespStart = 'API.ai response<br><textarea cols="40" rows="10">'
htmlAPIRespEnd   = '</textarea>'

myForm = htmlHeader+formStart+formTextArea+formInput+formEnd

app = Flask(__name__)
@app.route('/')
def main_page():
    return myForm

@app.route('/submit', methods=['POST'])
def submit_post():
    my_dir = os.path.dirname(__file__)
    my_file_path = os.path.join(my_dir, 'OMSCSLexJson1.json')
    with open(my_file_path) as json_data:
        OMSCSDict = json.load(json_data)

    WitClient = myWit.myWit( OMSCSDict )
    LUISClient = myLUIS.myLUIS( OMSCSDict )
    APIClient = myAPI.myAPI( OMSCSDict )
    WITresp = WitClient.GetIntent(request.form["text"])
    LUISresp = LUISClient.GetIntent(request.form["text"])
    APIresp = APIClient.GetIntent(request.form["text"])
    retResponse = myForm + '<table style="width:100%"><tr>'
    retResponse += ('<td>' + htmlWitRespStart + WITresp + htmlWitRespEnd + '</td>')
    retResponse += ('<td>' + htmlLUISRespStart + LUISresp +  htmlLUISRespEnd + '</td>')
    retResponse += ('<td>' + htmlAPIRespStart + APIresp +  htmlAPIRespEnd + '</td>')
    retResponse += '</tr></table>'
    return retResponse

if __name__ == '__main__':
    app.run()