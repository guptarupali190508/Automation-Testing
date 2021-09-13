import pandas as pd
import json
import csv
#sheet_url = "https://docs.google.com/spreadsheets/d/1fHiBtzxBC_3Q7I5SXr_GpNA4ivT73w4W4hjK6IkGDBY/edit#gid=2074968679"

#For single sheet
#url_1 = sheet_url.replace("/edit#gid=", "/export?format=csv&gid=") #give output as CSV when called

#For multiple sheets
sheet_id = "1fHiBtzxBC_3Q7I5SXr_GpNA4ivT73w4W4hjK6IkGDBY"
sheet_name = "Beds"
CSVFile = f'https://docs.google.com/spreadsheets/d/{sheet_id}/gviz/tq?tqx=out:csv&sheet={sheet_name}'




#df2 = df.assign(description=df.Contact.astype(str) + ' ' + df.Availability.astype(str) + ' ' + df.Item.astype(str) + ' ' + df.Comments.astype(str))
#df2 = df2.drop(['Contact', 'Availability', 'Item', 'Comments'], axis=1)# remove unwanted columns
#print(df2)
#dictionary = df2.to_dict(orient="index")

#print(dictionary)

#jsonString = json.dumps(dictionary, indent=4)
#print(jsonString)

