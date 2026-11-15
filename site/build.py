"""Génère le site (docs/) en français et en anglais à partir d'une seule source.

Usage : python site/build.py
Les pages partagent l'en-tête, le pied de page et les métadonnées ; le contenu de chaque page est écrit
ici dans les deux langues, côte à côte, pour qu'elles restent alignées. Les captures d'écran sont dans
docs/assets/shots/<langue>/ (vraies captures de l'application, thème clair).
"""
from datetime import date
from html import escape
from pathlib import Path

DOCS = Path(__file__).resolve().parent.parent / "docs"
BASE = "https://mikedns.github.io/TranscriPilote/"
RELEASES = "https://github.com/MikeDns/TranscriPilote/releases"
LATEST = RELEASES + "/latest"
ISSUES = "https://github.com/MikeDns/TranscriPilote/issues/new/choose"
CONTACT = "https://mikedansou.me/contact/"
LICENSE = "https://github.com/MikeDns/TranscriPilote/blob/main/LICENSE"
NOTICES = "https://github.com/MikeDns/TranscriPilote/blob/main/THIRD_PARTY_NOTICES.md"
PUBLISHER = "MikeDns Labs"
CSP = ("default-src 'self'; script-src 'self' 'sha256-Du+OJKJSbdUgz5nrHeWWINvez6XKDDU/tyj/5c2uvwo='; "
       "style-src 'self'; style-src-attr 'unsafe-inline'; img-src 'self' data:; font-src 'self'; "
       "connect-src https://api.github.com https://nujxmiqbaxgrnvmjyecu.supabase.co; object-src 'none'; "
       "base-uri 'self'; form-action 'self'; upgrade-insecure-requests")

# Pages : clé -> (fichier fr, fichier en)
PAGES = {
    "home": ("index.html", "en/index.html"),
    "features": ("fonctionnalites.html", "en/features.html"),
    "download": ("telecharger.html", "en/download.html"),
    "news": ("nouveautes.html", "en/whats-new.html"),
    "faq": ("faq.html", "en/faq.html"),
    "privacy": ("confidentialite.html", "en/privacy.html"),
    "legal": ("mentions-legales.html", "en/legal.html"),
}
REDIRECTS = {"avantages.html": "./#pourquoi", "en/benefits.html": "./#why"}

DOWNLOAD_ICON = ('<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" '
                 'stroke-linejoin="round" aria-hidden="true"><path d="M12 3v12M7 10l5 5 5-5M5 21h14"/></svg>')


def href(lang, key, anchor=""):
    """Lien relatif d'une page vers une autre, dans la même langue."""
    target = PAGES[key][0 if lang == "fr" else 1]
    if lang == "en":
        target = target[3:]
    if target == "index.html":
        target = "./"
    return target + anchor


def abs_url(path):
    return BASE + ("" if path == "index.html" else "en/" if path == "en/index.html" else path)


def shot(lang, name, alt, cls="shot", eager=False):
    pre = "" if lang == "fr" else "../"
    loading = "eager" if eager else "lazy"
    return (f'<figure class="{cls}"><div class="window"><div class="window-bar" aria-hidden="true"><span></span><span></span><span></span></div>'
            f'<img src="{pre}assets/shots/{lang}/{name}.webp" alt="{escape(alt)}" width="1280" height="800" loading="{loading}" decoding="async"></div></figure>')


def download_button(lang, label=None):
    label = label or ("Télécharger pour Windows" if lang == "fr" else "Download for Windows")
    return f'<a class="btn btn-primary btn-lg" data-download href="{LATEST}">{DOWNLOAD_ICON}{label}</a>'


# ---------------------------------------------------------------------------------------------------
# En-tête, pied de page
# ---------------------------------------------------------------------------------------------------

def header(lang, key):
    t = {
        "fr": dict(features="Fonctionnalités", news="Nouveautés", faq="Aide", download="Télécharger", menu="Ouvrir le menu",
                   nav="Navigation principale", by=f"par {PUBLISHER}", group="Langue"),
        "en": dict(features="Features", news="What's new", faq="Help", download="Download", menu="Open menu",
                   nav="Main navigation", by=f"by {PUBLISHER}", group="Language"),
    }[lang]
    pre = "" if lang == "fr" else "../"
    cur = lambda k: ' aria-current="page"' if k == key else ""
    fr_file, en_file = PAGES[key]
    if lang == "fr":
        switch = (f'<span aria-current="true">FR</span><a href="{en_file}" hreflang="en" lang="en" title="English version">EN</a>')
    else:
        other = "../" if fr_file == "index.html" else "../" + fr_file
        switch = (f'<a href="{other}" hreflang="fr" lang="fr" title="Version française">FR</a><span aria-current="true">EN</span>')
    return f'''<header class="site-header"><div class="wrap">
    <a class="brand" href="{href(lang, 'home')}"><img src="{pre}assets/icon.svg" alt="" width="30" height="30"><span class="brand-text"><span class="brand-name">TranscriPilote</span><span class="brand-by">{t['by']}</span></span></a>
    <button class="nav-toggle" type="button" aria-label="{t['menu']}" aria-expanded="false"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><path d="M4 7h16M4 12h16M4 17h16"/></svg></button>
    <nav class="site-nav" aria-label="{t['nav']}">
        <a href="{href(lang, 'features')}"{cur('features')}>{t['features']}</a>
        <a href="{href(lang, 'news')}"{cur('news')}>{t['news']}</a>
        <a href="{href(lang, 'faq')}"{cur('faq')}>{t['faq']}</a>
        <div class="lang-switch" role="group" aria-label="{t['group']}">{switch}</div>
        <a class="btn btn-primary" href="{href(lang, 'download')}"{cur('download')}>{t['download']}</a>
    </nav>
</div></header>'''


