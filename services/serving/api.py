# services/serving/api.py
import joblib
from fastapi import FastAPI
from pydantic import BaseModel
import redis


app = FastAPI()


r = redis.Redis(host='redis', port=6379, db=0)


MODEL_PATH = '/data/models/item_sim.pkl'
model = None


class Req(BaseModel):
user_id: str
recently_viewed: list = []


@app.on_event('startup')
def load_model():
global model
model = joblib.load(MODEL_PATH)
print('Model loaded')


@app.post('/recommend')
def recommend(req: Req):
cache_key = f"rec:{req.user_id}"
cached = r.get(cache_key)
if cached:
return {'user_id': req.user_id, 'recommendations': eval(cached)}


# naive: for each recently viewed, aggregate similar items
scores = {}
for pid in req.recently_viewed:
if pid not in model.index:
continue
sims = model.loc[pid]
for other, score in sims.items():
scores[other] = scores.get(other, 0) + float(score)


# exclude items user already saw
for pid in req.recently_viewed:
scores.pop(pid, None)


recs = sorted(scores.items(), key=lambda x: x[1], reverse=True)[:10]
rec_ids = [r[0] for r in recs]


r.set(cache_key, str(rec_ids), ex=60)
return {'user_id': req.user_id, 'recommendations': rec_ids}
