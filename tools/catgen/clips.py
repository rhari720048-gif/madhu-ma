from props import *
from props import _P,_L
D0=dict(head=0,hdx=0,hdy=0,earL=0,earR=0,tail=0,jump=0,sy=1,sx=1,lean=0,breath=0,lid=0,sq=0,arch=-6,blush=0,mouth='smile',mo=0,lookx=0,looky=0,wide=0,glass=0,tx=0,flut=1.0)
T0=2.4;TAU=2*math.pi
def env(t,a,b,c,d):return float(ss(a,b,t)*(1-ss(c,d,t)))
def blink(t,tb,dur=.2):
    x=(t-tb)/dur;return math.sin(math.pi*x)**.7 if 0<x<1 else 0.0
def talk(t,a,b,amp=.7):
    e=env(t,a,a+.15,b-.15,b);return e*(.12+amp*abs(math.sin(TAU*3.3*t+.9*math.sin(TAU*.7*t))))
def base(t):
    p=dict(D0);p['breath']=math.sin(TAU*t/T0);p['tail']=8*math.sin(TAU*2*t/T0);p['head']=1.3*math.sin(TAU*t/T0);p['lookx']=1.6*math.sin(TAU*t/T0);p['hdy']=.8*math.sin(TAU*t/T0)
    return p
def mix(p,**k):
    for a,b in k.items():p[a]=p[a]+b if a in('head','hdx','hdy','earL','earR','tail','jump','lean','lookx','looky') else b
    return p
def anchor(p,t,x,y):return fp(x,y,p,t,T0)
# ---------------- clips: (duration, loop, fn(t)->(params, drawfn|None))
def idle(t):
    p=base(t);p['lid']=max(blink(t,1.5),blink(t,.45)*0);p['earR']=-7*math.sin(math.pi*min(max((t-.7)/.25,0),1))**2;return p,None
def ask1(t):
    p=base(t);e=env(t,.2,.7,3.3,3.9)
    mix(p,head=7*env(t,.2,.8,3.3,3.9),hdy=3*e)
    p['mouth']='talk';p['mo']=talk(t,.4,3.0)
    up=env(t,.4,.9,1.9,2.3);p['looky']=-5*up;p['lookx']=4*up
    sad=env(t,1.9,2.4,3.3,3.8)
    p['earL']=-20*sad;p['earR']=20*sad;p['hdy']+=9*sad;p['glass']=.7*sad;p['sy']=1-.02*sad;p['looky']+=5*env(t,2.7,3.0,3.4,3.8);p['blush']=.5*env(t,2.8,3.2,3.5,3.9)
    p['lid']=max(blink(t,1.2),blink(t,3.5))*1.0
    def dr(im,d):
        a=env(t,.35,.7,1.9,2.3)
        if a>.02:
            L=Image.new('RGBA',im.size,(0,0,0,0));dd=ImageDraw.Draw(L)
            bob=4*math.sin(TAU*.9*t)
            for k,(x,y) in enumerate([(OX+312,OY+40),(OX+352,OY+82)]):
                earring(dd,x,y+bob+k*3*math.sin(TAU*.9*t+1),22)
            for k in range(3):sparkle(dd,OX+332+30*math.cos(k*2.1+t*3),OY+60+30*math.sin(k*2.1+t*3),6+3*math.sin(t*9+k),(255,255,255,255),t*2)
            _P(im,L,a)
    return p,dr
def ask2(t):
    p=base(t);cl=env(t,.55,.95,2.2,2.6)
    p['lid']=cl;p['arch']=-6;p['head']=6*math.sin(TAU*.6*t)*env(t,.3,.9,2.3,2.8);p['lean']=3*math.sin(TAU*.6*t)*env(t,.3,.9,2.3,2.8)
    p['mouth']='talk';p['mo']=talk(t,.3,3.1,.55)
    sad=env(t,2.4,2.9,3.4,3.95);p['earL']=-16*sad;p['earR']=16*sad;p['glass']=.5*sad;p['hdy']+=6*sad;p['blush']=.3*sad
    if sad>.5:p['mouth']='frown'
    def dr(im,d):
        L=Image.new('RGBA',im.size,(0,0,0,0));dd=ImageDraw.Draw(L)
        for k in range(7):
            st=.35+k*.28;a=(t-st)/1.5
            if 0<a<1:
                x=OX+60+k*38+12*math.sin(TAU*(.8*a+k*.2));y=OY+70-a*105-12
                note(dd,x,y,15,[(190,120,255,255),(255,140,200,255),(130,200,240,255)][k%3])
        _P(im,L,env(t,.3,.6,2.5,2.9) if True else 1)
    return p,dr