def footer(lang):
    if lang == "fr":
        cols = [
            ("Produit", [("Fonctionnalités", href(lang, "features")), ("Nouveautés", href(lang, "news")),
                         ("Télécharger", href(lang, "download")), ("Configuration requise", href(lang, "download", "#configuration")),
                         ("Toutes les versions", RELEASES)]),
            ("Aide", [("Questions fréquentes", href(lang, "faq")), ("Signaler un problème", ISSUES), ("Contact", CONTACT)]),
            ("Informations légales", [("Conditions d'utilisation", LICENSE), ("Confidentialité", href(lang, "privacy")),
                                      ("Mentions légales", href(lang, "legal")), ("Composants tiers", NOTICES)]),
        ]
        about = (f"TranscriPilote est un logiciel gratuit pour Windows, édité par {PUBLISHER}. "
                 "Conçu et maintenu par Mike DANSOU.")
        copy = f"© 2026 {PUBLISHER}. Tous droits réservés."
    else:
        cols = [
            ("Product", [("Features", href(lang, "features")), ("What's new", href(lang, "news")),
                         ("Download", href(lang, "download")), ("System requirements", href(lang, "download", "#requirements")),
                         ("All releases", RELEASES)]),
            ("Help", [("FAQ", href(lang, "faq")), ("Report a problem", ISSUES), ("Contact", CONTACT)]),
            ("Legal", [("Terms of use", LICENSE), ("Privacy", href(lang, "privacy")),
                       ("Legal notice", href(lang, "legal")), ("Third-party components", NOTICES)]),
        ]
        about = (f"TranscriPilote is free software for Windows, published by {PUBLISHER}. "
                 "Designed and maintained by Mike DANSOU.")
        copy = f"© 2026 {PUBLISHER}. All rights reserved."
    pre = "" if lang == "fr" else "../"
    columns = "".join(
        f'<div class="footer-col"><h2>{title}</h2><ul>' + "".join(f'<li><a href="{u}">{escape(n)}</a></li>' for n, u in links)
        + "</ul></div>" for title, links in cols)
    return f'''<footer class="site-footer"><div class="wrap">
    <div class="footer-top">
        <div class="footer-about"><a class="brand" href="{href(lang, 'home')}"><img src="{pre}assets/icon.svg" alt="" width="28" height="28"><span class="brand-name">TranscriPilote</span></a>
            <p>{about}</p></div>
        {columns}
    </div>
    <div class="footer-bottom"><span>{copy}</span></div>
</div></footer>'''


def page(lang, key, title, description, body, extra_head=""):
    fr_file, en_file = PAGES[key]
    me = fr_file if lang == "fr" else en_file
    pre = "" if lang == "fr" else "../"
    og_locale = "fr_FR" if lang == "fr" else "en_GB"
    return f'''<!doctype html>
<html lang="{lang}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{escape(title)}</title>
<meta name="description" content="{escape(description)}">
<link rel="canonical" href="{abs_url(me)}">
<link rel="alternate" hreflang="fr" href="{abs_url(fr_file)}">
<link rel="alternate" hreflang="en" href="{abs_url(en_file)}">
<link rel="alternate" hreflang="x-default" href="{abs_url(fr_file)}">
<meta name="author" content="Mike DANSOU">
<meta name="publisher" content="{PUBLISHER}">
<meta name="google-site-verification" content="O0swOZqCXVkIEmv03IDjbLMx8_pzLGd5VeqcyB9ZoxQ">
<meta name="robots" content="index, follow, max-image-preview:large">
<meta name="theme-color" content="#ffffff">
<link rel="icon" href="{pre}assets/icon.svg" type="image/svg+xml">
<link rel="icon" href="{pre}assets/icon.png" type="image/png">
<link rel="apple-touch-icon" href="{pre}assets/icon.png">
<meta property="og:type" content="website">
<meta property="og:locale" content="{og_locale}">
<meta property="og:site_name" content="TranscriPilote">
<meta property="og:title" content="{escape(title)}">
<meta property="og:description" content="{escape(description)}">
<meta property="og:url" content="{abs_url(me)}">
<meta property="og:image" content="{BASE}assets/social-preview.png">
<meta property="og:image:width" content="1280">
<meta property="og:image:height" content="640">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:image" content="{BASE}assets/social-preview.png">
<script>document.documentElement.classList.add('js')</script>
<meta http-equiv="Content-Security-Policy" content="{CSP}">
<meta name="referrer" content="strict-origin-when-cross-origin">
<link rel="stylesheet" href="{pre}assets/site.css">
<script src="{pre}assets/site.js" defer></script>
{extra_head}</head>
<body>
<a class="skip" href="#contenu">{"Aller au contenu" if lang == "fr" else "Skip to content"}</a>
{header(lang, key)}
<main id="contenu">
{body}
</main>
{footer(lang)}
</body>
</html>
'''


def jsonld(lang):
    desc = ("Application Windows gratuite de transcription, de résumé et d'analyse de réunions, qui fonctionne entièrement sur le PC, hors ligne."
            if lang == "fr" else
            "Free Windows app that transcribes, summarizes and analyses meetings, entirely on the PC, offline.")
    url = BASE if lang == "fr" else BASE + "en/"
    return f'''<script type="application/ld+json">
{{
  "@context": "https://schema.org",
  "@graph": [
    {{ "@type": "WebSite", "@id": "{url}#site", "name": "TranscriPilote", "url": "{url}", "inLanguage": "{lang}",
       "alternateName": ["Transcri Pilote", "Transcrit Pilote"] }},
    {{ "@type": "Organization", "@id": "{BASE}#publisher", "name": "{PUBLISHER}", "url": "{BASE}",
       "founder": {{ "@type": "Person", "name": "Mike DANSOU", "url": "https://github.com/MikeDns" }} }},
    {{ "@type": "SoftwareApplication", "@id": "{url}#app", "name": "TranscriPilote",
       "alternateName": ["Transcri Pilote", "Transcrit Pilote", "TranscriPilot"],
       "description": "{desc}", "applicationCategory": "BusinessApplication",
       "operatingSystem": "Windows 10, Windows 11", "inLanguage": ["fr", "en"], "isAccessibleForFree": true,
       "offers": {{ "@type": "Offer", "price": "0", "priceCurrency": "EUR" }},
       "downloadUrl": "{LATEST}", "url": "{url}", "image": "{BASE}assets/social-preview.png",
       "publisher": {{ "@id": "{BASE}#publisher" }},
       "author": {{ "@type": "Person", "name": "Mike DANSOU", "url": "https://github.com/MikeDns" }} }}
  ]
}}
</script>
'''


# ---------------------------------------------------------------------------------------------------
# Contenu
# ---------------------------------------------------------------------------------------------------

