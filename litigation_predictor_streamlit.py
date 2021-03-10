import pandas as pd 
import numpy as np 
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.ensemble import StackingClassifier

import pickle 
import streamlit as st 
from PIL import Image 
st.set_option('deprecation.showPyplotGlobalUse', False)

# LOAD MODELS AND LISTS 

pickle_in = open('ProjectData/final_model.data', 'rb') 
clf = pickle.load(pickle_in) 

pickle_in2 = open('ProjectData/strmlit_lists.data', 'rb') 
import_lists = pickle.load(pickle_in2)

case_type = import_lists[0]
judges = import_lists[1]
counties = import_lists[2]
scaled_probs_affirmed = import_lists[3]
unscaled_probs_affirmed = import_lists[4]

pickle_in3 = open('ProjectData/fit_ohe.data', 'rb')
ohe = pickle.load(pickle_in3)

pickle_in4 = open('ProjectData/sample_df.data', 'rb')
X2 = pickle.load(pickle_in4) 

# FUNCTIONS

def scaler(list_, element):
    minx = min(list_)
    maxx = max(list_)
    diff = maxx-minx
    return((element-minx)/diff)

def distribution_plot(list_of_probabilities, sample_probability):
    
    plt.figure(figsize=(8,6))
    sns.set_style("whitegrid")
    sns.distplot(list_of_probabilities, color = 'b', hist=False)
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
    # giving the webpage a title 
    # st.title("NC Litigation Predictor") 
      
    # here we define some of the front end elements of the web page like  
    # the font and background color, the padding and the text to be displayed 
    html_temp = """ 
    <div style ="background-color: #ABBAEA;padding:13px"> 
    <h1 style ="color:black;text-align:center;">North Carolina Litigation Predictor</h1> 
    <p> This app provides a prediction of the relative probability of success TESTETESTEST, 
    github.com/jnels13. 
    <p> The input essay should be typed or pasted into the text box below.
    </div> 
    """
      
    # this line allows us to display the front end aspects we have  
    # defined in the above code 
    st.markdown(html_temp, unsafe_allow_html = True) 
      


# INPUT DROP-DOWNS:

    judge = st.selectbox('Select the trial judge hearing your motion:',judges)
    county = st.selectbox('Select the county where the case is being heard:',counties)
    casetype = st.selectbox('Select the case type:',case_type)

    st.write('You selected: judge: '+str(judge)+', county: '+str(county)+', and case type: '+str(casetype))

 #   result ="" 
      
    # the below line ensures that when the button called 'Predict' is clicked,  
    # the prediction function defined above is called to make the prediction  
    # and store it in the variable result 
    if st.button("Predict"): 
        result = prediction(casetype, judge, county)
        scaled_pred = round(scaler(unscaled_probs_affirmed,result),4)
        distribution_plot(unscaled_probs_affirmed, result)
        avg_success = np.average(scaled_probs_affirmed)
        difference = round(((scaled_pred - avg_success)/avg_success)*100,2)
        st.success("Given the trial judge, county, and case type, your motion has a "+str(difference)+"% greater/worse chance of being affirmed than the average.")


if __name__=='__main__': 
    main() 