"""Illustrations du site, dessinées en HTML et CSS : nettes à toutes les tailles, légères, bilingues.

Elles représentent l'application de façon stylisée (comme une plaquette de logiciel), sans capture d'écran
réduite. Les vraies captures, en pleine résolution, sont sur la page « Captures d'écran ».
"""
import math


def waveform(n=42, seed=3, cls="wave", active=None):
    """Barres d'une onde sonore, hauteurs déterministes. active : (début, fin) en indices, surlignées."""
    bars = []
    for i in range(n):
        h = 0.25 + 0.75 * abs(math.sin(i * 0.61 + seed) * math.cos(i * 0.23 + seed * 0.7))
        on = active is None or active[0] <= i < active[1]
        bars.append(f'<i style="height:{round(h * 100)}%"{"" if on else " class=off"}></i>')
    return f'<div class="{cls}" aria-hidden="true">{"".join(bars)}</div>'


def lines(widths, cls="sk"):
    return "".join(f'<span class="{cls}" style="width:{w}%"></span>' for w in widths)


T = {
    "fr": dict(summary="Résumé", actions="Actions", local="IA locale", offline="Hors ligne", nogpu="Sans carte graphique",
               win="Windows 10 et 11", teams="Teams, Zoom, Meet", room="Réunion en salle", file="Fichier audio ou vidéo",
               pc="Sur votre PC", out_t="Transcription", out_s="Résumé et actions", out_q="Réponses", out_e="Exports",
               q="Qui relit les textes anglais, et pour quand ?", a="Sophie relit les textes anglais d'ici vendredi.",
               l1="Bonjour à tous. On fait le point sur la sortie de la version anglaise.",
               l2="Côté traduction, l'application est terminée. Il reste le site web.",
               l3="Sophie, tu peux relire les textes anglais d'ici vendredi ?",
               l4="Oui, je m'en occupe.",
               keys="Points clés", k1="Version anglaise prévue en janvier", k2="Budget du trimestre respecté",
               t1="Relire les textes anglais", t2="Valider la date de sortie",
               keep="Garder", trim_from="14:05", trim_to="15:20", dict="Quelles décisions ont été prises sur le bud",
               listen="Je vous écoute…"),
    "en": dict(summary="Summary", actions="Action items", local="Local AI", offline="Offline", nogpu="No graphics card",
               win="Windows 10 and 11", teams="Teams, Zoom, Meet", room="In-room meeting", file="Audio or video file",
               pc="On your PC", out_t="Transcript", out_s="Summary and actions", out_q="Answers", out_e="Exports",
               q="Who is proofreading the English copy, and by when?", a="Sarah is proofreading the English copy by Friday.",
               l1="Good morning everyone. Let's review the launch plan for the English release.",
               l2="The app translation is finished. We still need to update the website.",
               l3="Sarah, could you proofread the English copy by Friday?",
               l4="Sure, I'll take care of it.",
               keys="Key points", k1="English release planned for January", k2="Quarterly budget on track",
               t1="Proofread the English copy", t2="Confirm the release date",
               keep="Keep", trim_from="2:05 pm", trim_to="3:20 pm", dict="What was decided about the bud",
               listen="Listening…"),
}


def app(lang):
    """Grande illustration de l'accueil : la fenêtre de l'application, stylisée."""
    t = T[lang]
    rows = [("#8b7cf6", "00:00:12", [78, 54]), ("#f5a623", "00:00:47", [70, 82, 40]), ("#3ddc84", "00:01:05", [84, 60])]
    rows_html = "".join(
        f'<div class="ill-row"><span class="dot" style="background:{c}"></span><div><div class="ill-meta">'
        f'<span class="sk sk-strong" style="width:22%"></span><span class="time">{tm}</span></div>{lines(w)}</div></div>'
        for c, tm, w in rows)
    return f'''<div class="ill ill-app" role="img" aria-label="{'Illustration de TranscriPilote : enregistrement, transcription horodatée et résumé' if lang == 'fr' else 'TranscriPilote illustration: recording, timestamped transcript and summary'}">
    <div class="ill-window">
        <div class="ill-chrome"><i></i><i></i><i></i><span class="sk" style="width:26%"></span></div>
        <div class="ill-recbar"><span class="rec"></span>{waveform(38, 1.7)}<span class="clock">01:14:32</span></div>
        <div class="ill-body">
            <div class="ill-rows">{rows_html}</div>
            <div class="ill-panel">
                <p class="ill-h">{t['summary']}</p>{lines([92, 76, 84])}
                <p class="ill-h">{t['actions']}</p>
                <div class="ill-check on"></div><div class="ill-check on"></div><div class="ill-check"></div>
                <span class="ill-pill">{t['local']}</span>
            </div>
        </div>
    </div>
    <div class="ill-badges"><span>{t['offline']}</span><span>{t['nogpu']}</span><span>{t['win']}</span></div>
</div>'''