def home(lang):
    if lang == "fr":
        title = "TranscriPilote – Transcription et résumé de réunions, sur votre PC"
        desc = ("TranscriPilote transcrit, résume et analyse vos réunions Teams, Zoom ou en salle, directement sur votre PC Windows. "
                "Gratuit, hors ligne, sans compte ni droits administrateur.")
        T = dict(
            announce=('<a class="announce" href="nouveautes.html">Nouveau dans la version 2.2 : la dictée sans Internet</a>'),
            h1="Vos réunions, transcrites et résumées sur votre ordinateur.",
            lead=("TranscriPilote enregistre vos réunions Teams, Zoom, Meet ou en salle, les transcrit, en tire un résumé "
                  "et répond à vos questions. Tout se passe sur votre PC Windows : aucun compte, aucun abonnement, "
                  "aucune réunion envoyée sur Internet."),
            meta="Windows 10 et 11, gratuit",
            more="Voir les fonctionnalités",
            hero_alt="TranscriPilote affichant la transcription horodatée d'une réunion d'équipe",
            facts=[("Traité sur votre PC", "Transcription, résumé et questions tournent sur votre processeur."),
                   ("Sans carte graphique", "Un PC portable ordinaire suffit, sans droits administrateur."),
                   ("Français et anglais", "L'application, les transcriptions et les résumés.")],
            flow_title="De la réunion aux décisions",
            flow_lead="Quatre étapes, du premier mot prononcé à la liste des actions à faire.",
            flow=[("recorder", "Enregistrez", "Une réunion en ligne (Teams, Zoom, Meet), une réunion en salle au micro, ou un fichier audio ou vidéo existant. TranscriPilote suit le casque ou les haut-parleurs si vous en changez en cours de route.",
                   "L'écran Enregistrement de TranscriPilote"),
                  ("transcription", "Transcrivez", "La parole devient un texte horodaté, fidèle, même sur un processeur de plusieurs années. Une transcription interrompue reprend là où elle s'était arrêtée.",
                   "Une transcription horodatée"),
                  ("summary", "Résumez", "Une IA installée sur votre PC rédige le résumé, les points clés et les actions à faire. Ajoutez le nom des participants pour un résultat plus juste.",
                   "Le résumé d'une réunion, avec ses points clés et ses actions"),
                  ("discussion", "Interrogez", "Posez vos questions à la réunion : « qui relit les textes, et pour quand ? ». Les réponses s'appuient uniquement sur ce qui s'y est dit.",
                   "Une question posée à une réunion et la réponse de l'IA")],
            new_title="Pensé pour les vraies journées de travail",
            news=[("Une réunion oubliée en marche ?", "Choisissez la partie utile à l'heure près, transcrivez seulement elle, ou coupez l'enregistrement."),
                  ("Dictée sans Internet", "Un bouton micro écrit vos questions et vos consignes pendant que vous parlez."),
                  ("Rien ne s'interrompt", "Ni une mise à jour, ni une fermeture de fenêtre, ni une coupure de courant ne fait perdre un travail en cours."),
                  ("Arrêt automatique, si vous le voulez", "Quand plus personne ne parle, ou après une durée maximale. Désactivé par défaut, et discret.")],
            privacy_title="Vos réunions restent chez vous.",
            privacy_lead="Rien de ce qui se dit en réunion ne quitte votre ordinateur. TranscriPilote ne se connecte à Internet que pour :",
            privacy_list=["vérifier qu'une nouvelle version existe, sur GitHub ;",
                          "télécharger une fois les modèles de transcription, au premier usage ;",
                          "copier vos données vers votre propre Google Drive ou OneDrive, si vous activez la sauvegarde."],
            privacy_link="Lire la politique de confidentialité",
            why_title="Face aux services de transcription en ligne",
            compare=[("", "TranscriPilote", "Services en ligne habituels"),
                     ("Où sont traitées vos réunions", "Sur votre PC", "Sur des serveurs distants"),
                     ("Prix", "Gratuit, sans limite", "Abonnement ou quota de minutes"),
                     ("Compte à créer", "Aucun", "Obligatoire"),
                     ("Fonctionne hors connexion", "Oui", "Non"),
                     ("Questions sur la réunion", "Oui, en local", "Selon l'offre")],
            cta_title="Essayez-le sur votre prochaine réunion.",
            cta_lead="Gratuit, sans inscription. L'installation prend quelques minutes, dans votre profil Windows.",
            why_id="pourquoi",
        )
    else:
        title = "TranscriPilote – Meeting transcription and summaries, on your PC"
        desc = ("TranscriPilote transcribes, summarizes and analyses your Teams, Zoom or in-room meetings, right on your Windows PC. "
                "Free, offline, no account or admin rights needed.")
        T = dict(
            announce=('<a class="announce" href="whats-new.html">New in version 2.2: offline dictation</a>'),
            h1="Your meetings, transcribed and summarized on your own computer.",
            lead=("TranscriPilote records your Teams, Zoom, Meet or in-room meetings, transcribes them, writes a summary "
                  "and answers your questions. Everything happens on your Windows PC: no account, no subscription, "
                  "no meeting sent over the Internet."),
            meta="Windows 10 and 11, free",
            more="See all features",
            hero_alt="TranscriPilote showing the timestamped transcript of a team meeting",
            facts=[("Processed on your PC", "Transcription, summaries and questions run on your processor."),
                   ("No graphics card", "An ordinary laptop is enough, with no admin rights."),
                   ("English and French", "The app, the transcripts and the summaries.")],
            flow_title="From meeting to decisions",
            flow_lead="Four steps, from the first spoken word to the list of action items.",
            flow=[("recorder", "Record", "An online meeting (Teams, Zoom, Meet), an in-room meeting with the microphone, or an existing audio or video file. TranscriPilote follows your headset or speakers if you switch during the meeting.",
                   "The TranscriPilote Recording screen"),
                  ("transcription", "Transcribe", "Speech becomes accurate, timestamped text, even on a processor several years old. An interrupted transcription resumes where it stopped.",
                   "A timestamped transcript"),
                  ("summary", "Summarize", "An AI installed on your PC writes the summary, key points and action items. Add the participants' names for a more accurate result.",
                   "A meeting summary with key points and action items"),
                  ("discussion", "Ask", "Ask the meeting your questions: “who is proofreading the copy, and by when?”. Answers rely only on what was said.",
                   "A question asked to a meeting and the AI's answer")],
            new_title="Built for real working days",
            news=[("Forgot to stop a recording?", "Pick the useful part to the minute, transcribe only that part, or cut the recording."),
                  ("Offline dictation", "A microphone button writes your questions and instructions as you speak."),
                  ("Nothing gets interrupted", "No update, closed window or power cut makes you lose work in progress."),
                  ("Automatic stop, if you want it", "When nobody is speaking any more, or after a maximum duration. Off by default, and discreet.")],
            privacy_title="Your meetings stay with you.",
            privacy_lead="Nothing said in a meeting leaves your computer. TranscriPilote only connects to the Internet to:",
            privacy_list=["check whether a new version exists, on GitHub;",
                          "download the transcription models once, on first use;",
                          "copy your data to your own Google Drive or OneDrive, if you turn on backup."],
            privacy_link="Read the privacy policy",
            why_title="Compared with online transcription services",
            compare=[("", "TranscriPilote", "Typical online services"),
                     ("Where your meetings are processed", "On your PC", "On remote servers"),
                     ("Price", "Free, no limits", "Subscription or minute quota"),
                     ("Account required", "None", "Mandatory"),
                     ("Works offline", "Yes", "No"),
                     ("Questions about the meeting", "Yes, locally", "Depends on the plan")],
            cta_title="Try it on your next meeting.",
            cta_lead="Free, no sign-up. Installation takes a few minutes, in your Windows profile.",
            why_id="why",
        )
    facts = "".join(f'<li><strong>{a}</strong><span>{b}</span></li>' for a, b in T["facts"])
    flow = "".join(
        f'''<li class="flow-row">
            <div class="flow-text"><span class="flow-num">{i}</span><h3>{h}</h3><p>{p}</p></div>
            {shot(lang, img, alt)}
        </li>''' for i, (img, h, p, alt) in enumerate(T["flow"], 1))
    news = "".join(f'<div class="note"><h3>{a}</h3><p>{b}</p></div>' for a, b in T["news"])
    plist = "".join(f"<li>{x}</li>" for x in T["privacy_list"])
    head, *rows = T["compare"]
    table = (f'<table class="compare"><thead><tr><th scope="col"><span class="sr">{"Critère" if lang == "fr" else "Criterion"}</span></th>'
             f'<th scope="col" class="us">{head[1]}</th><th scope="col">{head[2]}</th></tr></thead><tbody>'
             + "".join(f'<tr><th scope="row">{a}</th><td class="us">{b}</td><td>{c}</td></tr>' for a, b, c in rows)
             + "</tbody></table>")
    body = f'''<section class="hero">
    <div class="wrap hero-grid">
        <div class="hero-text">
            {T['announce']}
            <h1>{T['h1']}</h1>
            <p class="lead">{T['lead']}</p>
            <div class="cta">{download_button(lang)}<a class="link" href="{href(lang, 'features')}">{T['more']}</a></div>
            <p class="meta" data-version="{T['meta']}">{T['meta']}</p>
        </div>
        {shot(lang, "transcription", T['hero_alt'], "shot hero-shot", eager=True)}
    </div>
    <div class="wrap"><ul class="facts">{facts}</ul></div>
</section>

<section class="section">
    <div class="wrap">
        <header class="section-head"><h2>{T['flow_title']}</h2><p>{T['flow_lead']}</p></header>
        <ol class="flow">{flow}</ol>
    </div>
</section>

<section class="section section-alt">
    <div class="wrap">
        <header class="section-head"><h2>{T['new_title']}</h2></header>
        <div class="notes">{news}</div>
    </div>
</section>

<section class="band">
    <div class="wrap band-grid">
        <h2>{T['privacy_title']}</h2>
        <div><p>{T['privacy_lead']}</p><ul class="plain">{plist}</ul>
            <p><a class="link link-light" href="{href(lang, 'privacy')}">{T['privacy_link']}</a></p></div>
    </div>
</section>

<section class="section" id="{T['why_id']}">
    <div class="wrap narrow">
        <header class="section-head"><h2>{T['why_title']}</h2></header>
        <div class="table-wrap">{table}</div>
    </div>
</section>

<section class="section closing">
    <div class="wrap closing-inner">
        <div><h2>{T['cta_title']}</h2><p>{T['cta_lead']}</p></div>
        <div class="closing-cta">{download_button(lang)}<p class="meta" data-version="{T['meta']}">{T['meta']}</p>
            <p class="downloads-count" data-downloads hidden aria-live="polite"></p></div>
    </div>
</section>'''
    return page(lang, "home", title, desc, body, jsonld(lang))


