import csv
import pandas as pd
import numpy as np
from scipy.spatial.distance import cosine
        
if __name__ == "__main__":
    user_vec = [] # Vector for user's choices 
    csv_path = "DB_Test - Sheet1.csv" # Read the CSV file
    df1 = pd.read_csv(csv_path)
    df_view = df1[['Number', 'Description']]
    print df_view

    # User enters his choices 
    for i in range(1, (len(df1.index)+1)):
        print "Choose -1, 0, 1 for Dislike, Love or Like respectively for item", i, "or press q to quit"
        n = raw_input()
        if n == '-1' or n == '0' or n == '1':
            user_vec.append(n)
        elif n == 'q':
            break
##    print user_vec
    
    # Adding the data user selected to a dictionary
    reader = csv.DictReader(open(csv_path))
    result = {}
    c = 0
    for row in reader:
        if c < len(user_vec):
            if user_vec[c] == '1' or user_vec[c] == '0' or user_vec[c] == '-1':
                for column, value in row.iteritems():
                    result.setdefault(column.strip(), []).append(value.strip())
            else:
                user_vec.remove(user_vec[c])
                c = c-1
        elif c >= len(user_vec):
            break
        c = c+1
##    print result

    result['Zipcode'] = [int(i) for i in result['Zipcode']]
    result['Price'] = [float(i.strip('$')) for i in result['Price']]
    result['Offer_Delivery'] = [int(i) for i in result['Offer_Delivery']]
    
    df2 = pd.DataFrame(result)
    stacked = df2[['Type_of_meal','Genre','Class','Item1','Item2','Item3','Item4','Item5','Item6']].stack()
    df2[['Type_of_meal','Genre','Class','Item1','Item2','Item3','Item4','Item5','Item6']] = pd.Series(stacked.factorize()[0], index=stacked.index).unstack()
##    print (df2)
    cols_to_norm = ['Zipcode','Price','Type_of_meal','Genre','Class','Item1','Item2','Item3','Item4','Item5','Item6']
    df2[cols_to_norm] = df2[cols_to_norm].apply(lambda x: (x - x.min()) / (x.max() - x.min()))
    result =df2.to_dict('list')
    
    # Change the vector from string to int type
    for i in range(0,len(user_vec)):
        user_vec[i] = int(user_vec[i])
    
    # Add the data to a List
    L=[]
    for key, value in result.iteritems():
        if key == "Zipcode":
            L.append(value)
        elif key == "Price":
            L.append(value)
        elif key == "Offer_Delivery":
            L.append(value)
        elif key == "Type_of_meal":
            L.append(value)
        elif key == "Genre":
            L.append(value)
        elif key == "Class":
            L.append(value)
        elif key == "Item1":
            L.append(value)
        elif key == "Item2":
            L.append(value)
        elif key == "Item3":
            L.append(value)
        elif key == "Item4":
            L.append(value)
        elif key == "Item5":
            L.append(value)
        elif key == "Item6":
            L.append(value)
##    print L

    L = np.array(L)
    user_vec = np.array(user_vec)
    res = np.matmul(L,user_vec)
##    print "Resultant vector is",res
    res_vec = res/len(user_vec)
##    print "Resultant vector divided by total number of items selected is", res_vec

    # Adding all the data to a dictionary
    reader = csv.DictReader(open(csv_path))
    result_all = {}
    for row in reader:
        for column, value in row.iteritems():
            result_all.setdefault(column.strip(), []).append(value.strip())
##    print result_all

    result_all['Zipcode'] = [int(i) for i in result_all['Zipcode']]
    result_all['Price'] = [float(i.strip('$')) for i in result_all['Price']]
    result_all['Offer_Delivery'] = [int(i) for i in result_all['Offer_Delivery']]

    df1 = pd.DataFrame(result_all)
    stacked = df1[['Type_of_meal','Genre','Class','Item1','Item2','Item3','Item4','Item5','Item6']].stack()
    df1[['Type_of_meal','Genre','Class','Item1','Item2','Item3','Item4','Item5','Item6']] = pd.Series(stacked.factorize()[0], index=stacked.index).unstack()
