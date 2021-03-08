import pandas as pd 
import numpy as np 
from sklearn.ensemble import StackingClassifier

import pickle 
import streamlit as st 
from PIL import Image 
  
# ===================================================================================================
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

# ===================================================================================================
# TO DO - REPLACE THIS FUNCTION WITH A NEW ON
# def welcome(): 
#     return 'welcome all'
  
# defining the function which will make the prediction using  
# the data which the user inputs 

def scaler(list_, element):
    minx = min(list_)
    maxx = max(list_)
    diff = maxx-minx
    return((element-minx)/diff)

def distribution_plot(list_of_probabilities, sample_probability):
    
    plt.figure(figsize=(10,8))
    sns.distplot(list_of_probabilities, color = 'b')
    avg_prob = round(np.average(list_of_probabilities),4)
    plt.axvline(avg_prob, color = 'r')
    plt.axvline(sample_probability, color = 'g')
    plt.title("Distribution of Probabilities of Summary Judgment Being Affirmed\n", fontsize=18)
    plt.legend(["Average Probability: "+str(avg_prob), "Sample Prediction of Test Row x: "+str(sample_probability)], 
               loc='upper left')
    perc_change = round((sample_proba-avg_prob)/avg_prob*100,3)
    plt.show()

def prediction(df=X2, case_type, judge, county, probs=unscaled_probs_affirmed, scaled_probs=scaled_probs_affirmed):  
    """
    Takes one row of a three-column dataframe (type, judge, county) 
    and returns a probability relative to the average probability
    that the motion would be affirmed.
    """
    df['Case_Type'][0] = case_type
    df['Trial_Judge'][0] = judge
    df['County'][0] = county

    transformed_df = ohe.transform(df)
    pred = round(clf.predict_proba(transformed_df).tolist()[0][1],4)
    scaled_pred = round(scaler(probs,pred),4)

    distribution_plot(probs, pred)

    avg_success = np.average(scaled_probs_affirmed)
    difference = round(((scaled_pred-avg_success)/avg_success)*100,2)
    print("Given the trial judge, county, and case type, your motion has a "+str(difference)+"% greater/worse chance of being affirmed.")

    return ()


# ===================================================================================================
# MAIN FN DEFINES WEB PAGE

def main(): 
    # giving the webpage a title 
    # st.title("NC Litigation Predictor") 
      
    # here we define some of the front end elements of the web page like  
    # the font and background color, the padding and the text to be displayed 
    html_temp = """ 
    <div style ="background-color: #ABBAEA;padding:13px"> 
    <h1 style ="color:black;text-align:center;">North Carolina Litigation Predictor</h1> 
    <p> This app provides a prediction of the relative probability of success , 
    github.com/jnels13. 
    <p> The input essay should be typed or pasted into the text box below.

    </div> 
    """
      
    # this line allows us to display the front end aspects we have  
    # defined in the above code 
    st.markdown(html_temp, unsafe_allow_html = True) 
      
    # the following lines create text boxes in which the user can enter  
    # the data required to make the prediction 
    # text = st.text_input("STUDENT'S TEXT:", "Type or Paste Here") <<<<<<<<<<<<<<<<<<,OLD, DELETE
# ===================================================================================================
# REPEAT BELOW LINES FOR EACH OF THE THREE INPUTS, 
    judge = st.selectbox(
                        'Select the trial judge hearing your motion:', <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
...     ('Email', 'Home phone', 'Mobile phone'))
>>>
>>> st.write('You selected:', option) 

    result ="" 
      
    # the below line ensures that when the button called 'Predict' is clicked,  
    # the prediction function defined above is called to make the prediction  
    # and store it in the variable result 
    if st.button("Predict"): 
        try:
            result = prediction(text) 
        except:
            st.error('Your text was too short or did not otherwise work; please try again.')
    try:
        st.success('The predicted grade level is:  \nGrades {} using tf-idf weighting, and  \nGrades {} using Word2vec vectoring'.format(result[0], result[1])) 
    except:
        pass

if __name__=='__main__': 
    main() 