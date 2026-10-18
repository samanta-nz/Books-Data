"""Check the final-exam blueprint, exact numeric answers and symbolic worked keys."""
import json,re
from pathlib import Path
from collections import Counter
import sympy as sp
from sympy.parsing.sympy_parser import parse_expr,standard_transformations,implicit_multiplication_application
from final_questions import questions,MARKS
from verify_book import verify,expression

def key_expression(s):
 s=s.strip().replace('−','-').replace('²','**2').replace('³','**3').replace('π','pi')
 s=re.sub(r'√(\d+)',r'sqrt(\1)',s)
 return parse_expr(s,local_dict={'x':sp.Symbol('x',real=True),'y':sp.Symbol('y',real=True)},transformations=standard_transformations+(implicit_multiplication_application,))

def run(write=True):
 counts=Counter();chapter_marks=None
 for level in range(1,5):
  for v in range(1,7):
   qs=questions(level,v);assert len(qs)==38 and len({q['id'] for q in qs})==38
   assert sum(q['marks'] for q in qs)==20
   for g,marks in enumerate(MARKS,1):assert sum(q['marks'] for q in qs if q['group']==g)==marks
   m=Counter()
   for q in qs:
    m[q['chapterNumber']]+=q['marks'];pair=(q['group'],q['part'])
    assert q['marks']>0 and q['marks']*4==int(q['marks']*4)
    if q['type'] in ('short','set'):verify(q);counts['exactAutomaticAnswers']+=1
    elif q['type']=='tf':
     expected='درست' if (v%2==1 if pair[1]!=2 else v%2==0) else 'نادرست'
     assert q['answer']==expected,(pair,v,q['answer']);counts['logicalAnswersReviewed']+=1
    elif q['type']=='mcq':
     assert len(q['options'])==len(set(q['options']))==4 and q['options'].count(q['answer'])==1
     assert q['answer']=={1:'√x',2:'(4/3)πR³',3:str(4+v+level),4:'دایره'}[q['part']]
     counts['logicalAnswersReviewed']+=1
    elif q['type']=='text':
     assert q['answer']=={(2,4):'طول‌ها',(4,2):'∈',(15,1):'مخروط'}[pair];counts['logicalAnswersReviewed']+=1
    else:
     assert q['type']=='essay' and sum(x['marks'] for x in q['rubric'])==q['marks']
     cert=q['check'].get('expression')
     if pair in [(8,2),(8,3),(9,1),(9,2),(12,2),(12,3)]:
      sample=q['answer'].split('؛')[0];got=key_expression(sample)
      assert sp.simplify(expression(cert)-got)==0,(pair,q['answer'],cert)
      counts['symbolicWorkedKeys']+=1
     if pair==(9,3):
      k,a,target=map(int,re.search(r'−(\d+)x\+(\d+)≤(\d+)',q['prompt']).groups())
      assert q['answer'].replace('−','-')=='x≥'+str(sp.Rational(a-target,k));counts['symbolicWorkedKeys']+=1
     if pair==(11,1):
      rhs1,rhs2=map(int,re.search(r'2x\+y=(\d+) و x−y=(-?\d+)',q['prompt']).groups());x,y=sp.symbols('x y')
      sol=sp.solve([2*x+y-rhs1,x-y-rhs2],[x,y]);sx,sy=map(int,re.search(r'x=(-?\d+) و y=(-?\d+)',q['answer']).groups())
      assert sol[x]==sx and sol[y]==sy;counts['symbolicWorkedKeys']+=1
     if pair==(13,1):
      p,d=re.search(r'تقسیم (.+?) بر ([^ ]+) را',q['prompt']).groups();quot,rem=sp.div(key_expression(p),key_expression(d),sp.Symbol('x',real=True));qbody,rb=re.search(r'خارج‌قسمت (.+?)؛ باقی‌مانده (\d+)؛',q['answer']).groups()
      assert sp.simplify(quot-key_expression(qbody))==0 and rem==int(rb);counts['symbolicWorkedKeys']+=1
     if pair==(14,1):
      coef=int(re.search(r'(\d+)π',q['answer']).group(1));assert sp.simplify(expression(cert)-coef*sp.pi)==0;counts['symbolicWorkedKeys']+=1
     if pair==(15,2):
      value=int(re.search(r'حجم (\d+)',q['answer']).group(1));assert sp.simplify(expression(cert)-value)==0;counts['symbolicWorkedKeys']+=1
     counts['manualRubricsReviewed']+=1
   if chapter_marks is None:chapter_marks=dict(m)
   assert chapter_marks==dict(m)
 report=dict(variants=24,mainQuestionsPerPaper=16,partsPerPaper=38,totalMarks=20,mainQuestionMarks=MARKS,chapterMarks=chapter_marks,checks=dict(counts),manualPolicy='هیچ برهان، رسم یا پاسخ تشریحی با ادعای تصحیح ماشینی قطعی نمره نمی‌گیرد؛ نمرهٔ راه‌حل با خودارزیابی مرحله‌ای و برچسب نیاز به تأیید دبیر ثبت می‌شود.',blueprintSource='هماهنگ کشوری ریاضی نهم، نوبت صبح ۱۴۰۴/۰۳/۰۴')
 if write:
  root=Path(__file__).resolve().parents[2]/'reports/math-book';(root/'final-verification.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
  path=root/'research/final-blueprint.json';d=json.loads(path.read_text());d['chapterMarks']=chapter_marks;d['sourceClassificationNote']='توزیع فصل‌ها از دسته‌بندیِ بخش‌های همین فرم استخراج شده؛ جدول همیشگی همهٔ سال‌ها نیست.';path.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n')
 print('PASS: 24 final papers, exactly 20 marks,',dict(counts),flush=True)
 return report
if __name__=='__main__':run()
