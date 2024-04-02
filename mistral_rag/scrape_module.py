import os
import sys
import json
import uuid
import requests
from datetime import datetime
from newspaper import Article
import re
import time

class Scraper:
    def __init__(self, input_file):
        self.input_file = input_file
        self.articles_dir = './articles'
        self.url_to_uuid = {}

    def generate_uuid_for_article(self, article_url):
        if article_url not in self.url_to_uuid:
            self.url_to_uuid[article_url] = uuid.uuid4().hex
        return self.url_to_uuid[article_url]

    def extract_urls(self, data):
        urls = []
        if isinstance(data, dict):
            for value in data.values():
                urls.extend(self.extract_urls(value))
        elif isinstance(data, list):
            for item in data:
                urls.extend(self.extract_urls(item))
        elif isinstance(data, str) and data.startswith("http"):
            urls.append(data)
        return urls

    def scrape(self):
        os.makedirs(self.articles_dir, exist_ok=True)
        articles_list = []
        try:
            with open(self.input_file, 'r') as file:
                data = json.load(file)

            urls = self.extract_urls(data)
            print(f"Extracted {len(urls)} URLs")

            for url in urls:
                try:
                    headers = {'User-Agent': 'Mozilla/5.0'}
                    response = requests.get(url, headers=headers, timeout=(5, 10))
                    if response.status_code == 200:
                        article = Article(url)
                        article.set_html(response.text)
                        article.parse()
                        article.nlp()
                        article_details = {
                            'url': url,
                            'date': datetime.now().strftime('%Y-%m-%d'),
                            'time': datetime.now().strftime('%H:%M:%S %Z'),
                            'title': article.title,
                            'body': article.text,
                            'summary': article.summary,
                            'keywords': article.keywords,
                            'image_url': article.top_image
                        }
                        articles_list.append(article_details)
                        self.save_article_as_json(article_details, self.articles_dir)
                        print(f"Saved article: {article.title}")
                    else:
                        print(f"Request failed with status code: {response.status_code}")
                except requests.exceptions.Timeout:
                    print(f"Timeout occurred for URL: {url}")
                except requests.exceptions.RequestException as e:
                    print(f"Request exception for URL {url}: {e}")
                except Exception as e:
                    print(e)
                    print('continuing...')
                time.sleep(1)
            return articles_list
        except Exception as e:
            raise Exception(f'Error in "Scraper.scrape()": {e}')

    def save_article_as_json(self, article, directory):
        article_id = self.generate_uuid_for_article(article['url'])
        article_with_id = {'id': article_id}
        article_with_id.update(article)

        sanitized_title = re.sub(r'[\\/*?:"<>|]', '_', article['title'])
        sanitized_title = re.sub(r'\s+', '_', sanitized_title)[:50]

        formatted_date = article['date'].replace('-', '') + '_' + article['time'].split(':')[0] + article['time'].split(':')[1]

        filename = f"{sanitized_title}_{formatted_date}.json"
        filepath = os.path.join(directory, filename)

        with open(filepath, 'w', encoding='utf-8') as file:
            json.dump(article_with_id, file, ensure_ascii=False, indent=4)

        print(f"Article saved: {filepath}")

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage: python scraper.py <input_file.json>")
        sys.exit(1)

    input_file = sys.argv[1]
    scraper = Scraper(input_file)
    articles = scraper.scrape()
