import joblib
import pandas as pd
import os
from flask import current_app


countVectorizer_path = r"count-vectorizer.pkl"
emotion_nv_model_path = r"emotion_classifier_nv_model.sav"
emotion_lr_model_path = r"emotion_classifier_lr_model.sav"



def load_NV_Model(emotion_nv_model):
    nv_path = os.path.join(current_app.config['MODEL_FOLDER'], emotion_nv_model)
    # load nv model Naive Baynes
    nv_model = joblib.load(nv_path)
    return nv_model


def load_LR_Model(emotion_lr_model):
    lr_path = os.path.join(current_app.config['MODEL_FOLDER'], emotion_lr_model)
    # load lr model Logical Regression
    lr_model = joblib.load(lr_path)
    return lr_model

def load_Vectorizer(countVectorizer):
    lr_path = os.path.join(current_app.config['MODEL_FOLDER'], countVectorizer)
    # loading pickled vectorizer
    vectorizer = joblib.load(lr_path)
    return vectorizer


def predict_emotion(sample_text, model, vectorizer):
    myvect = vectorizer.transform(sample_text).toarray()
    # Make Prediction
    prediction = model.predict(myvect)
    # find the highest probability
    pred_proba = model.predict_proba(myvect)
    pred_percentage_for_all = dict(zip(model.classes_, pred_proba[0]))

    res = {
        "Emotion": prediction[0],
        "Proba": pred_percentage_for_all[prediction[0]],
        "Distribute": pred_percentage_for_all
    }
    return res

def compare_model(nv_res, lr_res):
    if (nv_res["Proba"] > lr_res["Proba"]):
        # nv model rank higher prediction
        res = {
            "HighProba":{
                "Emotion": nv_res["Emotion"],
                "Proba": nv_res["Proba"],
                "Distribute": nv_res["Distribute"]
            },
            "lowProba":{
                "Emotion": lr_res["Emotion"],
                "Proba": lr_res["Proba"],
                "Distribute": lr_res["Distribute"]
            }
        }
        return res
    else:
        # lr model rank higher prediction
        res = {
            "HighProba":{
                "Emotion": lr_res["Emotion"],
                "Proba": lr_res["Proba"],
                "Distribute": lr_res["Distribute"]
            },
            "lowProba":{
                "Emotion": nv_res["Emotion"],
                "Proba": nv_res["Proba"],
                "Distribute": nv_res["Distribute"]
            }
        }
        return res

def get_emotion_predict_res(sample_text):
    # load the model
    nv_model = load_NV_Model(emotion_nv_model_path)
    lr_model = load_LR_Model(emotion_lr_model_path)
    vectorizer = load_Vectorizer(countVectorizer_path)

    # get the predict result
    nv_res = predict_emotion(sample_text, nv_model, vectorizer)
    lr_res = predict_emotion(sample_text, lr_model, vectorizer)

    # compare the predict result
    res = compare_model(nv_res, lr_res)
    return res



""" all = get_emotion_predict_res(sample_text)
print("########################")
print("Higher Prediction: ")
print(all["HighProba"])
print("------------------------")
print("Lower Prediction: ")
print(all["lowProba"]) """