def page_head(title, lead, wide=False):
    return f'<section class="page-head"><div class="wrap{"" if wide else " narrow"}"><h1>{title}</h1><p class="lead">{lead}</p></div></section>'


def features(lang):
    fr = lang == "fr"
    items = [
        ("enregistrement" if fr else "recording", "recorder",
         "Enregistrement" if fr else "Recording",
         "Captez n'importe quelle réunion" if fr else "Capture any meeting",
         ["Réunions en ligne : Teams, Zoom, Meet, webinaires", "Réunions en salle, au micro", "Les deux à la fois : votre voix et celle des autres participants",
          "Import de fichiers audio et vidéo (MP3, M4A, WAV, MP4, MKV, MOV…)", "Bascule automatique quand vous branchez un casque",
          "Bouton « Tester le son » avant une réunion importante"] if fr else
         ["Online meetings: Teams, Zoom, Meet, webinars", "In-room meetings, with the microphone", "Both at once: your voice and the other participants'",
          "Import audio and video files (MP3, M4A, WAV, MP4, MKV, MOV…)", "Automatic switch when you plug in a headset",
          "“Test sound” button before an important meeting"]),
        ("transcription", "transcription",
         "Transcription", "Un texte fidèle, sans carte graphique" if fr else "Accurate text, no graphics card",
         ["Texte horodaté, facile à relire et à citer", "Français, anglais ou détection automatique", "Plusieurs niveaux de précision, et un mode rapide pour les enregistrements de plusieurs heures",
          "Reprise automatique après une coupure", "Fonctionne hors connexion"] if fr else
         ["Timestamped text, easy to read and quote", "English, French or automatic detection", "Several accuracy levels, and a fast mode for recordings lasting several hours",
          "Automatic resume after an interruption", "Works offline"]),
        ("decoupe" if fr else "trim", "trim",
         "Découpe" if fr else "Trimming",
         "Une réunion oubliée en marche" if fr else "A recording left running",
         ["Une vue d'ensemble montre où l'on parle", "Choix du début et de la fin à l'heure près, ou en durée", "Écoute de chaque limite avant de décider",
          "Transcrire seulement cette partie, ou couper l'enregistrement",
          "En option : arrêt quand plus personne ne parle, arrêt après une durée maximale, rappel discret, icône près de l'horloge"] if fr else
         ["An overview shows where people are speaking", "Start and end chosen to the minute, or as durations", "Listen to each boundary before deciding",
          "Transcribe only that part, or cut the recording",
          "Optional: stop when nobody is speaking, stop after a maximum duration, discreet reminder, icon near the clock"]),
        ("resumes" if fr else "summaries", "summary",
         "Résumés" if fr else "Summaries",
         "L'essentiel, en un clic" if fr else "The essentials, in one click",
         ["Résumé, points clés et actions à faire", "Contexte facultatif : participants, rôles, sujet", "Réunions longues prises en charge",
          "Rédigé dans la langue de l'interface", "Plusieurs modèles d'IA au choix, avec Ollama"] if fr else
         ["Summary, key points and action items", "Optional context: participants, roles, topic", "Long meetings supported",
          "Written in the interface language", "Choice of AI models, with Ollama"]),
        ("discussion", "discussion",
         "Discussion", "Posez vos questions à la réunion" if fr else "Ask the meeting your questions",
         ["« Qui a validé le budget ? », « Quelles sont les échéances ? »", "Réponses fondées uniquement sur la réunion", "Questions de suivi qui tiennent compte de l'échange",
          "Dictée sans Internet : posez vos questions à voix haute"] if fr else
         ["“Who approved the budget?”, “What are the deadlines?”", "Answers based only on the meeting", "Follow-up questions that remember the conversation",
          "Offline dictation: ask your questions out loud"]),
        ("historique" if fr else "history", "history",
         "Historique et exports" if fr else "History and exports",
         "Retrouvez tout, partagez facilement" if fr else "Find everything, share easily",
         ["Recherche dans toutes les transcriptions", "Export Markdown, Excel, texte et sous-titres", "Base de données complète, pour Power BI, PostgreSQL ou Python",
          "Sauvegarde facultative vers votre Google Drive ou OneDrive"] if fr else
         ["Search across all transcripts", "Export to Markdown, Excel, text and subtitles", "Full database, for Power BI, PostgreSQL or Python",
          "Optional backup to your Google Drive or OneDrive"]),
    ]
    rows = "".join(
        f'''<article class="feature" id="{fid}">
            <div class="feature-text"><p class="kicker">{kicker}</p><h2>{h}</h2><ul class="ticks">{"".join(f"<li>{x}</li>" for x in lst)}</ul></div>
            {shot(lang, img, h)}
        </article>''' for fid, img, kicker, h, lst in items)
    speakers = ('<article class="feature feature-solo" id="locuteurs"><div class="feature-text"><p class="kicker">Locuteurs <span class="beta">Bêta</span></p>'
                '<h2>Qui a dit quoi ?</h2><p>TranscriPilote peut reconnaître les différentes voix et attribuer chaque phrase à son intervenant. '
                'Cette fonction est encore en développement : activez-la quand elle vous est utile.</p></div></article>') if fr else (
                '<article class="feature feature-solo" id="speakers"><div class="feature-text"><p class="kicker">Speakers <span class="beta">Beta</span></p>'
                '<h2>Who said what?</h2><p>TranscriPilote can recognise the different voices and attribute each sentence to its speaker. '
                'This feature is still in development: turn it on when it helps.</p></div></article>')
    head = page_head("Fonctionnalités" if fr else "Features",
                     "De l'enregistrement aux décisions, sans rien envoyer sur Internet." if fr else
                     "From recording to decisions, without sending anything over the Internet.", wide=True)
    closing = f'''<section class="section closing"><div class="wrap closing-inner">
        <div><h2>{"Prêt à essayer ?" if fr else "Ready to try it?"}</h2><p>{"Gratuit, sans inscription, installé en quelques minutes." if fr else "Free, no sign-up, installed in a few minutes."}</p></div>
        <div class="closing-cta">{download_button(lang)}</div></div></section>'''
    body = head + f'<section class="section section-tight"><div class="wrap">{rows}{speakers}</div></section>' + closing
    return page(lang, "features", "Fonctionnalités – TranscriPilote" if fr else "Features – TranscriPilote",
                "Enregistrement, transcription, découpe, résumés, questions et exports : tout ce que fait TranscriPilote, sur votre PC." if fr else
                "Recording, transcription, trimming, summaries, questions and exports: everything TranscriPilote does, on your PC.", body)


