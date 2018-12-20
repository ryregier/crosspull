email = "" #Please enter your email here in between the quotes. This is so the Crossref and OADOI know who is making use of their APIs.

import urllib.request, urllib.parse, urllib.error
import json
import ssl
import re
from datetime import datetime
import csv


ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE


if email == "":
    print ("You need to enter your email in the first line of code.")
    print ("When you using Public APIs like this python code does, entering an email is standard practice.")
    quit()

def strippy(x): #stripping whitespace from strings
    try:
        return x.strip()
    except:
        return x


def pull(x):
    try:
        return x[0]
    except:
        return x

doi_list = []

while True:
    institution_full = input("Enter the full name of your Institution:") #Pulling full name to match against later
    #institution_full = "University of Guelph"
    if len(institution_full)==0: #If length is 0 then quit
        quit()

    institution_short = input("Enter the distinguishing and unique ONE word in your institution's name:") #Pulling short name to query with now
    #institution_short = "Guelph"
    if len(institution_short)==0:
        quit()

    csv_name="Crosspull-"+institution_full+".csv"

    crossref_baseurl = "https://api.crossref.org/works?query.affiliation=" #Crossref URL for querying

    items = 1000
    rows = 1000
    cursor = "*"

    run_count = 1

    while items == rows and run_count < 10:

        url = crossref_baseurl + urllib.parse.quote(institution_short) + "&rows="+str(rows)+"&mailto=" + email +"&cursor="+cursor
        #print(url)

        try:
             #Getting Crossref API for ISSN
            #print(url)
            # https://api.crossref.org/works?query.affiliation=Guelph&rows=1000&mailto=rregier@uoguelph.ca
            #print('Retrieving Crossref API at', url)

            uh = urllib.request.urlopen(url)
            data = uh.read().decode()
            info = json.loads(data)

        except:
            print ("Error connecting to Crossref!")
            run_count = run_count+1
            continue

        #print(url)
        #break

        print('Please wait. Pulling results. Doing 1000 at a time. Currently in round number:',run_count)

        total_results = info['message']['total-results']
        #print (total_results)

        cursor = info['message']['next-cursor']

        if "+" in cursor: #fixing error with + in crossref cursor string https://github.com/CrossRef/rest-api-doc/issues/417
            cursor = cursor.replace('+','%2B')

        #print(cursor)

        rows = 1000

        items = info['message']['items-per-page']
        #print(info['message']['items-per-page'])

        run_count = run_count+1


        count = 0


        for item in info['message']['items']: # Looping through different records
            DOI = info['message']['items'][count]['DOI']
            #print(DOI)
            indexed = False

            author_count = 0

            #print(info['message']['items'][count].get(['author']))

            author_check = info['message']['items'][count].get('author',"None")

            if author_check == "None":
                #print (DOI,'no author')
                continue

            #print(DOI)
            for author in info['message']['items'][count]['author']: # Looping through different authors

                if indexed == True:
                    continue

                aff_count = 0

                for affiliation in info['message']['items'][count]['author'][author_count]['affiliation']: #looping through different affilations

                        #try:
                        ## print(info['message']['items'][count]['author'][author_count]['affiliation'][aff_count]['name'])
                        listed_aff = info['message']['items'][count]['author'][author_count]['affiliation'][aff_count]['name']

                        #print(listed_aff)

                        if institution_full in listed_aff:
                            #print (institution_full)
                            indexed = True

                            doi_dict = dict()

                            doi_dict = {"DOI":"https://doi.org/"+DOI,
                                      "type": info['message']['items'][count].get('type',),
                                       "journal":pull(info['message']['items'][count].get('container-title',)),
                                       "title":pull(info['message']['items'][count].get('title',)),
                                        #"year":info['message']['items'][count]['published-print']['date-parts'][0][0],
                                        "year":pull(info['message']['items'][count]['created']['date-parts'][0]),
                                        "article_title":info['message']['items'][count]['title'][0],
                                        "ISSN":pull(info['message']['items'][count].get('ISSN',)),
                                        "ISBN":pull(info['message']['items'][count].get('ISBN',)),
                                        "publisher":info['message']['items'][count].get('publisher',),
                                        'affiliation': info['message']['items'][count]['author'][author_count]['affiliation'][aff_count]['name']
                                        }

                            #print (DOI)

                            doi_list.append(doi_dict)


                        aff_count += 1
                        #except:
                        #    aff_count += 1
                        #    continue

                author_count += 1
            count += 1

    myFile = open(csv_name,'w',newline="", encoding='utf-8')
    with myFile:
        writer = csv.writer(myFile)
        writer.writerow(['Title', 'Type', 'Series', 'Publisher', 'Year', 'ISSN', 'ISBN', 'DOI','Affiliation'])
        for a in doi_list:
            data2 = [a["title"], a["type"], strippy(a["journal"]), strippy(a["publisher"]), a["year"], a["ISSN"], a["ISBN"], a["DOI"],strippy(a['affiliation'])]
            writer.writerow(data2)

    print("- - - - - - - - -")
    print("All done!")
    print("This many publications found that have your insitution listed in author affilations:",len(doi_list))
    print("A csv file has been exported to the same file this program is saved in. The file is called:",csv_name)
    print("___________________")
    print("\n")
    #break
