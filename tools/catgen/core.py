import numpy as np, cv2, math, os
ROOT=os.path.abspath(os.path.join(os.path.dirname(__file__),'..','..'))
from PIL import Image, ImageDraw, ImageFont
FONT=next((f for f in ['/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf','C:/Windows/Fonts/arialbd.ttf','/System/Library/Fonts/Supplemental/Arial Bold.ttf'] if os.path.exists(f)),'DejaVuSans-Bold.ttf')
raw=np.asarray(Image.open(os.path.join(ROOT,'cat','front.png')).convert('RGBA')).astype(np.float32)/255
Hs,Ws=raw.shape[:2]; OX,OY=50,80; CW,CH=Ws+2*OX,Hs+OY+12
def fix_fringe(im):
    a=im[...,3].copy();rgb=im[...,:3]
    m=(a>.5).astype(np.uint8);dt=cv2.distanceTransform(m,cv2.DIST_L2,3)
    core=(dt>7).astype(np.float32)
    num=cv2.GaussianBlur(rgb*core[...,None],(0,0),5);den=cv2.GaussianBlur(core,(0,0),5)[...,None]
    blur=num/np.maximum(den,1e-4)
    k=np.clip(1-dt/5,0,1)[...,None]*.9
    out=im.copy();out[...,:3]=rgb*(1-k)+blur*k
    out[...,3]=np.clip((a-.1)/.9,0,1);return out
S0=fix_fringe(raw)
ss=lambda a,b,x:(lambda t:t*t*(3-2*t))(np.clip((x-a)/(b-a),0,1))
EDGE=(lambda a:4*a*(1-a))(cv2.GaussianBlur(S0[...,3],(0,0),7))
EDGE=np.clip(EDGE*1.6,0,1)
EYES=[dict(cx=110,cy=165,rx=37,ry=33),dict(cx=244,cy=165,rx=37,ry=31)]
_m=np.zeros((Hs,Ws),np.uint8)
for _e in EYES:cv2.ellipse(_m,(_e['cx'],_e['cy']),(_e['rx']+7,_e['ry']+9),0,0,360,255,-1)
_inp=cv2.inpaint((S0[...,:3]*255).astype(np.uint8),_m,11,cv2.INPAINT_TELEA).astype(np.float32)/255
_bl=cv2.GaussianBlur(_inp,(0,0),3.5);_mf=cv2.GaussianBlur(_m.astype(np.float32)/255,(0,0),2.5)[...,None]
PLATE=_inp*(1-_mf)+_bl*_mf
PLATE=PLATE+(cv2.GaussianBlur(np.random.RandomState(3).randn(Hs,Ws).astype(np.float32),(0,0),1.1)*.018)[...,None]
BASE=(180,470);NECK=(180,285);EARL=(88,105);EARR=(272,105);TAILB=(292,395)
def rot(x,y,cx,cy,deg):
    r=np.deg2rad(deg);c,s=np.cos(r),np.sin(r);dx,dy=x-cx,y-cy
    return cx+dx*c-dy*s,cy+dx*s+dy*c
def F(u,v,p,t,T):
    wh=ss(305,245,v);wl=ss(135,70,v)*ss(170,100,u);wr=ss(135,70,v)*ss(190,260,u)
    wt=ss(280,325,u)*ss(255,310,v)*(1-ss(425,455,v))
    x,y=u.copy(),v.copy()
    x=BASE[0]+(x-BASE[0])*p['sx'];y=BASE[1]+(y-BASE[1])*(p['sy']+p['breath']*.011)*1.0 if False else BASE[1]+(y-BASE[1])*(p['sy']+p['breath']*.011)
    x,y=rot(x,y,NECK[0],NECK[1]+(0),p['head']*wh)
    x=x+p['hdx']*wh;y=y+p['hdy']*wh
    for w,b,a in((wl,EARL,p['earL']),(wr,EARR,p['earR'])):
        x2,y2=rot(x,y,b[0],b[1],a*w);x,y=x2,y2
    x2,y2=rot(x,y,TAILB[0],TAILB[1],p['tail']*wt);x,y=x2,y2
    lean=p['lean']*np.clip((BASE[1]-v)/470,0,1)**1.3;x=x+lean
    y=y-p['jump']
    ph=2*np.pi*t/T;fa=p.get('flut',1.0)
    wf=EDGE[np.clip(v.astype(int),0,Hs-1),np.clip(u.astype(int),0,Ws-1)]*(u>=0)*(u<Ws)*(v>=0)*(v<Hs)
    amp=(0.35+2.3*wf)*fa
    x=x+amp*(np.sin(u*.045+v*.02+ph*2)+.6*np.sin(v*.09-ph*3))
    y=y+amp*.8*(np.sin(v*.05-u*.03+ph*3)+.5*np.sin(u*.11+ph*2))
    return x,y
