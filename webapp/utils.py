import gdown
import joblib
import os
import numpy as np

def load_model(id, debug = False):
    '''
        Download from Gdrive and load the scikit-learn model  
    '''
    model = None 
    try:
        if debug and os.path.exists('./models/random_forest.joblib'): return joblib.load('./models/random_forest.joblib')

        output = './models/'
        filepath = gdown.download(id=id, output=output)        
        
        model = joblib.load(filepath)
    except:
        print("Error downloading and loading scikit model.")        
    return model

def encode_ownership(person_home_ownership):
    if person_home_ownership == 'RENT':
        return [1.0, 0.0, 0.0, 0.0]
    elif person_home_ownership == 'MORTGAGE':
        return [0.0, 1.0, 0.0, 0.0]
    elif person_home_ownership == 'OWN':
        return [0.0, 0.0, 1.0, 0.0]
    elif person_home_ownership == 'OTHER':
        return [0.0, 0.0, 0.0, 1.0]
    else:
        raise ValueError
    
def parse_request(json):
    '''
        Parse the json request into the correct input for the model
    '''
    try:
        loan_grade = float(json['loan_grade'])
        loan_percent_income = float(json['loan_percent_income'])
        person_income = int(json['person_income'])
        person_home_ownership = json['person_home_ownership']
        person_home_ownership = encode_ownership(person_home_ownership)    
        loan_amnt = int(json['loan_amnt'])
        cb_person_default_on_file = int(json['cb_person_default_on_file'])
    except:
        print("Error parsing request")
        return None

    return np.array([loan_grade,
                     loan_percent_income,
                     person_income,
                     person_home_ownership[0],
                     person_home_ownership[1],
                     person_home_ownership[2],
                     person_home_ownership[3],
                     loan_amnt,
                     cb_person_default_on_file])