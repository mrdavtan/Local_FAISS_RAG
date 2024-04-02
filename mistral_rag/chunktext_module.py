import os
import json
import spacy

class ChunkingModule:
    def __init__(self, articles_dir, output_dir):
        self.articles_dir = articles_dir
        self.output_dir = output_dir
        self.nlp = spacy.load("en_core_web_sm")

    def chunk_articles(self):
        chunked_data = []
        for filename in os.listdir(self.articles_dir):
            if filename.endswith('.json'):
                filepath = os.path.join(self.articles_dir, filename)
                with open(filepath, 'r') as file:
                    article = json.load(file)
                    text = article['body']
                    doc = self.nlp(text)
                    chunks = [sent.text.strip() for sent in doc.sents]
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

        os.makedirs(self.output_dir, exist_ok=True)
        output_file = os.path.join(self.output_dir, 'chunked_text_data.json')
        with open(output_file, 'w') as file:
            json.dump(chunked_data, file, indent=4)

        print(f"Chunked data saved to {output_file}")
        return chunked_data

def main(articles_dir, output_dir):
    chunking_module = ChunkingModule(articles_dir, output_dir)
    chunked_data = chunking_module.chunk_articles()
    return chunked_data

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description='Chunk articles into smaller pieces.')
    parser.add_argument('articles_dir', type=str, help='Path to the directory containing article JSON files')
    parser.add_argument('output_dir', type=str, help='Name of the output directory')
    args = parser.parse_args()

    main(args.articles_dir, args.output_dir)
