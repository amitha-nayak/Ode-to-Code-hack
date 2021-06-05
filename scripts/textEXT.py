from google.cloud import storage
import pandas as pd
import numpy as np
class textEXTR:

    def async_detect_document(self,gcs_source_uri, gcs_destination_uri):
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
        return o
        
    def main(self):
        storage_client = storage.Client()
        bucket = storage_client.get_bucket("riscovry_documents")
        blobs_specific = list(bucket.list_blobs(prefix='Valid'))
        #print(blobs_specific)
        j=0
        df = pd.DataFrame(columns=['text','valid'])
        for i in range(1,len(blobs_specific)):
            print(blobs_specific[i].name)
            text=self.async_detect_document('gs://riscovry_documents/'+blobs_specific[i].name,'gs://riscovry_documents/'+str(j))
            valid=0
            for i in text:
                df = df.append({'text':i,'valid':valid},ignore_index=True)
            j+=1
        blobs_specific = list(bucket.list_blobs(prefix='Invalid'))
        for i in range(1,len(blobs_specific)):
            print(blobs_specific[i].name)
            text=self.async_detect_document('gs://riscovry_documents/'+blobs_specific[i].name,'gs://riscovry_documents/'+str(j))
            valid=1
            for i in text:
                df = df.append({'text':i,'valid':valid},ignore_index=True)
            j+=1
        return df
