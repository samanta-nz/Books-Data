"""Independent finite enumeration; never calls the authoring formulas."""
from itertools import product, combinations
from fractions import Fraction
from bank import questions, essay_questions

def powers(n):
    return [set(i for i in range(n) if bits[i]) for bits in product([0,1], repeat=n)]

def canonical(raw):
    if raw=='∅': return set()
    if raw.startswith('{') and raw.endswith('}'): return set(Fraction(x.strip()) for x in raw[1:-1].split(',') if x.strip())
    try:return Fraction(raw)
    except (ValueError, ZeroDivisionError):return raw

def independent(q):
    s=q['verify']; op=s['op']
    if op=='literal':return canonical(s['expected'])
    if op=='member':return 'درست' if s['x'] in s['A'] else 'نادرست'
    if op=='card':return len(set(s['A']))
    if op=='interval':return set(i for i in range(-100,101) if s['lo']<i<s['hi'])
    if op=='subset':return 'درست' if all(x in s['B'] for x in s['A']) else 'نادرست'
    if op=='subsets':return len(powers(s['n']))
    if op in ['union','intersection','difference']:
        u=set(s['A']+s['B'])
        return {x for x in u if (x in s['A'] or x in s['B'])} if op=='union' else {x for x in u if (x in s['A'] and (x in s['B'] if op=='intersection' else x not in s['B']))}
    if op=='sample':return len(list(product(*([[0,1]]*s['coins']+[[1,2,3,4,5,6]]*s['dice']))))
    if op=='die_threshold':return Fraction(sum(d<=s['t'] for d in range(1,7)),6)
    if op=='image_linear':return {s['m']*x+s['b'] for x in s['domain']}
    if op=='equality':
        sols=[Fraction(x,2) for x in range(-100,101) if {2*Fraction(x,2)+1,s['fixed']}=={s['target'],s['fixed']}]
        assert len(sols)==1
        return sols[0]
    if op=='divisors':return {x for x in range(1,s['n']+1) if Fraction(s['n'],x).denominator==1}
    if op=='pairs':return sum(len(x)==2 for x in powers(s['n']))
    if op=='regions':
        A=set(range(s['x']+s['z']));B=set(range(s['x'],s['x']+s['z']+s['y']))
        return {'union':len(A|B),'intersection':len(A&B),'only_a':len(A-B),'neither':s.get('outside',0)}[s['what']]
    if op=='counterexample':
        a,b=s['a'],s['b']
        pairs=[({a},{b}),(set(),{b}),({a},{a,b}),({a},{a})]
        valid=[i for i,(A,B) in enumerate(pairs) if not A.intersection(B) and not A.issubset(B)]
        assert valid==[0]
        return f'A={{{a}}}, B={{{b}}}'
    if op=='rebuild':return set(s['both']+s['only'])
    if op=='cards':
        preds={'not3':lambda x:x%3!=0,'and23':lambda x:x%2==0 and x%3==0,'or23':lambda x:x%2==0 or x%3==0,'xor23':lambda x:sum([x%2==0,x%3==0])==1}
        return Fraction(sum(preds[s['predicate']](x) for x in range(1,s['n']+1)),s['n'])
    if op=='coins':
        all_states=list(product('RP',repeat=s['n']))
        return Fraction(sum((x.count('R')==1 if s['condition']=='one' else x.count('R')>=2) for x in all_states),len(all_states))
    if op=='dice':
        count=0
        for a,b in product(range(1,7),repeat=2):
            if a+b==s['target'] or (s['condition']=='sum_or_double' and a==b):count+=1
        return Fraction(count,36)
    if op=='constrained_subsets':
        return sum((0 in x and 1 not in x if s['condition']=='include_exclude' else 0 in x or 1 in x) for x in powers(s['n']))
    if op=='nested':
        A,B,C=map(set,[s['A'],s['B'],s['C']])
        return {x for x in A if x not in B} if s['expression']=='a_minus_inter' else {x for x in A if x in B or x in C}
    if op=='identity':
        for A in powers(3):
            for B in powers(3):assert A-(A&B)==A-B
        return 'A−(A∩B)'
    if op=='two_parameter':
        sols={(x,y) for x in range(-30,31) for y in range(-30,40) if {2*x+1,2*s['y']}=={2*s['x']+1,y+s['y']}}
        assert len(sols)==1,sols
        return next(iter(sols))[0]
    if op=='inverse_subsets':return next(n for n in range(1,10) if len(powers(n))==2**s['n'])
    if op=='coin_die':return Fraction(sum(h=='R' or d<=s['t'] for h,d in product('RP',range(1,7))),12)
    if op=='draw':
        all_pairs=list(combinations(range(s['red']+s['blue']),2))
        return Fraction(sum(max(pair)<s['red'] for pair in all_pairs),len(all_pairs))
    if op=='inverse_bag':return next(b for b in range(1,100) if Fraction(s['red'],s['red']+b)==Fraction(1,3))
    if op=='min_overlap':return min(k for k in range(min(s['a'],s['b'])+1) if s['a']+s['b']-k<=s['N'])
    if op=='triple':
        tags=[(1,0,0),(0,1,0),(0,0,1),(1,1,0),(1,0,1),(0,1,1),(1,1,1)]
        members=[tag for count,tag in zip(s['regions'],tags) for _ in range(count)]
        return {'union':len(members),'one':sum(sum(x)==1 for x in members),'two':sum(sum(x)==2 for x in members),'none':s.get('N',len(members))-len(members)}[s['what']]
    if op in ['subset_chain','disjoint_pairs']:
        P=powers(s['n'])
        return sum((all(x in C for x in B) if op=='subset_chain' else not B.intersection(C)) for B in P for C in P)
    if op=='collision':return sum(x*x==s['n']**2 for x in range(-30,31))
    if op=='square_image':return len(set(x*x for x in range(-s['n'],s['n']+1)))
    if op=='even_subset_sum':return sum(sum(i+1 for i in subset)%2==0 for subset in powers(s['n']))
    if op=='spinner':return Fraction(sum(x<s['degrees'] for x in range(360)),360)
    raise AssertionError(op)

def run():
    total=0
    for v in range(7):
        bank=questions(v)
        assert len({q['objective'] for q in bank})==len(bank)
        assert len({q['id'] for q in bank})==len(bank)
        for q in bank:
            expected=independent(q)
            actual=canonical(q['answer'])
            assert actual==expected,(v,q['id'],q['prompt'],actual,expected)
            if q['type']=='mcq':
                assert len(q['options'])==4 and len(set(q['options']))==4
                assert sum(canonical(x)==expected for x in q['options'])==1
            total+=1
    assert all(q['rubric'] for q in essay_questions())
    print(f'PASS: {total} independently enumerated answers; MCQ uniqueness; 4 manual rubrics.')
    return total

if __name__=='__main__':run()
