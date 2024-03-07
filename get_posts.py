import datetime
import requests

from collections import Counter


def get_posts_last_3_days(subreddit: str) -> requests.Response:
    three_days_ago_timestamp = int((datetime.datetime.utcnow() - datetime.timedelta(days=3)).timestamp())
    url = f"https://www.reddit.com/r/{subreddit}/.json?time={three_days_ago_timestamp}"
    return requests.get(url)


def get_all_author_and_comments(response: requests.Response) -> list[tuple]:
    data = response.json()
    names_and_comments = [(child['data']['author_fullname'], child['data']['num_comments']) for child in data['data']['children']]
    return names_and_comments


def get_top_three_authors(names_and_comments: list[tuple, ...]) -> str:
    authors_only_names = [name[0] for name in names_and_comments]
    authors_counts = Counter(authors_only_names)
    most_common_authors = authors_counts.most_common(3)
    common_author_name = [author[0] for author in most_common_authors]
    return f'The list of top three authors - {common_author_name}'


def get_top_three_authors_collected_most_comments(names_and_comments: list[tuple, ...]) -> str:
    sorted_data = sorted(names_and_comments, key=lambda x: x[1], reverse=True)
    top_authors_with_most_comments = [item[0] for item in sorted_data[:3]]
    return f'The list of top authors with most comments - {top_authors_with_most_comments}'


if __name__ == '__main__':
    response = get_posts_last_3_days('Cryptocurrency')
    names_and_comments = get_all_author_and_comments(response)
    print(get_top_three_authors(names_and_comments))
    print(get_top_three_authors_collected_most_comments(names_and_comments))