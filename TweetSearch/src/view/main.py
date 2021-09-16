import json
import datetime
import os.path as path
from src.business.JsonToObj import jsonToObj
from src.business.Common import Common
from src.business.APITweetSearch import APITweetSearch
from src.business.APIAppClient import APIAppClient

def read_appconfig() -> object:
    ''' read the configuration file '''
    try:
        proj_path = path.abspath(__file__)
        dir_business = path.dirname(proj_path)
        dir_src = path.dirname(dir_business)
        file_path = path.join(dir_src, Common.APP_CONFIG_FILE)
        appconf = dict()
        with (open(file_path, mode='r', encoding='utf-8')) as f:                
            appconf = json.loads(f.read())
        return appconf['Configuration']
    except Exception as ex:
        return print('App.config there is not exists.')


def main():
    print('Let''s start.')
    t1 = datetime.datetime.now()

    Common.Configuration = read_appconfig()

    Twitter_NextToken = ''    
    try:        
        app = APIAppClient()
        if not app.Get_App_data():
            print('Something wrong with App data, friend. Look for help.')

        SearchList = app.Not_Integrated_Search()        
        UpdatedList = list()

        if SearchList:
            for search in SearchList:

                t2 = datetime.datetime.now()
                print('Start search: ')
                print(search['user_query'])

                ts = APITweetSearch(search)

                # Tweets_Max is how many tweets will be saved 
                Tweets_Max = Common.Configuration['Max_Tweets']
                while Tweets_Max > 0: 
                    # get the tweets based on App user search
                    tweets = ts.getRecentTweets(Twitter_NextToken)
                    objTweets = jsonToObj(tweets)
                    Twitter_NextToken = ''

                    if objTweets.meta.next_token != None:
                        Twitter_NextToken = objTweets.meta.next_token
            
                    if objTweets.meta.result_count == 0:
                        print('Nothing found, Bro :(')
                        break
                    else:                
                        if ts.InsertRecentSearch():
                            if Twitter_NextToken == '':
                                break # end of API result
                        else:
                            raise Exception('There are some errors occurred on database insert .')

                    Tweets_Max -= objTweets.meta.result_count

                UpdatedList.append(search['_id'])

                t3 = datetime.datetime.now()
                print(t3-t2)
            
            #update Search document with flag of integrated
            app.Update_user_search(UpdatedList)
            print(f'Total: {t3-t1}')
    except Exception as ex:
        print('Main error: {ex}')
    
if __name__ == "__main__":
    main()
