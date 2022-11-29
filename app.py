import pandas as pd
import random
from flask import Flask
from flask import jsonify


def predict_code_for_text(text,dataframe=model):
    x = random.uniform(0,1)
    for i,r in dataframe.iterrows():
        if i==0:
            continue
        if r.proportion>=x and dataframe.loc[i-1].proportion<=x:
            return r.code


def save_patient_record(patient_id, text, df):
    new_record_df = pd.DataFrame(zip([patient_id], [text]), columns = ['patient_id', 'text'])
    df = pd.concat([df, new_record_df])
    df.to_csv('patients.csv', index=False)


def is_patient_exist(patient_id, text):
    is_exist = None
    df = pd.read_csv('patients.csv')
    if df[df['patient_id'] == patient_id].shape[0] > 0:
        is_exist = True
    else:
        is_exist = False
    save_patient_record(patient_id, text, df)
    return is_exist


app = Flask(__name__)
@app.route('/get_inference/<string:patient_id>/<string:text>/', methods=['GET', 'POST'])
def get_inference(patient_id, text):
    icd_codes = predict_code_for_text(text)
    is_new_patient = not is_patient_exist(patient_id, text)
    return jsonify(patient_id, text, icd_codes, is_new_patient)


if __name__ == '__main__':
    df = pd.read_excel('MIMIC III per sentence annotated dataset.xlsx')
    model = pd.DataFrame(df.code.value_counts(normalize=True).sort_values().cumsum()).reset_index().rename(columns={'index':'code','code':'proportion'})
    app.run(host='0.0.0.0', port=105)
