# -*- coding: utf-8 -*-
"""
Created on Sun Oct  9 15:53:39 2022

@author: chloe
"""

#%% Extraction des données
import json
from copy import deepcopy 

badges=open(r'C:\Users\chloe\Documents\ESILV\Annee_2022-2023\S9\Structure des Donnees\stats\badges.json','r',encoding='utf-8').read()
badges=json.loads(badges)
comments=open(r'C:\Users\chloe\Documents\ESILV\Annee_2022-2023\S9\Structure des Donnees\stats\comments.json','r',encoding='utf-8').read()
comments=json.loads(comments)
postHistory=open(r'C:\Users\chloe\Documents\ESILV\Annee_2022-2023\S9\Structure des Donnees\stats\postHistory.json','r',encoding='utf-8').read()
postHistory=json.loads(postHistory)
postLinks=open(r'C:\Users\chloe\Documents\ESILV\Annee_2022-2023\S9\Structure des Donnees\stats\postLinks.json','r',encoding='utf-8').read()
postLinks=json.loads(postLinks)
posts=open(r'C:\Users\chloe\Documents\ESILV\Annee_2022-2023\S9\Structure des Donnees\stats\posts.json','r',encoding='utf-8').read()
posts=json.loads(posts)
tags=open(r'C:\Users\chloe\Documents\ESILV\Annee_2022-2023\S9\Structure des Donnees\stats\tags.json','r',encoding='utf-8').read()
tags=json.loads(tags)
users=open(r'C:\Users\chloe\Documents\ESILV\Annee_2022-2023\S9\Structure des Donnees\stats\users.json','r',encoding='utf-8').read()
users=json.loads(users)
votes=open(r'C:\Users\chloe\Documents\ESILV\Annee_2022-2023\S9\Structure des Donnees\stats\votes.json','r',encoding='utf-8').read()
votes=json.loads(votes)

#%% Write json files
def toJSON(table_json, destination_file):
    with open(destination_file, 'w', encoding='utf-8') as writefile:
        writefile.write('[')
        for x in range(len(table_json)):
            json.dump(table_json[x], writefile)
            if x!=len(table_json)-1:
                writefile.write(',\n')
        writefile.write(']')

#%% Premier schéma
#%% Fusion de badges dans users sous forme de liste
fusers = deepcopy(users)
fusers=sorted(fusers, key=lambda x: x['Id_users'])
fbadges = deepcopy(badges)
fbadges=sorted(fbadges, key=lambda x:x['UserId_badges'])
for user in fusers:
    #print(user['Id_users'])
    user['badges']=[]
    a=False
    pos=0
    for n in range(pos, len(fbadges)):
        if fbadges[n]['UserId_badges']==user['Id_users']:
            user['badges'].append(fbadges[n])
            pos=n
            a=True
        elif a==True:
            a=False
            break
            
#%% Surcharge de DisplayName dans Post et Comments
names={}
for user in fusers:
    names[str(user['Id_users'])]=user['DisplayName_users']
#%%
fposts=deepcopy(posts)
for post in fposts:
    #print(post['Id_posts'])
    if post['OwnerUserId_posts'] is not None:
        post['DisplayName_users']=names[str(post['OwnerUserId_posts'])]

#%%
fcomments=deepcopy(comments)
for comment in fcomments:
    #print(comment['Id_comments'])
    if comment['UserId_comments'] is not None:
        comment['DisplayName_users']=names[str(comment['UserId_comments'])]

#%% Eclatement puis fusion des ...Count (avec l'id) dans User
fpostcounts=[]
for post in fposts:
    counts={}
    if post['OwnerUserId_posts'] is not None:
        counts['OwnerUserId_posts']=post['OwnerUserId_posts']
        counts['Id_posts']=post['Id_posts']
        counts['ViewCount_posts']=post.pop('ViewCount_posts',None)
        counts['AnswerCount_posts']=post.pop('AnswerCount_posts',None)
        counts['CommentCount_posts']=post.pop('CommentCount_posts',None)
        counts['FavoriteCount_posts']=post.pop('FavoriteCount_posts', None)
        fpostcounts.append(counts)

#%%
fpostcounts.sort(key=lambda x: x['OwnerUserId_posts'])
for user in fusers:
    print(user['Id_users'])
    user['counts']=[]
    a=False
    pos=0
    for n in range(pos, len(fpostcounts)):
        if fpostcounts[n]['OwnerUserId_posts']==user['Id_users']:
            user['counts'].append(fpostcounts[n])
            pos=n
            a=True
        elif a==True:
            a=False
            break

