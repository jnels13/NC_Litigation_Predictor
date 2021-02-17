# NC_Litigation_Predictor

The NC_Litigation_Predictor is a probabilistic classifier; it provides a probability of sucess of a motion for summary judgment when considering the features of a given lawsuit. The model applies machine learning, built upon all of North Carolina's appelate decisions, and provides a prediction grounded in data, not just intuition, so that stakeholders can make an informed cost-benefit analysis on litigation strategy.

### Index

This README follows the following format: 
<ul>
    <li> Repo Contents
    <li> Background
    <li> Process
    <li> Results
</ul>

### Repo Contents
<ul>
    <li> README.md: Project description, processes, and outcome
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
        <li> ProjectData: Folder containing the project data (PDFs) and initial dataframes, NOT tracked in Git  
    </ul>
</ul>

### Background

#### The Common Law and Appellate Court's Opinions

Laws are composed of statutes/regulations (prepared by legislative and executive brances) and the common law. The common law are written opinions (or rulings) of courts, typically courts of appeals, which review trial courts' application of the law in a given case (either "affirming" or "reversing" the trial court). These written opinions, if comparable in the underlying facts, are binding upon future cases. For instance, if an appellate decision holds that a certain law applies only to persons driving pale magenta Buicks, then that's the law for pale magenta Buicks (but maybe not light blue Buicks).  One state's court's rulings are typically only applicable within that state, and these state courts are distinct from federal courts (but that's a whole separate discussion). Because an appellate opinion is binding upon future cases, given similarity in the underlying facts, we can look at the facts of our case and compare them to previous written opinions to obtain some predictive value from them. 

#### Appellate Courts Affirm or Reverse Trial Courts' Rulings on Motions for Summary Judgement

This project will provide some predictive value, focusing on a single component: a motion for summary judgment. In civil (non-criminal) cases, a motion for summary judgment (or "MSJ") may be brought if both sides essentially agree on the material facts and the movant is entitled to judgment as a matter of law. For instance, in a contract case, if the facts under the opponent's best world simply don't amount to the legal standard for formation of a contract, MSJ may be granted. 

MSJs are significant because a granted MSJ would typically end a case, usually resulting in an appeal (every litigant is entitled to a first-level appeal in NC). Accordingly, the body of North Carolina appellate opinions will address many cases where MSJs have been allowed, providing some insight into the features common to those cases where motions have been affirmed or reversed.

#### A Predictor for a Given Set of Features Will Assist Stakeholders 

Like most components of legal representation, MSJs can be expensive, from a few thousand dollars in a lower-value case, to many multiples of this as the stakes go up. While attorneys' and law firms' collective experience with a given judge or on a given issue can be valuable, a objective number will assist stakeholders perform a cost-benefit analysis. For instance, some insurance companies ask attorneys to provide such a prediction to complete a decision-tree-type analysis, though this prediction is usually based only upon anecdotal reports. Lawyers can advise on whether a case will meet a legal standard, but this model provides an objective probability-of-success probablity based upon the non-legal factors, including the trial judge hearing the motion, the county, the case-type and others, based upon the corpus of North Carolina's appellate decisions from 1998 to the present. 

### Process

#### Creating the Data Set

Opinions are stored in individual PDF files at the North Carolina Court of Appeals' web site. Beautiful Soup was used to generate a list of web addresses, which were then gathered via requests. PDFs were then imported, converted to strings using the PDFMiner library, combined into an initial Pandas DataFrame, and then reduced to only those opinions containing the phrase "summary judgment". The dataset was further reduced to avoid further complicating factors.  Labels were extracted using regular expressions with decreasing levels of confidence. 

I then created feature sets, including the trial judge, case type, and county. Some of these were simple, while others required more detailed extractions, such as the case-type extraction. This function was built using a keyword dictionary, with the most prominent case-type match resulting. The features were reassuring; for instance, the following chart illustrates that the proportion of decisions affirming/reversing summary judgment does **not** follow any apparent time-trends (suggesting the historical performance does not need to be adjusted):

<img src="https://github.com/jnels13/NC_Litigation_Predictor/blob/main/images/motions_by_year.png">

On other hand, the case-type predictor does show different relative degrees of probablity of being affirmed, as shown below:

<img src="https://github.com/jnels13/NC_Litigation_Predictor/blob/main/images/motions_by_case_type.png">

Similarly, the trial judges also have varying degrees of likelihood of being affirmed or reversed. The following illustrates the top ten judges (based upon the number of their cases involving summary judgment motions), ranked by their percentage of cases being affirmed.  (_This is a retrospective review; Judge Spainhour -- who granted one of my summary judgment motions -- passed away in 2020, and Judge Eagles was appointed as a federal district court judge in 2010, while this model only involves state-court cases. The model will be updated with new judges as new opinions come in._)  

<img src="https://github.com/jnels13/NC_Litigation_Predictor/blob/main/images/top_ten_judge.png">

### Results

- Probability distribution and illustration
- Multiple models to compare range of distributions
