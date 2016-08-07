import os
import numpy as np
import sys
if os.getcwd() == '/home/keeda/Documents/scientist/demo/recosys/demo/reco':
    serverPath = "/home/keeda/Documents/scientist/demo/recosys/demo/"
    mypath ='/home/keeda/Documents/scientist/demo/recosys/demo/'
else:
    serverPath = "/home/ubuntu/demo/"
    #mypath ='/home/ubuntu/scientist_demoes/media/documents/'

import os
from subprocess import call
import ipdb
import json
import re
import datetime
import pandas as pd
import numpy as np

#ipdb.set_trace()
print('reading ratings file')
ratings = pd.read_csv('ratings_liked.csv',dtype = {'userId': np.int32, 'movieId': np.int32,'liked':np.bool})
movies = pd.read_csv('movies.csv')
print('creating one hot encoding')
ratings_wide = pd.pivot_table(ratings, values='liked', index=['userId'],columns=['movieId'], aggfunc=np.sum)

from rbm import RBM
vi_unit = ratings_wide.shape[1]
rbm = RBM(num_visible = vi_unit, num_hidden = 20)
ratings_wide = ratings_wide.fillna(0)
ratings_wide = ratings_wide.astype(int)
training_data = ratings_wide.as_matrix()

print('starting training')
rbm.train(training_data, max_epochs = 2) # Don't run the training for more than 5000 epochs.

while(True):
    userInput = raw_input('enter "run" to predict: ')
    if userInput=="run":
        
        
        user_liked =[]
        with open(serverPath+'user_liked.json', 'r') as infile:
            user_liked = json.load(infile)
        #ipdb.set_trace()
        user_liked = [ int(i) for i in re.sub(r"\[|]","",user_liked).split(',')]
        user_liked_vec = [int(j) for j in [i in user_liked for i in pd.Series(ratings_wide.columns) ]]
        visible_data = np.array([user_liked_vec])
        hidden = rbm.run_visible(visible_data)
        recom = rbm.run_hidden(hidden)
        recom_idx = [idx for idx,i in enumerate(recom[0]) if i==1]
        recom_movies = pd.Series(ratings_wide.columns)[recom_idx]
        recommendations = recom_movies.tolist()
        if(len(recommendations))>=10:
            recommendations = recommendations[0:10] 
        recommendations_title = movies.loc[[i in recommendations for i in movies['movieId']]][['movieId','title']]
        
        #ipdb.set_trace()
        with open(serverPath+'recommendations.json', 'w') as outfile:
            json.dump(recommendations_title.to_json(), outfile)
