import Query2vec
import SimpleClassWorkload as SCW
import pandas as pd
timespan=[]
irange=range(200,2001,200)
original = pd.read_csv('anonQCut.csv', engine='python')
original["id"] = range(len(original))
df = original.loc[original['dbname'].isin(['UKIDSSDR10PLUS', 'UKIDSSDR8PLUS', 'UKIDSSDR7PLUS'])]
outputpath="/lustre/home/d171/s1926539/dissertation/s1926539/Data_code/Dissertationcode/WorkloadSumOutput/SimpleClassifier/"
timespan = []
timespan2 = []




OutPath2='/lustre/home/d171/s1926539/dissertation/s1926539/Data_code/Dissertationcode/WorkloadSumOutput/Query2vec/'


F=[]
S=[]


for i in irange:
        model_name = 'Try'
        CSV_name = 'try.csv'
        Image_name = "try.png"
        Bar_name = "try.png"
        k=11
        if i==200:  k = 9
        if i==400:  k = 8
        if i == 600:  k = 9
        if i == 800:  k = 11
        if i == 1000:  k = 11
        if i == 1200:  k = 9
        if i == 1400:  k = 5
        if i == 1600:  k = 9
        if i == 1800:  k = 11
        if i == 2000:  k = 9

        model_name = str(i) + model_name
        CSV_name = str(i) + CSV_name
        Image_name = str(i) + Image_name
        Bar_name = str(i) + Bar_name
        endtime,T_LEN,S_len=SCW.main(df, outputpath, i)
        F.append(T_LEN);S.append(S_len);
        timespan = Query2vec.Workload_sum(df, k, i, OutPath2, model_name, CSV_name, Image_name, Bar_name)
        timespan2.append(timespan)


print(F)

print(S)

