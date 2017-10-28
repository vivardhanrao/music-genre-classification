# music-genre-classification
A machine learning project that tries to predict the genre of a given music track using Ensemble Learning technique.

# Abstract
Music tracks can be classified into different categories based on how they “sound”. A music genre is a generic category that classifies music tracks as belonging to a common tradition or set of conventions. Music can be divided into different genres in many different ways. The artistic nature of music means that these classifications are often subjective and controversial, and some genres may overlap. A music track’s sound is based on various properties, qualities or features of that track; how a music track sounds is based on these properties. Humans have been the primary tool in attributing genre-tags to songs. Automating this classification process using a machine is a more intricate task. As machine learning excels at deciphering patterns from complex data, we aimed to train a machine learning classifier, with these properties as features and corresponding genres as labels. This classifier can then be used to predict the genres of other music tracks based on those songs’ properties. Our dataset consists of two hundred totals songs, evenly distributed across rap, reggae, classical, and country genres. The summary feature data of each of the songs are taken from Spotify. We hypothesized that by using techniques like feature engineering (feature selection) and ensemble learning, the efficiency and the accuracy of the classifier can be improved. We were able to increase the efficiency of the model by 3-4% by using aforementioned techniques.

# Purpose
Genre tagging is generally a manual work which can be tedious. By using a machine to tag genres to music tracks, the speed and efficiency can be increased. 

# Hypotheses
> Feature engineering is used to improve the richness and the quality of the data by selecting and assigning proper weights to each of the features that is used to train the machine learning model, which in turn is used for predictions. We hypothesized that by implementing Feature Engineering - by selecting important features will improve the data.

> X-fold Cross Validation can be used to increase the efficiency of the testing.

> By using Ensemble Learning and assigning weights to the classifiers/estimators based on intuition and trial-and-error (based on the accuracy of the model developed using these data)  the accuracy of the model can be improved.

# Data Collection
Spotify Web API lets developers’ applications fetch data from the Spotify music catalogue and manage their playlists and saved music. We used "Get Audio Features for Several Tracks" API endpoint to get audio features about music tracks. The API returns various audio features of the tracks as follows:

> Danceability

> Energy

> Key

> Loudness

> Mode

> Speechiness

> Acousticness

> Instrumentalness

> Liveness

> Valence

> Tempo

> Time

> Signature

# Data Pre-processing / Feature Engineering
Here we look to optimize the data features. Firstly we normalized data using Min-Max normalization to fit all the feature data between 0 - 1 range. 

# Classification
After selecting the features for training the machine learning classifier, we looked at selecting the classification models or algorithms. For this we used the sklearn library in Python. We used 5 algorithms as follows:

> Logistic Regression

> Support Vector Machine

> Decision Tree

> Random Forest

> Gaussian Naïve Bayes

We then used the Ensemble Learning technique – majority voting for classification.

# Results

a) Classification using general machine learning classifiers:

> Logistic Regression:	  0.85 (+/- 0.05)

> Random Forest:	        0.87 (+/- 0.04)

> Gaussian Naïve Bayes:	  0.84 (+/- 0.03)

> Support Vector Machine:	0.89 (+/- 0.04)

> Decision Tree:	        0.82 (+/- 0.06)

b) Classification using Ensemble Classifier:

> Voting Classifier without weights:	0.92 (+/- 0.05)

> Voting Classifier with weights:     0.93 (+/- 0.04)

