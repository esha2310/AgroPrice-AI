"""Build four portable HTML pages with embedded images and frozen data."""
from pathlib import Path
import json,base64
R=Path(__file__).resolve().parent
ASSETS=[('__PADDY__','paddy.jpg'),('__LANDSCAPE__','landscape.jpg'),('__LEAF__','leaf-botanical.svg'),('__RICE_ART__','rice-botanical.svg'),('__LENTILS_ART__','lentils-botanical.svg'),('__FLOUR_ART__','flour-botanical.svg'),('__OIL_ART__','oil-botanical.svg')]
def compile_page(text):
 variables=[]
 for key,file in ASSETS:
  b=base64.b64encode((R/'assets'/file).read_bytes()).decode();url=('data:image/svg+xml;base64,' if file.endswith('.svg') else 'data:image/jpeg;base64,')+b
  css="url('"+key+"')";name='--asset-'+file.split('.')[0]
  if css in text:text=text.replace(css,'var('+name+')');variables.append(name+":url('"+url+"')")
  text=text.replace(key,url)
 return text.replace('</style>',':root{'+ ';'.join(variables)+'}</style>',1)
data=json.loads((R/'data/dashboard.json').read_text(encoding='utf-8'))
text=(R/'frontend/site.html').read_text(encoding='utf-8').replace('__DATA__',json.dumps(data,ensure_ascii=False,separators=(',',':')).replace('<','\\u003c'))
text=compile_page(text)
(R/'index.html').write_text(text,encoding='utf-8')
(R/'dashboard.html').write_text(text.replace('data-page="welcome"','data-page="workspace"',1),encoding='utf-8')
for name in ['login','signup']:(R/(name+'.html')).write_text(compile_page((R/'frontend'/(name+'.html')).read_text(encoding='utf-8')),encoding='utf-8')
print('Built index.html, login.html, signup.html and dashboard.html. No external asset dependency.')
