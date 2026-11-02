# Son « couleurs complémentaires » (reel court) : même méthode que le reel 180° v3.
# Nappe douce dès la 1re image, pulsation feutrée sans batterie, sons de Point au premier plan,
# effets doux (pas de boum, pas de montée, pas de marimba).
import numpy as np, wave, json
from scipy.signal import lfilter
TM=json.load(open('times.json'))
import os
MASCOT=os.environ.get('MASCOT','/home/claude/hcstudio/motion-source/mascot')
SR=48000; DUR=TM['dur']; N=int(SR*DUR)
dry=np.zeros((N,2)); send=np.zeros((N,2)); rng=np.random.default_rng(16)
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
def air(d=1.1,lo=200,hi=1800,shape=3):   # souffle feutré, en cloche (aucune montée de hauteur)
    n=int(d*SR); x=np.linspace(0,1,n); sh=np.sin(np.pi*x)**shape
    return lp(lp(rng.standard_normal(n),lo+hi*sh),2400)*sh*0.6
def click(f=1100,d=0.006):
    t=T(0.04); return fadeio(lp(np.sin(2*np.pi*f*t)*np.exp(-t/d),6000),0.004,0.01)
def tock(f=180):    # petit « toc » de bois, sans partiel métallique
    t=T(0.16); s=np.sin(2*np.pi*f*t)*np.exp(-t/0.06)+0.15*np.sin(2*np.pi*f*2*t)*np.exp(-t/0.02)
    return fadeio(lp(s,2500),0.005,0.03)
def keys(f,d=4.0,dec=1.6):
    t=T(d); s=np.sin(2*np.pi*f*t)+0.18*np.sin(2*np.pi*2*f*t)*np.exp(-t/0.6)+0.05*np.sin(2*np.pi*3*f*t)*np.exp(-t/0.3)
    return fadeio(lp(s*np.exp(-t/dec),2200),0.012,0.4)
def key_tap():      # frappe de clavier feutrée : un petit bruit court + un toc très bas
    t=T(0.05); n=lp(hp(rng.standard_normal(len(t)),900),3500)*np.exp(-t/0.008)
    return fadeio(n*0.7+0.4*np.sin(2*np.pi*240*t)*np.exp(-t/0.012),0.002,0.01)
def pencil(d,speed=None):   # crayon doux : bruit bande étroite, enveloppe = vitesse du trait
    t=T(d); n=lp(lp(hp(rng.standard_normal(len(t)),800),2400),2400); n=lp(n,5000)
    tex=0.6+0.4*np.abs(np.sin(2*np.pi*(3.5+1.5*np.sin(2*np.pi*0.5*t))*t))**1.5
    env=speed(t/d) if speed else np.ones(len(t))
    return n*tex*env*np.minimum(1,np.minimum(t/0.05,(d-t)/0.1))*0.5
def wav(name):
    w=wave.open(f'{MASCOT}/point-{name}.wav'); return np.frombuffer(w.readframes(w.getnframes()),'<i2').astype(float)/32768
# ---------- nappe ----------
t=np.arange(N)/SR
def saw(f): return 2*((t*f)%1)-1
prog=[(0,[110,164.8,261.6,329.6,493.9]),             # la m9 : les deux couleurs se battent
      (TM['s1'],[87.3,130.8,261.6,329.6,392]),        # fa maj7 : le cercle
      (TM['s2'],[73.4,146.8,261.6,349.2,440]),        # ré m7 : contraste simultané
      (TM['s3'],[82.4,123.5,246.9,293.7,392]),        # mi m7 : 50/50, l'oeil fatigue
      (TM['s4'],[65.4,130.8,246.9,329.6,392,587.3]),  # do maj9 : dominante + accent
      (TM['s5'],[98,146.8,246.9,293.7,440]),          # sol 9 : désaturer
      (TM['end'],[110,164.8,261.6,329.6,493.9]),      # la m9 : fin
      (TM['land'],[87.3,130.8,261.6,329.6,392,523.3])]# fa maj9 : signature
pad=np.zeros(N)
for k,(a,ch) in enumerate(prog):
    b=prog[k+1][0] if k+1<len(prog) else DUR+2
    env=np.clip(np.minimum((t-(a-0.4))/0.8+(1 if k==0 else 0),(b+0.4-t)/0.8),0,1)
    pad+=sum(saw(f*1.003)+saw(f*0.997) for f in ch)/len(ch)/2*env
cut=520+380*(0.5+0.5*np.sin(2*np.pi*t/8))+np.where((t>TM['domE'])&(t<TM['s5']),220,0)
pad=lp(lp(pad,cut),cut)
bt=60/90
swell=np.clip(0.75+t/2.0,0,1)                                                   # déjà là à la 1re image
gate=1-0.10*np.exp(-((t-TM['s1'])%(2*bt))/0.3)*((t>TM['s1'])&(t<TM['end']))    # pulsation feutrée 90 BPM
PT=[TM['oh'],TM['pfff'],TM['hm'],TM['pfff2'],TM['tadam'],TM['bip'],TM['land']]
duck=np.ones(N)
for a in PT: duck-=0.35*np.clip(np.minimum((t-a+0.05)/0.05,1),0,1)*np.exp(-np.clip(t-a-0.4,0,None)/0.3)*(t>a-0.05)
duck=np.clip(duck,0.6,1)
L=pad*swell*gate*duck*0.17
dry[:,0]+=L; dry[:,1]+=L; send[:,0]+=L*0.6; send[:,1]+=L*0.6
# ---------- accroche : deux aplats qui vibrent (frémissement très doux, pas de bruit agressif) ----------
put(0.0,keys(220,5),0.045,-0.2,0.7); put(0.25,keys(329.6,5),0.03,0.2,0.7)
def shimmer(d,f=1300):   # léger frémissement filtré, modulé lentement (le bord qui tremble)
    tt=T(d); n=lp(hp(rng.standard_normal(len(tt)),f*0.6),f)*(0.6+0.4*np.sin(2*np.pi*2.2*tt))
    return fadeio(n*np.minimum(1,np.minimum(tt/0.4,(d-tt)/0.6)),0.02,0.1)
