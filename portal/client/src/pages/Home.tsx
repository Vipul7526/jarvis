/* Orbital Instrument direction: aerospace information design, deep ink surfaces, copper signal pins, honest release states. */
import { useState } from "react";
import {
  ArrowUpRight,
  BookOpen,
  Check,
  ChevronRight,
  CircleHelp,
  Download,
  ExternalLink,
  FileText,
  Github,
  Laptop,
  LockKeyhole,
  Menu,
  Play,
  Radio,
  ShieldCheck,
  Smartphone,
  Terminal,
  X,
} from "lucide-react";

const storage = {
  hero: "/manus-storage/jarvis-orbital-hero_2badad64.png",
  mark: "/manus-storage/jarvis-orbital-mark_347dddc9.png",
  network: "/manus-storage/jarvis-network-constellation_fdc5b179.png",
  release: "/manus-storage/jarvis-release-instrument_77baf359.png",
};

const releases = [
  { name: "Android APK", meta: "ARM64 • planned", state: "planned", icon: Smartphone, detail: "The Android package will ship after Flutter, Java platform channels, permissions, and signed release builds are verified." },
  { name: "Windows EXE", meta: "x64 • scaffolded", state: "scaffolded", icon: Laptop, detail: "The Windows service boundary and local AI integration are scaffolded. A signed executable is not published yet." },
  { name: "Windows setup wizard", meta: "MSI / wizard • planned", state: "planned", icon: Download, detail: "The installer will include service registration, model selection, diagnostics, and safe uninstall steps." },
  { name: "macOS DMG", meta: "Apple Silicon + Intel • planned", state: "planned", icon: Download, detail: "A DMG distribution is on the roadmap after the desktop client and signing pipeline are ready." },
  { name: "Linux packages", meta: "Ubuntu • Debian • Kali • planned", state: "planned", icon: Terminal, detail: "AppImage, deb, and distribution-specific packaging are planned for Ubuntu, Debian, Kali Linux, and other Linux systems." },
];

const faqs = [
  ["Is J.A.R.V.I.S. available as a finished APK or EXE?", "Not yet. The current release surface distinguishes scaffolded components from planned signed installers so nobody mistakes a roadmap item for a downloadable binary."],
  ["Where are AI credentials stored?", "Provider secrets belong on the backend or in local deployment configuration. They must never be embedded in Flutter, Android, Windows, or browser bundles."],
  ["Can it work without the Internet?", "The architecture includes a deterministic Offline Core and a localhost-only llama.cpp boundary. Offline model readiness will be shown only after a real model is installed and verified."],
  ["How do I request support?", "Use the project repository issues for implementation bugs and the Help Center below for setup guidance. Include diagnostics output without sharing API keys."],
];

function StatusPill({ state }: { state: string }) {
  return <span className={`status-pill status-${state}`}><span className="status-dot" />{state}</span>;
}