GX,GY=np.meshgrid(np.arange(CW,dtype=np.float32)-OX,np.arange(CH,dtype=np.float32)-OY)
def warp(Sim,p,t,T):
    u,v=GX.copy(),GY.copy()
    for _ in range(4):
        fx,fy=F(u,v,p,t,T);u=GX-(fx-u);v=GY-(fy-v)
    P=Sim.copy();P[...,:3]*=P[...,3:4]
    o=cv2.remap(P,u.astype(np.float32),v.astype(np.float32),cv2.INTER_CUBIC,borderMode=cv2.BORDER_CONSTANT,borderValue=0)
    a=np.clip(o[...,3:4],0,1);rgb=np.where(a>1e-3,o[...,:3]/np.maximum(a,1e-3),0)
    return np.dstack([np.clip(rgb,0,1),a])
def fp(x,y,p,t,T):
    a=np.array([[x]],np.float32);b=np.array([[y]],np.float32);fx,fy=F(a,b,p,t,T);return float(fx[0,0])+OX,float(fy[0,0])+OY
# ---- source-space face editing
def mask_poly(pts,ss_=3,blur=1.0):
    m=np.zeros((Hs*ss_,Ws*ss_),np.uint8);cv2.fillPoly(m,[np.round(np.array(pts)*ss_).astype(np.int32)],255,cv2.LINE_AA)
    m=cv2.resize(m,(Ws,Hs),interpolation=cv2.INTER_AREA).astype(np.float32)/255
    return cv2.GaussianBlur(m,(0,0),blur) if blur else m
def mask_line(pts,th,ss_=3):
    m=np.zeros((Hs*ss_,Ws*ss_),np.uint8);cv2.polylines(m,[np.round(np.array(pts)*ss_).astype(np.int32)],False,255,max(1,int(th*ss_)),cv2.LINE_AA)
    return cv2.resize(m,(Ws,Hs),interpolation=cv2.INTER_AREA).astype(np.float32)/255
def comp(S,m,col):
    m=np.clip(m,0,1)[...,None]*(S[...,3:4]>.5);S[...,:3]=S[...,:3]*(1-m)+np.array(col,np.float32)*m
def compc(S,m,col):
    m=np.clip(m,0,1)[...,None]*(S[...,3:4]>.5);S[...,:3]=S[...,:3]*(1-m)+col*m
def ell(cx,cy,rx,ry,n=48):
    return [(cx+rx*math.cos(2*math.pi*i/n),cy+ry*math.sin(2*math.pi*i/n)) for i in range(n)]
def local_eye(S,p):
    mapx,mapy=np.meshgrid(np.arange(Ws,dtype=np.float32),np.arange(Hs,dtype=np.float32))
    for e in EYES:
        d2=((mapx-e['cx'])**2+(mapy-e['cy'])**2);g=np.exp(-d2/(2*24**2))
        mapx=mapx-g*p['lookx']-(mapx-e['cx'])*g*p['wide']*.22
        mapy=mapy-g*p['looky']-(mapy-e['cy'])*g*p['wide']*.22
    return cv2.remap(S,mapx,mapy,cv2.INTER_CUBIC,borderMode=cv2.BORDER_REPLICATE)
def lids(S,p):
    lid,sq,arch=p['lid'],p['sq'],p['arch']
    if lid<.02 and sq<.02 and abs(p['glass'])<.02:return
    for k,e in enumerate(EYES):
        cx,cy,rx,ry=e['cx'],e['cy'],e['rx']+4,e['ry']+5
        xs=np.linspace(-1,1,40);xx=cx+xs*rx
        top=cy-ry*np.sqrt(np.clip(1-xs**2,0,1));bot=cy+ry*np.sqrt(np.clip(1-xs**2,0,1))
        closed=cy+8-arch*(1-xs**2)
        yt=top+(closed-top)*lid;yb=bot+(closed-bot)*max(sq,lid*.96)
        yb=np.maximum(yb,yt)
        # skin colour sampled around the eye
        SKIN=PLATE
        full=np.concatenate([np.stack([xx,top-6],1),np.stack([xx[::-1],bot[::-1]+6],1)])
        eyem=mask_poly(full,blur=.8)
        if lid>.02:
            up=mask_poly(np.concatenate([np.stack([xx,top-8],1),np.stack([xx[::-1],yt[::-1]],1)]),blur=1.4)*eyem
            compc(S,up,SKIN)
        if max(sq,lid*.96)>.02:
            dn=mask_poly(np.concatenate([np.stack([xx,yb],1),np.stack([xx[::-1],bot[::-1]+8],1)]),blur=.9)*eyem
            compc(S,dn,SKIN)
        if lid>.12:
            line=mask_line(np.stack([xx,yt],1),3.4);line=cv2.GaussianBlur(line,(0,0),.5)
            comp(S,line,(.17,.08,.33))
            fl=mask_line([(xx[-1]-1,yt[-1]),(xx[-1]+6*(1 if k==1 else -1)*(-1)+ (0),yt[-1]-3)],2.4) if False else 0
    # glassy/teary highlight
    if p['glass']>.02:
        for e in EYES:
            m=mask_poly(ell(e['cx']-9,e['cy']-8,10,8),blur=1.2)*p['glass'];comp(S,m,(1,1,1))
            m=mask_poly(ell(e['cx']+12,e['cy']+14,6,4),blur=1.0)*p['glass']*.8;comp(S,m,(.95,.97,1))
            ar=mask_line([(e['cx']-24+i*3,e['cy']+22+6*math.sin(i/9*math.pi)-4*math.sin(i/9*math.pi)) for i in range(17)],3)
            comp(S,ar*p['glass']*.45,(.75,.85,1))