#%% Export of the first schema
toJSON(fusers, r'C:\Users\chloe\Documents\ESILV\Annee_2022-2023\S9\Structure des Donnees\stats\Schema_1\users.json')
toJSON(fposts, r'C:\Users\chloe\Documents\ESILV\Annee_2022-2023\S9\Structure des Donnees\stats\Schema_1\posts.json')
toJSON(fcomments, r'C:\Users\chloe\Documents\ESILV\Annee_2022-2023\S9\Structure des Donnees\stats\Schema_1\comments.json')

#%%
#%% Second schéma
#%% Fusion de comments dans posts
scomments=deepcopy(comments)
scomments=sorted(scomments, key=lambda x: x['PostId_comments'])
sposts=deepcopy(posts)
sposts=sorted(sposts, key=lambda x:x['Id_posts'])
for post in sposts:
    print(post['Id_posts'])
    post['comments']=[]
    a=False
    pos=0
    for n in range(pos, len(scomments)):
        if scomments[n]['PostId_comments']==post['Id_posts']:
            post['comments'].append(scomments[n])
            pos=n
            a=True
        elif a==True:
            a=False
            break

#%% Surcharge des ...Count dans User sous forme de listes
viewcount={}
answercount={}
commentcount={}
favoritecount={}

susers=deepcopy(users)
susers=sorted(susers, key=lambda x: x['Id_users'])

for user in susers:
    viewcount[str(user['Id_users'])]=[]
    answercount[str(user['Id_users'])]=[]
    commentcount[str(user['Id_users'])]=[]
    favoritecount[str(user['Id_users'])]=[]
for post in sposts:
    if post['OwnerUserId_posts'] is not None:
        viewcount[str(post['OwnerUserId_posts'])].append(post['ViewCount_posts'])
        answercount[str(post['OwnerUserId_posts'])].append(post['AnswerCount_posts'])
        commentcount[str(post['OwnerUserId_posts'])].append(post['CommentCount_posts'])
        favoritecount[str(post['OwnerUserId_posts'])].append(post['FavoriteCount_posts'])

#%%
for user in susers:
    print(user['Id_users'])
    user['ViewCount_posts']=viewcount[str(user['Id_users'])]
    user['AnswerCount_posts']=answercount[str(user['Id_users'])]
    user['CommentCount_posts']=commentcount[str(user['Id_users'])]
    user['FavoriteCount_posts']=favoritecount[str(user['Id_users'])]

#%% Eclatement de User
susersstuff=[]
susersdates=[]

for user in susers:
    stuff={}
    stuff['Id_users']=user['Id_users']
    stuff['UpVotes_users']=user.pop('UpVotes_users',None)
    stuff['DownVotes_users']=user.pop('DownVotes_users',None)
    stuff['ProfileImageUrl_users']=user.pop('ProfileImageUrl_users',None)
    stuff['WebsiteUrl_users']=user.pop('WebsiteUrl_users',None)
    stuff['AccountId_users']=user.pop('AccountId_users',None)
    susersstuff.append(stuff)
    
    dates={}
    dates['Id_users']=user['Id_users']
    dates['CreationDate_users']=user.pop('CreationDate_users',None)
    dates['LastAccessDate_users']=user.pop('LastAccessDate_users',None)
    susersdates.append(dates)

#%% Export of the first schema
#toJSON(scomments, r'C:\Users\chloe\Documents\ESILV\Annee_2022-2023\S9\Structure des Donnees\stats\Schema_2\comments.json')
toJSON(sposts, r'C:\Users\chloe\Documents\ESILV\Annee_2022-2023\S9\Structure des Donnees\stats\Schema_2\posts.json')
toJSON(susers, r'C:\Users\chloe\Documents\ESILV\Annee_2022-2023\S9\Structure des Donnees\stats\Schema_2\users.json')
toJSON(susersstuff, r'C:\Users\chloe\Documents\ESILV\Annee_2022-2023\S9\Structure des Donnees\stats\Schema_2\usersstuff.json')
toJSON(susersdates, r'C:\Users\chloe\Documents\ESILV\Annee_2022-2023\S9\Structure des Donnees\stats\Schema_2\userscomments.json')