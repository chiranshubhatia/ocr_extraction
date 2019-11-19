import os
from flask import Flask,request,redirect,url_for,send_from_directory
from datetime import date
import flask
import hcdf_form_text_extraction
import json
import pandas as pd
import requests
app=Flask(__name__)

@app.route('/')
def extract_text():
  print(" hello world")
  return "welcome to the page"
app.run()
