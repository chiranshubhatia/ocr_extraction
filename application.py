#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Nov 13 11:06:10 2019

@author: chiranshub
"""

# import os
from flask import Flask,request,redirect,url_for,send_from_directory
from datetime import date
# from flask_csv import send_csv
# from werkzeug.utils import secure_filename
import flask
# from pdf_to_png import pdf_to_png
import hcdf_form_text_extraction
import json
import pandas as pd
import requests
#os.chdir('/home/chiranshub/Downloads/HCDF_form')
#UPLOAD_FOLDER='/home/chiranshub/Downloads/HCDF_form'
app=Flask(__name__)

@app.route('/extract',methods=['POST','GET'])
def extract_text():
    if request.method=='POST':
        data=request.get_json()
        image_data_url=data['image_url']
        messID=data['messageID']
        image_data=requests.get(image_data_url)
        if image_data.status_code==200:
            texual_data=hcdf_form_text_extraction.ocr_extraction()
            text=texual_data.text_extract(image_data)
            text_new=hcdf_form_text_extraction.text_cleaning(text)
            entity_mapping=hcdf_form_text_extraction.entity_extraction()
            print("before extraction",entity_mapping.info)
            entity_mapping.get_entites(text_new)
            print("after extraction",entity_mapping.info)
            url='https://msairesponsereciever20191104013958.azurewebsites.net/api/AIResponse/GetPostedImages'
            send_data={"Response":entity_mapping.info,"MessageId":mess}
            headers = {'Content-Type': 'application/json'}
            x=requests.post(url,data=json.dumps(send_data),headers=headers)
            print("check the status code for response",x.status_code)
            return pd.DataFrame.from_dict(entity_mapping.info,orient='index').to_html()
        else:
            return redirect(url_for('error_page'))
    return '''
<html><head><title>Upload new File</title>
    </head><body><h1>OCR extraction for HDCF form 1500</h1>
     <h2>HIT button for demo run</h2>
  
    <form method="post" enctype="multipart/form-data">
          
         <input type="text" name="RUN">
         <input type="text" name="messageID">
         </p>
         </form></h2><div style="background-color: rgb(255, 143, 0); display: none; color: white; text-align: center; position: fixed; top: 0px; left: 0px; width: 100%; height: auto; min-width: 100%; min-height: auto; max-width: 100%; font: 12px &quot;Helvetica Neue&quot;, Helvetica, Arial, Geneva, sans-serif; cursor: pointer; padding: 5px;"><span style="color: white; font: 12px &quot;Helvetica Neue&quot;, Helvetica, Arial, Geneva, sans-serif;">You have turned off the paragraph player. You can turn it on again from the options page.</span><img src="chrome-extension://gfjopfpjmkcfgjpogepmdjmcnihfpokn/img/icons/icon-close_16.png" style="width: 20px; height: auto; min-width: 20px; min-height: auto; max-width: 20px; float: right; margin-right: 10px;"></div></body></html>
'''
# def extract_text():
#     if request.method=='POST':
#         print(request.files['file'])
#         f=request.files['file']
#         print(f.filename)
#         if('.pdf' in f.filename ):
            
#             f.save(secure_filename(f.filename))
#             png_file=pdf_to_png(f.filename.replace(' ','_'))
                       
#             image_path=png_file.pdf_to_png()
#             image_data=open(image_path[0],"rb").read()
#             texual_data=hcdf_form_text_extraction.ocr_extraction()
#             text=texual_data.text_extract(image_data)
#             text_new=hcdf_form_text_extraction.text_cleaning(text)
#             entity_mapping=hcdf_form_text_extraction.entity_extraction()
#             print("before extraction",entity_mapping.info)
#             entity_mapping.get_entites(text_new)
#             print("after extraction",entity_mapping.info)
#             return pd.DataFrame.from_dict(entity_mapping.info,orient='index').to_html()
#         else:
#             return redirect(url_for('error_page'))
#     return '''
# <html><head><title>Upload new File</title>
#     </head><body><h1>OCR extraction for HDCF form 1500</h1>
#      <h2>Upload the file in pdf format</h2>
       
#     <form method="post" enctype="multipart/form-data">
#       <p><input type="file" name="file">
      
#          <input type="submit" value="Upload">
#          </p>
#          </form></h2><div style="background-color: rgb(255, 143, 0); display: none; color: white; text-align: center; position: fixed; top: 0px; left: 0px; width: 100%; height: auto; min-width: 100%; min-height: auto; max-width: 100%; font: 12px &quot;Helvetica Neue&quot;, Helvetica, Arial, Geneva, sans-serif; cursor: pointer; padding: 5px;"><span style="color: white; font: 12px &quot;Helvetica Neue&quot;, Helvetica, Arial, Geneva, sans-serif;">You have turned off the paragraph player. You can turn it on again from the options page.</span><img src="chrome-extension://gfjopfpjmkcfgjpogepmdjmcnihfpokn/img/icons/icon-close_16.png" style="width: 20px; height: auto; min-width: 20px; min-height: auto; max-width: 20px; float: right; margin-right: 10px;"></div></body></html>
# '''

@app.route('/file_error')        
def error_page():
    return ''' <html><head><title> Invalid Parameters </title></head>
<body>
<h1> Error Occured</h1><br>
</body>
  </html>'''

