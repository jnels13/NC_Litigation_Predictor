# NC_Litigation_Predictor

The NC_Litigation_Predictor provides a probability of sucess of a motion for summary judgment when considering the features of a given lawsuit. The model applies machine learning built upon all of North Carolina's appelate decisions and provides a prediction grounded in data, not just intuition, so that stakeholders can make an informed cost-benefit analysis on litigation strategy.

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
        <li> Litigation_Predictor.ipynb: Jupyter notebook containing the project 
    </ul>
    <li> Data:
    <ul>
        <li> SampleData: Folder containing sample data used throughout the project
        <li> pp_msj_df.data: Dataframe of NC Appellate Opinions containing the phrase "summary judgment"     
    </ul>
    <li> Materials NOT Tracked in Git/Github:
    <ul>
        <li> Scraped_PDFs: Collection of scraped PDF opinions from NC COA 1998-2020 
        <li> Initial DataFrames: Versions of the scraped opinions in a DataFrame format at various levels of processing
    </ul>
</ul>

### Background

#### The Common Law and Appellate Court's Opinions

Laws are composed of statutes/regulations (prepared by legislative and executive brances) and the common law. The common law are written opinions (or rulings) of courts, typically courts of appeals, which review trial courts' application of the law in a given case (either "affirming" or "reversing" the trial court). These written opinions, if comparable in the underlying facts, are binding upon future cases. For instance, if an appellate decision holds that a certain law applies only to persons driving pale magenta Buicks, then that's the law.  One state's court's rulings are typically only applicable within that state, and these state courts are distinct from federal courts (but that's a whole separate discussion). Because an appellate opinion is binding upon future cases, given similarity in the underlying facts, we can look at the facts of our case and compare them to previous written opinions to obtain some predictive value from them. 

#### Appellate Courts Affirm or Reverse Trial Courts' Rulings on Motions for Summary Judgement

This project will provide some predictive value, focusing on a single component: a motion for summary judgment. In civil (non-criminal) cases, a motion for summary judgment (or "MSJ") may be brought if both sides essentially agree on the material facts, and the movant is entitled to judgment as a matter of law. For instance, in a contract case, if the facts under the opponent's best world simply don't amount to the formation of a contract, MSJ may be granted. 

MSJs are significant because a granted MSJ would typically end a case (though not always), usually resulting in an appeal (every litigant is entitled to a first-level appeal). Accordingly, the body of North Carolina appellate opinions will address many cases where MSJ's have been allowed, providing some insight into the features common to those cases where motions have been affirmed or reversed.

#### A Predictor for a Given Set of Features Will Assist Stakeholders 

Like most components of legal representation, MSJs can be expensive, from a few thousand dollars in a lower-value case, to hundreds of thousands of dollars as the stakes go up. While attorneys and law firms' collective experience with a given judge or on a given issue can be valuable, a objective number will assist stakeholders perform a cost-benefit analysis. For instance, some insurance companies ask attorneys to provide such a prediction to complete a decision-tree-type analysis, though this prediction is usually based only upon anecdotal reports.  This model provides an objective probability-of-success based upon the corpus of North Carolina's appellate decisions from 1998 to the present. 

### Process

#### Creating the Data Set

Opinions are stored in individual PDF files at the North Carolina Court of Appeals' web site. Beautiful Soup was used to generate a list of web addresses, which were then gathered via requests. PDFs were then imported, converted to strings using the PDFMiner library, combined into an initial Pandas DataFrame, and then reduced to only those opinions containing the phrase "summary judgment".  

THEN:
- Create labels 
- Create feature list (appellate judge, trial judge, case type, party type individ/corp,

VISUALIZE BREAKDOWN OF CASES


### Results