def download(lang):
    fr = lang == "fr"
    req = [("Système", "Windows 10 ou 11, 64 bits"), ("Mémoire", "16 Go recommandés, 8 Go minimum"),
           ("Espace disque", "Environ 10 Go (application et modèles)"), ("Carte graphique", "Aucune n'est nécessaire"),
           ("Droits administrateur", "Non nécessaires : installation dans votre profil"),
           ("Résumés et questions", "Ollama, gratuit, installé une fois")] if fr else [
          ("System", "Windows 10 or 11, 64-bit"), ("Memory", "16 GB recommended, 8 GB minimum"),
          ("Disk space", "About 10 GB (app and models)"), ("Graphics card", "None required"),
          ("Admin rights", "Not required: installs in your profile"),
          ("Summaries and questions", "Ollama, free, installed once")]
    steps = [("Téléchargez l'installateur", "Avec le bouton ci-dessus. Il pèse une quinzaine de mégaoctets."),
             ("Lancez-le", "Il prépare tout seul les composants nécessaires. Comptez quelques minutes la première fois."),
             ("Ouvrez TranscriPilote", "Depuis le menu Démarrer ou le bureau. Une visite guidée d'une minute, facultative, présente chaque fonction.")] if fr else [
            ("Download the installer", "With the button above. It is about fifteen megabytes."),
            ("Run it", "It prepares the required components by itself. Allow a few minutes the first time."),
            ("Open TranscriPilote", "From the Start menu or the desktop. An optional one-minute tour presents each feature.")]
    rows = "".join(f'<tr><th scope="row">{a}</th><td>{b}</td></tr>' for a, b in req)
    st = "".join(f"<li><h3>{a}</h3><p>{b}</p></li>" for a, b in steps)
    ollama = '<a href="https://ollama.com/download">Ollama</a>'
    if fr:
        faq = f'''<details><summary>Windows affiche « Windows a protégé votre ordinateur »</summary>
            <p>L'installateur n'est pas encore signé numériquement, ce qui déclenche cet avertissement pour les logiciels récents. Cliquez sur « Informations complémentaires », puis « Exécuter quand même ».
            Chaque version est publiée avec ses sommes de contrôle SHA-256 (fichier <code>SHA256SUMS.txt</code>), qui permettent de vérifier que le fichier n'a pas été modifié.</p></details>
        <details><summary>Faut-il installer autre chose ?</summary>
            <p>Pour les résumés et les questions, installez aussi {ollama}, gratuit, qui fait tourner l'IA sur votre PC. TranscriPilote le démarre et le configure tout seul. La transcription, elle, fonctionne sans.</p></details>
        <details><summary>Comment se font les mises à jour ?</summary>
            <p>Les nouvelles versions se préparent en arrière-plan et s'installent quand vous le décidez, sans réinstaller et sans perte de données. Jamais pendant un enregistrement ou une transcription.</p></details>
        <details><summary>Où sont mes données ? Comment désinstaller ?</summary>
            <p>Vos réunions et réglages sont dans <code>%LOCALAPPDATA%\\TranscriPilote</code>. Pour désinstaller : Paramètres Windows, Applications, TranscriPilote. Vos données sont conservées ; supprimez ce dossier pour tout effacer.</p></details>'''
    else:
        faq = f'''<details><summary>Windows shows “Windows protected your PC”</summary>
            <p>The installer is not digitally signed yet, which triggers this warning for recent software. Click “More info”, then “Run anyway”.
            Each release is published with its SHA-256 checksums (<code>SHA256SUMS.txt</code> file), so you can check that the file has not been modified.</p></details>
        <details><summary>Do I need to install anything else?</summary>
            <p>For summaries and questions, also install {ollama}, free, which runs the AI on your PC. TranscriPilote starts and configures it by itself. Transcription works without it.</p></details>
        <details><summary>How do updates work?</summary>
            <p>New versions are prepared in the background and installed when you decide, without reinstalling and without losing data. Never during a recording or a transcription.</p></details>
        <details><summary>Where is my data? How do I uninstall?</summary>
            <p>Your meetings and settings are in <code>%LOCALAPPDATA%\\TranscriPilote</code>. To uninstall: Windows Settings, Apps, TranscriPilote. Your data is kept; delete that folder to erase everything.</p></details>'''
    meta = "Windows 10 et 11, gratuit" if fr else "Windows 10 and 11, free"
    body = f'''<section class="page-head download-head"><div class="wrap narrow">
        <img class="app-icon" src="{"" if fr else "../"}assets/icon.svg" alt="" width="88" height="88">
        <h1>{"Télécharger TranscriPilote" if fr else "Download TranscriPilote"}</h1>
        <p class="lead">{"Gratuit, pour Windows 10 et 11. L'installation se fait dans votre profil, sans droits administrateur." if fr else "Free, for Windows 10 and 11. Installs in your profile, with no admin rights."}</p>
        <div class="cta">{download_button(lang)}<a class="link" href="{RELEASES}">{"Toutes les versions" if fr else "All releases"}</a></div>
        <p class="meta" data-version="{meta}">{meta}</p>
        <p class="downloads-count" data-downloads hidden aria-live="polite"></p>
    </div></section>
    <section class="section section-tight"><div class="wrap narrow">
        <h2 class="h-sm">{"Installation" if fr else "Installation"}</h2>
        <ol class="steps">{st}</ol>
        <h2 class="h-sm" id="{"configuration" if fr else "requirements"}">{"Configuration requise" if fr else "System requirements"}</h2>
        <div class="table-wrap"><table class="specs"><tbody>{rows}</tbody></table></div>
        <h2 class="h-sm">{"Bon à savoir" if fr else "Good to know"}</h2>
        <div class="faq">{faq}</div>
    </div></section>'''
    return page(lang, "download", "Télécharger TranscriPilote pour Windows" if fr else "Download TranscriPilote for Windows",
                "Téléchargez gratuitement TranscriPilote pour Windows 10 et 11 : installation sans droits administrateur, configuration requise." if fr else
                "Download TranscriPilote for Windows 10 and 11 for free: no admin rights needed, system requirements.", body)