def flow(lang):
    """Schéma vectoriel : d'où vient le son, ce qui se passe sur le PC, ce qui en sort."""
    t = T[lang]
    ins = [t["teams"], t["room"], t["file"]]
    outs = [t["out_t"], t["out_s"], t["out_q"], t["out_e"]]
    W, H, bw, bh = 1000, 380, 230, 50
    yin = [80, 190, 300]
    yout = [55, 145, 235, 325]
    cx, cy, cw, ch = 420, 120, 160, 140
    parts = []
    for y in yin:
        parts.append(f'<path class="fl" d="M{40 + bw} {y} C {340} {y}, {360} {cy + ch / 2}, {cx} {cy + ch / 2}"/>')
    for y in yout:
        parts.append(f'<path class="fl" d="M{cx + cw} {cy + ch / 2} C {640} {cy + ch / 2}, {660} {y}, {W - 40 - bw} {y}"/>')
    for y, label in zip(yin, ins):
        parts.append(f'<rect class="fb" x="40" y="{y - bh / 2}" width="{bw}" height="{bh}" rx="9"/>'
                     f'<text x="{40 + bw / 2}" y="{y + 5}">{label}</text>')
    for y, label in zip(yout, outs):
        parts.append(f'<rect class="fb fb-out" x="{W - 40 - bw}" y="{y - bh / 2}" width="{bw}" height="{bh}" rx="9"/>'
                     f'<text x="{W - 40 - bw / 2}" y="{y + 5}">{label}</text>')
    parts.append(f'<rect class="fc" x="{cx}" y="{cy}" width="{cw}" height="{ch}" rx="16"/>'
                 f'<image href="{{pre}}assets/icon.svg" x="{cx + cw / 2 - 26}" y="{cy + 20}" width="52" height="52"/>'
                 f'<text class="fc-name" x="{cx + cw / 2}" y="{cy + 98}">TranscriPilote</text>'
                 f'<text class="fc-sub" x="{cx + cw / 2}" y="{cy + 120}">{t["pc"]}</text>')
    label = ("Schéma : réunions en ligne, en salle ou fichiers, traitées sur votre PC, donnent transcription, résumé, réponses et exports"
             if lang == "fr" else
             "Diagram: online meetings, in-room meetings or files, processed on your PC, produce transcripts, summaries, answers and exports")
    fallback = ('<div class="flow-list" aria-hidden="true"><ul>' + "".join(f"<li>{x}</li>" for x in ins) + '</ul>'
                f'<p class="flow-mid">TranscriPilote, {t["pc"].lower()}</p><ul>' + "".join(f"<li>{x}</li>" for x in outs) + '</ul></div>')
    return (f'<div class="ill-flow"><svg viewBox="0 0 {W} {H}" role="img" aria-label="{label}">'
            f'<defs><filter id="glow" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="18"/></filter></defs>'
            f'<rect x="{cx - 10}" y="{cy - 10}" width="{cw + 20}" height="{ch + 20}" rx="24" fill="#7c6cf0" opacity=".35" filter="url(#glow)"/>'
            + "".join(parts) + f'</svg>{fallback}</div>')


def mini(kind, lang):
    """Petites illustrations des tuiles et des pages de fonctionnalités."""
    t = T[lang]
    if kind == "record":
        chips = "".join(f'<span class="chip">{x}</span>' for x in (t["teams"], t["room"], t["file"]))
        return f'<div class="mini mini-record" aria-hidden="true"><div class="chips">{chips}</div>{waveform(30, 2.4, "wave wave-lg")}</div>'
    if kind == "transcript":
        rows = "".join(f'<p><span class="time">{tm}</span>{x}</p>' for tm, x in
                       (("00:00:00", t["l1"]), ("00:00:06", t["l2"]), ("00:00:14", t["l3"]), ("00:00:20", t["l4"])))
        return f'<div class="mini mini-transcript" aria-hidden="true">{rows}</div>'
    if kind == "summary":
        return (f'<div class="mini mini-summary" aria-hidden="true"><p class="ill-h">{t["keys"]}</p>'
                f'<ul><li>{t["k1"]}</li><li>{t["k2"]}</li></ul><p class="ill-h">{t["actions"]}</p>'
                f'<p class="todo"><span class="box on"></span>{t["t1"]}</p><p class="todo"><span class="box"></span>{t["t2"]}</p></div>')
    if kind == "chat":
        return (f'<div class="mini mini-chat" aria-hidden="true"><p class="bubble me">{t["q"]}</p>'
                f'<p class="bubble ai">{t["a"]}</p></div>')
    if kind == "trim":
        return (f'<div class="mini mini-trim" aria-hidden="true"><div class="trim-sel">{waveform(44, 0.9, "wave wave-lg", (8, 27))}'
                f'<span class="handle" style="left:18.2%"></span><span class="handle" style="left:61.4%"></span></div>'
                f'<p class="trim-label">{t["keep"]} <b>{t["trim_from"]}</b> → <b>{t["trim_to"]}</b></p></div>')
    if kind == "dictation":
        return (f'<div class="mini mini-dict" aria-hidden="true"><div class="field">{t["dict"]}<span class="caret"></span>'
                f'<span class="mic"></span></div><p class="hint"><span class="live"></span>{t["listen"]}</p></div>')
    if kind == "export":
        files = "".join(f'<span class="file"><b>{ext}</b></span>' for ext in (".md", ".xlsx", ".txt", ".srt", ".db"))
        return f'<div class="mini mini-export" aria-hidden="true">{files}</div>'
    raise ValueError(kind)
