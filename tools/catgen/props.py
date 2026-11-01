from core import *
import math
S2=2
def _L():
    im=Image.new('RGBA',(CW*S2,CH*S2),(0,0,0,0));return im,ImageDraw.Draw(im)
def _P(base,im,alpha=1.0):
    if alpha<1:
        a=im.getchannel('A').point(lambda v:int(v*alpha));im.putalpha(a)
    base.alpha_composite(im)
def poly(d,pts,fill,outline=None,w=0):
    d.polygon([(x*S2,y*S2) for x,y in pts],fill=fill)
    if outline:d.line([(x*S2,y*S2) for x,y in pts+[pts[0]]],fill=outline,width=int(w*S2),joint='curve')
def star5(d,cx,cy,r,col=(255,214,64,255),rot=0):
    pts=[]
    for i in range(10):
        a=rot+math.pi/5*i-math.pi/2;rr=r if i%2==0 else r*.45;pts.append((cx+rr*math.cos(a),cy+rr*math.sin(a)))
    poly(d,pts,col,(255,255,255,255),1.2)
def sparkle(d,cx,cy,r,col=(255,255,255,255),rot=0):
    pts=[]
    for i in range(8):
        a=rot+math.pi/4*i;rr=r if i%2==0 else r*.22;pts.append((cx+rr*math.cos(a),cy+rr*math.sin(a)))
    poly(d,pts,col)
def heart(d,cx,cy,s,col=(255,120,190,255)):
    pts=[]
    for i in range(41):
        t=i/40*2*math.pi;x=16*math.sin(t)**3;y=-(13*math.cos(t)-5*math.cos(2*t)-2*math.cos(3*t)-math.cos(4*t))
        pts.append((cx+x*s/16,cy+y*s/16))
    poly(d,pts,col,(255,255,255,200),1)
def note(d,cx,cy,s,col=(190,120,255,255)):
    d.ellipse([(cx-s*.5)*S2,(cy-s*.3)*S2,(cx+s*.5)*S2,(cy+s*.3)*S2],fill=col,outline=(255,255,255,255),width=S2)
    d.line([((cx+s*.45)*S2,cy*S2),((cx+s*.45)*S2,(cy-s*1.6)*S2)],fill=col,width=int(s*.18*S2))
    poly(d,[(cx+s*.45,cy-s*1.6),(cx+s*1.1,cy-s*1.0),(cx+s*.45,cy-s*1.1)],col)
def teardrop(d,cx,cy,s,col=(150,205,255,230)):
    pts=[(cx,cy-s*1.5)]+[(cx+s*math.sin(a),cy+s*(.5-math.cos(a))*1.0) for a in [i/14*math.pi*2 for i in range(0,15)]]
    pts=[(cx+s*.9*math.sin(a),cy+s*.5*(1-math.cos(a))*0.9+ (s*.0)) for a in [i/20*math.pi*2 for i in range(21)]]
    d.polygon([(cx*S2,(cy-s*1.6)*S2)]+[((cx+s*math.sin(a))*S2,(cy+s*(.1-math.cos(a)))*S2) for a in [(i/20)*2*math.pi for i in range(21)]],fill=col)
    d.ellipse([(cx-s*.45)*S2,(cy-s*.1)*S2,(cx-s*.05)*S2,(cy+s*.3)*S2],fill=(255,255,255,200))
def earring(d,cx,cy,s):
    d.arc([(cx-s*.4)*S2,(cy-s*1.1)*S2,(cx+s*.4)*S2,(cy-s*.1)*S2],180,360,fill=(255,215,120,255),width=int(s*.12*S2))
    pts=[(cx,cy-s*.1),(cx+s*.55,cy+s*.55),(cx,cy+s*1.4),(cx-s*.55,cy+s*.55)]
    poly(d,pts,(160,90,230,255),(255,235,170,255),s*.12)
    poly(d,[(cx-s*.1,cy+s*.2),(cx+s*.15,cy+s*.5),(cx-s*.1,cy+s*.6)],(230,200,255,255))
def glyph(im,ch,cx,cy,size,col,rot=0):
    f=ImageFont.truetype(FONT,int(size*S2));t=Image.new('RGBA',(int(size*3*S2),int(size*3*S2)),(0,0,0,0));d=ImageDraw.Draw(t)
    d.text((t.width/2,t.height/2),ch,font=f,fill=col,anchor='mm',stroke_width=int(size*.12*S2),stroke_fill=(255,255,255,255))
    t=t.rotate(rot,resample=Image.BICUBIC);im.alpha_composite(t,(int(cx*S2-t.width/2),int(cy*S2-t.height/2)))
def hat(d,ax,ay,ang,s=1.0):
    def R(x,y):
        r=math.radians(ang);return ax+(x*math.cos(r)-y*math.sin(r))*s,ay+(x*math.sin(r)+y*math.cos(r))*s
    cone=[R(-34,0),R(34,0),R(0,-92)];poly(d,cone,(150,90,235,255),(255,255,255,255),2)
    for i,(x,y) in enumerate([(-14,-22),(12,-36),(-2,-58),(16,-12),(-20,-44)]):
        px,py=R(x,y);d.ellipse([(px-3*s)*S2,(py-3*s)*S2,(px+3*s)*S2,(py+3*s)*S2],fill=(255,225,130,255))
    px,py=R(0,-94);d.ellipse([(px-9*s)*S2,(py-9*s)*S2,(px+9*s)*S2,(py+9*s)*S2],fill=(255,214,100,255),outline=(255,255,255,255),width=S2)
    bx,by=R(0,2);d.ellipse([(bx-36*s)*S2,(by-5*s)*S2,(bx+36*s)*S2,(by+6*s)*S2],fill=(255,170,215,255))
def notebook(d,cx,cy,ang):
    r=math.radians(ang);L=46;W=15
    def R(x,y):return cx+x*math.cos(r)-y*math.sin(r),cy+x*math.sin(r)+y*math.cos(r)
    poly(d,[R(-L,-W),R(L,-W),R(L,W),R(-L,W)],(250,244,225,255),(120,80,170,255),2)
    for x in(-30,-10,10,30):poly(d,[R(x,-W),R(x+2,-W),R(x+2,W),R(x,W)],(210,200,225,255))
    ex,ey=R(L,0);d.ellipse([(ex-6)*S2,(ey-W)*S2,(ex+6)*S2,(ey+W)*S2],fill=(235,225,205,255),outline=(120,80,170,255),width=2*S2)
    poly(d,[R(-L,-W*.35),R(L,-W*.35),R(L,W*.05),R(-L,W*.05)],(170,110,235,255))
def confetti(d,seed,t,n=26,x0=0,y0=0,spread=1.0,fall=1.0):
    rs=np.random.RandomState(seed)
    for i in range(n):
        ang=rs.uniform(-math.pi*.95,-math.pi*.05);v=rs.uniform(110,300)*spread;ph=rs.uniform(0,6);col=[(255,214,100,255),(190,120,255,255),(255,140,200,255),(130,220,240,255),(255,255,255,255)][i%5]
        x=x0+v*math.cos(ang)*t;y=y0+v*math.sin(ang)*t+330*t*t*fall
        if y>CH or t<0:continue
        w=5;h=9;a=ph+t*rs.uniform(5,12)
        pts=[(x+(px*math.cos(a)-py*math.sin(a)),y+(px*math.sin(a)+py*math.cos(a))) for px,py in[(-w/2,-h/2),(w/2,-h/2),(w/2,h/2),(-w/2,h/2)]]
        poly(d,pts,col)