def news(lang):
    fr = lang == "fr"
    body = page_head("Nouveautés" if fr else "What's new",
                     "Ce qui change, version après version. Cette page se met à jour à chaque nouvelle version." if fr else
                     "What changes, release after release. This page updates itself with each new version.") + f'''
    <section class="section section-tight"><div class="wrap narrow">
        <div id="releases"><p>{"Chargement des nouveautés…" if fr else "Loading release notes…"}</p></div>
        <noscript><p>{"Activez JavaScript pour afficher les nouveautés, ou" if fr else "Turn on JavaScript to see the release notes, or"} <a href="{RELEASES}">{"consultez les versions sur GitHub" if fr else "see the releases on GitHub"}</a>.</p></noscript>
    </div></section>'''
    return page(lang, "news", "Nouveautés – TranscriPilote" if fr else "What's new – TranscriPilote",
                "Les nouveautés de chaque version de TranscriPilote." if fr else "What's new in each TranscriPilote release.", body)


FAQ_FR = [
    ("TranscriPilote est-il gratuit ?", "Oui. TranscriPilote est gratuit, sans abonnement, sans limite de minutes et sans publicité, pour un usage personnel comme professionnel."),
    ("Mes réunions sont-elles envoyées sur Internet ?", "Non. La transcription, les résumés et les questions sont traités sur votre PC. Rien n'est envoyé à un service en ligne, sauf la sauvegarde vers votre propre cloud si vous l'activez. Voir la <a href=\"confidentialite.html\">politique de confidentialité</a>."),
    ("Qui édite TranscriPilote ?", f"TranscriPilote est édité par {PUBLISHER}, le nom sous lequel Mike DANSOU publie ses logiciels. Il le conçoit et le maintient lui-même. Voir les <a href=\"mentions-legales.html\">mentions légales</a>."),
    ("Faut-il une carte graphique ou des droits administrateur ?", "Non. TranscriPilote fonctionne sur un PC ordinaire et s'installe dans le profil Windows de l'utilisateur, sans droits administrateur."),
    ("Peut-on transcrire une réunion Teams, Zoom ou Meet ?", "Oui. TranscriPilote enregistre vos réunions en ligne, quel que soit l'outil, ainsi que vos réunions en salle. Il accepte aussi les fichiers audio et vidéo."),
    ("Quelles langues sont prises en charge ?", "Le français et l'anglais, avec détection automatique de la langue. L'application elle-même existe en français et en anglais, et les résumés sont rédigés dans la langue choisie pour l'interface."),
    ("Combien de temps prend une transcription ?", "Sans carte graphique, comptez entre la moitié et deux fois la durée de l'enregistrement selon le niveau de précision choisi. La transcription se fait en arrière-plan : vous pouvez continuer à utiliser l'application."),
    ("J'ai oublié d'arrêter l'enregistrement. Que faire ?", "Dans l'historique, le bouton ciseaux ouvre « Découper la réunion » : choisissez la partie utile à l'heure près, puis transcrivez seulement elle ou coupez l'enregistrement. Dans les réglages, des aides facultatives peuvent aussi l'arrêter quand plus personne ne parle."),
    ("Comment fonctionnent les mises à jour ?", "TranscriPilote vérifie au démarrage si une nouvelle version existe et la prépare en arrière-plan. Elle s'installe quand vous le décidez, jamais pendant un enregistrement ou une transcription, sans réinstaller ni perdre vos données."),
    ("Y a-t-il un tutoriel ?", "Oui. Au premier lancement, TranscriPilote propose une visite guidée d'environ une minute, que vous pouvez refuser. Elle se relance à tout moment avec le bouton d'aide en bas du menu."),
    ("Comment contacter l'auteur ?", f"Par la <a href=\"{CONTACT}\">page Contact</a>, pour une question, un partenariat ou un retour d'expérience. Pour signaler un problème dans l'application, utilisez plutôt la <a href=\"{ISSUES}\">page de signalement</a>."),
    ("TranscriPilote s'écrit-il « Transcri Pilote » ?", "Le nom officiel s'écrit en un mot : TranscriPilote. On le trouve parfois écrit « Transcri Pilote » ou « Transcrit Pilote »."),
]
FAQ_EN = [
    ("Is TranscriPilote free?", "Yes. TranscriPilote is free, with no subscription, no minute limit and no ads, for personal and professional use."),
    ("Are my meetings sent over the Internet?", "No. Transcription, summaries and questions are processed on your PC. Nothing is sent to an online service, except the backup to your own cloud if you turn it on. See the <a href=\"privacy.html\">privacy policy</a>."),
    ("Who publishes TranscriPilote?", f"TranscriPilote is published by {PUBLISHER}, the name under which Mike DANSOU publishes his software. He designs and maintains it himself. See the <a href=\"legal.html\">legal notice</a>."),
    ("Do I need a graphics card or admin rights?", "No. TranscriPilote runs on an ordinary PC and installs in the user's Windows profile, with no admin rights."),
    ("Can it transcribe a Teams, Zoom or Meet meeting?", "Yes. TranscriPilote records your online meetings, whatever the tool, as well as in-room meetings. It also accepts audio and video files."),
    ("Which languages are supported?", "English and French, with automatic language detection. The app itself is available in English and French, and summaries are written in the interface language."),
    ("How long does a transcription take?", "Without a graphics card, allow between half and twice the length of the recording, depending on the accuracy level. Transcription runs in the background: you can keep using the app."),
    ("I forgot to stop the recording. What can I do?", "In the history, the scissors button opens “Trim the meeting”: choose the useful part to the minute, then transcribe only that part or cut the recording. Optional aids in the settings can also stop it when nobody is speaking."),
    ("How do updates work?", "TranscriPilote checks for a new version at startup and prepares it in the background. It installs when you decide, never during a recording or a transcription, without reinstalling or losing data."),
    ("Is there a tutorial?", "Yes. On first launch, TranscriPilote offers a guided tour of about one minute, which you can decline. Restart it at any time with the help button at the bottom of the menu."),
    ("How do I contact the author?", f"Through the <a href=\"{CONTACT}\">Contact page</a>, for a question, a partnership or feedback. To report a problem in the app, use the <a href=\"{ISSUES}\">issue page</a> instead."),
    ("Is it spelled “Transcri Pilote”?", "The official name is one word: TranscriPilote. It is sometimes written “Transcri Pilote” or “Transcrit Pilote”."),
]


