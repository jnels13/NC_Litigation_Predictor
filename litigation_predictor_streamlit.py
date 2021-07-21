import pandas as pd 
import numpy as np 
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.ensemble import StackingClassifier

import pickle 
from urllib.request import urlopen
import streamlit as st 
from PIL import Image 
st.set_option('deprecation.showPyplotGlobalUse', False)

# LOAD MODELS AND LISTS 
clf_link = 'https://github.com/jnels13/NC_Litigation_Predictor/blob/main/Streamlit_files/final_model.data?raw=true'
f1 = urlopen(clf_link)
clf = pickle.load(f1) 

lists_link = 'https://github.com/jnels13/NC_Litigation_Predictor/blob/main/Streamlit_files/strmlit_lists.data?raw=true'
f2 = urlopen(lists_link)
import_lists = pickle.load(f2)

case_type = import_lists[0]
judges = import_lists[1]
counties = import_lists[2]
scaled_probs_affirmed = import_lists[3]
unscaled_probs_affirmed = import_lists[4]

ohe_link = 'https://github.com/jnels13/NC_Litigation_Predictor/blob/main/Streamlit_files/fit_ohe.data?raw=true'
f3 = urlopen(ohe_link)
ohe = pickle.load(f3)

X2_link = 'https://github.com/jnels13/NC_Litigation_Predictor/blob/main/Streamlit_files/sample_df.data?raw=true'
f4 = urlopen(X2_link)
X2 = pickle.load(f4) 

# FUNCTIONS

def scaler(list_, element):
    minx = min(list_)
    maxx = max(list_)
    diff = maxx-minx
    return((element-minx)/diff)

def distribution_plot(list_of_probabilities, sample_probability):
    
    plt.figure(figsize=(8,6))
    sns.set_style("whitegrid")
    lower_limit = int(0.45 * len(list_of_probabilities))
    sns.distplot(list_of_probabilities[lower_limit:], color = 'b', hist=False, kde_kws={'clip': (0.45, 1.0)})
    plt.xticks([])
    avg_prob = round(np.average(list_of_probabilities),4)
    plt.axvline(avg_prob, color = 'r')
    plt.axvline(sample_probability, color = 'g')
    plt.title("Distribution of Probabilities of Summary Judgment Being Affirmed\n", fontsize=18)
    plt.legend(["Average Probability: "+str(avg_prob), "Probability for Selected Case: "+str(sample_probability)], 
               loc='upper left')
    perc_change = round((sample_probability-avg_prob)/avg_prob*100,3)
    plt.show()
    st.pyplot()

def prediction(case_type, judge, county):  
    """
    Takes one row of a three-column dataframe (type, judge, county) 
    and returns a probability relative to the average probability
    that the motion would be affirmed.
    """
    
    X2['Case_Type'][0] = case_type
    X2['Trial_Judge'][0] = judge
    X2['County'][0] = county

    transformed_df = ohe.transform(X2)
    pred = round(clf.predict_proba(transformed_df).tolist()[0][1],4)
    return(pred)

# MAIN FUNCTION DEFINES WEB PAGE

def main(): 
    #st.title("NC Litigation Predictor") 
      
    html_temp = """ 
    <div style ="background-color: #ABBAEA;padding:13px"> 
    <h1 style ="color:black;text-align:center;">North Carolina Litigation Predictor</h1> 
    <p> This app provides a prediction of the <b>relative</b> probability of success of a 
    summary judgment motion, assuming that the legal standard is met. The probabilities are generally
    high (in the 70s) because the majority of summary judgment motions across the board are
    affirmed. Accordingly, the meaningful metric provided by this model indicates your 
    <b>relative</b> likelihood of being affirmed upon selecting the judge, 
    jurisdiction, and case type of your motion vs the average.  
    <p> The probability chart allows you to visualize the distance between the 
    red line (average) and green line (your selections) and provides a "%-greater- or 
    %-less-than-average" metric. You may re-run the model while tweaking the various factors 
    to see which will most affect your probability of success. The model is built upon 
    multiple machine-learning models, and was trained upon 23 years of North Carolina's 
    appellate decisions, going back to 1998.   
    <p>Code may be viewed on github.com/jnels13.
    </div> 
    """
      
    st.markdown(html_temp, unsafe_allow_html = True) 
      


# INPUT DROP-DOWNS:

    judge = st.selectbox('Select the trial judge hearing your motion:',judges)
    county = st.selectbox('Select the county where the case is being heard:',counties)
    casetype = st.selectbox('Select the case type:',case_type)

    st.write('You selected: judge: '+str(judge)+', county: '+str(county)+', and case type: '+str(casetype))
   
    if st.button("Predict"): 
        result = prediction(casetype, judge, county)
        scaled_pred = round(scaler(unscaled_probs_affirmed,result),4)
        distribution_plot(scaled_probs_affirmed, scaled_pred) #unscaled_probs_affirmed, result)
        avg_success = np.average(scaled_probs_affirmed)
        difference = round(((scaled_pred - avg_success)/avg_success)*100,2)
        if difference > 0: 
            greater = 'greater' 
        else: 
            greater = 'worse'
        st.success("""Given the trial judge, county, and case type selected, your probability 
        of being affirmed (indicated by the green line), assuming the legal standard is met, 
        is {}% {} than the average. \n\n The blue curve above represents the 
        distribution of the probabilities of success; the red line is the average probability 
        of a successful motion being affirmed (presuming the legal standard is met).""".format(abs(difference), greater))


if __name__=='__main__': 
    main() 