put(0.0,shimmer(TM['s1']-0.1),0.035,0,0.4)
put(TM['oh'],wav('oh'),0.18,0,0.3)
put(TM['pfff'],wav('pfff'),0.19,0,0.3)
for c in [TM['s1'],TM['s2'],TM['s3'],TM['s4'],TM['s5']]: put(c-0.1,air(0.7,250,1000),0.08,0.2 if int(c)%2 else -0.2,0.6)
# ---------- le cercle : segments qui se posent, traits entre complémentaires ----------
for i in range(6): put(TM['wheel']+i*0.08,click(1000+80*i,0.004),0.014,-0.5+0.2*i,0.5)
put(TM['hm'],wav('hm'),0.15,0,0.35)
sp=lambda u: np.sin(np.pi*np.clip(u,0,1))**0.7
for j,(f,pn) in enumerate([(392,0),(440,-0.2),(523.3,0.2)]):
    put(TM['pr%d'%(j+1)],pencil(0.5,sp),0.18,pn,0.3); put(TM['pr%d'%(j+1)]+0.48,keys(f,2.5,1.0),0.02,pn,0.7)
# ---------- contraste simultané ----------
put(TM['s2']+0.15,tock(170),0.03,-0.2,0.35); put(TM['row2'],tock(160),0.03,0.1,0.35)
put(TM['glow'],keys(587.3,3,1.2),0.022,0.2,0.8); put(TM['glow']+0.05,keys(392,3,1.2),0.018,-0.1,0.8)
# ---------- 50/50 : la paire grandit, le bord revibre ----------
put(TM['grow'],air(TM['growE']-TM['grow']+0.2,220,900,2),0.07,0,0.5)
put(TM['growE']-0.2,shimmer(TM['s4']-TM['growE']+0.2),0.035,0,0.4)
put(TM['pfff2'],wav('pfff'),0.17,0,0.3)
# ---------- dominante + accent ----------
put(TM['dom'],air(TM['domE']-TM['dom']+0.2,250,800,2),0.06,0.2,0.5); put(TM['domE'],tock(150),0.035,0.4,0.35)
put(TM['tadam'],wav('tadam'),0.17,0,0.35)
for f,d in [(261.6,0),(329.6,0.06),(392,0.12)]: put(TM['tadam']+0.6+d,keys(f,4.5),0.022,0,0.8)
# ---------- désaturer ----------
put(TM['back'],air(TM['backE']-TM['back']+0.2,220,900,2),0.06,0,0.5)
put(TM['backE']-0.1,shimmer(TM['desatE']-TM['backE']+0.1),0.03,0.2,0.4)
put(TM['desat'],pencil(TM['desatE']-TM['desat'],sp),0.08,0.3,0.3)
put(TM['bip'],wav('bip'),0.15,0.1,0.35); put(TM['bip']+0.03,keys(523.3,3,1.2),0.024,0.1,0.7)
# ---------- fin : signature ----------
put(TM['end']-0.1,air(1.0,200,1000),0.12,0,0.6)
put(TM['hero']+0.2,air(1.2,300,1200,2),0.07,0.2,0.6)
put(TM['end']+0.28,pencil(0.95,sp),0.3,0,0.25); put(TM['end']+1.04,pencil(0.36,sp),0.22,0.05,0.25)
put(TM['land']-0.01,wav('bip'),0.16,0.15,0.4); put(TM['land']+0.02,keys(880,4,1.8),0.035,0.2,0.8); put(TM['land']+0.04,keys(659.3,4,1.8),0.025,-0.2,0.8)
put(TM['end']+1.0,click(1000),0.025,0,0.5)
# ---------- réverbe (IR synthétique ~1,2 s) ----------
ir_t=T(2.0); ir=lp(rng.standard_normal(len(ir_t)),4000)*np.exp(-ir_t/0.35); ir2=lp(rng.standard_normal(len(ir_t)),4000)*np.exp(-ir_t/0.35)
def conv(x,h):
    n=len(x)+len(h); nf=1<<int(np.ceil(np.log2(n))); return np.fft.irfft(np.fft.rfft(x,nf)*np.fft.rfft(h,nf),nf)[:len(x)]
wet=np.stack([conv(send[:,0],ir),conv(send[:,1],ir2)],1); wet/=np.max(np.abs(wet))+1e-9; wet*=np.max(np.abs(send))*0.9
out=dry+wet*0.55
out=np.stack([lp(out[:,0],9000),lp(out[:,1],9000)],1)
fn=int(0.6*SR); fade=np.ones(N); fade[-fn:]=np.linspace(1,0.2,fn)       # la nappe sonne encore quand la boucle repart
out*=fade[:,None]; out=np.tanh(out*0.8)/np.tanh(0.8); out/=np.max(np.abs(out))*1.12
w=wave.open('audio.wav','wb'); w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR)
w.writeframes((out*32767).astype('<i2').tobytes()); w.close(); print('ok')
