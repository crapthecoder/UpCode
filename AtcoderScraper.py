import grequests
import requests
import json
from time import sleep
from bs4 import BeautifulSoup


headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.5005.63 Safari/537.36',
}


def get_submission_info(username):
    cur = 0

    while True:
        submissions = json.loads(requests.get(f'https://kenkoooo.com/atcoder/atcoder-api/v3/user/submissions?user={username}&from_second={cur}').text)
        if not submissions:
            break

        for submission in submissions:
            if submission['result'] == 'AC':
                try:
                    yield {
                        'language': submission['language'],
                        'problem_code': submission['problem_id'],
                        'solution_id': submission['id'],
                        'link': f'https://atcoder.jp/contests/{submission["contest_id"]}/submissions/{submission["id"]}',
                    }

                except KeyError:
                    pass

            cur = submission['epoch_second'] + 1


def get_code(html):
    soup = BeautifulSoup(html, 'lxml')
    return soup.select_one('#submission-code').text


def get_solutions(username, all_info=None):
    if all_info is None:
        all_info = list(get_submission_info(username))

    responses = grequests.imap(grequests.get(info['link'], headers=headers) for info in all_info)
    for response, info in zip(responses, all_info):
        yield {
            'language': info['language'],
            'problem_code': info['problem_code'],
            'solution_id': info['solution_id'],
            'link': info['link'],
            'solution': get_code(response.text),
        }


if __name__ == '__main__':
    for d in get_solutions('crap_the_coder'):
        print(d['solution'])
        print()
        print('-' * 100)
        print()