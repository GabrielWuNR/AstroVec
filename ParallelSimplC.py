
import concurrent.futures
import pyodbc
import pandas as pd
import extract as EX
import datetime
from sklearn.model_selection import train_test_split


server ='dissertation6539.database.windows.net'
database = 'DissertationClassifier'
username = 'adminNR'
password = 'Qwaszx9e8d7c!'
driver= '{ODBC Driver 17 for SQL Server}'



def Endtime(starttime):
  endtime = datetime.datetime.now()
  timspan = ((endtime - starttime).seconds) / 60
  print(timspan)
  return timspan

def ModelTrain(train):

    iter = 0
    second = []
    with pyodbc.connect(
            'DRIVER=' + driver + ';SERVER=' + server + ';PORT=1433;DATABASE=' + database + ';UID=' + username + ';PWD=' + password) as conn:
        with conn.cursor() as cursor:

            for index, row in train.iterrows():
                Query_id = index
                queryStr = row["queryStr"]
                time = row["time"]
                cpu_sec = row["cpu_sec"]
                elapsed_time = row["elapsed_time"]
                physical_IO = row["physical_IO"]
                row_count = row["row_count"]
                ipaddress = row["ipaddress"]
                dbname = row["dbname"]
                row_size = row["row_size"]
                userID = row["userID"]
                writeintoQuery = "INSERT INTO Queryinfo (time ,cpu_sec,elapsed_time,physical_IO , row_count,ipaddress,dbname,row_size ," \
                                 " userID , queryStr) " \
                                 "values(?,?,?,?,?,?,?,?,?,?)"
                cursor.execute(writeintoQuery, time, cpu_sec, elapsed_time, physical_IO, row_count, ipaddress, dbname,
                               row_size, userID, queryStr)
                findQid = "select MAX(Query_id) from Queryinfo"
                Q_id = cursor.execute(findQid).fetchall()[0][0]
                search = "select * from Firstlayer where T_features= '" + str(
                    EX.SqlExtractor(queryStr).triple["table"]).replace("'", "") + "';"
                result = cursor.execute(search)
                row = len(result.fetchall())
                if row <= 0:
                    insert = "INSERT INTO Firstlayer (T_features, T_feature_num) " \
                             " VALUES('" + str(EX.SqlExtractor(queryStr).triple["table"]).replace("'", "") + "', " \
                             + str(len(EX.SqlExtractor(queryStr).triple["table"])) + "); "

                    queryinsert = cursor.execute(insert)
                    findTid = "select MAX(T_id) from Firstlayer"
                    T_id = cursor.execute(findTid).fetchall()[0][0]

                    insertSecond = "INSERT INTO SecondLayer (Attri_features,Parent_id, Attri_feature_num)  VALUES('" + str(
                        EX.SqlExtractor(queryStr).triple["where"]).replace("'", "") + "', " + str(T_id) + "," + str(
                        len(EX.SqlExtractor(queryStr).triple["where"])) + "); "
                    try:
                        resultSecondI = cursor.execute(insertSecond)
                    except:
                        print("Insert fail")
                    findSid = "select MAX(Attri_id) from SecondLayer"
                    S_id = cursor.execute(findSid).fetchall()[0][0]

                    UpdateQuery = "UPDATE Queryinfo SET T_layer_id=" + str(S_id) + " WHERE Query_id=" + str(Q_id) + ";"
                    cursor.execute(UpdateQuery)

                    second.append(S_id)
                    conn.commit()

                if row > 0:

                    T_id = cursor.execute(search).fetchall()[0][0]

                    searchSecond = "select * from SecondLayer where Parent_id= " + str(T_id) + " and Attri_features='" \
                                   + str(EX.SqlExtractor(queryStr).triple["where"]).replace("'", "") + \
                                   "';"

                    resultSecond = cursor.execute(searchSecond)

                    countSecond = len(resultSecond.fetchall())

                    if countSecond <= 0:
                        insertSecond = "INSERT INTO SecondLayer (Attri_features,Parent_id, Attri_feature_num)  VALUES('" + str(
                            EX.SqlExtractor(queryStr).triple["where"]).replace("'", "") + "', " + str(T_id) + "," + str(
                            len(EX.SqlExtractor(queryStr).triple["where"])) + "); "
                        try:
                            resultSecondI = cursor.execute(insertSecond)
                        except:
                            print("Insert fail")
                        conn.commit()
                        findSid = "select MAX(Attri_id) from SecondLayer"
                        S_id = cursor.execute(findSid).fetchall()[0][0]
                        UpdateQuery = "UPDATE Queryinfo SET T_layer_id=" + str(S_id) + " WHERE Query_id=" + str(
                            Q_id) + ";"
                        cursor.execute(UpdateQuery)
                        second.append(S_id)
                    else:
                        S_id = cursor.execute(searchSecond).fetchall()[0][0]
                        UpdateQuery = "UPDATE Queryinfo SET T_layer_id=" + str(S_id) + " WHERE Query_id=" + str(
                            Q_id) + ";"
                        cursor.execute(UpdateQuery)
                        second.append(S_id)
                conn.commit()





original = pd.read_csv('anonQCut.csv', engine='python')
original["id"] = range(len(original))
df = original.loc[original['dbname'].isin(['UKIDSSDR10PLUS', 'UKIDSSDR8PLUS', 'UKIDSSDR7PLUS'])]
df = df.sample(n=170000)
train, test = train_test_split(df, test_size=0.09, random_state=42)
test.to_csv("Testload0.csv")


def parallel(i):
    start = i
    len_responses = 150000
    if start > len_responses - 1:
      pass
    end = start + 10000
    if end > len_responses:
           end = len_responses
    sub_train = train[start:end]
    print("Start parallel....")
    ModelTrain(sub_train)







def main():
    starttime = datetime.datetime.now()
    i = range(0, 150000, 10000)
    with concurrent.futures.ThreadPoolExecutor() as executor:
        executor.map(parallel, i)
    Endtime(starttime)


if __name__ == '__main__':
    main()