def mouth(S,p):
    mo=p['mo'];mode=p['mouth']
    if mode=='smile':return
    patch=mask_poly(ell(180,221,46,15),blur=2.2)
    patch=patch*(np.linspace(0,1,Hs)[:,None]>-1)
    patch=np.clip(patch*np.clip((np.arange(Hs)[:,None]-210)/3,0,1),0,1)
    ca=S[231:237,160:200,:3].reshape(-1,3).mean(0)
    k=1.0 if mode!='talk' else float(np.clip(mo*10,0,1))
    comp(S,patch*k,ca)
    dark=(.36,.11,.2);pink=(.9,.42,.52);line=(.5,.3,.34)
    cx,cy=179,215
    def lipcurve(th=1.8,lift=0):
        l1=[(cx-i*1.0,cy+4+lift+((i/22)**2)*-6*0+ (1-math.cos(i/22*math.pi))*3) for i in range(0,23)]
        r1=[(cx+i*1.0,cy+4+lift+(1-math.cos(i/22*math.pi))*3) for i in range(0,23)]
        comp(S,mask_line(l1,th),line);comp(S,mask_line(r1,th),line)
        comp(S,mask_line([(cx,209),(cx,cy+4+lift)],th),line)
    if mode in('talk','open'):
        o=mo if mode=='talk' else p.get('mo',.6)
        rx=9+o*9;ry=1.5+o*11
        pts=ell(cx,cy+8+o*5,rx,ry)
        m=mask_poly(pts,blur=.7);comp(S,m,dark)
        t=mask_poly(ell(cx,cy+8+o*5+ry*.55,rx*.7,ry*.5),blur=.8)*m;comp(S,t,pink)
        comp(S,mask_line(pts+[pts[0]],1.6),line);lipcurve(1.6,-1)
    elif mode=='grin':
        g=p.get('mo',1)
        top=[(cx-26+i*52/20,cy+2+4*math.sin(i/20*math.pi)*-1+ (i/20-.5)**2*14-3) for i in range(21)]
        bot=[(cx+26-i*52/20,cy+4+ (28*g)*math.sin(i/20*math.pi)) for i in range(21)]
        pts=top+bot;m=mask_poly(pts,blur=.7);comp(S,m,dark)
        t=mask_poly(ell(cx,cy+6+24*g,16,9*g+1),blur=.8)*m;comp(S,t,pink)
        comp(S,mask_line(pts+[pts[0]],1.8),line)
    elif mode=='frown':
        pts=[(cx-22+i*44/20,cy+9-9*math.sin(i/20*math.pi)+ (i/20-.5)**2*8) for i in range(21)]
        comp(S,mask_line(pts,2.0),line);comp(S,mask_line([(cx,209),(cx,cy+2)],1.8),line)
    elif mode=='o':
        pts=ell(cx,cy+10,7+mo*2,8+mo*6);m=mask_poly(pts,blur=.7);comp(S,m,dark);comp(S,mask_line(pts+[pts[0]],1.6),line)
    elif mode=='tongue':
        lipcurve(1.8,0);ph=p.get('tx',0)
        m=mask_poly(ell(cx+ph*14,cy+11,7,6),blur=.8);comp(S,m,pink);comp(S,mask_line([(cx+ph*14,cy+7),(cx+ph*14,cy+14)],.9),(.7,.3,.4))
def blush(S,p):
    b=p['blush']
    if b<.02:return
    for cx in(80,282):
        m=cv2.GaussianBlur(mask_poly(ell(cx,215,24,13),blur=0),(0,0),7)*b*1.8
        S[...,:3]=S[...,:3]*(1-np.clip(m,0,.7)[...,None]*(S[...,3:4]>.5))+np.array([1,.55,.7],np.float32)*np.clip(m,0,.7)[...,None]*(S[...,3:4]>.5)
def make_src(p):
    S=S0.copy()
    if abs(p['lookx'])+abs(p['looky'])+abs(p['wide'])>.01:S=local_eye(S,p)
    lids(S,p);mouth(S,p);blush(S,p);return S
