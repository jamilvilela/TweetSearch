import json
import datetime
from src.source.Tweet import jsonify
from src.data.MongoDB import ConnectMongoDB 
from src.Common import Common
from src.source.APITweetSearch import APITweetSearch

def InputData() -> dict:
    User_Email = input('Informe seu e-mail: ')
    User_Query = input('Pesquise sobre um assunto qualquer: ')
    User_Language = input('Qual é o idioma desejado? ')

    User_Search = [{
        #'_id': str(uuid.uuid4().hex),
        'user_email': User_Email,
        'user_query': User_Query,
        'user_language': User_Language,
        'inserted_at': datetime.datetime.now().strftime(Common.DATA_FIELD_DT_FMT)
    }]
    return User_Search

if __name__ == "__main__":
    # input data from scrren
    User_Search = InputData()

    Common.Print_time('calling Twitter')

    Twitter_NextToken = ''    
    try:
        ts = APITweetSearch(User_Search[0]['user_query'], User_Search[0]['user_language'])

        while Common.Tweets_Max:

            # get the tweets based on Twitter_Query 
            tweets = ts.getRecentTweets(Twitter_NextToken)
            objTweets = jsonify(tweets)
            Twitter_NextToken = ''

            Common.Print_time('It was got.')

            if objTweets.meta.next_token != None:
                Twitter_NextToken = objTweets.meta.next_token
            
            #save result into a backup file
            file_name = Common.save_to_file(objTweets)
            print(f'file created: {file_name}')

            if objTweets.meta.result_count == 0:
                print('Nothing found, Bro :(')
                break
            else:
                DataBase = ConnectMongoDB()
                if DataBase.InsertRecentSearch(User_Search, tweets):
                    if Twitter_NextToken == '':
                        break # end of API result
                else:
                    raise ValueError('There are some errors occurred on database insert .')
            Common.Tweets_Max -= objTweets.meta.result_count

        # end of the process and save result into a file
        Common.Print_time('that''s all folks!')            
    except Exception as ex:
        print('Main error: {ex}')
    except ValueError as ve:
        print('Insert error: {ve}')

