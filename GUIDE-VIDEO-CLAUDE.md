# GUIDE VIDÉO HC STUDIO (à lire par Claude avant toute vidéo)

Ce guide est écrit par Claude pour Claude. Quand Gabriel écrit « vidéo : [sujet] », relis-le en entier, puis suis-le à la lettre.
La vidéo de référence est `medias/motion/reel-regle-180-v3.mp4`, validée le 4 oct. 2026 (« c dla frappe, vraiment bien »). Ses sources complètes sont dans `motion-source/regle-180-v3/`.

## 0. Contexte

- **Le compte :** @horscadre.studioo (HC Studio) est un compte d'astuces anonyme, dans la niche création / médiamatique (vidéo, design, web).
  - Ce n'est pas une agence : pas de pitch client, pas de « écris-nous ».
- **La langue :** tu réponds à Gabriel en français. Il écrit vite et en abrégé.
- **Le budget :** tout doit être gratuit. Pas de service payant, pas de banque de sons, pas de voix payante.
- **Les posts déjà programmés dans Metricool :** on n'y touche pas.
- **Le réseau du cloud :** Instagram, Reddit et huggingface sont bloqués. Pour une référence, demande des captures ou un enregistrement d'écran.

## 1. Historique de ses retours (pour comprendre ses goûts)

1. v1 : « pas assez dynamique ».
2. v2 : rapide, slams, shakes, sons de jouet/marimba. Il l'a rejetée : « fait enfant, trop rapide, on arrive pas à lire ».
3. v3 : premium, lent, son cinéma doux. Retour : « ça donne vraiment bien ».
4. La voix TTS a été rejetée : « horrible la voix ». Donc **pas de voix**.
5. Un fond brun ou merlot l'a fait réagir : « garde tout en bordeaux ».
6. Sur le 1er reel 180°, il a trouvé l'intro trop longue (le sujet arrivait à 15 s). Il veut quand même la méthode PVSE, mais invisible.
7. Il a envoyé une référence « super qualitatif » (pub « Claude Cooked ») en demandant « pareil mais avec mes critères ». Son analyse est dans `motion-source/charte-qualite-reference.json`.
8. Le reel 180° v3 a été validé.

## 2. Couleurs et typo

- **Couleurs autorisées :**
  - bordeaux `#5C0F1E` ;
  - blanc cassé `#F7F3F1` ;
  - merlot `#1C0509`, seulement en touche rare.
