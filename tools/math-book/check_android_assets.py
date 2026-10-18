"""Merge and byte-check the current real grade-nine HTML and theme assets."""
from pathlib import Path
import json,os,subprocess
from urllib.parse import urlparse

ROOT=Path(__file__).resolve().parents[2];REPORT=ROOT/'reports/math-book';APP=Path('/workspace/hamyar-math-app')
def main():
 env=os.environ.copy();env['JAVA_HOME']='/workspace/toolchains/jdk-21.0.12.1';env['ANDROID_HOME']='/workspace/android-sdk';env['ANDROID_USER_HOME']='/workspace/runtime-home/.android';env['PATH']=env['JAVA_HOME']+'/bin:'+env['PATH']
 proxy=urlparse(env.get('HTTPS_PROXY',''));options=env.get('JAVA_TOOL_OPTIONS','')+' -Djavax.net.ssl.trustStore=/etc/ssl/certs/java/cacerts'
 if proxy.hostname:
  for scheme in ['https','http']:options+=' -D'+scheme+'.proxyHost='+proxy.hostname+' -D'+scheme+'.proxyPort='+str(proxy.port or 8080)
 env['JAVA_TOOL_OPTIONS']=options
 with (REPORT/'android-assets-current.log').open('w') as log:subprocess.run(['./gradlew','--no-daemon','--max-workers=2',':hamyar-app:mergeP09DebugAssets'],cwd=APP,env=env,stdout=log,stderr=subprocess.STDOUT,check=True)
 matches=list((APP/'apps/student/build/intermediates').rglob('math/c905/practice/N10.1/TAB05.html'));assert matches
 assets=max(matches,key=lambda p:p.stat().st_mtime).parents[4]
 routes=json.loads((REPORT/'routes.json').read_text())['routes'];themes=0
 for route in routes:
  source=ROOT/route['bucketKey'];assert source.read_bytes()==(assets/route['assetPath']).read_bytes()
  theme=source.parent/'assets/css/theme'/(source.stem+'.theme.css')
  assert theme.read_bytes()==(assets/Path(route['assetPath']).parent/'assets/css/theme'/theme.name).read_bytes();themes+=1
 for name in ['books-menu.json','math-practice-routes.json']:assert (APP/'grades/g09/src/main/assets/content'/name).read_bytes()==(assets/'content'/name).read_bytes()
 report=json.loads((REPORT/'android-tests.json').read_text());assert report['total']==154 and all(not m['failures'] and not m['errors'] for m in report['modules'].values())
 report.update(mergedHtmlFiles=len(routes),byteComparisons=len(routes),mergedThemeFiles=themes,menuAndManifestMatch=True,currentAssetsMerge='passed',unitTestsLog='android-tests.log',currentAssetsLog='android-assets-current.log',deviceRun=False)
 (REPORT/'android-tests.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n');print('PASS current merge: HTML',len(routes),'themes',themes,'menu/manifest; existing 154 native tests remain recorded separately.')
if __name__=='__main__':main()
