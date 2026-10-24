# Son « Espace blanc » : même méthode que le reel 180° v3.
# Nappe douce dès la 1re image, pulsation feutrée sans batterie, sons de Point au premier plan,
# effets doux (pas de boum, pas de montée, pas de marimba).
import numpy as np, wave, json
from scipy.signal import lfilter
TM=json.load(open('times.json'))
SR=48000; DUR=TM['dur']; N=int(SR*DUR)
dry=np.zeros((N,2)); send=np.zeros((N,2)); rng=np.random.default_rng(29)
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
    w=wave.open(f'../mascot/point-{name}.wav'); return np.frombuffer(w.readframes(w.getnframes()),'<i2').astype(float)/32768
# ---------- nappe ----------
t=np.arange(N)/SR
def saw(f): return 2*((t*f)%1)-1
prog=[(0,[110,164.8,261.6,329.6,493.9]),           # la m9 : Point est écrasé
      (TM['open'],[87.3,130.8,261.6,329.6,392]),    # fa maj7 : l'espace s'ouvre
      (TM['h3'],[65.4,130.8,246.9,329.6,392]),      # do maj7 : les marges
      (TM['h4'],[73.4,146.8,261.6,349.2,440]),      # ré m7 : les groupes
      (TM['snap'],[65.4,130.8,246.9,329.6,392,587.3]), # do maj9 : écarts constants
      (TM['end'],[110,164.8,261.6,329.6,493.9]),    # la m9 : fin
      (TM['land'],[87.3,130.8,261.6,329.6,392,523.3])]  # fa maj9 : signature
pad=np.zeros(N)
for k,(a,ch) in enumerate(prog):
    b=prog[k+1][0] if k+1<len(prog) else DUR+2
    env=np.clip(np.minimum((t-(a-0.5))/1.0+(1 if k==0 else 0),(b+0.5-t)/1.0),0,1)
    pad+=sum(saw(f*1.003)+saw(f*0.997) for f in ch)/len(ch)/2*env
cut=480+340*(0.5+0.5*np.sin(2*np.pi*t/10))+np.where(t<TM['open'],-120,0)+np.where((t>TM['tad'])&(t<TM['end']),300,0)
pad=lp(lp(pad,cut),cut)
bt=60/90
swell=np.clip(0.7+t/2.0,0,1)                                             # déjà là à la 1re image
gate=1-0.10*np.exp(-((t)%(2*bt))/0.3)*(t<TM['end'])                      # pulsation feutrée 90 BPM
PT=[TM['pfff'],TM['oh'],TM['landF'],TM['hm'],TM['tad'],TM['land']]
duck=np.ones(N)
for a in PT: duck-=0.35*np.clip(np.minimum((t-a+0.05)/0.05,1),0,1)*np.exp(-np.clip(t-a-0.4,0,None)/0.3)*(t>a-0.05)
duck=np.clip(duck,0.6,1)
L=pad*swell*gate*duck*0.17
dry[:,0]+=L; dry[:,1]+=L; send[:,0]+=L*0.6; send[:,1]+=L*0.6
# ---------- accroche : Point écrasé ----------
put(0.0,keys(220,5),0.045,-0.2,0.7); put(0.3,keys(329.6,5),0.03,0.2,0.7)
put(0.15,air(0.7,200,700,2),0.06,0.1,0.5)
put(TM['pfff'],wav('pfff'),0.19,0.1,0.3)
for k in range(3): put(1.9+k*0.45,tock(150+6*k),0.03,0.1,0.25)            # il pousse, ça ne bouge pas
put(TM['push'],air(0.8,200,800,2),0.06,0.1,0.4)
# ---------- l'espace s'ouvre ----------
put(TM['open']-0.1,air(1.3,250,1100,2),0.12,0,0.6)
put(TM['oh'],wav('oh'),0.17,0.0,0.3)
for i in range(5): put(TM['open']+0.9+i*0.08,tock(170+8*i),0.03,0.25,0.3)   # les blocs se posent
put(TM['landF'],wav('bip'),0.15,-0.55,0.35)
for c in [TM['h3'],TM['h4'],TM['h5']]: put(c-0.15,air(0.7,250,1000),0.08,0.2 if int(c)%2 else -0.2,0.6)   # changements de titre
# ---------- marges ----------
put(TM['marg'],air(1.1,200,900,2),0.09,0.2,0.5)
put(TM['marg']+0.2,click(1250),0.03,0.25,0.4); put(TM['marg']+0.25,keys(523.3,3,1.2),0.025,0.25,0.7)
# ---------- groupes ----------
put(TM['hm'],wav('hm'),0.16,-0.55,0.35)
put(TM['group'],air(1.2,250,1000,2),0.1,0.2,0.5)
for k in range(3): put(TM['outl']+k*0.15,click(1150+80*k),0.03,0.25,0.4); put(TM['outl']+k*0.15,keys([523.3,587.3,659.3][k],3,1.2),0.022,0.25,0.7)
# ---------- écarts constants ----------
for k in range(4): put(TM['labs']+k*0.12,click(1300),0.025,0.45,0.4)
put(TM['snap'],air(0.9,300,1200,2),0.08,0.3,0.5)
for k in range(4): put(TM['snap']+0.55+k*0.05,tock(190+10*k),0.035,0.45,0.3)
put(TM['tad'],wav('tadam'),0.17,-0.5,0.35)
for f,d in [(261.6,0),(329.6,0.06),(392,0.12)]: put(TM['tad']+0.5+d,keys(f,4.5),0.025,0,0.8)
# ---------- fin : signature ----------
put(TM['end']-0.1,air(1.0,200,1000),0.12,0,0.6)
put(TM['hero']+0.2,air(1.2,300,1200,2),0.07,0.2,0.6)
sp2=lambda u: np.sin(np.pi*np.clip(u,0,1))**0.7
put(TM['end']+0.28,pencil(0.95,sp2),0.3,0,0.25); put(TM['end']+1.04,pencil(0.36,sp2),0.22,0.05,0.25)
put(TM['land']-0.01,wav('bip'),0.16,0.15,0.4); put(TM['land']+0.02,keys(880,4,1.8),0.035,0.2,0.8); put(TM['land']+0.04,keys(659.3,4,1.8),0.025,-0.2,0.8)
put(TM['end']+1.36,click(1000),0.025,0,0.5)
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