- **Couleurs interdites :** brun, orange, rose poudré, gris neutre, noir pur, bleu bébé (il l'a essayé puis refusé).
  - Les ombres et dégradés sont teintés bordeaux.
- **Vérification couleur :** échantillonne des images du rendu. Tout pixel saturé doit avoir une teinte entre 335° et 360° ou entre 0° et 10°.
- **Polices :**
  - Bricolage Grotesque : mots clés en gras condensé, le reste de la phrase en light (contraste gras/léger).
  - Geist Mono : labels, chiffres, HUD, timecodes.
  - Les fichiers sont dans `regle-180-v3/fonts`.
- **Logo de fin :** la vraie signature « hc. » (fichiers dans `medias/logo/`). Jamais un faux logo.

## 3. Lisibilité (règle n°1, c'est ce qui a tué la v2)

- **Durée minimale à l'écran :** chaque texte reste au moins 0,8 s + 0,3 s par mot.
  - Le compte part du moment où le texte est **net**, pas du début de l'animation.
  - Calcule-le pour chaque ligne avant de rendre.
- **Un seul titre à l'écran à la fois.** 8 mots maximum par titre.
- **Labels :** au moins 25-28 px, avec un liseré bordeaux autour du texte quand il passe sur une image.
- **Zone sûre :**
  - contenu entre y 270 et y 1250 ;
  - sous y 1050, rien au-delà de x 936 (boutons like/commentaire d'Instagram) ;
  - rien d'important tout en bas (légende Instagram).
- **Fin :**
  - une question à l'audience ;
  - puis « Envoie-moi « MOTION » en message » ;
  - le tout tenu au moins 3 s une fois net.

## 4. Style et rythme

- **Ton :** premium et calme, façon Apple. Chaque écran dure environ 3 s minimum.
  - Interdit : slam, shake, glitch, whip pan, zooms brutaux.
- **Apparition du texte :** mot par mot, du flou au net, avec un léger décalage vertical.
  - Courbes de mouvement ease-in-out douces. Rien ne claque.
- **Densité :** elle vient de la profondeur, pas de la vitesse.
  - Décor en 2,5D : sol en perspective avec une grille de points, une flaque de lumière, des poussières qui flottent, du grain.
  - La caméra est toujours un peu vivante : grue, dérive lente.
  - Les transitions se font par transformation d'un objet (élément partagé). Une seule vraie coupe maximum.
- **Image littérale :** chaque phrase a une image littérale. Teste-la en coupant le son et en cachant le texte : l'image seule doit raconter.
  - Exemples dans le 180° : le soulignement de « le fil » tombe et devient l'axe ; des cartes viseur sortent des caméras ; le ✕ se transforme en ✓ ; « s'inversent » se retourne comme un miroir.
- **Micro-détails vrais :** REC, timecode qui défile, cadre de mise au point, label CAM, valeurs réelles.
- **Durée totale :** environ 25-35 s. Le 180° v3 fait 28,7 s.

## 5. Script : méthode PVSE (invisible)

Structure demandée par Gabriel :
- **Promesse ;**
- **Validation :** faits ou sources vraies ;
- **Structure :** annoncer ce qui vient ;
- **Enjeux :** ce qu'on rate si on part.

Comment l'appliquer :
- Le sujet est à l'écran dès la 1re image, avec le label du thème déjà visible (ex. « RÈGLE DES 180° »).
- Les quatre étapes passent dans les titres et les images, condensées sur les premières secondes.
  - Jamais d'écran « La promesse », « Au programme » ou « Reste jusqu'au bout ».
- Uniquement des infos vraies et vérifiables. Aucun faux chiffre, client ou projet.
- Déroulé type :
  1. accroche avec le sujet ;
  2. montrer le problème (Point se trompe) ;
  3. pourquoi ;
  4. la solution (Point réussit) ;
  5. question + CTA MOTION ;
  6. Point devient le point de « hc. ».

## 6. Point, la mascotte

- **Rôle :** protagoniste et cobaye. Il tente, se trompe, réagit, puis réussit. Dans le 180°, il est CAM 2, la caméra à l'épaule.
- **Apparence :**
  - corps en cercle, yeux seulement, pas de bouche ;
  - membres au trait ;
  - il ne parle jamais.
- **Il est vivant :** il respire (léger scale), cligne des yeux et regarde ce qui compte.
- **Réactions :**
  - surpris « ! » + son oh ;
  - ennuyé + son pfff ;
  - content + son tadam ;
  - sons hm (réflexion) et bip (atterrissage).
  - Les fichiers sont dans `motion-source/mascot/`.
- **Jamais de clone de Point.** Les autres personnages ont d'autres formes (A = carré arrondi, B = gélule) avec le même style d'yeux.
- **À la fin,** il vole dans la signature et devient le point de « hc. ».
- **Board :** `insta-identite/mascotte/mascotte-point-brand-board.png` (fichiers du projet).

## 7. Son (tout synthétisé en numpy, gratuit)

- Pas de voix.
- **Nappe :** douce (saw désaccordées + passe-bas lent), présente dès la 1re image pour que la boucle Instagram ne saute pas. Une progression d'accords suit les étapes du récit.
- **Rythme :** pulsation feutrée de la nappe (environ 90 BPM). Pas de batterie.
- **Point au premier plan :** ses 5 sons passent devant le reste.
- **Effets :** très doux, calés sur l'image (souffle, toc de bois, clic, crayon).
  - Pas de boum, pas de montée (riser), pas de marimba, pas de sons de jouet.
- **Spatialisation :** panoramique selon la position x à l'écran, réverbe synthétique d'environ 1,2 s.
- **Master :** -14 LUFS intégré, crête à -1,5 dB.
- **Calage :** les temps de l'image (objet `T` dans scene.html) sont exportés dans `times.json`, et `synth.py` les lit. Une seule source de vérité pour le timing.

## 8. Pipeline technique

1. **Scène :** `scene.html` en 1080x1920. Elle expose `window.render(t)`, une fonction pure du temps, sans animation CSS libre.
   - La 2,5D est une projection perspective JS maison (`pr(X,Y,Z)`, `camAt(t)`).
   - Sol et poussières sont dessinés en canvas, les personnages en SVG (`chr()`).
2. **Rendu image :** `node reel.js scene.html out.mp4 <secondes> 60`.
   - Playwright capture chaque image, ffmpeg encode en crf 14 (master).
   - Chromium : `/opt/pw-browsers/...`. Ne jamais lancer `playwright install`.
3. **Son :** `python3 synth.py` produit `audio.wav`. Il lit `times.json` et `../mascot/point-*.wav`.
4. **Mix :** mux vidéo + audio, normalisation -14 LUFS (loudnorm).
5. **Livraison :**
   - encodage crf 20 (environ 15 Mo) en h264 yuv420p, faststart, AAC ;
   - plus une cover JPG ;
   - dépôt dans `medias/motion/` (GitHub) et dans `/mnt/project-files/insta-identite/motion/`.
6. **Publication :** via Metricool, seulement si Gabriel le demande. « Mets-le sur GitHub » veut dire GitHub seulement, pas Instagram.

## 9. Contrôle avant livraison (obligatoire)

Fais une revue sous 4 angles, idéalement avec des agents séparés et une vérification adversariale.
1. **Lisibilité :** mesure le temps net de chaque texte, les tailles, la zone sûre.
2. **Logique et pédagogie :** chaque image est-elle juste et littérale ? Le sujet arrive-t-il tout de suite ? Les faits sont-ils vrais ?
3. **Direction artistique et couleurs :** lint des teintes, rien d'enfantin, pas de clone.
4. **Son :** nappe dès 0 s, pas de son interdit, -14 LUFS, synchro avec l'image.

Corrige tout ce qui est confirmé, puis re-rends. Regarde des captures toutes les 0,5 s avant d'envoyer.

## 10. Sujets possibles (astuces vraies)

Règle des tiers, 60-30-10, J-cut/L-cut, 180° (déjà fait), raccord dans le mouvement, contraste typo, hiérarchie visuelle, règle des 3 polices, plan d'ensemble / plan moyen / gros plan, kerning, etc.
Vérifie toujours le contenu avant de le montrer.
