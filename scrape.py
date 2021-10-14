"""
scrape.py

Collect submission and comment data from the top submissions of a Subreddit.

Eddie Chapman
2021-10-14

"""
import csv
from datetime import datetime
import pathlib

import praw

CLIENT_ID = ''
CLIENT_SECRET = ''
USER_AGENT = 'Subreddit Scraping'
SUBREDDIT = ''  # "cats" not "r/cats"
N_SUBMISSIONS = 10
OUTPUT_FILE = pathlib.Path.cwd() / 'comments.csv'


def main():
    print('Authenticating with Reddit API...')
    reddit = praw.Reddit(
        client_id=CLIENT_ID, 
        client_secret=CLIENT_SECRET,
        user_agent=USER_AGENT
    )
    
    print(f'Fetching subreddit {SUBREDDIT}...')
    subreddit = reddit.subreddit(SUBREDDIT)
    
    print(f'Fetching top {N_SUBMISSIONS} submissions...')
    top_submissions = subreddit.top(limit=N_SUBMISSIONS)
    
    reddit_data = []

    for submission in top_submissions:
        print(f'Collecting data from submission {submission.id}...')
        reddit_data.append({
            'subreddit': submission.subreddit.display_name,
            'submission_id': submission.id,
            'comment_id': None,
            'type': 'submission',
            'author': submission.author.name if submission.author else None,
            'timestamp': datetime.utcfromtimestamp(submission.created_utc),
            'score': submission.score,
            'title': submission.title,
            'text': submission.selftext,
            'is_submitter': True,
            'reply_to': None,
            'url': submission.url,
            
        })

        print(f'Unpacking comments for submission {submission.id}...')
        print(f'This may take a while. Total comments: {submission.num_comments}')
        submission.comments.replace_more(limit=None)
        comments = submission.comments.list()

        for comment in comments:
            print(f'Collecting data from comment {comment.id}...')
            reddit_data.append({
                'subreddit': comment.subreddit.display_name,
                'submission_id': submission.id,
                'comment_id': comment.id,
                'type': 'comment',
                'author': comment.author.name if comment.author else None,
                'timestamp': datetime.utcfromtimestamp(comment.created_utc),
                'score': comment.score,
                'title': None,
                'text': comment.body,
                'is_submitter': comment.is_submitter,
                'reply_to': comment.parent_id,
                'url': comment.permalink
            })
        
    column_names = [
        'subreddit', 'submission_id', 'comment_id', 'type', 'author', 'timestamp', 
        'score', 'title', 'text', 'is_submitter', 'reply_to', 'url'
    ]

    if OUTPUT_FILE.exists():
        print(f'Caution: Overwriting output file: {OUTPUT_FILE}')

    with OUTPUT_FILE.open('w') as f:
        writer = csv.DictWriter(f, fieldnames=column_names)
        writer.writeheader()
        writer.writerows(reddit_data)
        print(f'Data written to output file: {OUTPUT_FILE}')


if __name__ == '__main__':
    main()
