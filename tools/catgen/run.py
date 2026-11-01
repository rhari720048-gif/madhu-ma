import sys,os,time;sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
from core import ROOT
from clips import *
names=sys.argv[1].split(',');frames=sys.argv[2] if len(sys.argv)>2 else None
for n in names:
    D,loop,fn=CLIPS[n];N=int(round(D*FPS));os.makedirs(f'{ROOT}/cat/{n}',exist_ok=True)
    idx=[int(x) for x in frames.split(',')] if frames else range(N)
    t0=time.time()
    for i in idx:
        if os.path.exists(f'{ROOT}/cat/{n}/{i+1:03d}.webp') and not frames:continue
        im=render(n,i,N);im=im.resize((int(CW*.8),int(CH*.8)),Image.LANCZOS)
        im.save(f'{ROOT}/cat/{n}/{i+1:03d}.webp',quality=72,alpha_quality=85,method=4)
    print(n,N,'frames',round(time.time()-t0,1),'s',flush=True)
