# scrape-subreddit

> Collect submission and comment data from a Subreddit and save in a CSV file.

## Installation

Clone this repository onto your machine:

```
git clone https://www.github.com/eddiechapman/scrape-subreddit.git
```

Make a Python virtual environment and activate it:

```console
cd scrape-subreddit
python3 -m venv venv
source venv/bin/activate
```

Install the required Python packages into your virtual environment:

```console
pip install -r requirements.txt
```

## Usage

Enter your Reddit info in `scrape.py` lines 16-20:

```python
CLIENT_SECRET = ''
CLIENT_ID = ''
SUBREDDIT = ''  # "cats" not "r/cats"
N_SUBMISSIONS = 10
```

Run `scrape.py`:

```console
python3 scrape.py
```

Results will be written to `scrape-subreddit/comments.csv`. It will be overwritten if you run the program again. 
