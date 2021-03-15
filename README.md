<img align="center" src="https://github.com/jnels13/NC_Litigation_Predictor/blob/main/images/NC_Litigation_Banner.JPG" width="auto" height="auto">

The NC_Litigation_Predictor is a probabilistic classifier; it provides a relative probability of success of a motion for summary judgment when considering the features of a given lawsuit. The model applies machine learning, built upon 23 years of North Carolina's appellate decisions, and provides a prediction grounded in data, based upon the user's judge, jurisdiction, and case type, to supplement the legal-threshold criteria, so that stakeholders can make an informed cost-benefit analysis on litigation strategy. The final model may be run <a href="https://share.streamlit.io/jnels13/nc_litigation_predictor/main/litigation_predictor_streamlit.py">HERE.</a>

This README follows the following format: 
<ul>
    <li> Repo Contents
    <li> Background
    <li> Process + Modeling
    <li> Results
</ul>

### Repo Contents
<ul>
    <li> README.md: Background, Process (and abstract), and Outcome
    <li> Notebooks:
    <ul>
        <li> NC_COA_Scraper.ipynb: Jupyter notebook which indexes and downloads the initial set of appellate opinions (NC COA, 1998-2020)
        <li> DF_Creation.ipynb: Jupyter notebook which the opinions are converted from PDFs to a functional dataframe with minimal preprocessing
        <li> Label and Feature Creation.ipynb: notebook where labels and features are extracted from the appellate opinions
        <li> Litigation_Predictor.ipynb: Jupyter notebook containing the project model and results
    </ul>
    <li> Data:
    <ul>
        <li> SampleData: Folder containing sample data used throughout the project
        <li> Streamlit_files: Data files for Streamlit deployment
        <li> ProjectData: Folder containing the project data (PDFs) and initial dataframes, NOT tracked in Git  
    </ul>
    <li> Images (folder): Visualizations and example images
    <li> litigation_predictor_streamlit.py: Streamlit deployment files
    <li> requirements.txt: dependencies file required for Streamlit
</ul>

## Background

#### The Common Law and Appellate Court's Opinions

Laws are composed of statutes/regulations (prepared by legislative and executive branches) and the common law. The common law is composed of written opinions (or rulings) of courts, typically courts of appeals, which review trial courts' application of the law to a given lawsuit (either "affirming" or "reversing" the trial court). These written opinions, if comparable in the underlying facts, are binding upon future cases within that state. 

#### Appellate Courts Affirm or Reverse Trial Courts' Rulings on Motions for Summary Judgement

This project will provide predictive value on a single component of a lawsuit: a motion for summary judgment. In civil (non-criminal) cases, a motion for summary judgment (or "MSJ") may be successful if, when the facts are assumed true in the other side's favor, the side bringing the motion would still be entitled to judgment as a matter of law. For instance, in a contract formation case, if the facts under the opponent's best world simply don't amount to the legal standard for formation of a contract, an MSJ may be granted. 

MSJs are significant because if a court granted an MSJ, that would typically end a case. This usually results in an appeal (asking a higher court to confirm whether the lower court made the right decision). Every litigant is entitled to a first-level appeal in North Carolina. Accordingly, the body of North Carolina appellate opinions will address many cases where MSJs have been allowed, providing some insight into the features common to those cases where the decisions on these motions have either been affirmed or reversed.

#### A Predictor for a Given Set of Features Will Assist Stakeholders 

Like most components of legal representation, MSJs can be expensive, costing from a few thousand dollars in a lower-value case, to many multiples of this as the stakes go up. While attorneys' and law firms' judgment on meeting the legal standard is crucial and fact-dependent, their collective experience with a given judge or on a given issue can also be valuable; however, an objective prediction based upon thousands of cases will valuably assist stakeholders in performing an informed and accurate cost-benefit analysis. 

## Process (OSEMN)

#### Abstract

