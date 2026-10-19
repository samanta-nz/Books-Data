"""Check the final changed pages at a narrow mobile viewport with offline assets."""
import asyncio, hashlib, json
from pathlib import Path
from playwright.async_api import async_playwright
from test_book import serve, url, persian

ROOT=Path(__file__).resolve().parents[2]
REPORT=ROOT/'reports/math-book/qa-fix-20261019'

async def main():
    baseline=json.loads((REPORT/'comprehensive-browser-inputs.json').read_text())
    changed=[p for p,h in baseline.items() if hashlib.sha256((ROOT/p).read_bytes()).hexdigest()!=h]
    errors=[]
    async with async_playwright() as pw:
        browser=await pw.chromium.launch(executable_path='/usr/bin/chromium',args=['--no-sandbox'])
        ctx=await browser.new_context(viewport={'width':320,'height':800},color_scheme='dark')
        await serve(ctx)
        p=await ctx.new_page()
        p.on('pageerror',lambda e:errors.append(str(e)))
        for path in changed:
            await p.goto(url(path.split('/C905/')[1]))
            await p.evaluate('async()=>{await Promise.all([400,500,700].map(w=>document.fonts.load(w+" 16px Vazir")));await document.fonts.ready}')
            assert await p.evaluate('document.documentElement.scrollWidth<=innerWidth'),path
            await persian(p)
        await p.goto(url('N10.1/TAB05-brilliant-06.html'))
        await p.screenshot(path=str(REPORT/'final-corrected-mobile.png'),full_page=True)
        await browser.close()
    assert not errors
    (REPORT/'mobile-tests.json').write_text(json.dumps(dict(verdict='AUTHOR_PASS',viewportWidth=320,changedPages=len(changed),allChangedPagesWithinViewport=True,persianDigits=True,loadedVazirWeights=[400,500,700],errors=errors,deviceRun=False),indent=2)+'\n')
    print('PASS narrow mobile: all',len(changed),'changed pages; no overflow or non-Persian visible digits')

if __name__=='__main__':asyncio.run(main())
