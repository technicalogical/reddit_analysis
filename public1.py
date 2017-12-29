#!/usr/local/bin/python2.7 python2.7
import praw
import MySQLdb
import datetime

db = MySQLdb.connect(host='localhost', user='ENTER_USER', passwd='ENTER_PASS', db='DB_NAME', use_unicode='True', charset='utf8mb4')
cur = db.cursor()
#cur.execute("CREATE TABLE IF NOT EXISTS politics ( id INT UNSIGNED PRIMARY KEY AUTO_INCREMENT, submission_id TEXT NOT NULL)")
reddit = praw.Reddit(user_agent='political_analysis v.1 (by /u/)',
                     client_id='', client_secret="",
                     username='', password='')

# create function that downloads data from a given subreddit
top_posts = []
def submission_fetcher(sub, limit):
    subreddit = reddit.subreddit(sub)
    for submission in subreddit.hot(limit=limit):
	now = datetime.datetime.now()
        submission_data = {'sub_name': subreddit.display_name, 'title': submission.title, 'author': submission.author,
                           'num_comments': submission.num_comments, 'downs': submission.downs, 'ups': submission.ups,
                           'score': submission.score, 'post_id': submission.id, 'url_result': submission.url, 
                           'domain': submission.domain, 'datetime': now}
        top_posts.append(submission_data)

def mysql_writer():
    with db.cursor() as cursor:
        sql = "CREATE TABLE IF NOT EXISTS `political_analysis` (id MEDIUMINT NOT NULL AUTO_INCREMENT PRIMARY KEY, sub_name VARCHAR(50) NOT NULL, title VARCHAR(1000) NOT NULL, author VARCHAR(20) NULL, num_comments SMALLINT NULL, downs INT NULL, ups INT NULL, score INT NULL, post_id VARCHAR(30) NOT NULL, url_result TEXT NULL, domain TEXT NULL, datetime TIMESTAMP DEFAULT CURRENT_TIMESTAMP)"
        cur.execute(sql)    

    for submission in top_posts:
        try:
            with db.cursor() as cursor:
                sql = "INSERT INTO `political_analysis` (`sub_name`, `title`, `author`, `num_comments`, `downs`, `ups`, `score`, `post_id`, `url_result`, `domain`, `datetime`) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, NOW())"
                cur.execute(sql, (submission['sub_name'],
                                     submission['title'],
                                     submission['author'],
                                     submission['num_comments'],
                                     submission['downs'],
                                     submission['ups'],
                                     submission['score'],
                                     submission['post_id'],
                                     submission['domain'],
				     submission['url_result']
                                     )
                               )
                db.commit()
        finally:
 #           connection.close()
             pass


subreddits =["politics",
"news",
"the_donald",
"conspiracy",
"the_congress",
"askthe_donald",
"therightboycott",
"therightpurchase",
"the_doghouse",
"RightwingLGBT",
"rightwing",
"republicanmemes",
"Conservative",
"Republican",
"asktrumpsupporters",
"libertarian",
"richard_spencer",
"freespeech",
"uncensorednews",
"the_donald_uncensored",
"worldpolitics",
"the_donaldunleashed",
"politic",
"neutralpolitics",
"worldevents",
"inthenews",
"anythinggoesnews",
"full_news",
"qualitynews",
"usnews",
"truenews",
"usanews",
"altnewz",
"open_news", 
"abetterworldnews", 
"fullnews", 
"thenews", 
"uncensorednewsnetwork", 
"russia",
"rightist",
"new_right",
"alternative_right",
"tea_party",
"environment",
"gunsarecool",
"cornbreadliberals",
"politicalfactchecking",
"ElectionPolls",
"ForeignPolicyAnalysis",
"ModelUSGov",
"BlueMidterm2018",
"Democrats2020",
"Tuesday",
"AmericanPolitics",
"USpolitics",
"Democrats",
"Liberal",
"Progressive",
"NeoProgs",
"Socialism",
"Greed",
"SocialDemocracy",
"Politics",
"Presidents",
"Anarchism",
"liberal",
"women",
"greed",
"libs",
"NoCorporations",
"HillaryClinton",
"WorldPolitics",
"Labor",
"Democracy",
"Obama",
"GeoPolitics",
"ModeratePolitics",
"POTUSWatch",
"QualityNews",
"centerleftpolitics",
"centrist",
"Communism",
"Longshoremen",
"LabourUK",
"unite",
"neutralnews"]
for subreddit in subreddits:
    submission_fetcher(subreddit, 15)
# submission_fetcher('worldsnews', 10)
# submission_fetcher('the_donald', 10)
# submission_fetcher('news', 10)
# submission_fetcher('worldsnews', 10)
#submission_fetcher('all', 10)
mysql_writer()