def ask3(t):
    p=base(t);e=env(t,.25,.85,3.3,3.9)
    p['mouth']='talk';p['mo']=talk(t,.3,2.1);mix(p,head=9*e,hdy=2*e)
    p['lookx']=6*e;p['looky']=-4*e;p['earR']=-10*math.sin(math.pi*np.clip((t-1.5)/.4,0,1))**2-4*e;p['tail']=14*math.sin(TAU*1.2*t)*e
    p['lid']=max(blink(t,1.1),blink(t,2.9))
    def dr(im,d):
        a=env(t,1.1,1.5,3.5,3.9)
        if a>.02:
            L=Image.new('RGBA',im.size,(0,0,0,0));x,y=anchor(p,t,235,-4)
            glyph(L,'?',x+20,y-6+5*math.sin(TAU*1.1*t),44,(160,90,235,255),8*math.sin(TAU*.7*t));_P(im,L,a)
    return p,dr
def ask4(t):
    p=base(t);p['tail']=22*math.sin(TAU*3*t/T0*1.0);hop=max(0,math.sin(TAU*2*t/T0))
    p['jump']=12*hop;p['sy']=1+.012*math.sin(TAU*4*t/T0);p['mouth']='talk';p['mo']=.15+.6*abs(math.sin(TAU*3*t*1.0/T0*2.0))*(1 if True else 0)
    p['lid']=.85;p['sq']=.85;p['arch']=14;p['blush']=.6;p['earL']=6;p['earR']=-6
    def dr(im,d):
        L=Image.new('RGBA',im.size,(0,0,0,0));dd=ImageDraw.Draw(L);x,y=anchor(p,t,185,18);hat(dd,x+8,y+8,10+4*math.sin(TAU*2*t/T0),1.15)
        for k in range(5):sparkle(dd,OX+40+k*70+8*math.sin(t*5+k),OY+30+40*math.sin(k*1.7+t*3),5+2*math.sin(t*8+k),(255,235,150,255),t*3)
        _P(im,L)
    return p,dr
def happy(t):
    p=base(t);hop=max(0,math.sin(TAU*1.6*(t-.2)))*env(t,.2,.3,1.6,1.9)
    e=env(t,.25,.55,1.7,2.1);p['jump']=26*hop;p['sy']=1-.03*(1-hop)*e;p['lid']=.88*e;p['sq']=.88*e;p['arch']=14;p['mouth']='grin' if e>.3 else 'smile';p['mo']=1
    p['blush']=.7*e;p['tail']=26*math.sin(TAU*3*t)*e;p['earL']=8*e;p['earR']=-8*e
    def dr(im,d):
        L=Image.new('RGBA',im.size,(0,0,0,0));dd=ImageDraw.Draw(L)
        for k in range(6):
            a=(t-.3-k*.2)/1.0
            if 0<a<1:heart(dd,OX+60+k*52+10*math.sin(a*7+k),OY+70-a*80,16+4*(k%2),[(255,120,190,255),(190,120,255,255)][k%2])
        for k in range(4):sparkle(dd,OX+35+k*100,OY+25+30*math.sin(k*2+t*4),7*abs(math.sin(t*6+k))+2,(255,255,255,255),t*2)
        _P(im,L,env(t,.2,.4,1.8,2.3))
    return p,dr
def sad(t):
    p=base(t);e=env(t,.2,.7,1.8,2.4);m=env(t,.1,.5,1.9,2.4)
    p['earL']=-24*e;p['earR']=24*e;p['hdy']+=11*e;p['head']+=-4*e;p['glass']=1.0*e;p['sy']=1-.025*e;p['hdx']=.8*math.sin(TAU*7*t)*e
    p['lid']=.28*e+blink(t,1.3);p['mouth']='frown' if e>.35 else 'smile';p['looky']=4*e
    if t>2.0:p['mouth']='smile'
    def dr(im,d):
        L=Image.new('RGBA',im.size,(0,0,0,0));dd=ImageDraw.Draw(L)
        for k,sx in enumerate((110,244)):
            for j in range(2):
                a=((t-.5-j*.7)%1.4)/1.4
                if t>.5 and t<2.2:
                    x,y=anchor(p,t,sx+(-6 if k==0 else 6),188+a*55);teardrop(dd,x,y,5.5)
        _P(im,L,e)
    return p,dr
