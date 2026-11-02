# Son « room tone » : même méthode que le reel 180° v3 / 4 types de coupe.
# Nappe douce dès la 1re image, pulsation feutrée sans batterie, sons de Point au premier plan.
# Le « fond » de la pièce est un souffle très doux : à l'accroche il tombe à zéro dans les trous (micro-coupure douce),
# pendant la prise de room tone on l'entend seul, au montage il devient continu.
import numpy as np, wave, json, os
from scipy.signal import lfilter
TM=json.load(open('times.json'))
SR=48000; DUR=TM['dur']; N=int(SR*DUR)
dry=np.zeros((N,2)); send=np.zeros((N,2)); rng=np.random.default_rng(31)
MASC='../mascot' if os.path.exists('../mascot/point-oh.wav') else '/home/claude/hcstudio/motion-source/mascot'
def lp(x,fc):
    fc=np.asarray(fc,float)
    if fc.ndim==0:
        a=np.exp(-2*np.pi*float(fc)/SR); return lfilter([1-a],[1,-a],x)
    a=np.exp(-2*np.pi*fc/SR); y=np.empty_like(x); s=0.0
    for i in range(len(x)): s=a[i]*s+(1-a[i])*x[i]; y[i]=s
    return y
def hp(x,fc): return x-lp(x,fc)
def T(d): return np.arange(int(d*SR))/SR
def put(t,sig,g=1.0,pan=0.0,rev=0.3):
    i=int(round(t*SR)); n=min(len(sig),N-i)
    if n<=0 or i<0: return
    s=sig[:n]*g; st=np.stack([s*np.sqrt((1-pan)/2),s*np.sqrt((1+pan)/2)],1)
    dry[i:i+n]+=st; send[i:i+n]+=st*rev
def fadeio(x,a=0.01,r=0.05):
    n=len(x); e=np.ones(n); na=max(1,int(a*SR)); nr=max(1,int(r*SR)); e[:na]=np.linspace(0,1,na); e[-nr:]=np.linspace(1,0,nr); return x*e
def air(d=1.1,lo=200,hi=1800,shape=3):
    n=int(d*SR); x=np.linspace(0,1,n); sh=np.sin(np.pi*x)**shape
    return lp(lp(rng.standard_normal(n),lo+hi*sh),2400)*sh*0.6
def click(f=1100,d=0.006):
    t=T(0.04); return fadeio(lp(np.sin(2*np.pi*f*t)*np.exp(-t/d),6000),0.004,0.01)
def tock(f=180):
    t=T(0.16); s=np.sin(2*np.pi*f*t)*np.exp(-t/0.06)+0.15*np.sin(2*np.pi*f*2*t)*np.exp(-t/0.02)
    return fadeio(lp(s,2500),0.005,0.03)
def keys(f,d=4.0,dec=1.6):
    t=T(d); s=np.sin(2*np.pi*f*t)+0.18*np.sin(2*np.pi*2*f*t)*np.exp(-t/0.6)+0.05*np.sin(2*np.pi*3*f*t)*np.exp(-t/0.3)
    return fadeio(lp(s*np.exp(-t/dec),2200),0.012,0.4)
def wav(name):
    w=wave.open(f'{MASC}/point-{name}.wav'); return np.frombuffer(w.readframes(w.getnframes()),'<i2').astype(float)/32768
t=np.arange(N)/SR
def win(a,b,r=0.04):   # fenêtre douce : 1 entre a et b, rampes de r secondes
    return np.clip(np.minimum((t-a)/r+0.5,(b-t)/r+0.5),0,1)
# ---------- nappe ----------
def saw(f): return 2*((t*f)%1)-1
prog=[(0,[110,164.8,261.6,329.6,493.9]),           # la m9 : les trous
      (TM['s1'],[87.3,130.8,261.6,329.6,392]),      # fa maj7 : on enregistre le silence
      (TM['s2'],[65.4,130.8,246.9,329.6,392]),      # do maj7 : on bouche les trous
      (TM['ok'],[65.4,130.8,246.9,329.6,392,587.3]),# do maj9 : fond continu
      (TM['s3'],[73.4,146.8,261.6,349.2,440]),      # ré m7 : nouvelle pièce
      (TM['end'],[110,164.8,261.6,329.6,493.9]),    # la m9 : fin
      (TM['land'],[87.3,130.8,261.6,329.6,392,523.3])]
