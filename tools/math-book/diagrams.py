"""Original inline SVG diagrams; labels are converted to Persian by the HTML builder."""
from html import escape

def line_svg(m,c):
 xmin,xmax=-4,4;ymin,ymax=-6,10
 def xy(x,y):return (38+(x-xmin)*34,244-(y-ymin)*13)
 out=['<figure><svg class="coordinate-plot" viewBox="0 0 360 280" role="img" aria-label="نمودار خط با محورهای مدرج">']
 for x in range(xmin,xmax+1):
  p,q=xy(x,ymin),xy(x,ymax);out.append(f'<path d="M{p[0]},{p[1]} L{q[0]},{q[1]}" stroke="#d8dde4"/>')
 for y in range(ymin,ymax+1,2):
  p,q=xy(xmin,y),xy(xmax,y);out.append(f'<path d="M{p[0]},{p[1]} L{q[0]},{q[1]}" stroke="#d8dde4"/>')
 x0,y0=xy(0,0)
 out.append(f'<path d="M38,{y0} H325 M{x0},245 V25" stroke="#334e60" stroke-width="2"/>')
 for x in range(xmin,xmax+1):
  px,py=xy(x,0);out.append(f'<text x="{px}" y="{py+19}" text-anchor="middle">{x}</text>')
 for y in range(ymin,ymax+1,2):
  if y:
   px,py=xy(0,y);out.append(f'<text x="{px-9}" y="{py+5}" text-anchor="end">{y}</text>')
 points=[]
 for x in [xmin+i/100 for i in range((xmax-xmin)*100+1)]:
  y=m*x+c
  if ymin<=y<=ymax:points.append(xy(x,y))
 out.append('<polyline fill="none" stroke="#67518f" stroke-width="3" points="'+' '.join(f'{x:.2f},{y:.2f}' for x,y in ([points[0],points[-1]] if points else []))+'"/>')
 out.append('<text x="335" y="'+str(y0-8)+'">x</text><text x="'+str(x0+9)+'" y="20">y</text></svg><figcaption>محورها مدرج‌اند؛ همهٔ فاصله‌ها در هر محور مقیاس یکسان دارند.</figcaption></figure>')
 return ''.join(out)

def triangle_svg(labels=('A','B','C'),extra=''):
 return '<figure><svg class="geometry-plot" viewBox="0 0 360 230" role="img" aria-label="طرح شماتیک مثلث"><path d="M180,25 L35,195 L325,195 Z" fill="#efeaf6" stroke="#67518f" stroke-width="3"/><text x="176" y="19">'+escape(labels[0])+'</text><text x="13" y="208">'+escape(labels[1])+'</text><text x="332" y="208">'+escape(labels[2])+'</text>'+extra+'</svg><figcaption>شکل شماتیک است؛ داده‌های متن مبنای حل‌اند.</figcaption></figure>'

def solid_svg(kind):
 if kind=='sphere':
  body='<circle cx="160" cy="110" r="80" fill="#e7edf8" stroke="#67518f" stroke-width="3"/><ellipse cx="160" cy="110" rx="80" ry="24" fill="none" stroke="#67518f" stroke-dasharray="5 4"/><path d="M160,110 H240" stroke="#376553" stroke-width="3"/><text x="196" y="101">r</text>'
 elif kind=='cone':
  body='<path d="M60,180 L160,20 L260,180" fill="#e7edf8" stroke="#67518f" stroke-width="3"/><ellipse cx="160" cy="180" rx="100" ry="27" fill="#e7f2ea" stroke="#67518f" stroke-width="3"/><path d="M160,20 V180 H260" fill="none" stroke="#376553" stroke-dasharray="5 4"/><text x="168" y="100">h</text><text x="210" y="171">r</text>'
 else:
  body='<path d="M50,160 L130,210 L270,160 L185,115 Z M50,160 L160,15 L130,210 M160,15 L270,160 M160,15 L185,115" fill="#efeaf6" stroke="#67518f" stroke-width="2"/><path d="M160,15 V162" stroke="#376553" stroke-dasharray="5 4"/><text x="166" y="95">h</text>'
 return '<figure><svg class="geometry-plot" viewBox="0 0 320 245" role="img" aria-label="شکل شماتیک حجم">'+body+'</svg><figcaption>شکل شماتیک است؛ اندازه‌های متن را به کار ببر.</figcaption></figure>'