def faq(lang):
    fr = lang == "fr"
    items = FAQ_FR if fr else FAQ_EN
    qa = "".join(f"<details{' open' if i == 0 else ''}><summary>{q}</summary><p>{a}</p></details>" for i, (q, a) in enumerate(items))
    lead = (f'Une question qui n\'est pas ici ? <a href="{ISSUES}">Posez-la sur la page du projet</a>.' if fr else
            f'A question that is not here? <a href="{ISSUES}">Ask it on the project page</a>.')
    body = page_head("Questions fréquentes" if fr else "Frequently asked questions", lead) + \
        f'<section class="section section-tight"><div class="wrap narrow"><div class="faq">{qa}</div></div></section>'
    return page(lang, "faq", "Questions fréquentes – TranscriPilote" if fr else "FAQ – TranscriPilote",
                "Réponses aux questions fréquentes sur TranscriPilote : gratuité, confidentialité, langues, mises à jour." if fr else
                "Answers to common questions about TranscriPilote: price, privacy, languages, updates.", body)


def privacy(lang):
    fr = lang == "fr"
    today = "15 novembre 2026" if fr else "15 November 2026"
    if fr:
        text = f'''
        <p class="updated">Dernière mise à jour : {today}</p>
        <h2>En bref</h2>
        <p>TranscriPilote traite vos réunions sur votre ordinateur. Ni l'éditeur ni personne d'autre n'a accès à vos enregistrements, à vos transcriptions ou à vos résumés. L'application ne contient aucune mesure d'audience, aucun traceur et aucune publicité.</p>
        <h2>L'application</h2>
        <p>Vos enregistrements, transcriptions, résumés et réglages sont conservés dans le dossier <code>%LOCALAPPDATA%\\TranscriPilote</code> de votre compte Windows. Ils ne sont envoyés nulle part.</p>
        <p>L'application se connecte à Internet uniquement dans les cas suivants :</p>
        <ul>
            <li>vérifier et télécharger les nouvelles versions, sur GitHub (désactivable dans les réglages) ;</li>
            <li>télécharger les modèles de transcription, une fois, au premier usage, depuis Hugging Face ;</li>
            <li>télécharger l'outil de conversion vidéo FFmpeg, une fois, si vous importez une vidéo ;</li>
            <li>copier vos données vers votre propre Google Drive ou OneDrive, si vous activez la sauvegarde : elles vont directement de votre PC à votre compte ;</li>
            <li>utiliser l'identification des intervenants (bêta), qui télécharge un modèle avec la clé Hugging Face que vous fournissez.</li>
        </ul>
        <p>Les résumés et les questions sont traités par Ollama, qui fonctionne sur votre PC.</p>
        <h2>Ce site</h2>
        <p>Le site est hébergé par GitHub Pages, et les installateurs par GitHub. Comme tout hébergeur, GitHub reçoit l'adresse IP des visiteurs pour délivrer les pages ; voir la <a href="https://docs.github.com/fr/site-policy/privacy-policies/github-general-privacy-statement">déclaration de confidentialité de GitHub</a>.</p>
        <p>Pour afficher la dernière version et le nombre de téléchargements, votre navigateur interroge l'API publique de GitHub. Le site n'utilise aucun cookie ni outil de mesure d'audience.</p>
        <p>Après un clic sur « Télécharger », deux questions facultatives vous sont proposées : votre pays et la façon dont vous avez connu TranscriPilote. Si vous y répondez, seules ces réponses et le numéro de version sont enregistrés, chez le prestataire Supabase, sans nom ni adresse e-mail. Elles servent uniquement à savoir où le logiciel est utilisé. Votre navigateur retient localement que la question vous a déjà été posée.</p>
        <h2>Vos droits</h2>
        <p>Pour toute question sur vos données, ou pour exercer vos droits d'accès et d'effacement, écrivez via la <a href="{CONTACT}">page Contact</a>. Vous pouvez aussi saisir la CNIL.</p>'''
    else:
        text = f'''
        <p class="updated">Last updated: {today}</p>
        <h2>In short</h2>
        <p>TranscriPilote processes your meetings on your computer. Neither the publisher nor anyone else has access to your recordings, transcripts or summaries. The app contains no analytics, no trackers and no ads.</p>
        <h2>The app</h2>
        <p>Your recordings, transcripts, summaries and settings are kept in the <code>%LOCALAPPDATA%\\TranscriPilote</code> folder of your Windows account. They are not sent anywhere.</p>
        <p>The app connects to the Internet only in the following cases:</p>
        <ul>
            <li>checking for and downloading new versions, on GitHub (can be turned off in the settings);</li>
            <li>downloading the transcription models, once, on first use, from Hugging Face;</li>
            <li>downloading the FFmpeg video conversion tool, once, if you import a video;</li>
            <li>copying your data to your own Google Drive or OneDrive, if you turn on backup: it goes straight from your PC to your account;</li>
            <li>using speaker identification (beta), which downloads a model with the Hugging Face key you provide.</li>
        </ul>
        <p>Summaries and questions are processed by Ollama, which runs on your PC.</p>
        <h2>This website</h2>
        <p>The website is hosted by GitHub Pages, and the installers by GitHub. Like any host, GitHub receives visitors' IP addresses to deliver the pages; see the <a href="https://docs.github.com/en/site-policy/privacy-policies/github-general-privacy-statement">GitHub privacy statement</a>.</p>
        <p>To show the latest version and the download count, your browser queries GitHub's public API. The website uses no cookies and no analytics.</p>
        <p>After you click “Download”, two optional questions are offered: your country and how you heard about TranscriPilote. If you answer, only those answers and the version number are stored, with the provider Supabase, with no name or e-mail address. They are only used to know where the software is used. Your browser remembers locally that you have already been asked.</p>
        <h2>Your rights</h2>
        <p>For any question about your data, or to exercise your rights of access and erasure, write through the <a href="{CONTACT}">Contact page</a>.</p>'''
    body = page_head("Politique de confidentialité" if fr else "Privacy policy",
                     "Ce que TranscriPilote et ce site font de vos données, et ce qu'ils n'en font pas." if fr else
                     "What TranscriPilote and this website do with your data, and what they don't.") + \
        f'<section class="section section-tight"><div class="wrap narrow prose">{text}</div></section>'
    return page(lang, "privacy", "Confidentialité – TranscriPilote" if fr else "Privacy – TranscriPilote",
                "Politique de confidentialité de TranscriPilote et de son site." if fr else "Privacy policy of TranscriPilote and its website.", body)


