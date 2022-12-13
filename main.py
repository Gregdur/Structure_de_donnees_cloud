
from flask import Flask, render_template, request
import pandas as pd
from pymongo import MongoClient
app = Flask(__name__)

client = MongoClient('mongodb://mesiin592022-0007.westeurope.cloudapp.azure.com:30000/')
db = client['Stats']

collection1=db["comments"]
collection2=db["postHistory"]
collection3=db["postLinks"]
collection4=db["posts"]
collection5=db["tags"]
collection6=db["users"]
collection7=db["votes"]

requests={
    'R1':[{"$match":{'counts.0':{"$exists": 1},"AboutMe_users": {"$regex": "developer",'$options':'i'}}}, {"$project": {"Id_users": 1, "DisplayName_users": 1}}],
    'R2':[{"$match": {'counts.FavoriteCount_posts': {"$gt": 100},'counts.ViewCount_posts': {"$gt": 10000}}}, {"$project": {"Id_users": 1,"DisplayName_users": 1}}],
    'R3':[{"$match": {"CreationDate_comments": {"$gte": '2014-09-13'}}}, {"$project": {"UserId_comments": 1,"DisplayName_users": 1,"Score_comments": 1,"CreationDate_comments": 1,"Text_comments": 1}}, {"$group": {"_id": "null","max_score": {"$max": '$Score_comments'},"items": {"$push": '$$CURRENT'}}}, {"$project": {"Comments": {"$filter": {"input": '$items',"as": 'r',"cond": {"$eq": ['$$r.Score_comments','$max_score']}}}}}, {"$unwind": '$Comments'}],
    'R4':[{'$match':{"OwnerUserId_posts":5269}}],
    'R5':[{"$unwind": '$badges'}, {"$unwind": '$counts'}, {"$group": {"_id": '$badges.Name_badges',"nb_posts": {"$sum": 1}}}, {"$sort": {"nb_posts": -1}}, {"$limit": 1}],
    'R6':[{"$group": {"_id": '$OwnerUserId_posts',"avg_score": {"$avg": '$Score_posts'},"name_user": {"$first": '$DisplayName_users'}}}, {"$sort": {"avg_score": -1}}, {"$limit": 5}],
    'R7':[{"$match": {'badges.Name_badges': 'Student', "$and": [{"AboutMe_users": {"$regex":"software", "$options":'i'}},{"AboutMe_users": {"$regex":"student", "$options":'i'}}]}}, {"$group": {"_id": "null","minAge": {"$min": '$Age_users'},"maxAge": {"$max": '$Age_users'},"avgAge": {"$avg": '$Age_users'}}}],
    'R8':[{"$group": {"_id": '$OwnerUserId_posts',"nbPosts": {"$sum": 1},"titles": {"$addToSet": '$Title_posts'},"dates": {"$addToSet": '$CreaionDate_posts'}}}, {"$match": {"titles": {"$regex": "\\?",'$options':'i'}}}, {"$unwind": '$dates'}, {"$group": {"_id": {"user": '$_id',"Year": {"$year": {"$dateFromString": {"dateString": '$dates',"format": '%Y-%m-%d %H:%M:%S'}}}},"nbPosts": {"$sum": 1}}}]
}

requests_col1=["R3"]
requests_col2=[]
requests_col3=[]
requests_col4=["R6","R4","R8"]
requests_col5=[]
requests_col6=["R1","R2","R5","R7"]
requests_col7=[]



@app.route('/')
def man():
    return render_template('home.html')

#ADMIN SECTION=========================================================================================================
@app.route('/Admin')
def baseAdmin():
    return render_template('Admin.html')

