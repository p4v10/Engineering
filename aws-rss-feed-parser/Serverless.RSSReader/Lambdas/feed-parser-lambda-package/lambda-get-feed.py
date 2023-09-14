from datetime import datetime
import json
import feedparser
import re

def lambda_handler(event, context):
    parsed = feedparser.parse('https://cointelegraph.com/rss')
    articles = get_feed_info_and_articles(parsed)
    
    response = {
        "statusCode": 200,
        "body": json.dumps({
            "articles": articles
        })
    }
    
    return response

def get_feed_info_and_articles(parsed):
    feed = parsed['feed']
    feed_info = {
        'rss_feed_title': feed['title'],
        'rss_feed_subtitle': feed['subtitle'],
        'rss_feed_link': feed['link']
    }
    
    articles = []
    entries = parsed['entries']
    
    for entry in entries:
        # Convert published_parsed to a valid date format
        date_list = entry['published_parsed'][:6]  # Extract the first 6 elements
        date_obj = datetime(*date_list)  # Convert to datetime
        formatted_date = date_obj.strftime("%Y-%m-%d %H:%M:%S")  # Format the date

        article = {
            'feed_article_id': entry['id'],
            'feed_article_link': entry['link'],
            'feed_article_published_date': formatted_date,
            'feed_article_title': entry['title'],
            'feed_article_author': entry['author_detail']['name'],
            'feed_article_summary': remove_html_tags(entry['summary'])
        }
        # Merge the feed_info and article dictionaries
        article.update(feed_info)
        articles.append(article)
        
    return articles

def remove_html_tags(text):
    clean = re.compile('<.*?>')
    return re.sub(clean, '', text)