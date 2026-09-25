from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

app = FastAPI(title="Batch Sentiment Analysis")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

analyzer = SentimentIntensityAnalyzer()

class SentimentRequest(BaseModel):
    sentences: list[str]

def classify(sentence: str) -> str:
    compound = analyzer.polarity_scores(sentence)["compound"]
    if compound >= 0.05:
        return "happy"
    if compound <= -0.05:
        return "sad"
    return "neutral"

@app.post("/sentiment")
async def batch_sentiment(payload: SentimentRequest):
    return {
        "results": [
            {"sentence": sentence, "sentiment": classify(sentence)}
            for sentence in payload.sentences
        ]
    }

@app.get("/")
async def root():
    return {"message": "Batch sentiment API is running"}