pad=np.zeros(N)
for k,(a,ch) in enumerate(prog):
    b=prog[k+1][0] if k+1<len(prog) else DUR+2
    env=np.clip(np.minimum((t-(a-0.5))/1.0+(1 if k==0 else 0),(b+0.5-t)/1.0),0,1)
    pad+=sum(saw(f*1.003)+saw(f*0.997) for f in ch)/len(ch)/2*env
cut=520+380*(0.5+0.5*np.sin(2*np.pi*t/10))
pad=lp(lp(pad,cut),cut)
bt=60/90
swell=np.clip(0.75+t/2.0,0,1)
gate=1-0.10*np.exp(-((t-TM['s1'])%(2*bt))/0.3)*((t>TM['s1'])&(t<TM['end']))
# le trou : la nappe baisse doucement pendant que la tête de lecture traverse un trou (jamais à zéro)
hole=1-0.45*np.maximum(win(TM['g1a'],TM['g1b'],0.06),win(TM['g2a'],TM['g2b'],0.06))
# pendant les prises de room tone : tout le monde se tait, la nappe se retire un peu
quiet=1-0.35*np.maximum(win(TM['rec'],TM['recE'],0.5),win(TM['recB'],TM['recBE'],0.4))
PT=[TM['oh'],TM['pfff'],TM['ok'],TM['hm'],TM['land']]
duck=np.ones(N)
for a in PT: duck-=0.35*np.clip(np.minimum((t-a+0.05)/0.05,1),0,1)*np.exp(-np.clip(t-a-0.4,0,None)/0.3)*(t>a-0.05)
duck=np.clip(duck,0.6,1)
L=pad*swell*gate*hole*quiet*duck*0.17
dry[:,0]+=L; dry[:,1]+=L; send[:,0]+=L*0.6; send[:,1]+=L*0.6
# ---------- le fond de la pièce (souffle très doux) ----------
nz=lp(lp(hp(rng.standard_normal(N),120),900),900); nz/=np.max(np.abs(nz))
nzB=lp(hp(rng.standard_normal(N),180),1400); nzB/=np.max(np.abs(nzB))
fond=np.ones(N)*0.5
fond*=1-np.maximum(win(TM['g1a'],TM['g1b'],0.02),win(TM['g2a'],TM['g2b'],0.02))     # le trou : silence numérique
fond*=np.clip(1-np.clip((t-TM['s1']-0.2)/0.6,0,1)+np.clip((t-TM['rec']+0.3)/0.5,0,1),0,1)
fond=np.where(t>TM['recE']+0.2,np.clip(1-(t-TM['recE']-0.2)/0.5,0,1)*0.5+np.clip((t-TM['sweep']+0.3)/0.4,0,1)*0.5*(t<TM['s3']+0.3),fond)
fond=np.where(t>TM['s3'],np.clip(1-(t-TM['s3'])/0.4,0,1)*0.5,fond)
fond=lp(fond,30)
fB=lp(win(TM['recB'],TM['recBE'],0.3)*0.6,30)
F=nz*fond*0.06+nzB*fB*0.05
F=F*np.clip(1-(t-TM['end'])/0.6,0,1)
dry[:,0]+=F; dry[:,1]+=F*0.9; send[:,0]+=F*0.3; send[:,1]+=F*0.3
# ---------- accroche ----------
put(0.0,keys(220,5),0.045,-0.2,0.7); put(0.25,keys(329.6,5),0.03,0.2,0.7)
put(TM['oh'],wav('oh'),0.18,-0.2,0.3)
put(TM['pfff'],wav('pfff'),0.19,-0.2,0.3)
for c in [TM['s1'],TM['s2'],TM['s3']]: put(c-0.1,air(0.7,250,1000),0.09,0.2 if int(c)%2 else -0.2,0.6)
# ---------- 01 : le micro descend, REC, on attend ----------
put(TM['mic']+0.75,tock(160),0.04,0.1,0.3)
put(TM['rec'],click(1000),0.035,0,0.4); put(TM['recE'],click(900),0.03,0,0.4)
put(TM['recE']+0.15,keys(523.3,3,1.2),0.025,0,0.7)
# ---------- 02 : les morceaux montent dans les trous ----------
for lt in [TM['lift1'],TM['lift2']]:
    put(lt,air(0.75,250,900,2),0.06,0,0.4); put(lt+0.72,tock(190),0.035,0,0.3)