def legal(lang):
    fr = lang == "fr"
    if fr:
        text = f'''
        <h2>Éditeur</h2>
        <p>Le site et le logiciel TranscriPilote sont édités par <strong>{PUBLISHER}</strong>, nom sous lequel Mike DANSOU publie ses logiciels, à titre personnel et non commercial.</p>
        <p>Directeur de la publication : Mike DANSOU.<br>Contact : <a href="{CONTACT}">page Contact</a>.</p>
        <h2>Hébergement</h2>
        <p>GitHub, Inc. (service GitHub Pages et GitHub Releases), 88 Colin P. Kelly Jr. Street, San Francisco, CA 94107, États-Unis.</p>
        <h2>Propriété intellectuelle</h2>
        <p>TranscriPilote, son nom, son logo, son code et ce site sont la propriété de leur auteur. Le logiciel est gratuit ; ses conditions d'utilisation sont décrites dans les <a href="{LICENSE}">conditions d'utilisation</a>. Les composants et modèles tiers restent soumis à leur propre licence : voir la <a href="{NOTICES}">liste des composants tiers</a>.</p>
        <h2>Données personnelles</h2>
        <p>Voir la <a href="confidentialite.html">politique de confidentialité</a>.</p>'''
    else:
        text = f'''
        <h2>Publisher</h2>
        <p>The TranscriPilote website and software are published by <strong>{PUBLISHER}</strong>, the name under which Mike DANSOU publishes his software, on a personal, non-commercial basis.</p>
        <p>Publication director: Mike DANSOU.<br>Contact: <a href="{CONTACT}">Contact page</a>.</p>
        <h2>Hosting</h2>
        <p>GitHub, Inc. (GitHub Pages and GitHub Releases services), 88 Colin P. Kelly Jr. Street, San Francisco, CA 94107, United States.</p>
        <h2>Intellectual property</h2>
        <p>TranscriPilote, its name, logo, code and this website belong to their author. The software is free; its terms are described in the <a href="{LICENSE}">terms of use</a>. Third-party components and models remain subject to their own licences: see the <a href="{NOTICES}">list of third-party components</a>.</p>
        <h2>Personal data</h2>
        <p>See the <a href="privacy.html">privacy policy</a>.</p>'''
    body = page_head("Mentions légales" if fr else "Legal notice", "Qui édite TranscriPilote et ce site." if fr else "Who publishes TranscriPilote and this website.") + \
        f'<section class="section section-tight"><div class="wrap narrow prose">{text}</div></section>'
    return page(lang, "legal", "Mentions légales – TranscriPilote" if fr else "Legal notice – TranscriPilote",
                f"Mentions légales de TranscriPilote, édité par {PUBLISHER}." if fr else f"Legal notice of TranscriPilote, published by {PUBLISHER}.", body)


def redirect(target, lang):
    return f'''<!doctype html>
<html lang="{lang}"><head><meta charset="utf-8"><title>TranscriPilote</title>
<meta http-equiv="refresh" content="0; url={target}"><link rel="canonical" href="{target}"><meta name="robots" content="noindex">
</head><body><p><a href="{target}">TranscriPilote</a></p></body></html>
'''


def sitemap():
    today = date.today().isoformat()
    out = ['<?xml version="1.0" encoding="UTF-8"?>',
           '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:xhtml="http://www.w3.org/1999/xhtml">']
    for fr_file, en_file in PAGES.values():
        for me in (fr_file, en_file):
            out += [f"  <url><loc>{abs_url(me)}</loc><lastmod>{today}</lastmod>",
                    f'    <xhtml:link rel="alternate" hreflang="fr" href="{abs_url(fr_file)}"/>',
                    f'    <xhtml:link rel="alternate" hreflang="en" href="{abs_url(en_file)}"/></url>']
    out.append("</urlset>")
    return "\n".join(out) + "\n"


def main():
    builders = {"home": home, "features": features, "download": download, "news": news, "faq": faq,
                "privacy": privacy, "legal": legal}
    for key, (fr_file, en_file) in PAGES.items():
        for lang, f in (("fr", fr_file), ("en", en_file)):
            (DOCS / f).write_text(builders[key](lang), encoding="utf-8")
    for f, target in REDIRECTS.items():
        (DOCS / f).write_text(redirect(target, "en" if f.startswith("en/") else "fr"), encoding="utf-8")
    (DOCS / "sitemap.xml").write_text(sitemap(), encoding="utf-8")
    print("site généré :", len(PAGES) * 2, "pages")


if __name__ == "__main__":
    main()
