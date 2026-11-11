(function () {
    "use strict";

    // En-tête : bordure au défilement, menu sur mobile.
    var header = document.querySelector(".site-header");
    var onScrollHeader = function () { if (header) header.classList.toggle("scrolled", window.scrollY > 8); };
    var toggle = document.querySelector(".nav-toggle");
    var nav = document.querySelector(".site-nav");
    if (toggle && nav) {
        toggle.addEventListener("click", function () {
            var open = nav.classList.toggle("open");
            toggle.setAttribute("aria-expanded", open ? "true" : "false");
        });
    }

    // Apparition des éléments au défilement.
    var reduceMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
    var revealed = document.querySelectorAll(".reveal");
    if ("IntersectionObserver" in window && !reduceMotion) {
        var io = new IntersectionObserver(function (entries) {
            entries.forEach(function (e) {
                if (e.isIntersecting) { e.target.classList.add("visible"); io.unobserve(e.target); }
            });
        }, { rootMargin: "0px 0px -12% 0px" });
        revealed.forEach(function (el) { io.observe(el); });
    } else {
        revealed.forEach(function (el) { el.classList.add("visible"); });
    }

    // Fil rouge : la ligne se remplit au défilement et chaque étape s'allume à son passage.
    var journeys = document.querySelectorAll(".journey");
    var updateJourneys = function () {
        var mid = window.innerHeight * 0.55;
        journeys.forEach(function (j) {
            var line = j.querySelector(".journey-line");
            var bar = j.querySelector(".journey-progress");
            var rect = line.getBoundingClientRect();
            var ratio = Math.max(0, Math.min(1, (mid - rect.top) / rect.height));
            bar.style.height = (ratio * 100) + "%";
            j.querySelectorAll(".step").forEach(function (step) {
                var dot = step.querySelector(".dot").getBoundingClientRect();
                step.classList.toggle("reached", dot.top + dot.height / 2 <= mid);
            });
        });
    };

    var ticking = false;
    window.addEventListener("scroll", function () {
        if (ticking) return;
        ticking = true;
        requestAnimationFrame(function () { onScrollHeader(); updateJourneys(); ticking = false; });
    }, { passive: true });
    window.addEventListener("resize", updateJourneys);
    onScrollHeader();
    updateJourneys();

    // Page « Nouveautés » : construite à partir des notes de chaque version publiée, donc à jour sans retouche.
    var releasesBox = document.getElementById("releases");
    if (releasesBox) {
        var clean = function (s) { return s.replace(/\*\*(.+?)\*\*/g, "$1").replace(new RegExp("`([^`]+)`", "g"), "$1"); };
        var renderNotes = function (text) {
            var box = document.createElement("div");
            box.className = "release-notes";
            var list = null;
            String(text || "").replace(/\r/g, "").split("\n").forEach(function (raw) {
                var line = raw.replace(/\s+$/, "");
                var node;
                if (/^#{1,4}\s/.test(line)) {
                    list = null; node = document.createElement("h4"); node.textContent = clean(line.replace(/^#+\s*/, "")); box.appendChild(node);
                } else if (/^\s*[-*]\s/.test(line)) {
                    if (!list) { list = document.createElement("ul"); box.appendChild(list); }
                    node = document.createElement("li"); node.textContent = clean(line.replace(/^\s*[-*]\s+/, "")); list.appendChild(node);
                } else if (/^\s{2,}\S/.test(line) && list && list.lastChild) {
                    list.lastChild.textContent += " " + clean(line.trim());
                } else if (line.trim()) {
                    list = null; node = document.createElement("p"); node.textContent = clean(line.trim()); box.appendChild(node);
                } else { list = null; }
            });
            return box;
        };
        var fail = function () {
            releasesBox.textContent = "";
            var p = document.createElement("p");
            p.appendChild(document.createTextNode("Impossible de charger les nouveautés pour l'instant. "));
            var a = document.createElement("a");
            a.href = "https://github.com/MikeDns/TranscriPilote/releases"; a.textContent = "Voir toutes les versions sur GitHub";
            p.appendChild(a);
            releasesBox.appendChild(p);
        };
        fetch("https://api.github.com/repos/MikeDns/TranscriPilote/releases?per_page=15")
            .then(function (r) { return r.ok ? r.json() : Promise.reject(); })
            .then(function (releases) {
                releasesBox.textContent = "";
                releases.filter(function (r) { return !r.draft && !r.prerelease; }).forEach(function (rel, i) {
                    var card = document.createElement("article");
                    card.className = "card release";
                    var head = document.createElement("div");
                    head.className = "release-head";
                    var h = document.createElement("h2");
                    h.textContent = "Version " + rel.tag_name.replace(/^v/, "");
                    var meta = document.createElement("span");
                    meta.className = "release-date";
                    meta.textContent = (i === 0 ? "Dernière version · " : "") +
                        new Date(rel.published_at).toLocaleDateString("fr-FR", { day: "numeric", month: "long", year: "numeric" });
                    head.appendChild(h); head.appendChild(meta);
                    card.appendChild(head);
                    card.appendChild(renderNotes(rel.body));
                    var exe = (rel.assets || []).filter(function (a) { return /^TranscriPilote-Setup-.+\.exe$/.test(a.name); })[0];
                    if (exe) {
                        var dl = document.createElement("a");
                        dl.className = "btn btn-ghost release-dl"; dl.href = exe.browser_download_url;
                        dl.textContent = "Télécharger cette version";
                        card.appendChild(dl);
                    }
                    releasesBox.appendChild(card);
                });
                if (!releasesBox.children.length) fail();
            })
            .catch(fail);
    }

    // ---------- Téléchargement : lien direct, compteur en direct, questionnaire facultatif ----------

    var targets = document.querySelectorAll("[data-download]");
    var versionEls = document.querySelectorAll("[data-version]");
    var counters = document.querySelectorAll("[data-downloads]");
    var latestVersion = null;

    var isSetup = function (a) { return /^TranscriPilote-Setup-.+\.exe$/.test(a.name); };

    // Une seule requête pour tout : la liste des versions donne la dernière version et le total des
    // téléchargements (GitHub compte chaque installateur téléchargé). Actualisée toutes les 2 minutes.
    var refresh = function () {
        if (!targets.length && !versionEls.length && !counters.length) return;
        fetch("https://api.github.com/repos/MikeDns/TranscriPilote/releases?per_page=100")
            .then(function (r) { return r.ok ? r.json() : Promise.reject(); })
            .then(function (releases) {
                var published = releases.filter(function (rel) { return !rel.draft && !rel.prerelease; });
                var total = 0;
                published.forEach(function (rel) {
                    (rel.assets || []).filter(isSetup).forEach(function (a) { total += a.download_count || 0; });
                });
                counters.forEach(function (el) {
                    el.textContent = total.toLocaleString("fr-FR") + " téléchargement" + (total > 1 ? "s" : "");
                    el.hidden = false;
                });
                var rel = published[0];
                var exe = rel && (rel.assets || []).filter(isSetup)[0];
                if (!exe) return;
                latestVersion = rel.tag_name.replace(/^v/, "");
                targets.forEach(function (a) { a.href = exe.browser_download_url; });
                var label = "Version " + latestVersion + " · " + Math.round(exe.size / 1048576) + " Mo";
                versionEls.forEach(function (el) { el.textContent = label + " · " + el.getAttribute("data-version"); });
            })
            .catch(function () {});
    };
    refresh();
    if (counters.length) {
        setInterval(function () { if (!document.hidden) refresh(); }, 120000);
        document.addEventListener("visibilitychange", function () { if (!document.hidden) refresh(); });
    }

    // Questionnaire facultatif après le clic : le téléchargement démarre de toute façon.
    var FEEDBACK_URL = "https://nujxmiqbaxgrnvmjyecu.supabase.co/rest/v1/transcripilote_feedback";
    var FEEDBACK_KEY = "sb_publishable_rBvne54r2erDhYCKuWC5UA_0n-CkvE9"; // clé publique : ajout de réponses seulement
    var ASKED_KEY = "tp-feedback-asked";
    var SOURCES = [
        ["bouche_a_oreille", "Bouche-à-oreille"], ["travail", "Au travail, par un collègue"],
        ["linkedin", "LinkedIn"], ["reseaux_sociaux", "Autres réseaux sociaux"],
        ["recherche", "Moteur de recherche"], ["github", "GitHub"], ["autre", "Autre"],
    ];
    var COUNTRIES = ("AD AE AF AG AL AM AO AR AT AU AZ BA BB BD BE BF BG BH BI BJ BN BO BR BS BT BW BY BZ CA CD CF CG CH CI CL CM CN CO CR CU CV CY CZ DE DJ DK DM DO DZ EC EE EG ER ES ET FI FJ FM FR GA GB GD GE GH GM GN GQ GR GT GW GY HK HN HR HT HU ID IE IL IN IQ IR IS IT JM JO JP KE KG KH KI KM KN KP KR KW KZ LA LB LC LI LK LR LS LT LU LV LY MA MC MD ME MG MH MK ML MM MN MR MT MU MV MW MX MY MZ NA NE NG NI NL NO NP NR NZ OM PA PE PG PH PK PL PS PT PW PY QA RE RO RS RU RW SA SB SC SD SE SG SI SK SL SM SN SO SR SS ST SV SY SZ TD TG TH TJ TL TM TN TO TR TT TV TW TZ UA UG US UY UZ VA VC VE VN VU WS YE ZA ZM ZW").split(" ");

    var storage = function (action, value) {
        try { return action === "get" ? localStorage.getItem(ASKED_KEY) : localStorage.setItem(ASKED_KEY, value); }
        catch (e) { return null; }
    };
    var guessCountry = function () {
        var langs = navigator.languages || [navigator.language || ""];
        for (var i = 0; i < langs.length; i++) {
            var m = /-([A-Z]{2})$/i.exec(langs[i] || "");
            if (m && COUNTRIES.indexOf(m[1].toUpperCase()) >= 0) return m[1].toUpperCase();
        }
        return "";
    };
    var countryName = (function () {
        try { var dn = new Intl.DisplayNames(["fr"], { type: "region" }); return function (c) { return dn.of(c) || c; }; }
        catch (e) { return function (c) { return c; }; }
    })();
    var make = function (tag, attrs, text) {
        var el = document.createElement(tag);
        Object.keys(attrs || {}).forEach(function (k) { el.setAttribute(k, attrs[k]); });
        if (text) el.textContent = text;
        return el;
    };

    var showFeedback = function () {
        if (document.querySelector(".feedback") || storage("get")) return;
        var box = make("section", { "class": "feedback", role: "dialog", "aria-labelledby": "feedback-title" });
        box.appendChild(make("h2", { id: "feedback-title" }, "Votre téléchargement démarre"));
        box.appendChild(make("p", { "class": "feedback-intro" },
            "Deux questions facultatives pour savoir où TranscriPilote est utilisé. Seules vos réponses sont enregistrées, sans nom ni adresse e-mail. L'application, elle, n'envoie jamais rien."));
        var form = make("form", {});

        var country = make("select", { id: "fb-country", name: "country" });
        country.appendChild(make("option", { value: "" }, "Je préfère ne pas répondre"));
        COUNTRIES.map(function (c) { return [c, countryName(c)]; })
            .sort(function (a, b) { return a[1].localeCompare(b[1], "fr"); })
            .forEach(function (p) { country.appendChild(make("option", { value: p[0] }, p[1])); });
        country.value = guessCountry();
        var f1 = make("div", { "class": "fb-field" });
        f1.appendChild(make("label", { "for": "fb-country" }, "Depuis quel pays téléchargez-vous ?"));
        f1.appendChild(country);

        var source = make("select", { id: "fb-source", name: "source" });
        source.appendChild(make("option", { value: "" }, "Je préfère ne pas répondre"));
        SOURCES.forEach(function (s) { source.appendChild(make("option", { value: s[0] }, s[1])); });
        var detail = make("input", { id: "fb-detail", type: "text", maxlength: "120", placeholder: "Précisez si vous le souhaitez", hidden: "" });
        source.addEventListener("change", function () {
            detail.hidden = source.value !== "autre";
            if (!detail.hidden) detail.focus();
        });
        var f2 = make("div", { "class": "fb-field" });
        f2.appendChild(make("label", { "for": "fb-source" }, "Comment avez-vous connu TranscriPilote ?"));
        f2.appendChild(source);
        f2.appendChild(detail);

        var actions = make("div", { "class": "fb-actions" });
        var send = make("button", { type: "submit", "class": "btn btn-primary" }, "Envoyer");
        var skip = make("button", { type: "button", "class": "btn btn-ghost" }, "Non merci");
        actions.appendChild(send);
        actions.appendChild(skip);
        var status = make("p", { "class": "fb-status", "aria-live": "polite" });

        form.appendChild(f1);
        form.appendChild(f2);
        form.appendChild(actions);
        form.appendChild(status);
        box.appendChild(form);
        document.body.appendChild(box);
        requestAnimationFrame(function () { box.classList.add("open"); });
        country.focus();

        var close = function () {
            box.classList.remove("open");
            setTimeout(function () { box.remove(); }, 250);
        };
        skip.addEventListener("click", function () { storage("set", "skipped"); close(); });
        box.addEventListener("keydown", function (e) { if (e.key === "Escape") { storage("set", "skipped"); close(); } });

        form.addEventListener("submit", function (e) {
            e.preventDefault();
            var payload = {
                country: country.value || null,
                source: source.value || null,
                source_detail: source.value === "autre" && detail.value.trim() ? detail.value.trim().slice(0, 120) : null,
                version: latestVersion,
            };
            if (!payload.country && !payload.source) { status.textContent = "Choisissez au moins une réponse, ou cliquez sur « Non merci »."; return; }
            send.disabled = true;
            status.textContent = "Envoi…";
            fetch(FEEDBACK_URL, {
                method: "POST",
                headers: { apikey: FEEDBACK_KEY, "Content-Type": "application/json", Prefer: "return=minimal" },
                body: JSON.stringify(payload),
            }).then(function (r) {
                if (!r.ok) return Promise.reject();
                storage("set", "answered");
                status.textContent = "Merci, c'est noté. Bonne installation !";
                setTimeout(close, 1600);
            }).catch(function () {
                send.disabled = false;
                status.textContent = "L'envoi n'a pas abouti. Vous pouvez réessayer ou fermer cette fenêtre : le téléchargement n'est pas concerné.";
            });
        });
    };

    targets.forEach(function (a) {
        a.addEventListener("click", function () { setTimeout(showFeedback, 400); });
    });
})();
