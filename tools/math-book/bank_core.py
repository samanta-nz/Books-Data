"""Original grade-nine questions. Machine data stays locale-neutral; UI renders Persian."""
from fractions import Fraction as F
from math import isqrt
LEVELS=['آسان','متوسط','دشوار','درخشان']
CHAPTERS={1:'مجموعه‌ها',2:'عددهای حقیقی',3:'استدلال و اثبات در هندسه',4:'توان و ریشه',5:'عبارت‌های جبری',6:'خط و معادله‌های خطی',7:'عبارت‌های گویا',8:'حجم و مساحت'}
def frac(n,d=1):return str(F(n,d))
def roster(xs):return '{'+', '.join(map(str,sorted(set(xs))))+'}' if xs else '∅'
def pwr(x,n):return f'({x})^{n}'
class Bank:
 def __init__(self,chapter,v):self.chapter=chapter;self.v=v;self.rows=[]
 def add(self,level,objective,topic,prompt,answer,feedback,kind='short',options=None,check=None,aliases=None,mistakes=None,diagram=None,rubric=None):
  family=f'f{self.chapter:02d}-{len(self.rows)+1:02d}'
  self.rows.append(dict(id=family,family=family,grade=9,book='ریاضی نهم',chapter='فصل '+str(self.chapter)+': '+CHAPTERS[self.chapter],chapterNumber=self.chapter,lesson=topic,topic=topic,objective=objective,semanticKey=f'{self.chapter}:{objective}',level=level,difficulty=LEVELS[level-1],prompt=prompt,answer=str(answer),feedback=feedback,type=kind,options=options or [],check=check,aliases=aliases or [],mistakes=mistakes or {},diagram=diagram,rubric=rubric or [],variant=self.v,origin='تألیفی با داده‌های تازه؛ بازبینی مستقل پاسخ',sources=[]))
 def n(self,l,o,t,p,a,f,e,**kw):self.add(l,o,t,p,a,f,check={'kind':'number','expression':e},**kw)
 def s(self,l,o,t,p,xs,f,expressions=None):self.add(l,o,t,p,roster(xs),f,'set',check={'kind':'set','expressions':expressions or list(map(str,xs))})
 def m(self,l,o,t,p,answer,wrong,f,expression=None,option_exprs=None,fact=None):
  opts=[str(answer)]+list(map(str,wrong));assert len(opts)==4 and len(set(opts))==4,(o,opts)
  check={'kind':'expression-options','expression':expression,'options':option_exprs or opts} if expression is not None else {'kind':'reviewed-fact','fact':fact or o}
  self.add(l,o,t,p,answer,f,'mcq',opts,check=check,mistakes={str(x):'گزینهٔ انتخابی شرط «'+o+'» را رعایت نمی‌کند' for x in wrong})
 def tf(self,l,o,t,p,truth,f,fact=None):self.add(l,o,t,p,'درست' if truth else 'نادرست',f,'tf',check={'kind':'reviewed-fact','fact':fact or o})
 def essay(self,l,o,t,p,answer,rubric):self.add(l,o,t,p,answer,'پاسخ را با مرحله‌های راهنما مقایسه کن؛ ارزیابی خودکار قطعی ندارد.','essay',rubric=rubric,check={'kind':'manual-review'})
 def finish(self):
  assert len({q['semanticKey'] for q in self.rows})==len(self.rows)
  return self.rows