@app.route('/Admin/Stats')
def baseAdminStats():
    ReplicaSets = ['RS18_1/MESIIN592022-0018:27017',
                   'RS19_2/MESIIN592022-0019:27017',
                   'RS3/MESIIN592022-0016:27017',
                   'RS4/MESIIN592022-0017:27017',
                   'RS34_5/MESIIN592022-0034:27017',
                   'RS35_6/MESIIN592022-0035:27017'
                   ]
    resp = db.command("dbstats")
    r = resp['raw']['RS3/MESIIN592022-0016:27017']
    column_names = ['replicaset'] + list(r.keys())
    df = pd.DataFrame(columns=column_names, dtype=object)
    i = 1
    for replicatset in ReplicaSets:
        dico = resp['raw'][replicatset]
        if ('fileSize' in dico):
            del dico['fileSize']
        df.loc[i] = [replicatset.split('/')[0]] + list(dico.values())
        i += 1
    return render_template('Admin.html',  tables=[df.to_html(classes='data', header="true")], titles=df.columns.values)


@app.route('/Admin/Indexes')
def baseAdminIndexes():
    collections = list(db.list_collections())
    column_names = ['name', 'type', 'idIndex']
    df = pd.DataFrame(columns=column_names, dtype=object)
    i = 1
    for col in collections:
        del col['options']
        del col['info']
        df.loc[i] = list(col.values())
        i += 1
    return render_template('Admin.html',  tables=[df.to_html(classes='data', header="true")], titles=df.columns.values)


#USER SECTION ==========================================================================================================
@app.route("/User")
def baseUser():
    return render_template('User.html')

@app.route("/User/R1")
def baseUserR1():
    result=collection6.aggregate(requests['R1'])
    final=pd.DataFrame.from_dict(result)
    return render_template('User.html',  tables=[final.to_html(classes='data', header="true")], titles=final.columns.values)

@app.route("/User/R2")
def baseUserR2():
    result = collection6.aggregate(requests['R2'])
    final = pd.DataFrame.from_dict(result)
    return render_template('User.html', tables=[final.to_html(classes='data', header="true")],titles=final.columns.values)


@app.route("/User/R3")
def baseUserR3():
    result = collection1.aggregate(requests['R3'])
    final = pd.DataFrame.from_dict(result)
    return render_template('User.html', tables=[final.to_html(classes='data', header="true")],
                           titles=final.columns.values)

@app.route("/User/R4")
def baseUserR4():
    result = collection4.aggregate(requests['R4'])
    final = pd.DataFrame.from_dict(result)
    return render_template('User.html', tables=[final.to_html(classes='data', header="true")],
                           titles=final.columns.values)




#DataAnalyst SECTION ==========================================================================================================

@app.route("/DataAnalyst")
def baseDataAnalyst():
    return render_template('DataAnalyst.html')

@app.route("/DataAnalyst/Ru1")
def baseDataAnalystRu1():
    result = collection6.aggregate(requests['R5'])
    final = pd.DataFrame.from_dict(result)
    return render_template('DataAnalyst.html', tables=[final.to_html(classes='data', header="true")],
                           titles=final.columns.values)

@app.route("/DataAnalyst/Ru2")
def baseDataAnalystRu2():
    result = collection4.aggregate(requests['R6'])
    final = pd.DataFrame.from_dict(result)
    return render_template('DataAnalyst.html', tables=[final.to_html(classes='data', header="true")],
                           titles=final.columns.values)

@app.route("/DataAnalyst/Ru3")
def baseDataAnalystRu3():
    result = collection6.aggregate(requests['R7'])
    final = pd.DataFrame.from_dict(result)
    return render_template('DataAnalyst.html', tables=[final.to_html(classes='data', header="true")],
                           titles=final.columns.values)

@app.route("/DataAnalyst/Ru4")
def baseDataAnalystRu4():
    result = collection4.aggregate(requests['R8'])
    final = pd.DataFrame.from_dict(result)
    return render_template('DataAnalyst.html', tables=[final.to_html(classes='data', header="true")],
                           titles=final.columns.values)



#MAIN SECTION =================================================================================================================
if __name__ == "__main__":
    app.run(debug=True)