def shy(t):
    p=base(t);e=env(t,.2,.6,1.6,2.1);p['blush']=1.0*e;p['hdy']+=5*e;p['head']+=10*e;p['lookx']=-5*e;p['looky']=5*e;p['lean']=4*math.sin(TAU*1.1*t)*e
    p['earL']=-8*e;p['earR']=8*e;p['lid']=.35*e+blink(t,1.0,.28);p['tail']=10*math.sin(TAU*2*t)*e
    def dr(im,d):
        L=Image.new('RGBA',im.size,(0,0,0,0));dd=ImageDraw.Draw(L)
        for k in range(4):
            a=(t-.4-k*.3)/1.1
            if 0<a<1:heart(dd,OX+250+k*20+8*math.sin(a*6+k),OY+90-a*70,13,(255,140,190,255))
        _P(im,L,e)
    return p,dr
def dream(t):
    p=base(t);e=env(t,.25,.7,2.2,2.7);p['lid']=e;p['arch']=-7;p['head']=7*math.sin(TAU*.55*t)*e;p['lean']=4*math.sin(TAU*.55*t)*e;p['blush']=.35*e
    p['mouth']='talk';p['mo']=(.1+.12*math.sin(TAU*1.1*t))*e;p['tail']=12*math.sin(TAU*.9*t)*e
    def dr(im,d):
        L=Image.new('RGBA',im.size,(0,0,0,0));dd=ImageDraw.Draw(L)
        for k in range(6):
            a=(t-.3-k*.32)/1.6
            if 0<a<1:note(dd,OX+40+k*60+14*math.sin(TAU*(.7*a+k*.15)),OY+75-a*105-10,15,[(190,120,255,255),(255,140,200,255),(130,200,240,255)][k%3])
        _P(im,L,env(t,.25,.5,2.3,2.8))
    return p,dr
def yum(t):
    p=base(t);e=env(t,.2,.55,1.8,2.3);p['lid']=.85*e;p['sq']=.85*e;p['arch']=10;p['blush']=.5*e;p['lean']=5*math.sin(TAU*1.6*t)*e;p['hdy']+=-3*abs(math.sin(TAU*1.6*t))*e
    p['mouth']='tongue' if e>.4 else 'smile';p['tx']=math.sin(TAU*1.8*(t-.4))
    p['tail']=16*math.sin(TAU*2.2*t)*e;p['earL']=6*e;p['earR']=-6*e
    def dr(im,d):
        L=Image.new('RGBA',im.size,(0,0,0,0));dd=ImageDraw.Draw(L)
        for k in range(5):sparkle(dd,OX+45+k*82,OY+35+25*math.sin(k*1.9+t*4),6*abs(math.sin(t*7+k))+2,(255,240,170,255),t*3)
        _P(im,L,e)
    return p,dr
def bonk(t):
    p=base(t);hit=.55;after=max(0,t-hit)
    sq=math.exp(-after*3.2)*math.cos(TAU*2.2*after) if t>hit else 0
    p['hdy']+=18*max(sq,0)*(1 if t>hit else 0);p['sy']=1-.07*max(sq,0);p['head']+=-9*math.exp(-after*1.5)*math.sin(TAU*1.7*after) if t>hit else 0
    ouch=env(t,hit,hit+.08,1.5,2.0);p['lid']=ouch;p['arch']=-8;p['mouth']='open' if ouch>.3 else 'smile';p['mo']=1
    dz=env(t,1.5,1.8,2.7,3.1);p['lookx']=5*math.cos(TAU*1.4*t)*dz;p['looky']=4*math.sin(TAU*1.4*t)*dz
    sadm=env(t,1.9,2.4,3.1,3.4);p['glass']=.9*max(ouch*.8,sadm);p['earL']=-18*max(ouch,sadm);p['earR']=18*max(ouch,sadm)
    if sadm>.5:p['mouth']='frown'
    def dr(im,d):
        L=Image.new('RGBA',im.size,(0,0,0,0));dd=ImageDraw.Draw(L)
        hx,hy=anchor(p,t,185,18)
        if t<hit+.9:
            y=hy-260*(1-ss(.0,hit,t))**2 if t<hit else hy-6-60*ss(hit,hit+.8,t)
            ang=-22+ (0 if t<hit else 50*ss(hit,hit+.8,t))
            nb=Image.new('RGBA',im.size,(0,0,0,0));nd=ImageDraw.Draw(nb);notebook(nd,hx+14,y-12,ang);_P(L,nb,1-ss(hit+.45,hit+.9,t))
        if t>hit+.05:
            a=env(t,hit+.05,hit+.3,2.5,3.0)
            for k in range(4):
                th=TAU*(.9*(t-hit)+k/4);star5(dd,hx+74*math.cos(th),hy+12+18*math.sin(th),14,rot=th*2)
            if a<1:L.putalpha(L.getchannel('A').point(lambda v:int(v*a)))
        _P(im,L)
    return p,dr
