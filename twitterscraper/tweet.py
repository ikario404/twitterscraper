from datetime import datetime

from bs4 import BeautifulSoup
from coala_utils.decorators import generate_ordering


@generate_ordering('timestamp', 'id', 'text', 'user', 'replies', 'retweets', 'likes', 'lang', 'img_url', 'tweet_url',
 'nb_mentionned_users', 'link_inside_twt', 'quote', 'media', 'mentionned_users')
class Tweet:
    def __init__(self, user, id, timestamp, fullname, text, replies, retweets, likes, lang, img_url, tweet_url,
     nb_mentionned_users, link_inside_twt, quote, media, mentionned_users):
        self.user = user
        self.id = id
        self.timestamp = timestamp
        self.fullname = fullname
        self.text = text
        self.replies = replies
        self.retweets = retweets
        self.likes = likes
        self.lang = lang
        self.img_url = img_url
        self.tweet_url = tweet_url
        self.nb_mentionned_users = nb_mentionned_users
        self.link_inside_twt = link_inside_twt
        self.quote = quote
        self.media = media
        self.mentionned_users = mentionned_users


    @classmethod
    def from_soup(cls, tweet):
        if tweet.find('div', 'AdaptiveMedia-photoContainer'):
            img_url = tweet.find('div', 'AdaptiveMedia-photoContainer').get('data-image-url')
        else:
            img_url = ""
        return cls(
            user=tweet.find('span', 'username').text[1:],
            id=tweet['data-item-id'],
            timestamp=datetime.utcfromtimestamp(
                int(tweet.find('span', '_timestamp')['data-time'])),
            fullname=tweet.find('strong', 'fullname').text,
            text=tweet.find('p', 'tweet-text').text or "",
            replies = tweet.find(
                'span', 'ProfileTweet-action--reply u-hiddenVisually').find(
                    'span', 'ProfileTweet-actionCount')['data-tweet-stat-count'] or '0',
            retweets = tweet.find(
                'span', 'ProfileTweet-action--retweet u-hiddenVisually').find(
                    'span', 'ProfileTweet-actionCount')['data-tweet-stat-count'] or '0',
            likes = tweet.find(
                'span', 'ProfileTweet-action--favorite u-hiddenVisually').find(
                    'span', 'ProfileTweet-actionCount')['data-tweet-stat-count'] or '0',
            lang = tweet.find('p', 'tweet-text')['lang'] or '',
            img_url = img_url,
            tweet_url = tweet.find('div', 'tweet')['data-permalink-path'] or '0',
            nb_mentionned_users = '',
            mentionned_users = '',
            link_inside_twt = '',
            quote = '',
            media = ''
        )

    @classmethod
    def from_html(cls, html):
        soup = BeautifulSoup(html, "lxml")
        tweets = soup.find_all('li', 'js-stream-item')
        if tweets:
            for tweet in tweets:
                try:
                    yield cls.from_soup(tweet)
                except AttributeError:
                    pass  # Incomplete info? Discard!
