import pandas as pd

#import CSV using pandas
file = pd.read_csv('Raw Report.csv')

#Used to make 'Labels' column split more than 3 times to ensure same row size at the end
file.loc[0, 'Labels'] += ', , ,'

#some of the columns needed in the final report file  
columns = ['ID', 'Team', 'Title', 'Priority', 'Project', 'Creator']

#splitting labels column into separate individual columns (ex. "bug, task, 123" is 1 cell, the below splits it into 3 cells)
labels = file['Labels'].str.split(',', expand=True).rename(columns={0: 'CID', 1: 'Ticket Type', 2: 'User-Error?', 3: 'Non-bug?'})

#Filter used to keep only the necessary labels for the report and gets rid of the others
filter = ['bug', 'task', 'non-bug', 'user error'] 

#For loop used to go through each value in 'labels' dataframe to organize labels into specific columns and delete unnecessary ones
for i in range(labels.shape[0]):
    for j in range (1,labels.shape[1]):

        if pd.isna(labels.iloc[i,j]) or labels.iloc[i,j].lower().lstrip(' ') not in filter: labels.iloc[i,j] = "-"

        if labels.iloc[i,j].lower().lstrip(' ') in ['bug', 'task'] and j != 1:
            labels.iloc[i,1] = labels.iloc[i,j]
            labels.iloc[i,j] = "-"

        elif labels.iloc[i,j].lower().lstrip(' ') == 'user error' and j != 2:
            labels.iloc[i,2] = labels.iloc[i,j]
            labels.iloc[i,j] = "-"

        elif labels.iloc[i,j].lower().lstrip(' ') == 'non-bug' and j != 3:
            labels.iloc[i,3] = labels.iloc[i,j]
            labels.iloc[i,j] = "-"

#Combining all dataframes for the final report
report = pd.concat([pd.DataFrame(file[f] for f in columns).T,                   #Copies columns from imported file to appropriate columns. Transposed to match column and rows with report
                    labels.drop(labels.columns[4:], axis=1),                     #Deletes column 5+ in labels as it will never have a value                    
                    file['Created'].str.replace('T', ' ').str[:-5],             #Coverting 'created' column into format yyyy/mm/dd hh/mm/ss
                    file['Completed'].str.replace('T', ' ').str[:-5]], axis = 1)  #Coverting 'completed' column into format yyyy/mm/dd hh/mm/ss

#Converts report to CSV and generates CSV file 'Ticket Report'
report.to_csv('Final Report.csv', index=False) 