def cheer(t):
    p=base(t);e=env(t,.1,.3,2.0,2.5);hop=abs(math.sin(TAU*1.4*t))
    p['jump']=34*hop*e;p['sy']=1-.03*(1-hop)*e;p['lid']=.9*e;p['sq']=.9*e;p['arch']=14;p['mouth']='grin' if e>.3 else 'smile';p['mo']=1;p['blush']=.7*e;p['tail']=26*math.sin(TAU*3*t)*e;p['earL']=8*e;p['earR']=-8*e
    def dr(im,d):
        L=Image.new('RGBA',im.size,(0,0,0,0));dd=ImageDraw.Draw(L);x,y=anchor(p,t,185,18);hat(dd,x+8,y+8,10+5*math.sin(TAU*1.4*t),1.15)
        confetti(dd,7,t-.1,34,OX+Ws/2,OY+60);confetti(dd,11,t-.5,22,OX+Ws/2,OY+60)
        _P(im,L)
    return p,dr
def laugh(t):
    p=base(t);e=env(t,.15,.4,1.9,2.3);p['head']=-6*e+3*math.sin(TAU*5*t)*e;p['lid']=.9*e;p['sq']=.9*e;p['arch']=14;p['mouth']='grin' if e>.3 else 'smile';p['mo']=.7+.3*math.sin(TAU*4*t);p['blush']=.6*e
    p['sy']=1+.016*math.sin(TAU*8*t)*e;p['hdy']+=3*math.sin(TAU*4*t)*e;p['tail']=22*math.sin(TAU*3*t)*e;p['earL']=6*e;p['earR']=-6*e
    def dr(im,d):
        L=Image.new('RGBA',im.size,(0,0,0,0));dd=ImageDraw.Draw(L)
        for k,sx in enumerate((110,244)):
            a=((t-.4-k*.2)%.9)/.9
            if t>.4:x,y=anchor(p,t,sx+(-26 if k==0 else 26),170+a*20);teardrop(dd,x,y+a*14,5)
        _P(im,L,e)
    return p,dr
def surprised(t):
    p=base(t);e=env(t,.08,.2,1.0,1.6);p['wide']=1.0*e;p['mouth']='o' if e>.3 else 'smile';p['mo']=.8;p['earL']=14*e;p['earR']=-14*e;p['jump']=18*env(t,.08,.2,.4,.7)
    p['sy']=1+.02*e;p['lean']=-3*e;p['tail']=10*math.sin(TAU*4*t)*e
    def dr(im,d):
        a=env(t,.15,.3,1.2,1.7)
        if a>.02:
            L=Image.new('RGBA',im.size,(0,0,0,0));x,y=anchor(p,t,235,-6);glyph(L,'!',x+22,y-10+3*math.sin(TAU*3*t),50,(255,110,180,255),6);_P(im,L,a)
    return p,dr
CLIPS={'idle':(2.4,1,idle),'ask1':(4.0,0,ask1),'ask2':(4.0,0,ask2),'ask3':(4.0,0,ask3),'ask4':(2.4,1,ask4),'happy':(2.4,0,happy),'sad':(2.6,0,sad),'shy':(2.2,0,shy),'dream':(3.0,0,dream),'yum':(2.4,0,yum),'bonk':(3.4,0,bonk),'cheer':(2.6,0,cheer),'laugh':(2.4,0,laugh),'surprised':(1.8,0,surprised)}
FPS=24
def render(name,i,N):
    D,loop,fn=CLIPS[name];t=(i/N*D) if loop else i/FPS
    p,dr=fn(t);full=dict(D0);full.update(p)
    S=make_src(full);o=warp(S,full,t,T0)
    im=Image.fromarray((o*255).astype(np.uint8),'RGBA')
    if dr:
        big=im.resize((CW*S2,CH*S2),Image.BICUBIC);dr(big,None);im=big.resize((CW,CH),Image.LANCZOS)
    return im
