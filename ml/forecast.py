"""Inspect bundled point forecasts; no model deserialization needed."""
import argparse,json
from pathlib import Path
p=argparse.ArgumentParser();p.add_argument('--commodity',choices=['rice','lentils','flour','oil'],default='rice');p.add_argument('--market',default='Barisal');a=p.parse_args()
d=json.loads((Path(__file__).resolve().parents[1]/'data/dashboard.json').read_text(encoding='utf-8'))
for s in d['series']:
 if s['commodity']==a.commodity and a.market.lower() in s['market'].lower():print(json.dumps({k:s[k] for k in ['label','market','unit','forecast_date','forecasts','forecast_reason','selected_model']},indent=2,ensure_ascii=False))
