# -*- coding: utf-8 -*-
"""
Author : Chiranshu Bhatia"""



import cv2
from wand.image import Image
from PIL import Image as PI
import io
import re
class pdf_to_png:
    def __init__(self,filename):
        print("pdf_to_png is defined")
        self.filename=filename
    def pdf_to_png(self):
        save_filename=[]
        count=1
        r=re.search('\.pdf',self.filename)
        img_filename=self.filename.replace(r.group(),'')
        print(self.filename)
        with Image(filename=self.filename, resolution=200) as img:
            img.compression_quality = 99
            png_filename=img_filename+str(count)+'.png'
            img.save(filename=png_filename)
            print("file conversion success",png_filename)
            save_filename.append(png_filename)
            count+=1
        return save_filename
if __name__=="__main__":
    filename="HCFA 1500 form.pdf"
    obj=pdf_to_png(filename)
    print(obj.pdf_to_png())
else:
    print("this file is being imported")
    