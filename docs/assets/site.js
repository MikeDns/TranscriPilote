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

    // Bouton « Télécharger » : lien direct vers l'installateur de la dernière version.
    var targets = document.querySelectorAll("[data-download]");
    var versionEls = document.querySelectorAll("[data-version]");
    if (!targets.length && !versionEls.length) return;
    fetch("https://api.github.com/repos/MikeDns/TranscriPilote/releases/latest")
        .then(function (r) { return r.ok ? r.json() : Promise.reject(); })
        .then(function (rel) {
            var exe = (rel.assets || []).filter(function (a) { return /^TranscriPilote-Setup-.+\.exe$/.test(a.name); })[0];
            if (!exe) return;
            targets.forEach(function (a) { a.href = exe.browser_download_url; });
            var label = "Version " + rel.tag_name.replace(/^v/, "") + " · " + Math.round(exe.size / 1048576) + " Mo";
            versionEls.forEach(function (el) { el.textContent = label + " · " + el.getAttribute("data-version"); });
        })
        .catch(function () {});
})();