put(TM['ok'],wav('tadam'),0.17,0,0.35)
for f,d in [(261.6,0),(329.6,0.06),(392,0.12)]: put(TM['ok']+0.6+d,keys(f,4.5),0.02,0,0.8)
# ---------- 03 : nouvelle pièce ----------
put(TM['hm'],wav('hm'),0.16,-0.2,0.35)
k=0
while TM['walk']+0.1+k*0.35<TM['walkE']: put(TM['walk']+0.1+k*0.35,tock(130+(k%2)*12),0.022,-0.2+0.4*k/3,0.2); k+=1
put(TM['mic2E'],tock(160),0.035,0.3,0.3)
put(TM['recB'],click(1000),0.03,0.3,0.4); put(TM['recBE'],click(900),0.025,0.3,0.4)
put(TM['liftB'],air(0.75,250,900,2),0.05,0.3,0.4); put(TM['liftB']+0.72,tock(190),0.03,0.3,0.3)
put(TM['liftB']+0.75,keys(659.3,3,1.2),0.022,0.2,0.7)
# ---------- fin : signature ----------
sp=lambda u: np.sin(np.pi*np.clip(u,0,1))**0.7
def pencil(d,speed=None):
    tt=T(d); n=lp(lp(hp(rng.standard_normal(len(tt)),800),2400),2400); n=lp(n,5000)
    tex=0.6+0.4*np.abs(np.sin(2*np.pi*(3.5+1.5*np.sin(2*np.pi*0.5*tt))*tt))**1.5
    env=speed(tt/d) if speed else np.ones(len(tt))
    return n*tex*env*np.minimum(1,np.minimum(tt/0.05,(d-tt)/0.1))*0.5
put(TM['end']-0.1,air(1.0,200,1000),0.12,0,0.6)
put(TM['hero']+0.2,air(1.2,300,1200,2),0.07,0.2,0.6)
put(TM['end']+0.28,pencil(0.95,sp),0.3,0,0.25); put(TM['end']+1.04,pencil(0.36,sp),0.22,0.05,0.25)
put(TM['land']-0.01,wav('bip'),0.16,0.15,0.4); put(TM['land']+0.02,keys(880,4,1.8),0.035,0.2,0.8); put(TM['land']+0.04,keys(659.3,4,1.8),0.025,-0.2,0.8)
put(TM['end']+1.36,click(1000),0.025,0,0.5)
# ---------- réverbe (IR synthétique ~1,2 s) ----------
ir_t=T(2.0); ir=lp(rng.standard_normal(len(ir_t)),4000)*np.exp(-ir_t/0.35); ir2=lp(rng.standard_normal(len(ir_t)),4000)*np.exp(-ir_t/0.35)
def conv(x,h):
    n=len(x)+len(h); nf=1<<int(np.ceil(np.log2(n))); return np.fft.irfft(np.fft.rfft(x,nf)*np.fft.rfft(h,nf),nf)[:len(x)]
wet=np.stack([conv(send[:,0],ir),conv(send[:,1],ir2)],1); wet/=np.max(np.abs(wet))+1e-9; wet*=np.max(np.abs(send))*0.9
out=dry+wet*0.55
out=np.stack([lp(out[:,0],9000),lp(out[:,1],9000)],1)
fn=int(0.6*SR); fade=np.ones(N); fade[-fn:]=np.linspace(1,0.2,fn)
out*=fade[:,None]; out=np.tanh(out*0.8)/np.tanh(0.8); out/=np.max(np.abs(out))*1.12
w=wave.open('audio.wav','wb'); w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR)
w.writeframes((out*32767).astype('<i2').tobytes()); w.close(); print('ok')
