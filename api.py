from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from jinja2 import Template
from scraper_and_summarizer.summarizer import PegasusSummarizer
from scraper_and_summarizer.context import get_context
import requests
import datetime
import json
import os
from dotenv import load_dotenv


load_dotenv()

HOST = os.getenv("HOST")
PORT = os.getenv("PORT")

app = FastAPI()

# In-memory cache to store the markdown content
news_cache = get_context()

summarizer = PegasusSummarizer()

class NewsRequest(BaseModel):
    json_data: dict

def generate_markdown(news_data, lanaguage="English"):
    request_data = f"{news_cache.context}\n\n{str(news_data)}"
    body = {
        "model": "meta-llama3-8b",
        "messages": [{"role": "system", "content": json.dumps(request_data)}],
    }
    response = requests.post(url=os.getenv("BASE_URL"), json=body, timeout=60)
    print(response.text)
    if response.status_code != 200:
        raise HTTPException(status_code=500, detail="Failed to generate news")

    markdown_content = response.json()["choices"][0]["message"]["content"]
    if "<scratchpad>" in markdown_content:
        markdown_content = markdown_content.split("<scratchpad>")[1].split("</scratchpad>")[0]
    if lanaguage != "en":
        print("translate") #  TODO add translation
        
    with open(f"news_data/{lanaguage}/{datetime.datetime.now().strftime('%Y%m%d')}.md", "w") as f:
        f.write(markdown_content)
    return markdown_content

@app.post("/generate_news/")
async def generate_news():
    news_data = summarizer.scrape_and_summarize_ticker()
    markdown_content = generate_markdown(news_data)
    date_str = datetime.datetime.now().strftime("%d-%m-%Y")
    news_cache[date_str] = markdown_content
    return {"message": "News generated successfully"}

@app.get("/news/{language}/{date}", response_class=HTMLResponse)
async def get_news(language: str, date: str):
    if date not in news_cache:
        raise HTTPException(status_code=404, detail="News not found for this date")
    
    markdown_content = news_cache[date]
    with open('templates/news.html') as f:
        template = Template(f.read())
    rendered_html = template.render(language=language, date=date, content=markdown_content)
    return HTMLResponse(content=rendered_html)

if __name__ == "__main__":
    with open("news_data/English/20240805.json", "r", encoding="utf-8") as f:
        news_cache.context = json.loads(f.read())
    generate_markdown(news_cache.context, "English")
#    import uvicorn
#    uvicorn.run("api:app", host=HOST, port=int(PORT), reload=True)