This project was created to assist in the cost-benefit analysis of an MSJ, to supplement anecdote with regard to the judge hearing the motion. To provide this insight, I first gathered the data by scraping all available appellate opinions (23 years' worth) and converting them into a Pandas DataFrame. After dropping cases that do not reference MSJs, I cleaned things like page numbers and PDF tags, and removed opinions that would confuse the model (i.e., dissents and 'substantial right' decisions). Finally, I extracted labels and features using primarily regular expressions functions. To extract the case type, I prepared a function using keywords for each case type.  All functions were varified extensively by hand. 

For the modeling, I first considered balancing the data, which was approximately 3:1 between the affirmed and reversed cases, and ultimately ran the models on both sets of data. I experimented across several different models, including logistic regression, random forest, and XG Boost. I had also implemented a simple neural network, with varying degrees of success. Ultimately, I implemented a stacking classifier incorporating all of these models, though the neural network was ultimatley dropped when the stacking classifier worked better without it. The final f-1 score was 0.86 with an accuracy of 0.76. I then deployed the final model to Streamlit, which may be accessed <a href="https://share.streamlit.io/jnels13/nc_litigation_predictor/main/litigation_predictor_streamlit.py">HERE.</a>  Future work includes creating a pipeline for future opinions (the model is current through the end of 2021).  

### __Obtain__: Understanding | Gathering Information | Sourcing Data

#### Understanding Presumptions/Considerations

This model returns a relative probability of success in the trial court, inferred from appellate opinions (North Carolina does not provide access to trial court rulings, which actually lack any insightful details anyway). This inference may be affected by such factors as the typical deference shown by courts of appeals; so, it should be clear that the model provides a __relative__ probability (as compared to the probability of an average judge/county/etc). Moreover, it presumes that __every__ granted MSJ is appealed (which is likely an overestimation), and that the legal bases for summary judgment (as set forth in N.C.G.S. s. 1A-1, Rule 56) are met, or are at least arguable.  

#### Sourcing the Data

```Notebook: NC_COA_Scraper.ipynb```: Initial data sourcing started with locating and obtaining the opnions. Opinions are stored in individual PDF files on the North Carolina Court of Appeals' web site. Beautiful Soup was used to generate a list of web addresses of the individual PDFs using Beautiful Soup. Then, using Requests and the help of some proxy servers, I scraped each of the 28,931 PDFs. 

```Notebook: DF_Creation.ipynb```: using the PDFMiner library, I combined each of the appellate opinions into a single-column DataFrame. I wrote a function to convert the PDFs into strings; this took nearly 4.5 hours to convert nearly all of the scraped PDFs.  An error list was created from those PDFs which did not process correctly, and to avoid unnecessary effort, I reviewed those error-list PDFs to see if they contained the phrase, "summary judgment"; only ten did, so these were concatenated to the master DataFrame individually. 

#### Scrubbing the Data

With the initial DataFrame formed, I performed some further preprocessing before it was ready for label and feature extraction.  Overall, the dataframe was very clean, though some obvious cleaning was needed. First, I filtered it down to only those opinions including the term "summary judgment," as to not include any opinions irrelevant to the model (only a relative few cases discuss summary judgment motions).  Then, I removed the PDF tags and made the entire DataFrame lowercase.  Other than the tags, the data was extremely clean.  Finally, I removed the duplicate rows, resulting in 3,922 potentially relevant texts, which were now ready for label and feature extraction, though further scrubbing was performed along the way.

```Notebook: Feature and Label Creation.ipynb```: The ultimate goal of this step was to extract labels ("affirmed" or "reversed"), as well as enough relevant and distinct features that would be helpful to as many new cases as possible.  Through this process, it became clear that further "clean-up" of the dataset was needed, including removing page numbers, cropping dissents from the end of some opinions, reviewing supreme court cases, and fixing potential issues like Irish names (i.e., "O'Connor" reading as two different words).  

Issues created by page numbers and Irish names are self-explanatory.  Dissents had to be removed because they would confuse the model. A dissent is when one of the three appellate judges doesn't agree with the other two; they are then free to write their reasoning in dissenting from the majority, which is then appended to the end of the opinion.  It may be considered by the Supreme Court if the case reviewed again.  For purposes of the model, however, they confuse the issues and inhibit the ability to accurately extract labels and features.  Accordingly, they were cropped off using a regex filter.  Similarly, the North Carolina Supreme Court may (or may not) elect to review an appellate court decision and then write its own opinion.  The questions are slightly different, and the fact that they're reviewing a review would confuse the models. They're also exceedingly rare.  Accordingly, the Supreme Court decisions were dropped. 

**Label Extraction:** After creating some initial features (including the year filed), just as a test run, I started to extract the labels.  To accomplish this, I created a function consisting of a series of nested try/except regex patterns, in decreasing order of reliability.  The function returned a series of labels, not all of which were helpful.  For instance, if the court dismissed an appeal, this was neither an "affirmed" or "denied." Opinions which were not easily categorized into "affirmed" or "denied" were dropped, leaving 2,817 opinions (this constituted the single largest filter of the initial batch of "summary judgment" opinions which were dropped. 

**Feature Extraction:** Features were extracted in roughly the same way.  I wrote functions to extract two more feature sets (trial judge and county) using regex.  Once again, the patterns were organized in decreasing levels of reliability, such that easily extracted features were obtained through the first or second "try" statement.  After running each function, I went back over several iterations to either tweak the initial regex pattern or add another layer in the nested try/except statements to address things like judge's suffixes (i.e, joe nelson, iii or jr) to those using a first initial.  

These nested try/except statements seemed perfectly functional and efficient (requiring fewer and fewer of the test cases not meeting the earlier "try" patterns to filter to the later patters).  I took some solace in one Stack Exchange reference to this style of code as a "common Python coding style," "clean and fast," as defined in the EAFP section of the Python glossary.  

To extract the case-type feature, I took a slightly different route, using a dictionary of case types with their associated, unique keywords.  For instance, "marriage" or "alimony" would be keywords for "family law," while "intestate" and "probate" would be keywords for "estate law."  Words like "will" were not used, even if strongly associated with estate law, since it would likely appear in different contexts.  Next, I wrote a function that counted the occurrences of keywords and scored them for case_type, returning the most likely case type.  The function also produces a confidence score; the potential for using embeddings to categorize future cases is exciting, though it would require labeled data, which this dictionary and confidence score provides.  

This function and accompanying dictionary was improved over many, many iterations, including the addition of an "other" case type, to avoid the function defaulting to the first-in-line.  To be sure, there may be some case types that are more condensed, and the dictionary can always be expanded and adjusted, but the ultimate result was pretty solid. 

Another problem arose during the feature extraction, which I hinted at above: There were some cases where summary judgment is denied that are allowed to be appealed.  The legal jargon for this is when denial of the motion affects a "substantial right."  In such cases, "reversed" and "affirmed" would mean the opposite of a traditional case (where "affirmed" equated to summary judgment being granted in the trial court, it would now mean summary judgment had been denied).  I wrote a function to filter these "substantial right" cases out, initially with the intent of "flipping" their labels. However, they were not many and the issues within these cases were convoluted, such that the process was better served by simply dropping those rows. 

### __Explore__: Reviewing the Dataset 

With a clean, labeled dataset, I was now able to perform some EDA.  The features were reassuring; for instance, when reviewing the proportion of affirmed to reversed cases over time, there was no obvious time-related pattern. The following chart illustrates that the proportion of decisions affirming/reversing summary judgment does **not** overtly follow any time-trends:

<img src="https://github.com/jnels13/NC_Litigation_Predictor/blob/main/images/motions_by_year.jpg">

When looking at chances of being affirmed by case type, there appeared to be some clear differences between the relative degrees of probablity of being affirmed, as shown below:

<img align="center" src="https://github.com/jnels13/NC_Litigation_Predictor/blob/main/images/motions_by_case_type.jpg">

Similarly, the trial judges also have varying degrees of likelihood of being affirmed or reversed. The following illustrates the top fifteen judges (based upon the number of their cases involving summary judgment motions), ranked by their percentage of cases being affirmed.  (_This is a retrospective review; Judge Spainhour -- who granted one of my summary judgment motions -- passed away in 2020, and Judge Eagles was appointed as a federal district court judge in 2010, while this model only involves state-court cases._)  

<img align="center" src="https://github.com/jnels13/NC_Litigation_Predictor/blob/main/images/top_ten_judges.jpg?raw=true">

### __Model__: Creating and Revising Predictive Models 

```Notebook: Litigation_Predictor.ipynb``` was used for the remaining work in this project. 

#### One-hot encoding and class balancing

I started the modeling process first by one hot encoding the categorical variables (which was all of the variables).  This resulted in a matrix of 2665 rows and 605 columns.  Class imbalance presented some issue, with the affirmed cases representing 74.4% of the corpus.  To account for this, I ran the models both on the unbalanced data set and on a balanced set using Smote-NC, a class-balancing algorithm better suited to categorical data than the original Smote algorithm. Ultimately, the models performed better using the unbalanced data, and the imbalance was not too significant; accordingly, the numbers below represent the runs on imbalanced data.

#### Modeling 

Then, I used scikit-learn's dummy classifier to produce a baseline, which returned an accuracy of 0.49 and an F1 score of 0.59 for the affirmed class (designated class 1 in the model) on the unbalanced data. I attempted to run several different models, including logistic regression, a simple neural network, random-forest classifier and the XG Boost classifier. each using a grid search or randomized search to tune the hyperparameters.  Each of these performed okay, as indicated below:

<img align="center" src="https://github.com/jnels13/NC_Litigation_Predictor/blob/main/images/acc_f1_scores.png">

I then combined these into a stacking classifier, using logistic regression as the final estimator.  The neural network became difficult as I experimented between the balanced and unbalanced data.  When using the balanced data, I moved from three to four layers, each of the first three followed by a dropout layer, and the loss curves followed each other nicely:

<img align="center" src="https://github.com/jnels13/NC_Litigation_Predictor/blob/main/images/nn_loss.jpg">

However, when returning to the unbalanced data, despite many attempts at tuning the model, the loss curves would diverge significantly after only a few epochs.  I eventually tried running the stacking classifier without the neural network, and results improved from when it was included, with a final accuracy of 0.76 and an f-1 score of 0.86. 

### __iNterpret__: What Does the Model Show? 

In the <a href="https://share.streamlit.io/jnels13/nc_litigation_predictor/main/litigation_predictor_streamlit.py">final Streamlit app</a>, when a judge, county, and case-type are selected, the model will provide and plot the relative likelihood of a summary judgment motion being affirmed , as illustrated below:  
<p  align="center" >
<img src="https://github.com/jnels13/NC_Litigation_Predictor/blob/main/images/Streamlit_Selection.jpg?raw=true" width=400>
<img src="https://github.com/jnels13/NC_Litigation_Predictor/blob/main/images/Streamlit_Predict.jpg?raw=true" width=400>
</p>
The probability of all cases to be affirmed is rather high -- generally in the 70%'s -- which can be misleading. Accordingly, I stress the intent of the model as demonstrating where a given case lies __in relation to__ the mean likelihood of being affirmed.

### Upcoming Work

Upcoming work is as follows: <ul>
    <li> Create pipeline to retrain model as new opinions come out (currently current through end of 2020).
</ul>
