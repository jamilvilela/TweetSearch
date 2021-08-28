import datetime 
class Common():
    '''Commons values or constants used over the project'''

    #date time format
    FILE_NAME_DT_FMT = '%Y%m%d_%H%M%S'
    DATA_FIELD_DT_FMT = '%Y-%m-%d %H:%M:%S'
    
    # database information
    DB_PASSWORD = 'dE012022'
    DB_USER_NAME = 'jamilvilela'
    DB_CLUSTER_NAME  = 'Cluster0'
    DB_DATABASE_NAME = 'TwitterDB'
    DB_TABLE_TWEET_DATA = 'Tweet'
    DB_TABLE_TWEET_AUTHOR = 'Author'
    DB_TABLE_USER_SEARCH = 'Search'
    
    # Twitter API
    Tweets_Max = 200
    Twitter_URL_Recent_Search = 'https://api.twitter.com/2/tweets/search/recent'
    Twitter_Bearer_Token = 'AAAAAAAAAAAAAAAAAAAAAEvVRAEAAAAApmNoSEh0jyl9coamnM88WOmgBSI%3DPky7EMgJ6CXQuafqiV5Xb80oi4ujDvkqVTigqr7CM3yZ2ekaKV'
    Twitter_Header = {'Authorization': (f'Bearer {Twitter_Bearer_Token}'),
                      'content-type': 'application/json; charset=utf-8',
                      'Accept': 'application/json; charset=utf-8'}
        
    Twitter_Params = {'query': '', 
            'max_results': '100', 
            'next_token': '',
            'tweet.fields': 'text,created_at,author_id,public_metrics,lang', 
            'expansions': 'author_id,geo.place_id', 
            'place.fields': 'contained_within,country,country_code,full_name,geo,id,name,place_type', 
            'user.fields': 'created_at,description,entities,id,location,name,pinned_tweet_id,profile_image_url,protected,public_metrics,username,verified,withheld'}; 
 
    Twitter_Stored_Fields = ['text', 'user', 'qualifiers', 'hastags', 'mentions', 
            'created_at','author_id', 'public_metrics','lang', 'author_id','geo.place_id', 
            'contained_within','country','country_code','full_name','geo','id,name','place_type', 
            'created_at','description','entities','id','location','name','pinned_tweet_id',
            'profile_image_url','protected','public_metrics','url','username','verified','withheld']
    

    def Print_time(text):
        dt = datetime.datetime.now().strftime(Common.DATA_FIELD_DT_FMT)
        return print(f'{text} --> {dt} ')

    def save_to_file(tweets) -> str:
        sdt = datetime.datetime.now().strftime(Common.FILE_NAME_DT_FMT)
        with (open(f'result_twitter_{sdt}.json', mode='w', encoding='utf-8')) as f:
            print(tweets, file=f)
        return f.name



