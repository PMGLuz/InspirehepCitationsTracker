import urllib.request, urllib.error
import json
import os.path
import pickle

class Paper:
    def __init__(self, title, num_citations):
        self.title = title
        self.num_citations = num_citations
    def __reduce__(self):
        return (self.__class__, (self.title, self.num_citations) )

class AuthorRecord:
    num_citations = 0
    num_papers = 0

    def __init__(self, author_name, papersList):
        self.author_name = author_name
        self.papersList = papersList
        self.count_total_articles()
        self.count_total_citations()
    
    def count_total_citations(self):
        for i in self.papersList.values():
            self.num_citations += i.num_citations

    def count_total_articles(self):
        for i in self.papersList:
            self.num_papers += 1

    def __str__(self):
        return f"The author {self.author_name} has {self.num_papers} entries in the INSPIREHEP database with a total of {self.num_citations} citations."

    def __reduce__(self):
        return ( self.__class__, 
                (self.author_name, self.papersList)
                )

CURRENT_FILE_DIR = os.path.dirname(__file__)

# Check if a previous version of the author's profile exists and asks the user if it wants to compare with the previous version
def compareQ(old_record_file_name = 'record.pkl' ):
    oldRecordExists = False

    if os.path.exists( os.path.join(CURRENT_FILE_DIR, old_record_file_name) ):
        oldRecordExists = True
        Ans = input("A version of the author's record was found on disk. Do you want to compare this with the current online version?[Y,n] ")
        if Ans == 'Y':
            with open( os.path.join(CURRENT_FILE_DIR, old_record_file_name), 'rb')  as file:
                oldRecord = pickle.load(file)
                return (oldRecordExists, oldRecord)
    
    #Returns oldRecord = None if it arrives at this point 
    return (oldRecordExists, None)

# Loads inspirehep author's profile data
def get_author_data(AUTHOR, MAX_NUM_PAPERS):
    InspireAuthorProfile = 'https://inspirehep.net/api/literature?sort=mostrecent&size=' + \
                            str(MAX_NUM_PAPERS) + '&q=a%20' + AUTHOR

    try:
        connection = urllib.request.urlopen(InspireAuthorProfile)
    except urllib.error.URLError as ERROR:
        print('Unable to connect to inspirehep profile.')
        exit()

    data = json.loads(connection.read())

    num_hits = data['hits']['total']

    # Gets the articles list and fills each paper with information in a dictionary whose keys are the article's id
    papersList = {}
    for i in range(num_hits):
        id = data['hits']['hits'][i]['id']
        title = data['hits']['hits'][i]['metadata']['titles'][0]['title']
        citations_count = data['hits']['hits'][i]['metadata']['citation_count']
        papersList[id] = Paper(title, citations_count)


    # saves the author's profile data in a class
    return AuthorRecord(AUTHOR, papersList)

def compare_citations(oldRecord, newRecord):
    if newRecord.num_citations > oldRecord.num_citations:
        print(f"{AUTHOR} has {newRecord.num_citations-oldRecord.num_citations} new citations.")
        for i in newRecord.papersList.keys():
            if i in oldRecord.papersList:
                if oldRecord.papersList[i].num_citations < newRecord.papersList[i].num_citations:
                    print(f"The article: \"{oldRecord.papersList[i].title}\" citations changed.\n"
                          f"Citations: {oldRecord.papersList[i].num_citations} -> {newRecord.papersList[i].num_citations}\n"
                          )
            else:
                print(f"New article found: {newRecord.papersList[i].title}")
    else:
        print("No new citations.")
        exit()

# save record to binary file on disk
def save_profile(new_record_file_name = 'record.pkl'):
    if oldRecordExists:
        Ans = input('\nDo you want to update the profile on disk?[Y/n]\nThis will replace the previous file.\n')
    else:
        Ans = input('\nDo you want to save the profile to disk?[Y/n] ')

    if Ans == 'Y':
        with open( os.path.join(CURRENT_FILE_DIR, new_record_file_name ), 'wb')  as file:
            pickle.dump(newRecord,file)
            print('New record was saved to disk.')
    else:
        print('The profile record was not saved.')


if __name__ == "__main__":

    AUTHOR =  'Stephen.W.Hawking.1'    # Author id in inspirehep database
    MAX_NUM_PAPERS = 1000              # Max number of papers requested from inspirehep
    old_record_file_name = AUTHOR + '_record.pkl'

    (oldRecordExists, oldRecord) = compareQ(old_record_file_name)
    
    newRecord = get_author_data(AUTHOR, MAX_NUM_PAPERS)
    print(newRecord)

    if oldRecord is not None:
        compare_citations(oldRecord, newRecord)

    save_profile(old_record_file_name)