'''
Improving your statistical inferences analysis script

This study uses a single python script to scrape data
from the Internet Movie Database, wrangle using pandas dataframes, hypothesis testing and effect size calculation using statsmodels.

The following dependancies are required:

imdbpy - A python tool to access the imdb api
numpy
pandas
statsmodels 

All data used for this study were downloaded from:

http://www.imdb.com

Peter Goodin, Nov 2016
'''

from imdb import IMDb
import pandas as pd
import numpy as np
from statsmodels import api as sm

#Extract data

def imdb_scrape():
    fran_id = ['st','sw']

    a = IMDb()

    st = a.search_movie('Star Trek', _episodes = False)

    sw = a.search_movie('Star Wars', _episodes = False)


    for j, fran in enumerate(fran_id):
        print 'Working on ' + fran
        if j == 0:
       
           df_st = pd.DataFrame(index = range(0,len(st)), columns = ['title', 'rating'])
           df_st['franchise'] = 1
           for x in range(0,len(st)):
               a.update(st[x])
               print st[x]['long imdb canonical title']
               try:
                  df_st.set_value(x,'title', st[x]['long imdb canonical title'])
                  df_st.set_value(x,'rating', st[x]['rating'])   
               except:
                   df_st.set_value(x,'title', st[x]['long imdb canonical title'])
                   df_st.set_value(x,'rating', 999)
        elif j == 1:
           df_sw = pd.DataFrame(index = range(0,len(st)), columns = ['title', 'rating'])
           df_sw['franchise'] = 2
           for x in range(0,len(sw)):
               a.update(sw[x])
                print sw[x]['long imdb canonical title']
                try:
                   df_sw.set_value(x,'title', sw[x]['long imdb canonical title'])
                   df_sw.set_value(x,'rating', sw[x]['rating'])
                except:
                   df_sw.set_value(x,'title', sw[x]['long imdb canonical title'])
                   df_sw.set_value(x,'rating', 999)

    return(df_sw, df_st)


def star_analysis(df_sw, df_st):
#Combine Dataframes
    df_all = pd.concat([df_st, df_sw],axis = 0)
    df_all_cull = df_all[df_all['rating']<999]

    st_scores = df_all_cull['rating'][df_all_cull['franchise']==1]
    sw_scores = df_all_cull['rating'][df_all_cull['franchise']==2]

    [t, p, df] = sm.stats.ttest_ind(sw_scores, st_scores,alternative = 'larger', usevar = 'unequal')

    st_mean = np.mean(st_scores)
    st_std = np.std(st_scores)

    sw_mean = np.mean(sw_scores)
    sw_std = np.std(sw_scores)

    pooled_sd = (st_std+sw_std)/2

    cohensD = (sw_mean - st_mean) / pooled_sd

    print '\nThe analysis showed a t value of %f with a p value of %f and effect size of %f' %(t, p, cohensD)