##    print(df1)
    cols_to_norm = ['Zipcode','Price','Type_of_meal','Genre','Class','Item1','Item2','Item3','Item4','Item5','Item6']
    df1[cols_to_norm] = df1[cols_to_norm].apply(lambda x: (x - x.min()) / (x.max() - x.min()))
    result_all =df1.to_dict('list')

    # Add all the data to a List and Names of food items to another List
    L_all=[]
    L_name=[]
    for key, value in result_all.iteritems():
        if key == "Zipcode":
            L_all.append(value)
        elif key == "Price":
            L_all.append(value)
        elif key == "Offer_Delivery":
            L_all.append(value)
        elif key == "Type_of_meal":
            L_all.append(value)
        elif key == "Genre":
            L_all.append(value)
        elif key == "Class":
            L_all.append(value)
        elif key == "Item1":
            L_all.append(value)
        elif key == "Item2":
            L_all.append(value)
        elif key == "Item3":
            L_all.append(value)
        elif key == "Item4":
            L_all.append(value)
        elif key == "Item5":
            L_all.append(value)
        elif key == "Item6":
            L_all.append(value)
        elif key == "Description":
            L_name.append(value)
##    print L_all

    L_name = L_name[0]
    L_all = np.array(L_all)
##    print L_all

    # Find the Euclidean Distance between the res_vec and all other food items
    dist=[]
    for i in range(0,len(L_all[1])):
        vector1 = res_vec
        vector2 = L_all[0:12,i]
        diff = vector2 - vector1
        squareDistance = np.dot(diff.T, diff)
        dist.append(squareDistance)

    rec={}
    for i in range(0,len(L_name)):
        rec[L_name[i]] = dist[i]

    rec = sorted(rec.items(), key=lambda x: x[1])
    print rec

    data = pd.read_csv('Sheet1.csv')
    data_items = data.drop('User',1)
    data_ibs = pd.DataFrame(index=data_items.columns,columns=data_items.columns)
    # Lets fill in those empty spaces with cosine similarities
    # Loop through the columns
    for i in range(0,len(data_ibs.columns)) :
    # Loop through the columns for each column
        for j in range(0,len(data_ibs.columns)) :
      # Fill in placeholder with cosine similarities
          data_ibs.ix[i,j] = 1-cosine(data_items.ix[:,i],data_items.ix[:,j])
    # Create a placeholder items for closes neighbours to an item

    data_neighbours = pd.DataFrame(index=data_ibs.columns,columns=range(1,11))
    # Loop through our similarity dataframe and fill in neighbouring item names
    for i in range(0,len(data_ibs.columns)):
        data_neighbours.ix[i,:10] = data_ibs.ix[0:,i].sort_values(ascending=False)[:10].index

    print data_neighbours
    # --- End Item Based Recommendations --- #

    # --- Start User Based Recommendations --- #
    # Helper function to get similarity scores
    def getScore(history, similarities):
       return sum(history*similarities)/sum(similarities)
     
    # Create a place holder matrix for similarities, and fill in the user name column
    data_sims = pd.DataFrame(index=data.index,columns=data.columns)
    data_sims.ix[:,:1] = data.ix[:,:1]
     
    #Loop through all rows, skip the user column, and fill with similarity scores
    for i in range(0,len(data_sims.index)):
        for j in range(1,len(data_sims.columns)):
            user = data_sims.index[i]
            product = data_sims.columns[j]
     
            if data.ix[i][j] == 1:
                data_sims.ix[i][j] = 0
            else:
                product_top_names = data_neighbours.ix[product][1:10]
                product_top_sims = data_ibs.ix[product].sort_values(ascending=False)[1:10]
                user_purchases = data_items.ix[user,product_top_names]
     
                data_sims.ix[i][j] = getScore(user_purchases,product_top_sims)
     
    # Get the top food items
    data_recommend = pd.DataFrame(index=data_sims.index, columns=['user','1','2','3','4','5','6'])
    data_recommend.ix[0:,0] = data_sims.ix[:,0]
     
    # Instead of top item scores, we want to see names
    for i in range(0,len(data_sims.index)):
        data_recommend.ix[i,1:] = data_sims.ix[i,:].sort_values(ascending=False).ix[1:7,].index.transpose()
     
    # Print a sample
    print data_recommend.ix[:10,:4]
