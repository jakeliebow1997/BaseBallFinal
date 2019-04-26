import numpy as np
#data.groupby(['home_team','events']).agg('count')
#from pybaseball import statcast
import pandas as pd
import pymongo
import boto3

def main(batter):
	c = boto3.client(
    's3',
    # Hard coded strings as credentials, not recommended.
    aws_access_key_id='null',
    aws_secret_access_key='null'
	)
	obj = c.get_object(Bucket='baseballs3', Key='data.csv')
	data = pd.read_csv(obj['Body'])
	df=df.loc[df['batter']==batter]#Mookie Betts
	P=0
	d={}
	for i,x in df.iterrows():
		if type(x['pitch_type'])==type('s'):
			if x['pitch_type'] not in [*d]:
				d[x['pitch_type']]=[0,0]
			if x['description']=='foul' or x['description']=='foul_tip':
				d[x['pitch_type']][0]+=0.5#foul worth half points as hit
				d[x['pitch_type']][1]+=1.0
			if x['description']=='swinging_strike' or x['description']=='swinging_strike_blocked':
				d[x['pitch_type']][1]+=1.0
			if x['description']=='hit_into_play' or x['description']=='hit_into_play_no_out' or x['description']=='hit_into_play_score':
				d[x['pitch_type']][0]+=1.0
				d[x['pitch_type']][1]+=1.0
	arr=[]
	for x in [*d]:
		arr.append(d[x][0]/d[x][1])

	s=0
	for x in arr:
		s+=(x-np.mean(arr))**2
	return (s/(len(arr)-1))
print(main(605141.0))
