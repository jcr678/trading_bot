import pandas as pd
def replaceZeros(dataframe):
    dataframe = pd.read_csv(dataframe)
    #get date and sentiment and subjectivity columns
    date = dataframe['Date'].tolist()
    sent = dataframe['Sentiment'].tolist()
    subj = dataframe['Subjectivity'].tolist()
    changeDay = date[0]
    sentList = []
    subjList = []

    for i, day in enumerate(date): # Get first seman/subj value
        if sent[i] != 0:
            #indiceList.append(0)
            sentList.append(sent[i])
            subjList.append(subj[i])
            break

    tempSent=0
    tempSubj=0

    for i, day in enumerate(date): # Get rest of seman/subj value
        if sent[i] != 0:
            tempSent = sent[i]
            tempSubj = subj[i]
        if day != changeDay:
          sentList.append(tempSent)
          subjList.append(tempSubj)
          #indiceList.append(i)
          changeDay=day
    indice = 0
    changeDay = date[0]
    for i, day in enumerate(date): #replace zeros of sent and subj
        if sent[i] == 0: # this is to make sure dataframe doesnt start with zeros
          sent[i] = sentList[indice]
          subj[i] = subjList[indice]
        else: # update so we replace zero with most recently seen value if we dont start with zero
          sentList[indice] = sent[i]
          subjList[indice] = subj[i]
        if day != changeDay:
          changeDay = day
          indice = indice + 1


    dataframe = dataframe.drop('Sentiment', 1)
    dataframe = dataframe.drop('Subjectivity', 1)
    dataframe['Sentiment'] = sent
    dataframe['Subjectivity'] = subj
    print(dataframe)
    return dataframe