export default function Home() {
  const [menuOpen, setMenuOpen] = useState(false);
  const [selectedRelease, setSelectedRelease] = useState(releases[0]);
  const [openFaq, setOpenFaq] = useState<number | null>(0);

  return (
    <main className="site-shell">
      <header className="topbar">
        <a className="brand" href="#top" aria-label="J.A.R.V.I.S. home">
          <img src={storage.mark} alt="" className="brand-mark" />
          <span>J.A.R.V.I.S.<small>CONTROL / PORTAL</small></span>
        </a>
        <button className="menu-toggle" onClick={() => setMenuOpen(!menuOpen)} aria-label="Toggle navigation">{menuOpen ? <X /> : <Menu />}</button>
        <nav className={menuOpen ? "nav-links nav-open" : "nav-links"}>
          <a href="#system" onClick={() => setMenuOpen(false)}>System</a>
          <a href="#releases" onClick={() => setMenuOpen(false)}>Releases</a>
          <a href="#legal" onClick={() => setMenuOpen(false)}>Legal Center</a>
          <a href="#help" onClick={() => setMenuOpen(false)}>Help Center</a>
          <a className="nav-cta" href="https://github.com/Vipul7526/jarvis" target="_blank" rel="noreferrer">Open repository <ArrowUpRight size={15} /></a>
        </nav>
      </header>

      <section className="hero" id="top">
        <img className="hero-art" src={storage.hero} alt="Abstract orbital instrumentation around a connected intelligence node" />
        <div className="hero-copy">
          <p className="eyebrow"><Radio size={14} /> SIGNAL / 01 — PRIVATE INTELLIGENCE SYSTEM</p>
          <h1>One assistant.<br /><em>Every authorized surface.</em></h1>
          <p className="hero-lede">J.A.R.V.I.S. is a secure, cross-platform AI control system for people who want cloud intelligence, local models, voice, and device orchestration without surrendering control.</p>
          <div className="hero-actions">
            <a className="button button-copper" href="#releases">Inspect releases <ChevronRight size={17} /></a>
            <a className="button button-quiet" href="https://www.youtube.com/@jarvissubsystems" target="_blank" rel="noreferrer"><Play size={15} /> Watch @jarvissubsystems</a>
          </div>
        </div>
        <div className="hero-readout">
          <div className="readout-head"><span>READINESS BOARD</span><span className="mono">JDP / 1.0</span></div>
          <div className="readout-row"><span>AUTH / PAIRING</span><StatusPill state="verified" /></div>
          <div className="readout-row"><span>OFFLINE CORE</span><StatusPill state="scaffolded" /></div>
          <div className="readout-row"><span>NATIVE CLIENTS</span><StatusPill state="planned" /></div>
          <div className="readout-footer"><span>LAST CHECK</span><span className="mono">2026-08-31 / LOCAL</span></div>
        </div>
      </section>

      <section className="section section-system" id="system">
        <div className="section-rail"><span>02</span><span>THE SYSTEM</span></div>
        <div className="section-content split-layout">
          <div>
            <p className="eyebrow">A CONTROL PLANE, NOT A CHAT BOX</p>
            <h2>Intelligence that knows where it is allowed to act.</h2>
            <p className="body-copy">The architecture separates identity, trust, model routing, command risk, and device capability. A device on the same network is not automatically trusted. A high-risk command does not silently run. A missing integration is not presented as ready.</p>
            <a className="text-link" href="https://github.com/Vipul7526/jarvis#security-principles" target="_blank" rel="noreferrer">Read the security model <ArrowUpRight size={15} /></a>
          </div>
          <div className="network-card">
            <img src={storage.network} alt="Diagram showing connected phone, desktop, Linux, and cloud nodes" />
            <div className="network-caption"><span className="signal-pin" /> Four surfaces, one permission boundary</div>
          </div>
        </div>
        <div className="feature-strip">
          <article><LockKeyhole /><h3>Trust by pairing</h3><p>Numeric pairing and revocation keep commands tied to known devices.</p></article>
          <article><ShieldCheck /><h3>Confirmation gates</h3><p>Risk classification separates safe offline actions from sensitive operations.</p></article>
          <article><Terminal /><h3>Offline by design</h3><p>Cloud, local model, phone-local, and deterministic fallback routes stay explicit.</p></article>
        </div>
      </section>

      <section className="section section-releases" id="releases">
        <div className="section-rail"><span>03</span><span>THE RELEASES</span></div>
        <div className="section-content">
          <div className="section-heading-row"><div><p className="eyebrow">DOWNLOADS / TRUTHFUL STATUS</p><h2>Choose a surface. Check the signal.</h2></div><span className="heading-note">No fake binaries.<br />No silent placeholders.</span></div>
          <div className="release-layout">
            <div className="release-list">{releases.map((release) => { const Icon = release.icon; return <button key={release.name} className={`release-item ${selectedRelease.name === release.name ? "selected" : ""}`} onClick={() => setSelectedRelease(release)}><span className="release-icon"><Icon size={19} /></span><span className="release-name"><strong>{release.name}</strong><small>{release.meta}</small></span><StatusPill state={release.state} /><ChevronRight size={17} /></button>; })}</div>
            <div className="release-detail"><img src={storage.release} alt="Abstract release verification instrument" /><div className="detail-overlay"><StatusPill state={selectedRelease.state} /><h3>{selectedRelease.name}</h3><p>{selectedRelease.detail}</p><button className="button button-quiet" onClick={() => alert("This package is not published yet. Follow the repository for verified release announcements.")}>{selectedRelease.state === "scaffolded" ? "View implementation" : "Notify me when verified"} <ArrowUpRight size={15} /></button></div></div>
          </div>
        </div>
      </section>

      <section className="section section-legal" id="legal">
        <div className="section-rail"><span>04</span><span>LEGAL CENTER</span></div>
        <div className="section-content legal-layout">
          <div><p className="eyebrow">READ BEFORE FIRST RUN</p><h2>Permission starts with understanding.</h2><p className="body-copy">These documents explain how local, cloud, offline, and device-processing paths differ. They are part of the product surface—not a footer afterthought.</p></div>
          <div className="legal-links"><a href="https://github.com/Vipul7526/jarvis/blob/main/docs/legal/PRIVACY_POLICY.md" target="_blank" rel="noreferrer"><FileText /><span><strong>Privacy Policy</strong><small>Cloud, local, offline, and device processing</small></span><ExternalLink size={15} /></a><a href="https://github.com/Vipul7526/jarvis/blob/main/docs/legal/TERMS_AND_CONDITIONS.md" target="_blank" rel="noreferrer"><BookOpen /><span><strong>Terms & Conditions</strong><small>Use, limits, responsibilities, and service boundaries</small></span><ExternalLink size={15} /></a><a href="https://github.com/Vipul7526/jarvis/blob/main/docs/legal/USER_AGREEMENT.md" target="_blank" rel="noreferrer"><Check /><span><strong>User Agreement</strong><small>Plain-language first-run consent wording</small></span><ExternalLink size={15} /></a><a href="https://github.com/Vipul7526/jarvis/blob/main/docs/legal/DISCLAIMERS.md" target="_blank" rel="noreferrer"><ShieldCheck /><span><strong>AI & Device Disclaimers</strong><small>Human confirmation and safety boundaries</small></span><ExternalLink size={15} /></a></div>
        </div>
      </section>

      <section className="section section-help" id="help">
        <div className="section-rail"><span>05</span><span>HELP CENTER</span></div>
        <div className="section-content help-layout">
          <div><p className="eyebrow">FIELD GUIDE / SETUP</p><h2>Get the signal right before you ask it to move.</h2><p className="body-copy">Use the guides in the repository for backend setup, API keys, local AI, pairing, legal acceptance, and platform integration. Never paste secrets into issues or client bundles.</p><a className="button button-copper" href="https://github.com/Vipul7526/jarvis#api-setup-guide" target="_blank" rel="noreferrer">Open API setup guide <ArrowUpRight size={16} /></a></div>
          <div className="faq-list">{faqs.map(([question, answer], index) => <div className={`faq ${openFaq === index ? "faq-open" : ""}`} key={question}><button onClick={() => setOpenFaq(openFaq === index ? null : index)}><CircleHelp size={17} /><span>{question}</span><ChevronRight size={17} /></button>{openFaq === index && <p>{answer}</p>}</div>)}</div>
        </div>
      </section>

      <footer className="footer"><div className="footer-brand"><img src={storage.mark} alt="" /><span>J.A.R.V.I.S.<small>JUST A RATHER VERY INTELLIGENT SYSTEM</small></span></div><div className="footer-links"><a href="https://github.com/Vipul7526/jarvis" target="_blank" rel="noreferrer"><Github size={16} /> GitHub</a><a href="https://www.youtube.com/@jarvissubsystems" target="_blank" rel="noreferrer"><Play size={15} /> YouTube</a><a href="#legal">Legal</a><a href="#help">Help</a></div><p className="footer-note">A verified foundation in progress. Built around user control.</p></footer>
    </main>
  );
}
