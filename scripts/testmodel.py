import pandas as pd
import numpy as np
from fastai.text.all import *
import json
import re
import glob
import pickle
from google.cloud import vision
from google.cloud import storage
from scipy import stats
       
def load_model():
    learn = load_learner('../Riskcovry-Hackathon-Bytes-/export.pkl')
    return learn

def pred(texts,learn):
    l=[]
    for text in texts:
        o=learn.predict(text)
        l.append(o[0])
    print(l)
    #print(stats.mode(l)[0][0])

def pushPDFtoCloud():
    codepath=glob.glob(r"myapp/static/upload/*")
    #print(codepath)
    code=codepath[0]
    client = storage.Client.from_service_account_json(json_credentials_path='riskcovry-315907-9d16d7e7c5e2.json')
    # Creating bucket object
    bucket = client.get_bucket('riscovry_documents')
    # Name of the object to be stored in the bucket
    object_name_in_gcs_bucket = bucket.blob('input_upload.pdf')
    # Name of the object in local file system
    object_name_in_gcs_bucket.upload_from_filename(code)

def async_detect_document(gcs_source_uri="gs://riscovry_documents/input_upload.pdf", gcs_destination_uri="gs://riscovry_documents/#"):
    """OCR with PDF/TIFF as source files on GCS"""
    import json
    import re
    from google.cloud import vision
    from google.cloud import storage

    # Supported mime_types are: 'application/pdf' and 'image/tiff'
    mime_type = 'application/pdf'

    # How many pages should be grouped into each json output file.
    batch_size = 2

    client = vision.ImageAnnotatorClient()

    feature = vision.Feature(
        type_=vision.Feature.Type.DOCUMENT_TEXT_DETECTION)

    gcs_source = vision.GcsSource(uri=gcs_source_uri)
    input_config = vision.InputConfig(
        gcs_source=gcs_source, mime_type=mime_type)

    gcs_destination = vision.GcsDestination(uri=gcs_destination_uri)
    output_config = vision.OutputConfig(
        gcs_destination=gcs_destination, batch_size=batch_size)

    async_request = vision.AsyncAnnotateFileRequest(
        features=[feature], input_config=input_config,
        output_config=output_config)

    operation = client.async_batch_annotate_files(
        requests=[async_request])

    #print('Waiting for the operation to finish.')
    operation.result(timeout=420)

    # Once the request has completed and the output has been
    # written to GCS, we can list all the output files.
    storage_client = storage.Client()

    match = re.match(r'gs://([^/]+)/(.+)', gcs_destination_uri)
    bucket_name = match.group(1)
    prefix = match.group(2)
    #print(type(gcs_destination))
    bucket = storage_client.get_bucket(bucket_name)

    blob_list = list(bucket.list_blobs(prefix=prefix))
    #print(blob_list)
    # Process the first output file from GCS.
    # Since we specified batch_size=2, the first response contains
    # the first two pages of the input file.
    o=[]
    for j in range(len(blob_list)):
        s=[]
        output = blob_list[j]
        output.download_to_filename('inputnew.json')
        f=open('inputnew.json',)
        df=json.load(f)
        #print(df['responses'])
        for i in df['responses']:
            if "fullTextAnnotation" in i:
                s.append(i['fullTextAnnotation']['text'])
        s="\n".join(s)
        o.append(s)
        blob_list[j].delete()
    return o


def main():
    pushPDFtoCloud()
    learn=load_model()
    o=async_detect_document()
    pred(o,learn)
    
if __name__=='__main__':
    main()

        
        