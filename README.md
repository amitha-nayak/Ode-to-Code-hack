# Riskcovry-Hackathon

![forthebadge energy-drink](https://forthebadge.com/images/badges/check-it-out.svg)
![forthebadge energy-drink](https://forthebadge.com/images/badges/powered-by-black-magic.svg)

## PROBLEM STATEMENT CHOSEN:
    Valid Discharge Summary Prediction(Problem 2)

<hr>
    
**Working website on public gcp url: http://34.70.84.140:8000/**

<hr>
    
## TECHSTACK
    Django, HTML, CSS, JavaScript, Pytorch+FastAI, Google Cloud Platform (VM, Cloud Storage)
    
## BASIC OVERVIEW
- Extraction of batched text from multipage PDF using Google's Vision API
- Implementing transfer learning on AWD-LSTM Text classification model
- Display results on an embedded Django Server running on a Google VM

## DETAILS
- Trained on a handpicked minimal dataset with edges cases like health records and medical research papers. All stored on GCP bucket.
- ~89% accuracy attained on AWD-LSTM model after 3 epochs with a training set of ~50 PDF files

## CODE OVERVIEW
- TextExtraction.ipynb: handpicked PDF dataset on Cloud Storage -> Vision API -> JSON on Cloud Storage
- Model.ipynb: JSON on Cloud Storage -> Training of AWD-LSTM -> exporting model 
- scripts/testmodel.py: runs the fine-tuned model on django frontend
- bytes: django files 

## HAVE A LOOK
<img src="/images/website-look.PNG" alt="front-end">

## TEAM BYTES
* Jigya Shah
* Amitha Nayak
