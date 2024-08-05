from transformers import PegasusTokenizer, PegasusForConditionalGeneration
from pathlib import Path
from bs4 import BeautifulSoup
from datetime import datetime
import requests
import json
from dotenv import load_dotenv

load_dotenv()

class PegasusSummarizer:
    def __init__(
        self, model_name="human-centered-summarization/financial-summarization-pegasus",
        url="https://ca.finance.yahoo.com/news/free-streaming-channels-have-become-sleeping-giants-as-netflix-max-others-hike-prices-154745358.html",
    ):
        self.model_name = model_name or "human-centered-summarization/financial-summarization-pegasus"
        self.tokenizer = PegasusTokenizer.from_pretrained(self.model_name)
        self.model = PegasusForConditionalGeneration.from_pretrained(self.model_name)
        self.url = url or "https://ca.finance.yahoo.com/news/free-streaming-channels-have-become-sleeping-giants-as-netflix-max-others-hike-prices-154745358.html"
        self.exclude_list = ["maps", "policies", "preferences", "accounts", "support", "setprefs"]
        self.save_dir = "news_data/"
        self.search_url = ""
        self.ticker_dict = {}
        self.arcitcle_dict = {}
        self.context = {}

    @property
    def monitored_tickers(self):
        return ["TSLA", "BTC", "ETH", "SOL", "COMAI", "CommuneAI", "TAO", "Bittensor"]

    def set_search_url(self, ticker):
        self.search_url = f"https://www.google.com/search?q=yahoo+finance+{ticker}&tbm=nws"
        return self.search_url

    def get_url_data(self, url):
        request_data = requests.get(url)
        soup = BeautifulSoup(request_data.text, 'html.parser')
        paragraphs = soup.find_all('p')
        return self.process_data(paragraphs)

    def process_data(self, paragraphs):
        text = [paragraph.text for paragraph in paragraphs]
        words = " ".join(text).split(" ")[:300]
        return " ".join(words)

    def summarize(self, text, model, tokenizer):
        input_ids = tokenizer.encode(text, return_tensors="pt")
        output = model.generate(input_ids, max_length=55, num_beams=5, early_stopping=True)
        return tokenizer.decode(output[0], skip_special_tokens=True)

    def scrape_and_summarize(self, url, model, tokenizer):
        paragraphs = self.get_url_data(url)
        article = self.process_data(paragraphs)
        return self.summarize(article, model, tokenizer)

    def search_for_ticker(self):
        soup = BeautifulSoup(requests.get(self.search_url).text, 'html.parser')
        atags = soup.find_all('a')
        return [link["href"] for link in atags]

    def process_url_data(self, url_links):
        url_list = []
        for link in url_links:
            if all(exclude not in link for exclude in self.exclude_list) and "?q=" in link:
                url = link.split("?q=")[1]
                if url.startswith("http"):
                    url_list.append(url.split("&")[0])
        return url_list

    def get_ticker_urls(self):
        self.ticker_dict = {}
        for ticker in self.monitored_tickers:
            self.set_search_url(ticker)
            search_result = self.search_for_ticker()
            urls = self.process_url_data(search_result)
            if ticker not in self.ticker_dict:
                self.ticker_dict[ticker] = {}
            self.ticker_dict[ticker]["urls"] = urls
        return self.ticker_dict

    def scrape_and_summarize_ticker(self, language="English"):
        self.ticker_dict = self.get_ticker_urls()
        self.article_dict = {}
        not_searched = []
        for ticker, url_dict in self.ticker_dict.items():
            if ticker not in self.article_dict.keys():
                self.article_dict[ticker] = {}
            for urls in url_dict.values():
                for url in urls:
                    self.article_dict[ticker][url] = {"url": url}
                    if url.startswith("http"):
                        paragraph = self.get_url_data(url)
                        if paragraph.startswith("Thank you for your patience"):
                            continue
                        self.article_dict[ticker][url]["article"] = paragraph
                        summary = self.summarize(paragraph, self.model, self.tokenizer)
                        self.article_dict[ticker][url]["summary"] = summary
                    else:
                        not_searched.append(url)
        self.article_dict["not_searched"] = not_searched
        return self.article_dict

    def save_articles(self, article_dict, language):
        article_dictionary = article_dict or self.arcitcle_dict
        timestamp = datetime.now().strftime("%Y%m%d")
        file_path = Path(f'{self.save_dir}{language}/{timestamp}.json')
        file_path.write_text(json.dumps(article_dictionary, indent=4), encoding='utf-8')

    def get_articles(self, date_ymd):
        save_path = Path(f"{self.save_dir}{date_ymd}.json")
        return save_path.read_text(encoding='utf-8')

    def run(self, language="English"):
        self.get_ticker_urls()
        self.scrape_and_summarize_ticker(language)
        
if __name__ == "__main__":
    summarizer = PegasusSummarizer()
    summarizer.run()
    
    
    
