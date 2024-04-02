import os
import json
from langchain_text_splitters import RecursiveCharacterTextSplitter

class ChunkingModule:
    def __init__(self, articles_dir, output_file):
        self.articles_dir = articles_dir
        self.output_file = output_file

    def chunk_articles(self):
        chunked_data = []

        for filename in os.listdir(self.articles_dir):
            if filename.endswith('.json'):
                filepath = os.path.join(self.articles_dir, filename)
                with open(filepath, 'r') as file:
                    article = json.load(file)
                    text = article['body']

                    text_splitter = RecursiveCharacterTextSplitter(
                        chunk_size=1000,
                        chunk_overlap=200,
                        length_function=len,
                    )

                    chunks = text_splitter.split_text(text)

                    for i, chunk in enumerate(chunks):
                        chunk_id = f"{article['id']}_{i}"
                        chunked_data.append({
                            'id': chunk_id,
                            'article_id': article['id'],
                            'chunk': chunk,
                            'metadata': {
                                'title': article['title'],
                                'url': article['url'],
                                'date': article['date'],
                                'time': article['time']
                            }
                        })

        with open(self.output_file, 'w') as file:
            json.dump(chunked_data, file, indent=4)

        print(f"Chunked data saved to {self.output_file}")
        return chunked_data

def main(articles_dir, output_file):
    chunking_module = ChunkingModule(articles_dir, output_file)
    chunked_data = chunking_module.chunk_articles()
    return chunked_data

if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(description='Chunk articles into smaller pieces.')
    parser.add_argument('articles_dir', type=str, help='Path to the directory containing article JSON files')
    parser.add_argument('output_file', type=str, help='Name of the output JSON file')

    args = parser.parse_args()

    main(args.articles_dir, args.output_file)
