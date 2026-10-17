#!/usr/bin/env python3
"""Generate the M2Log static pages from shared partials. Run from the repo root."""
import sys, os
from PIL import Image

ROOT = sys.argv[1] if len(sys.argv) > 1 else '.'
SITE = 'https://m2log-v2.vercel.app'
GA = 'G-XVNJRPJJVC'
CTA_LABEL = '無料で相談する'
TAG = '届けるまでが、つくること。'

NAV = [('Services', 'services'), ('About', 'about'), ('Plans', 'plans'), ('Contact', 'contact')]


def href(p, page):
    if page == 'home':
        return f'{p}index.html'
    return f'{p}pages/{page}.html' if p == '' else f'{page}.html'


CRUMBS = {'/pages/services.html': 'サービス', '/pages/about.html': '私たちについて', '/pages/plans.html': '料金・プラン',
          '/pages/contact.html': 'お問い合わせ', '/pages/privacy.html': 'プライバシーポリシー'}


def jsonld(path):
    import json
    org = {
        "@type": "Organization", "@id": SITE + "/#org", "name": "株式会社M2Log", "alternateName": "M2Log",
        "url": SITE + "/", "logo": SITE + "/assets/img/logo/m2log_logo_navy.svg", "email": "n.ryosuke@m2log.jp",
        "foundingDate": "2024-10", "founder": {"@type": "Person", "name": "中村陵介"},
        "address": {"@type": "PostalAddress", "addressLocality": "江東区", "addressRegion": "東京都", "addressCountry": "JP"},
        "areaServed": "JP", "sameAs": ["https://www.instagram.com/m2log_1003/"],
        "award": ["第13回 BOVA オンライン動画部門 協賛企業賞", "第13回 BOVA 縦型動画部門 ファイナリスト作品", "「推して、秋田」映像コンテスト2026 準グランプリ"],
        "knowsAbout": ["TikTok運用代行", "ショート動画広告", "ショートドラマ制作", "WebCM制作", "ブランドムービー制作", "SNS広告運用"],
    }
    graph = [org, {"@type": "WebSite", "@id": SITE + "/#website", "url": SITE + "/", "name": "M2Log", "inLanguage": "ja", "publisher": {"@id": SITE + "/#org"}}]
    if path in CRUMBS:
        graph.append({"@type": "BreadcrumbList", "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "ホーム", "item": SITE + "/"},
            {"@type": "ListItem", "position": 2, "name": CRUMBS[path], "item": SITE + path}]})
    return '<script type="application/ld+json">' + json.dumps({"@context": "https://schema.org", "@graph": graph}, ensure_ascii=False) + '</script>'


def head(title, desc, path, p):
    url = SITE + path
    fonts = 'https://fonts.googleapis.com/css2?family=Dela+Gothic+One&family=Zen+Kaku+Gothic+New:wght@400;500;700;900&display=swap'
    return f'''<!DOCTYPE html>
<html lang="ja">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{title}</title>
<meta name="description" content="{desc}">
<meta property="og:type" content="website">
<meta property="og:site_name" content="M2Log">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:image" content="{SITE}/assets/ogp_2026.jpg">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:image:alt" content="M2Log　届けるまでが、つくること。">
<meta property="og:url" content="{url}">
<meta name="twitter:card" content="summary_large_image">
<link rel="canonical" href="{url}">
<link rel="icon" href="{p}assets/favicon.ico">
<link rel="icon" type="image/svg+xml" href="{p}assets/favicon.svg">
<link rel="apple-touch-icon" href="{p}assets/apple-touch-icon.png">
<meta name="theme-color" content="#FFFEFA">
<script async src="https://www.googletagmanager.com/gtag/js?id={GA}"></script>
<script>window.dataLayer=window.dataLayer||[];function gtag(){{dataLayer.push(arguments);}}gtag('js',new Date());gtag('config','{GA}');</script>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="preload" as="style" href="{fonts}">
<link rel="stylesheet" href="{fonts}" media="print" onload="this.media='all'">
<noscript><link rel="stylesheet" href="{fonts}"></noscript>
<link rel="stylesheet" href="{p}assets/css/site.css">
{jsonld(path)}
</head>
<body>
'''


def header(p, current):
    items = ''.join(
        f'<a href="{href(p, key)}"{" aria-current=\"page\"" if key == current else ""}>{label}</a>'
        for label, key in NAV)
    return f'''<header class="hd">
  <div class="wrap">
    <a class="hd-logo" href="{href(p, 'home')}"><img src="{p}assets/img/logo/m2log_logo_navy.svg" alt="M2Log" width="122" height="30"></a>
    <button class="hd-menu" type="button" aria-expanded="false" aria-controls="hd-nav" aria-label="メニューを開く"><span></span><span></span><span></span></button>
    <nav class="hd-nav" id="hd-nav" aria-label="メインメニュー">
      {items}
      <a class="btn" href="{href(p, 'contact')}">{CTA_LABEL}</a>
    </nav>
  </div>
</header>
'''


def cta(p, title='まず30分、<br>話してみませんか。',
        body='何から手をつければいいか分からない状態でも大丈夫です。オンラインで30分、今の状況を伺い、その場で方向性と予算感までお伝えします。無理な提案・営業はしません。'):
    return f'''<section class="cta" aria-labelledby="cta-h">
  <div class="wrap">
    <h2 id="cta-h">{title}</h2>
    <div>
      <p>{body}</p>
      <div class="btns"><a class="btn btn--light" href="{href(p, 'contact')}">{CTA_LABEL}<small>30分・オンライン</small></a><a class="btn btn--ghost" href="{href(p, 'plans')}">料金を見る</a></div>
    </div>
  </div>
</section>
'''


def footer(p):
    nav = ''.join(f'<li><a href="{href(p, k)}">{l}</a></li>' for l, k in NAV)
    return f'''<footer class="ft">
  <div class="wrap">
    <div class="ft-top">
      <div>
        <a class="ft-logo" href="{href(p, 'home')}"><img src="{p}assets/img/logo/m2log_logo_white.svg" alt="M2Log" width="138" height="34"></a>
        <p class="ft-tag">{TAG}</p>
      </div>
      <div class="ft-cols">
        <ul class="ft-nav">{nav}<li><a href="{href(p, 'privacy')}">プライバシーポリシー</a></li></ul>
        <div class="ft-info"><span>株式会社M2Log</span><span>東京都江東区</span><a href="https://www.instagram.com/m2log_1003/" target="_blank" rel="noopener">Instagram</a></div>
      </div>
    </div>
    <p class="ft-copy">© 2026 M2Log Inc. All rights reserved.</p>
  </div>
</footer>
<div class="mcta" aria-hidden="true"><p><b>まず30分、話してみませんか</b>オンライン・無料</p><a class="btn" href="{href(p, 'contact')}" tabindex="-1">{CTA_LABEL}</a></div>
<script src="{p}assets/js/site.js" defer></script>
</body>
</html>
'''


def page_hd(p, crumb, en, h1, lead, extra=''):
    return f'''<div class="page-hd">
  <div class="wrap">
    <nav class="crumb" aria-label="パンくず"><a href="{href(p, 'home')}">Home</a><span aria-hidden="true">/</span><span>{crumb}</span></nav>
    <h1><span class="h1-kw">{en}</span>{h1}</h1>
    <p class="lead">{lead}</p>
    {extra}
  </div>
</div>
'''


def nextlink(p, key, label, title):
    return f'<div class="wrap"><a class="next" href="{href(p, key)}"><div><span>次のページ　{label}</span><b>{title}</b></div><span aria-hidden="true" style="font-size:22px;color:var(--navy)">›</span></a></div>\n'


# ----------------------------------------------------------------- works
WORKS = [
    ('169', 'works_award', '「水の通知 OFF」', '富士山GXホールディングス「エブリィフレシャス」課題', '第13回 BOVA オンライン動画部門 協賛企業賞'),
    ('916', 'works_sbi', '「青春を、僕らは愛してる」', 'SBI証券 課題', '第13回 BOVA 縦型動画部門 ファイナリスト作品'),
    ('169', 'works_akita', '「あなたの秋田推し度を診断します」', '「推して、秋田」映像コンテスト2026', '準グランプリ'),
    ('239', 'works_rinx', '「毎日の余白編」', 'RINX webCM', ''),
    ('916', 'works_fujisan', '富士山マラソン', 'アールビーズ', ''),
    ('916', 'works_kyoto', 'KYOTO 撮影の裏側', 'M2VLog オリジナル', ''),
]


def strip(p, works=None):
    out = []
    for r, key, title, meta, badge in (works or WORKS):
        ratio = {'169': '16:9 横型', '239': '横型 webCM', '916': '9:16 縦型'}[r]
        b = f'<br><span class="badge">{badge}</span>' if badge else ''
        out.append(f'''      <figure class="clip clip--{r}">
        <div class="clip-media">
          <video preload="none" playsinline poster="{p}assets/img/{key}_poster.jpg" aria-label="{title.strip('「」')}（{meta}）の動画"><source src="{p}assets/video/{key}.mp4" type="video/mp4"></video>
          <span class="clip-ratio">{ratio}</span>
          <button class="clip-play" type="button" aria-label="{title.strip('「」')}を再生"><span></span></button>
        </div>
        <figcaption><b>{title}</b>{meta}{b}</figcaption>
      </figure>''')
    return '\n'.join(out)


# ----------------------------------------------------------------- pages
def index():
    p = ''
    desc = 'TikTok運用代行、ショート動画広告・ショートドラマ制作、WebCM・ブランドムービー制作の株式会社M2Log。企画・撮影・編集・広告運用まで内製のチームが、担当者として成果まで伴走します。東京・江東区から全国対応。'
    h = head(f'TikTok運用代行・ショート動画制作のM2Log｜{TAG}', desc, '/', p) + header(p, 'home')
    body = f'''<main>
<section class="hero">
  <div class="wrap hero-grid">
    <h1 class="disp h-hero"><span class="h1-kw">TikTok運用代行・ショート動画広告・WebCM制作のM2Log</span>届けるまでが、<br>つくること。</h1>
    <div class="hero-side">
      <p class="lead">SNSで届く企画と、映像をつくる力。その両方を持つチームが、御社の担当者として隣で走り続けます。一本で終わらない関係を、つくりたいと思っています。</p>
      <div class="btns"><a class="btn" href="pages/contact.html">{CTA_LABEL}<small>30分・オンライン</small></a><a class="btn btn--ghost" href="#works">作品を見る</a></div>
    </div>
  </div>
  <div id="works" class="works">
    <div class="wrap works-head"><h2 class="works-h">縦型</h2><p>TikTok運用・ショート動画広告・ショートドラマ</p><a class="textlink" href="pages/services.html#sns">縦型のサービス</a></div>
    <div class="strip-wrap" tabindex="0" aria-label="縦型の作品（横にスクロールできます）">
      <div class="strip strip--v">
{strip(p, [w for w in WORKS if w[0] == '916'])}
      </div>
    </div>
    <div class="wrap works-head"><h2 class="works-h">横型</h2><p>WebCM・ブランドムービー</p><a class="textlink" href="pages/services.html#video">横型のサービス</a></div>
    <div class="strip-wrap" tabindex="0" aria-label="横型の作品（横にスクロールできます）">
      <div class="strip strip--h">
{strip(p, [w for w in WORKS if w[0] != '916'])}
      </div>
    </div>
  </div>
  <div class="wrap">
    <p class="strip-hint">横にスワイプすると、ほかの作品も見られます。</p>
    <ul class="proof" aria-label="受賞歴"><li>第13回 BOVA オンライン動画部門 協賛企業賞</li><li>第13回 BOVA 縦型動画部門 ファイナリスト作品</li><li>「推して、秋田」映像コンテスト2026 準グランプリ</li></ul>
    <p class="clients">制作・運用実績（五十音順）：奥ジャパン株式会社／有限会社キコリ／株式会社CS日本／株式会社西武・プリンスホテルズワールドワイド／セガサミーホールディングス株式会社／株式会社セガ フェイブ／テレビ愛知株式会社／日本トイザらス株式会社／株式会社パン・パシフィック・インターナショナルホールディングス／株式会社PHONE APPLI／福島鰹株式会社／株式会社MIXI／株式会社リンクスホールディングス／株式会社WAKAMATSU ほか</p>
  </div>
</section>

<section class="sec" aria-labelledby="st-h">
  <div class="wrap statement">
    <h2 class="disp h-sec" id="st-h">映像は、<br>公開してからが本番。</h2>
    <div>
      <p>いい映像をつくる。そこまでは、私たちにとって当たり前のことです。</p>
      <p>本当の勝負は公開したあと。最後まで見られるか、届いてほしい人に届くか、見た人が動いてくれるか。そこまで考えて企画し、数字を見ながら次の一本に活かす。私たちは、それを「つくる」と呼んでいます。</p>
    </div>
  </div>
</section>

<section class="sec sec--tint" aria-labelledby="svc-h">
  <div class="wrap">
    <div class="sec-head"><h2 class="disp h-sec" id="svc-h">できること</h2><p class="lead">縦型のSNS動画も、横型のCMも。どれも「誰に届けて、どう動いてもらうか」というマーケティングの視点から設計します。</p></div>
    <div class="svc-grid">
      <a class="svc" href="pages/services.html#sns">
        <div class="svc-media"><img src="assets/img/img_scene3.jpg" alt="" loading="lazy"><img src="assets/img/works_sbi_poster.jpg" alt="" loading="lazy"><img src="assets/img/works_kyoto_poster.jpg" alt="" loading="lazy"></div>
        <div><span class="label">縦型・SNS</span><h3>TikTokアカウント運用代行</h3></div>
        <p>担当者としてチームに入り、企画・撮影から投稿、月次の改善まで回します。</p>
        <span class="more">詳しく見る</span>
      </a>
      <a class="svc" href="pages/services.html#drama">
        <div class="svc-media"><img src="assets/img/IMG_3228.JPG" alt="" loading="lazy"><img src="assets/img/works_fujisan_poster.jpg" alt="" loading="lazy"><img src="assets/img/studio2.jpg" alt="" loading="lazy"></div>
        <div><span class="label">縦型・広告／ドラマ</span><h3>ショート動画広告・ショートドラマ制作</h3></div>
        <p>広告として成果を出すショート動画と、続きが気になるショートドラマ。テレビやCMの現場出身のメンバーがつくります。</p>
        <span class="more">詳しく見る</span>
      </a>
      <a class="svc" href="pages/services.html#video">
        <div class="svc-media svc-media--wide"><img src="assets/img/works_rinx_card.jpg" alt="" loading="lazy"></div>
        <div><span class="label">横型・CM／ブランド</span><h3>WebCM・ブランドムービー制作</h3></div>
        <p>WebCM、ブランドムービー、採用・広告。映像をどう使うかから設計します。</p>
        <span class="more">詳しく見る</span>
      </a>
    </div>
    <p class="note-inhouse"><b>企画・脚本・撮影・編集は、すべて内製。</b>外部委託を挟まないから、意図がずれず、修正も改善も速い。</p>
  </div>
</section>

<section class="sec sec--tint" aria-labelledby="team-h">
  <div class="wrap team">
    <figure class="team-photo"><img src="assets/img/team_pc.jpg" alt="M2Logのメンバー5人" loading="lazy"></figure>
    <div class="team-body">
      <h2 class="disp h-sec" id="team-h">映像をつくる前に、<br>チームに入る。</h2>
      <p>外注は、納品したら終わり。でも映像もSNSも、つくったあとが本番です。だからM2Logは担当者として会議に出て、一緒に考え、届くところまで動きます。</p>
      <blockquote class="quote">「チームが増えたみたい」と言ってもらえることが、一番うれしい。<cite>代表取締役　中村陵介</cite></blockquote>
      <a class="textlink" href="pages/about.html">メンバーを見る</a>
    </div>
  </div>
</section>

<section class="sec" aria-labelledby="flow-h">
  <div class="wrap">
    <div class="sec-head"><h2 class="disp h-sec" id="flow-h">相談から、最初の一本が<br>世に出るまで。</h2><p class="lead">ご契約から1か月〜1か月半ほどで、最初の動画を公開します。</p></div>
    <ol class="steps" style="list-style:none;padding:0;margin:0">
      <li class="step"><span class="step-n">0</span><span class="step-when">契約前・無料</span><h3>無料相談</h3><p>まず話して、課題を整理します。方向が見えてきたら、ご提案の際にコンセプトとKPIの考え方までお持ちします。</p></li>
      <li class="step"><span class="step-n">1</span><span class="step-when">1〜2週目</span><h3>キックオフ・インプット</h3><p>資料をいただき、話を聞き、現場にも足を運びます。企画の精度は、ここで決まります。</p></li>
      <li class="step"><span class="step-n">2</span><span class="step-when">2〜3週目</span><h3>企画・撮影</h3><p>設計に沿って企画を固め、撮影へ。企画から編集まで、同じチームが担当します。</p></li>
      <li class="step"><span class="step-n">3</span><span class="step-when">4〜6週目</span><h3>初稿・公開</h3><p>撮影から約10日で初稿をお送りします。チェックを経て、最初の動画が世に出ます。</p></li>
    </ol>
    <p class="after">公開後は、月1回以上の定例に<b>代表が直接参加</b>します。月次レポートと改善提案を重ね、翌月の企画に反映していきます。</p>
  </div>
</section>

<section class="sec sec--tint" aria-labelledby="ways-h">
  <div class="wrap">
    <div class="sec-head"><h2 class="disp h-sec" id="ways-h">頼み方は、2つ。</h2><p class="lead">1本だけでも、まるごとでも。どちらの入口からでも、同じチームが動きます。</p></div>
    <div class="ways">
      <div class="way">
        <span class="label">1本からの映像制作</span>
        <h3>映像を、1本からつくりたい</h3>
        <p>WebCM、ブランドムービー、採用動画、ショート動画。単発のご依頼も、企画から入って納品まで運びます。</p>
        <dl class="prices"><div><dt>ショート動画（縦型）</dt><dd>1本 <b>15</b>万円〜</dd></div><div><dt>WebCM・採用・ブランドムービー</dt><dd><b>30</b>万円〜</dd></div></dl>
        <p>企画・撮影・編集込み。お見積りは無償です。</p>
        <a class="btn btn--ghost" href="pages/plans.html#production">制作について見る</a>
      </div>
      <div class="way">
        <span class="label">継続のSNS運用</span>
        <h3>SNSを、まるごと任せたい</h3>
        <p>担当者としてチームに入り、企画・撮影・編集・投稿・分析まで一貫して。制作も内製だから、「つくる」と「届ける」を分けずに任せられます。</p>
        <dl class="prices"><div><dt>フル運用代行</dt><dd>月額 <b>60</b>万円〜</dd></div><div><dt>伴走型（3か月のトライアル）</dt><dd>月額 <b>29</b>万円〜</dd></div></dl>
        <p>どちらも広告費を含んだ金額で、まず3か月から始められます。別途かかるのは交通費・諸経費のみです。内容・本数・体制によって形が変わるため、ご相談時に「この予算で何ができるか」を率直にお伝えします。</p>
        <a class="btn btn--ghost" href="pages/plans.html#partnership">プランを見る</a>
      </div>
    </div>
  </div>
</section>

<section class="sec" aria-labelledby="faq-h">
  <div class="wrap">
    <div class="sec-head"><h2 class="disp h-sec" id="faq-h">よくある質問</h2></div>
    <div class="faq">
      <details><summary>金額感が分かりません。</summary><p class="a">目安として、単発のショート動画は1本15万円〜、まるごと任せるフル運用代行は月5本で月額60万円〜（広告費含む）、まず小さく試せる伴走型は、3か月のトライアルが月額29万円（広告費含む）です。内容・本数で変わるため、ご相談時に「この予算で何ができるか」を率直にお伝えします。お見積りは無償です。</p></details>
      <details><summary>具体的な案がなくても相談できますか？</summary><p class="a">できます。実際、ほとんどのご相談がその状態から始まります。方向が見えてきたら、ご提案の際にコンセプトとKPIの考え方までお持ちするので、比較検討の材料としてもお使いいただけます。</p></details>
      <details><summary>東京以外でも対応できますか？</summary><p class="a">撮影・打ち合わせとも、全国に伺えます。出張にかかる費用は、お見積りの段階で明示してご提案します。オンラインでの定例・相談にも対応しています。</p></details>
      <details><summary>ほかの映像制作会社・SNS運用会社との違いは？</summary><p class="a">一番の違いは、映像をつくる力とSNSを運用する力を、同じチームで持っていることです。テレビ、CM、スポーツ撮影と、それぞれ別の現場で経験を積んだ5人がいるので、企画から撮影・編集まで社内で完結できます。そのうえで、つくったあとの投稿や振り返りまで、担当者として一緒に追いかけます。SNS運用・広告・単発制作のどれかに縛られず、目的に合う形を選べるのも、この体制だからです。一度話してもらえれば、チームの雰囲気もすぐに伝わると思います。</p></details>
    </div>
    <p style="margin-top:24px"><a class="textlink" href="pages/plans.html#faq">ほかの質問を見る</a></p>
  </div>
</section>
</main>
'''
    return h + body + cta(p) + footer(p)


def services():
    p = '../'
    desc = 'M2LogのTikTok運用代行、ショート動画広告・ショートドラマ制作、WebCM・ブランドムービー制作。企画から撮影・編集・投稿・広告運用・改善まで、ひとつのチームで一貫して担当します。'
    h = head('サービス｜TikTok運用代行・ショート動画広告・WebCM制作｜M2Log', desc, '/pages/services.html', p) + header(p, 'services')
    extra = '<nav class="subnav" aria-label="ページ内"><a href="#sns">TikTok運用代行</a><a href="#drama">ショート動画広告・ドラマ</a><a href="#video">WebCM・ブランドムービー</a><a href="#how">進め方</a></nav>'
    body = page_hd(p, 'サービス', 'サービス｜TikTok運用代行・ショート動画広告・WebCM制作', 'つくって、届けて、<br>また一緒に考える。',
                   '外注ではなく、担当者として動く。だから意図がずれない。だから、届く。', extra) + f'''<main>
<section class="sec">
  <div class="wrap">
    <article class="sd" id="sns">
      <div class="sd-media"><img src="{p}assets/img/img_scene3.jpg" alt="スマートフォンで縦型動画を撮影する現場"><img src="{p}assets/img/works_sbi_poster.jpg" alt="縦型動画の一場面"></div>
      <div class="sd-body">
        <span class="label">縦型・SNS</span>
        <h2>TikTokアカウント運用代行</h2>
        <p>バズを生むことも大切ですが、それがゴールではありません。投稿には一本ずつ狙いがあります。来てほしいコメントは来たか。最後まで見られたか。狙い通りに保存されたか。再生数だけでなく「狙った反応」との答え合わせを繰り返し、翌月の企画に反映します。SNS担当者として、継続的に伴走します。</p>
        <ul class="tags"><li>コンセプト・KPI設計</li><li>企画・撮影・編集</li><li>投稿・コメント運用</li><li>月次レポート・改善</li><li>TikTok広告支援</li></ul>
      </div>
    </article>
    <article class="sd" id="drama">
      <div class="sd-media"><img src="{p}assets/img/IMG_3228.JPG" alt="スタジオでモニターを確認しながら撮影するスタッフ"><img src="{p}assets/img/works_fujisan_poster.jpg" alt="縦型動画の一場面"></div>
      <div class="sd-body">
        <span class="label">縦型・広告／ドラマ</span>
        <h2>ショート動画広告・ショートドラマ制作</h2>
        <p>広告のショート動画は、1本つくって終わりではありません。配信して反応を見ながら、切り口を変えて次の1本をつくる。その繰り返しで、成果の出る形を探していきます。ショートドラマも同じで、視聴者の反応を見ながら次の話を考えます。</p>
        <p>テレビやCMの現場で経験を積んだメンバーが、企画・撮影・編集をすべて社内で回しているので、このスピードで動けます。</p>
        <ul class="tags"><li>ショート動画広告</li><li>広告クリエイティブ開発（検証込み）</li><li>ショートドラマ</li><li>SNSキャンペーン動画</li><li>商品・サービス紹介</li><li>インタビュー動画</li><li>タレント・インフルエンサー起用</li></ul>
      </div>
    </article>
    <article class="sd" id="video">
      <div class="sd-media sd-media--wide"><img src="{p}assets/img/works_award_poster.jpg" alt="「水の通知 OFF」の一場面。スマートフォンを手にした男性と水の通知"><img src="{p}assets/img/works_akita_poster.jpg" alt="「あなたの秋田推し度を診断します」の一場面。夜の盆踊りと秋田県の輪郭線"></div>
      <div class="sd-body">
        <span class="label">横型・CM／ブランド</span>
        <h2>WebCM・ブランドムービー制作</h2>
        <p>SNSだけでなく、WebCM、ブランドムービー、採用、広告まで。「この映像をどこで、誰に、どう使うか」から一緒に考えます。目的に合わせた使い方まで設計し、つくって終わりにしない活用を提案します。</p>
        <ul class="tags"><li>WebCM・ブランドムービー</li><li>SNS・Web広告動画</li><li>採用動画・採用SNS</li><li>HP・LP掲載用動画</li><li>キャンペーン設計</li><li>キャスティング・PR</li></ul>
      </div>
    </article>
  </div>
</section>

<section class="sec sec--tint" id="how" aria-labelledby="how-h">
  <div class="wrap">
    <div class="sec-head"><h2 class="disp h-sec" id="how-h">企画から改善まで、<br>ひとつのチームで。</h2><p class="lead">企画・脚本・撮影・編集はすべて内製です。外部委託を挟まないから、意図がずれず、修正も改善も速い。</p></div>
    <ol class="cycle" style="list-style:none;padding:0;margin:0">
      <li class="step"><span class="step-n">1</span><h3>戦略・企画</h3><p>何を、誰に届けたいのか。整理するところから始めます。目的・ターゲット・媒体の特性を踏まえ、勝ち筋を設計します。</p></li>
      <li class="step"><span class="step-n">2</span><h3>制作・運用</h3><p>設計した方針をもとに、企画・撮影・編集・投稿まで一気通貫で。媒体ごとの見られ方も踏まえ、伝わる形に落とし込みます。</p></li>
      <li class="step"><span class="step-n">3</span><h3>分析・改善</h3><p>結果を振り返り、次にどう伸ばすかまで考えます。数字だけでなく、視聴者の反応や文脈も踏まえて改善を提案します。</p></li>
    </ol>
    <p class="loopnote">分析で得た学びは、次の企画へ。ここが「つくって終わり」との違いです。</p>
  </div>
</section>
</main>
''' + nextlink(p, 'about', 'About', 'つくっているのは、この5人。')
    return h + body + cta(p, 'なにをつくるかから、<br>一緒に考えられます。', '目的がまだ曖昧でも大丈夫です。整理するところから、担当者として入ります。') + footer(p)


def about():
    p = '../'
    desc = 'テレビ、CM、スポーツ撮影の現場から集まった5人のチーム。株式会社M2Logの会社概要、メンバー紹介、受賞歴（BOVA協賛企業賞ほか）をご紹介します。'
    h = head('私たちについて｜映像制作とSNS運用のチーム｜M2Log', desc, '/pages/about.html', p) + header(p, 'about')
    members = [
        ('member_ceo', '中村陵介', 'CEO／Creative Director', '元ランニングインストラクター', 'エンタメとマーケティングの掛け算で、成果から逆算する。'),
        ('member_director', '佐藤峻', 'Creative Director', '元テレビディレクター', '編集まで見据えて撮る。ユーモアで、最後まで見せる。'),
        ('member_camera', '川村敬亮', 'Videographer／Photographer', '元スポーツカメラマン', 'スポーツ撮影で鍛えた判断力で、一瞬の美しさを逃さない。'),
        ('member_editor', '佐藤可弥', 'Editor／Art Director', '元テレビディレクター', 'アートと実用のあいだで、伝わる見せ方をつくる。'),
        ('member_producer', '冨田祐子', 'Producer', '元テレビ・CM制作', 'テレビとCMで培った段取りで、チームを支える。'),
    ]
    mh = '\n'.join(f'''      <div class="member"><div class="member-photo"><img src="{p}assets/img/members/{k}.jpg" alt="{n}" width="600" height="600" decoding="async"></div><div><span class="role">{r}</span><h3>{n}</h3><span class="from">{f}</span></div><p>{q}</p></div>''' for k, n, r, f, q in members)
    scenes = [('scene9', '撮影現場で笑顔を見せるスタッフ'), ('scene3', 'スマートフォンで撮影する現場'), ('studio1', 'スタジオでモニターを確認する撮影'),
              ('scene_meeting', '打ち合わせの様子'), ('scene8', 'ショートドラマの撮影'), ('scene6', 'クライアント先での撮影'),
              ('scene7', '撮影の準備をするスタッフ'), ('prob', '制作の様子')]
    sh = ''.join(f'<figure class="scene"><img src="{p}assets/img/{k}.jpg" alt="{a}" loading="lazy" width="{Image.open("assets/img/"+k+".jpg").width}" height="{Image.open("assets/img/"+k+".jpg").height}"></figure>' for k, a in scenes)
    body = page_hd(p, '私たちについて', '私たちについて｜会社概要・メンバー', '映像をつくる前に、<br>チームに入る。',
                   'チームの一員として、企画から届けるところまで一緒に動く。それがM2Logのやり方です。') + f'''<main>
<section class="sec" aria-labelledby="mem-h">
  <div class="wrap">
    <div class="sec-head"><h2 class="disp h-sec" id="mem-h">チームを紹介します。</h2><p class="lead">テレビ、CM、スポーツ撮影。それぞれの現場から集まった5人です。</p></div>
    <div class="members">
{mh}
    </div>
  </div>
</section>

<section class="sec sec--tint" aria-labelledby="sc-h" style="padding-bottom:calc(var(--sec) - 8px)">
  <div class="wrap"><div class="sec-head"><h2 class="disp h-sec" id="sc-h">現場の空気感。</h2></div></div>
  <div class="strip-wrap" style="margin-top:0" tabindex="0" aria-label="制作現場の写真（横にスクロールできます）"><div class="scenes">{sh}</div></div>
</section>

<section class="sec" aria-labelledby="co-h">
  <div class="wrap">
    <div class="sec-head"><h2 class="disp h-sec" id="co-h">会社概要</h2></div>
    <div class="table-wrap"><table class="table">
      <tr><th scope="row">会社名</th><td>株式会社M2Log</td></tr>
      <tr><th scope="row">代表者</th><td>代表取締役　中村陵介</td></tr>
      <tr><th scope="row">設立</th><td>2024年10月</td></tr>
      <tr><th scope="row">所在地</th><td>東京都江東区</td></tr>
      <tr><th scope="row">事業内容</th><td>映像制作／SNSアカウント運用代行／映像マーケティング支援</td></tr>
      <tr><th scope="row">対応媒体</th><td>TikTok／Instagram／YouTube／Web広告</td></tr>
      <tr><th scope="row">受賞歴</th><td>第13回 BOVA（Brain Online Video Award）オンライン動画部門 協賛企業賞<br>第13回 BOVA 縦型動画部門 ファイナリスト作品<br>「推して、秋田」映像コンテスト2026 準グランプリ</td></tr>
    </table></div>
  </div>
</section>
</main>
''' + nextlink(p, 'plans', 'Plans', '頼み方と、料金のこと。')
    return h + body + cta(p, 'チームの一員として、<br>入らせてください。', 'まず話すだけで大丈夫です。どんな状態からでも構いません。') + footer(p)


def plans():
    p = '../'
    desc = 'M2Logの料金。ショート動画は1本15万円〜、TikTok運用代行は月額60万円〜（広告費含む）、まず小さく試せる3か月トライアルは月額29万円。プランの違いとよくある質問もまとめています。'
    h = head('料金・プラン｜TikTok運用代行・ショート動画制作の費用｜M2Log', desc, '/pages/plans.html', p) + header(p, 'plans')
    extra = '<nav class="subnav" aria-label="ページ内"><a href="#price">料金の早見表</a><a href="#production">1本からの映像制作</a><a href="#partnership">SNS運用プラン</a><a href="#start">まずは相談から</a><a href="#faq">よくある質問</a></nav>'
    faqs = [
        ('映像1本だけの依頼でもできますか？', 'できます。1本のご依頼でも、目的とターゲットの整理から入り、届く形で納品します。実際、最初の1本をきっかけに、運用や継続のお付き合いへ広がるケースがほとんどです。'),
        ('具体的な案が何もないのですが、ゼロから相談できますか？', 'できます。まずは「何を達成したいか（採用・認知・売上など）」と「今ある素材・体制」を伺い、企画の方向性から一緒に整理します。ラフなメモ1枚でも、想いだけでも大丈夫です。'),
        ('代理店経由での発注や、パートナーとしても依頼できますか？', 'できます。代理店さまの進行フローに合わせ、窓口一本で対応します。守秘・体制面（資料整備、提案同席など）もご相談ください。'),
        ('ほかの映像制作会社・SNS運用会社との違いは？', '一番の違いは、映像をつくる力とSNSを運用する力を、同じチームで持っていることです。テレビ、CM、スポーツ撮影と、それぞれ別の現場で経験を積んだ5人がいるので、企画から撮影・編集まで社内で完結できます。そのうえで、つくったあとの投稿や振り返りまで、担当者として一緒に追いかけます。SNS運用・広告・単発制作のどれかに縛られず、目的に合う形を選べるのも、この体制だからです。一度話してもらえれば、チームの雰囲気もすぐに伝わると思います。'),
        ('実績をもっと見せてもらえますか？', '公開できるものは一部のため、目的・業種・表現トーンが近い事例を中心にご案内します。お問い合わせ時に「つくりたい方向性」を添えていただけるとスムーズです。'),
        ('金額感が分かりません。どれくらいの予算で依頼できますか？', '目安として、ショート動画は1本15万円〜、WebCM・ブランドムービー・採用動画は30万円〜、まるごと任せるフル運用代行は月5本で月額60万円〜（広告費含む）、まず小さく試せる伴走型は、3か月のトライアルが月額29万円（広告費含む）です（いずれも企画・撮影・編集込み、交通費などの実費は別途）。内容・本数・体制によって形が変わるため、ご相談時に「この予算で何ができるか」を率直にお伝えします。広告用クリエイティブ開発など規模の大きな案件は、個別にお見積りします。お見積りは無償です。'),
        ('社員の出演は必要ですか？', '必須ではありません。出演者なしで成立する企画も設計できますし、外部キャストを立てての制作もできます。逆に「社内の人が出るからこそ効く」企画もあるため、目的と社内の事情に合わせて最適な形をご提案します。'),
        ('炎上などのリスクが心配です。', '企画の段階で「誰かを傷つけないか・誤解を招く表現はないか」を確認してから制作に進みます。攻めた企画をご提案することもありますが、無理に通すことはしません。狙いとリスクをご説明したうえで、必ず合意を得てから進めます。それでも想定外の反応が起きた場合は、担当者として状況の整理から対応まで一緒に動きます。'),
        ('対応エリアを教えてください。', '撮影・打ち合わせは、全国に伺えます。出張費は東京23区内が1回15,000円。それ以外の地域は、レンタカー・駐車場・交通費・宿泊などの実費を、お見積りの段階で明示してご提案します（お見積りは無料です）。'),
    ]
    fh = '\n'.join(f'      <details><summary>{q}</summary><p class="a">{a}</p></details>' for q, a in faqs)
    body = page_hd(p, '料金・プラン', '料金・プラン｜TikTok運用代行・動画制作の費用', '1本からでも、<br>まるごとでも。',
                   '1本だけの制作から、まるごと任せる運用まで。状況に合った始め方を選べます。', extra) + f'''<main>
<section class="sec sec--tint" id="price" aria-labelledby="pc-h" style="scroll-margin-top:72px">
  <div class="wrap">
    <div class="sec-head"><h2 class="disp h-sec" id="pc-h">料金の早見表</h2><p class="lead">やりたいことから選んでください。お見積りは、どれも無償です。</p></div>
    <ul class="menu">
      <li><a href="#start"><span class="m-when">まず話を聞いてほしい</span><span class="m-name">無料相談</span><span class="m-price"><b>0</b>円</span><span class="m-note">30分・オンライン。課題の整理から。</span></a></li>
      <li><a href="#start"><span class="m-when">方針だけ一緒に決めたい</span><span class="m-name">スポット支援</span><span class="m-price"><b>5</b>万円〜</span><span class="m-note">半日〜1日。コンセプト・KPI・投稿方針まで。</span></a></li>
      <li><a href="#production"><span class="m-when">映像を1本つくりたい</span><span class="m-name">1本からの映像制作</span><span class="m-price">ショート動画 <b>15</b>万円〜<br>WebCMなど <b>30</b>万円〜</span><span class="m-note">企画・撮影・編集込み。</span></a></li>
      <li><a href="#partnership"><span class="m-when">SNSをまるごと任せたい</span><span class="m-name">プランA　フル運用代行</span><span class="m-price">月額 <b>60</b>万円〜<br><small>※広告費含む</small></span><span class="m-note">企画から投稿・広告・改善まで、チームでまるごと。まず3か月、その後は6か月ごとの更新。</span></a></li>
      <li><a href="#partnership"><span class="m-when">まず小さく試したい</span><span class="m-name">プランB　伴走型SNS運用</span><span class="m-price">月額 <b>29</b>万円〜<br><small>※広告費含む</small></span><span class="m-note">3か月のトライアル（月3本）。続ける場合は月4本・月額35万円で9か月。交通費・諸経費は別途。</span></a></li>
    </ul>
  </div>
</section>

<section class="sec" id="production" aria-labelledby="pr-h" style="scroll-margin-top:72px">
  <div class="wrap ways" style="align-items:start">
    <div class="sec-head" style="margin-bottom:0">
      <span class="label">1本からの映像制作</span>
      <h2 class="disp h-sec" id="pr-h">1本から、つくれます。</h2>
      <p class="lead">単発のご依頼も歓迎です。ただし、つくり方は変わりません。目的とターゲットを整理し、「どこで・誰に見せる映像か」を決めてから企画に入ります。最初の1本から、長いお付き合いが始まることがほとんどです。</p>
      <ul class="tags"><li>WebCM</li><li>ブランドムービー</li><li>採用動画</li><li>縦型ショート動画</li><li>ショートドラマ</li><li>HP・LP掲載用動画</li></ul>
    </div>
    <div class="way">
      <h3 style="font-size:20px">料金の目安</h3>
      <dl class="prices"><div><dt>ショート動画（縦型）</dt><dd>1本 <b>15</b>万円〜</dd></div><div><dt>WebCM・ブランドムービー・採用動画</dt><dd><b>30</b>万円〜</dd></div></dl>
      <p>いずれも企画・撮影・編集込み。キャスティング・スタジオなどの実費は、内容に応じて別途。広告用クリエイティブ開発や複数本パッケージは、規模に応じて個別にお見積りします。お見積りは無償です。</p>
      <h4 class="label" style="margin-top:6px">同じ「1本」でも、設計の深さで規模は変わります（実際の案件例）</h4>
      <dl class="scale">
        <div style="--w:16.67%"><dt>HP掲載用ブランドムービー（1本）</dt><dd>50万円</dd><i aria-hidden="true"></i></div>
        <div style="--w:60%"><dt>WebCM（目的別・複数本納品）</dt><dd>180万円</dd><i aria-hidden="true"></i></div>
        <div style="--w:100%"><dt>広告用ショートクリエイティブ開発（検証設計込み）</dt><dd>300万円</dd><i aria-hidden="true"></i></div>
      </dl>
      <a class="btn" href="contact.html">{CTA_LABEL}</a>
    </div>
  </div>
</section>

<section class="sec" aria-labelledby="mk-h" style="padding-top:0">
  <div class="wrap">
    <div class="making">
      <h3 class="disp h-sub" id="mk-h">1本ができるまで</h3>
      <p class="lead">どんなに短い動画でも、つくり方は変わりません。1本の中に、これだけの工程が入っています。</p>
      <ol class="process">
        <li><span>1</span>ヒアリング</li>
        <li><span>2</span>目的・ターゲットの整理</li>
        <li><span>3</span>企画・構成</li>
        <li><span>4</span>台本・絵コンテ</li>
        <li><span>5</span>キャスティング・ロケハン</li>
        <li><span>6</span>撮影</li>
        <li><span>7</span>編集・テロップ・音</li>
        <li><span>8</span>修正・納品</li>
      </ol>
    </div>
  </div>
</section>

<section class="sec sec--tint" id="partnership" aria-labelledby="pt-h" style="scroll-margin-top:72px">
  <div class="wrap">
    <div class="sec-head"><span class="label">継続のSNS運用</span><h2 class="disp h-sec" id="pt-h">まるごと任せるか、<br>小さく試して育てるか。</h2><p class="lead">どちらも担当者として入り、広告もセットで動きます。迷ったら、まずBのトライアルで小さく試し、手応えを見てから本格化する進め方もおすすめです。</p></div>
    <p class="swipe-hint">横にスワイプすると、プランBも見られます。</p>
    <div class="plan-switch" role="group" aria-label="表示するプラン"><button type="button" data-plan="0" aria-pressed="true">A　まるごと任せる</button><button type="button" data-plan="1" aria-pressed="false">B　小さく試す</button></div>
    <div class="plan-grid" tabindex="0" aria-label="プランA・B（横にスクロールできます）">
      <div class="plan">
        <span class="label">プランA　フル運用代行</span>
        <h3>SNSを、<br>まるごと任せたい</h3>
        <p class="plan-meta">月額 <b>60</b>万円〜 <small class="incl">※広告費含む</small>／月5本〜<br>まず3か月、その後は6か月ごとの更新<br><span style="font-weight:500;color:var(--sub)">広告費を含んだ金額です。本数の追加は1本8万円。交通費・諸経費は別途。</span></p>
        <h4>こんな企業・担当者に</h4>
        <ul class="checks"><li>社内に映像・SNSの専任がいない</li><li>まずは任せて、スピーディに始めたい</li><li>SNSの運用を本格化したい</li><li>採用・認知・売上など、明確な目標がある</li></ul>
        <p>社内にリソースがなくても、すぐに始められます。企画・撮影・編集・投稿・分析まで、M2Logが担当者として一貫して動きます。投稿だけでなく広告もセットで回すので、良い反応が出た動画をすぐに広告で伸ばせます。毎月の投稿本数・予算に合わせてカスタマイズでき、続けるほどアカウントの土台が育っていきます。</p>
        <h4>1か月のあいだに動くこと</h4>
        <ol class="month">
          <li><b>企画会議</b>前月の数字と反応を見て、今月の狙いと企画を決める</li>
          <li><b>台本・撮影準備</b>台本、出演者、ロケ地、小道具まで手配する</li>
          <li><b>撮影・編集</b>月1回のまとめ撮りで撮影し、テロップ・音まで仕上げる。修正は2回まで</li>
          <li><b>投稿・コメント運用</b>TikTokに投稿し、コメントにも返す。InstagramやYouTubeショートへの転用もOK</li>
          <li><b>広告配信</b>反応の良い動画を広告で伸ばす</li>
          <li><b>振り返り・定例</b>月次レポートをもとに、代表が定例で次の打ち手を提案</li>
        </ol>
        <h4>含まれるもの</h4>
        <ul class="checks"><li>コンセプト・KPI設計</li><li>月5本〜のコンテンツ制作（月1回のまとめ撮り）</li><li>企画・撮影・編集・投稿</li><li>コメント運用サポート</li><li>月次レポート・改善提案</li><li>担当者として会議に参加</li><li>広告の配信・運用（広告費を含む）</li></ul>
        <a class="btn" href="contact.html">{CTA_LABEL}</a>
      </div>
      <div class="plan">
        <span class="label">プランB　伴走型SNS運用</span>
        <h3>まず小さく試して、<br>自分たちでも回せるようにしたい</h3>
        <p class="plan-meta">トライアル3か月：月額 <b>29</b>万円（月3本） <small class="incl">※広告費含む</small><br>続ける9か月：月額 <b>35</b>万円（月4本） <small class="incl">※広告費含む</small><br><span style="font-weight:500;color:var(--sub)">広告費と月1回のワークショップを含んだ金額です。別途かかるのは交通費・諸経費のみです。</span></p>
        <h4>こんな企業・担当者に</h4>
        <ul class="checks"><li>いきなり大きく始めるより、まず手応えを確かめたい</li><li>ゆくゆくは、企画や撮影を社内でも回したい</li><li>企画や撮影を担当する人を、社内で決められる</li></ul>
        <p>最初の3か月はトライアルです。M2Logが主導して月3本をつくり、どんな切り口が伸びるのかを一緒に確かめます。手応えがあれば、残りの9か月をまとめてご契約いただき、本数を増やしながら企画と撮影を少しずつ御社に移していきます。編集と広告の運用は、12か月ずっとM2Logが担当します。</p>
        <h4>12か月の関わり方</h4>
        <div class="table-wrap" tabindex="0" aria-label="12か月の関わり方（横にスクロールできます）"><table class="roles">
          <thead><tr><th scope="col"><span class="sr">項目</span></th><th scope="col">1〜3か月目<br><small>トライアル</small></th><th scope="col">4〜6か月目<br><small>一緒に回す</small></th><th scope="col">7〜12か月目<br><small>御社が主導</small></th></tr></thead>
          <tbody>
            <tr><th scope="row">企画会議</th><td class="r-m">M2Logが主導</td><td class="r-t">一緒に考える</td><td class="r-c">御社が主導<small>M2Logも出席</small></td></tr>
            <tr><th scope="row">撮影</th><td class="r-m">M2Logが撮影<small>担当者は同席</small></td><td class="r-t">一緒に撮る</td><td class="r-c">御社が撮影<small>M2Logも同行</small></td></tr>
            <tr><th scope="row">編集</th><td class="r-m">M2Log</td><td class="r-m">M2Log</td><td class="r-m">M2Log</td></tr>
            <tr><th scope="row">広告の運用</th><td class="r-m">M2Log</td><td class="r-m">M2Log</td><td class="r-m">M2Log</td></tr>
          </tbody>
        </table></div>
        <h4>12か月後に残るもの</h4>
        <ul class="checks"><li>育ったアカウント（もともと御社のものです）</li><li>企画と撮影を社内で回せるチーム</li><li>御社用にまとめた運用の手引き</li><li>卒業後も、ワークショップを月1回3万円で受講できます（通常5〜10万円）</li><li>卒業後も、編集や広告の運用だけM2Logに任せることもできます</li></ul>
        <a class="btn" href="contact.html">{CTA_LABEL}</a>
      </div>
    </div>

    <h3 class="disp h-sub" style="margin:64px 0 20px">AとBの違い</h3>
    <div class="table-wrap" tabindex="0" aria-label="プラン比較表（横にスクロールできます）"><table class="table cmp">
      <thead><tr><th scope="col"><span class="sr">項目</span></th><th scope="col">A　フル運用代行</th><th scope="col">B　伴走型SNS運用</th></tr></thead>
      <tbody>
        <tr><th scope="row">ゴール</th><td>M2Logに任せて、成果を出し続ける</td><td>小さく試し、企画と撮影を社内でも回せるようになる</td></tr>
        <tr><th scope="row">月額</th><td>60万円〜（広告費含む）</td><td>トライアル29万円、続ける9か月は35万円（どちらも広告費含む）</td></tr>
        <tr><th scope="row">月額に含まれるもの</th><td>広告費</td><td>広告費、月1回のワークショップ</td></tr>
        <tr><th scope="row">本数</th><td>月5本〜（追加は1本8万円）</td><td>トライアル月3本、その後は月4本</td></tr>
        <tr><th scope="row">期間</th><td>まず3か月。続ける場合は6か月ごとに更新</td><td>まず3か月。続ける場合は9か月を追加（計12か月）</td></tr>
        <tr><th scope="row">企画・撮影</th><td>ずっとM2Log</td><td>M2Logから御社へ、少しずつ移る（M2Logは12か月ずっと同席）</td></tr>
        <tr><th scope="row">投稿・コメント対応</th><td>M2Log</td><td>御社（投稿の考え方はワークショップで共有）</td></tr>
        <tr><th scope="row">分析・改善提案</th><td>M2Logが毎月レポートし、代表が定例で提案</td><td>ワークショップで一緒に振り返る</td></tr>
        <tr><th scope="row">編集・広告の運用</th><td>M2Log</td><td>12か月ずっとM2Log（卒業後も任せられます）</td></tr>
        <tr><th scope="row">御社の担当者</th><td>窓口になる方（確認や社内調整の担当）</td><td>窓口に加えて、企画・撮影を担当する方</td></tr>
        <tr><th scope="row">定例</th><td>月1回以上、代表が参加</td><td>月1回のワークショップと企画会議で実施</td></tr>
      </tbody>
    </table></div>
  </div>
</section>

<section class="sec" id="start" aria-labelledby="sr-h" style="scroll-margin-top:72px">
  <div class="wrap">
    <div class="sec-head"><h2 class="disp h-sec" id="sr-h">迷っているなら、<br>話すのが早い。</h2></div>
    <div class="starts">
      <div class="start"><span class="label">無料</span><h3>無料相談</h3><p>今の課題を整理する相談です。提案・営業はしません。Zoom・対面のどちらでも。</p><a class="btn" href="contact.html">申し込む</a></div>
      <div class="start"><span class="label">5万円〜</span><h3>スポット支援</h3><p>SNS発信の診断や戦略ワークショップ。半日〜1日で、コンセプト・KPI・投稿方針まで具体化します。継続契約は不要です。</p><a class="btn btn--ghost" href="contact.html">申し込む</a></div>
    </div>
  </div>
</section>

<section class="sec sec--tint" id="faq" aria-labelledby="fq-h" style="scroll-margin-top:72px">
  <div class="wrap">
    <div class="sec-head"><h2 class="disp h-sec" id="fq-h">よくある質問</h2></div>
    <div class="faq">
{fh}
    </div>
  </div>
</section>
</main>
'''
    return h + body + cta(p, 'どこから始めればいいか、<br>一緒に整理します。', 'まず話すだけで大丈夫です。どんな状態からでも構いません。') + footer(p)


def contact():
    p = '../'
    desc = 'TikTok運用・ショート動画・WebCM制作のご相談はこちら。オンライン30分の無料相談で、方向性と予算感までお伝えします。通常2〜3営業日以内にご返信します。'
    h = head('お問い合わせ・無料相談｜M2Log', desc, '/pages/contact.html', p) + header(p, 'contact')
    body = page_hd(p, 'お問い合わせ', 'お問い合わせ・無料相談', 'まず、話すところから。',
                   '何から手をつければいいか分からなくても、歓迎します。オンラインで30分、今の状況を伺います。') + f'''<main>
<section class="sec">
  <div class="wrap contact">
    <div class="c-info">
      <dl>
        <div><dt>会社名</dt><dd>株式会社M2Log</dd></div>
        <div><dt>所在地</dt><dd>東京都江東区</dd></div>
        <div><dt>メール</dt><dd><a class="textlink" href="mailto:n.ryosuke@m2log.jp">n.ryosuke@m2log.jp</a></dd></div>
      </dl>
      <div>
        <h2 class="h-sub disp" style="font-size:20px;margin-bottom:16px">ご連絡後の流れ</h2>
        <ol class="c-flow" style="list-style:none;padding:0;margin:0">
          <li>フォームまたはメールでご連絡ください（1分で終わります）。</li>
          <li>2〜3営業日以内に、担当の中村からご返信します。</li>
          <li>Zoomまたは対面でヒアリング。提案を急かすことはしません。</li>
        </ol>
      </div>
      <p style="font-size:14.5px;color:var(--sub)">代理店さまからのご相談も承っています。</p>
    </div>
    <div>
      <div class="form-box">
        <iframe src="https://docs.google.com/forms/d/e/1FAIpQLSecYJPiVju50KcnKzE18h6DgFp_D4D4tMyjU6SfXABlWqlfCg/viewform?embedded=true" title="お問い合わせフォーム" loading="lazy">読み込んでいます…</iframe>
      </div>
      <p class="form-note">送信いただいた個人情報は、<a class="textlink" href="privacy.html">プライバシーポリシー</a>に基づいて取り扱います。通常2〜3営業日以内にご返信します。</p>
    </div>
  </div>
</section>
</main>
'''
    return h + body + footer(p)


def privacy():
    p = '../'
    desc = '株式会社M2Logにおける個人情報の取り扱いについて定めたプライバシーポリシーです。'
    h = head('プライバシーポリシー｜M2Log', desc, '/pages/privacy.html', p) + header(p, 'privacy')
    body = page_hd(p, 'プライバシーポリシー', '株式会社M2Log', 'プライバシーポリシー', '株式会社M2Logにおける個人情報の取り扱いについて') + '''<main>
<section class="sec">
  <div class="wrap prose">
    <p>株式会社M2Log（以下「当社」）は、当社が提供するサービスおよび当社ウェブサイトにおける個人情報の取り扱いについて、以下のとおりプライバシーポリシーを定めます。</p>
    <h2>1. 取得する情報</h2>
    <p>当社は、お問い合わせフォーム等を通じて、以下の情報を取得することがあります。</p>
    <ul><li>氏名</li><li>会社名</li><li>メールアドレス</li><li>お問い合わせ内容</li></ul>
    <h2>2. 利用目的</h2>
    <p>取得した個人情報は、以下の目的で利用します。</p>
    <ul><li>お問い合わせへの回答・ご連絡</li><li>サービスの提供、契約の履行</li><li>サービスに関するご案内</li></ul>
    <h2>3. 第三者提供</h2>
    <p>当社は、法令に基づく場合を除き、ご本人の同意なく個人情報を第三者に提供しません。</p>
    <h2>4. 外部サービスの利用</h2>
    <p>当社ウェブサイトでは、お問い合わせフォームにGoogleフォームを、アクセス解析にGoogleアナリティクスを利用しています。GoogleアナリティクスはCookieを使用してトラフィックデータを収集しますが、このデータは匿名で収集されており、個人を特定するものではありません。詳細は<a href="https://policies.google.com/privacy?hl=ja" target="_blank" rel="noopener">Googleのプライバシーポリシー</a>をご確認ください。</p>
    <h2>5. 安全管理</h2>
    <p>当社は、個人情報の漏えい、滅失または毀損の防止のため、必要かつ適切な安全管理措置を講じます。</p>
    <h2>6. 開示・訂正・削除</h2>
    <p>ご本人から個人情報の開示・訂正・削除等のお申し出があった場合、ご本人であることを確認のうえ、速やかに対応します。</p>
    <h2>7. 改定</h2>
    <p>本ポリシーの内容は、法令の改正や運用の変更に応じて、予告なく改定されることがあります。改定後の内容は当ページにて公表します。</p>
    <h2>8. お問い合わせ窓口</h2>
    <p>個人情報の取り扱いに関するお問い合わせは、<a href="contact.html">お問い合わせフォーム</a>よりご連絡ください。<br>株式会社M2Log（東京都江東区）</p>
    <p style="margin-top:32px;color:var(--sub)">制定日：2026年7月3日</p>
  </div>
</section>
</main>
'''
    return h + body + footer(p)


def notfound():
    p = '/'
    h = head('ページが見つかりません｜M2Log', 'お探しのページは見つかりませんでした。', '/404.html', p).replace('href="/assets', 'href="/assets')
    body = header(p.rstrip('/') + '/', '') if False else ''
    hdr = f'''<header class="hd"><div class="wrap"><a class="hd-logo" href="/"><img src="/assets/img/logo/m2log_logo_navy.svg" alt="M2Log" width="122" height="30"></a><nav class="hd-nav" style="display:flex;position:static;flex-direction:row;padding:0;border:0;background:none"><a class="btn" href="/pages/contact.html">{CTA_LABEL}</a></nav></div></header>'''
    main = '''<main><section class="sec"><div class="wrap" style="display:grid;gap:22px;justify-items:start">
<p class="label">404</p><h1 class="disp h-sec">お探しのページが<br>見つかりませんでした。</h1>
<p class="lead">URLが変わったか、ページが移動した可能性があります。トップページから探してみてください。</p>
<a class="btn" href="/">トップページへ</a></div></section></main>
<script src="/assets/js/site.js" defer></script></body></html>
'''
    return h + hdr + main


PAGES = {
    'index.html': index, 'pages/services.html': services, 'pages/about.html': about,
    'pages/plans.html': plans, 'pages/contact.html': contact, 'pages/privacy.html': privacy, '404.html': notfound,
}
for path, fn in PAGES.items():
    with open(os.path.join(ROOT, path), 'w', encoding='utf-8') as f:
        f.write(fn())
    print('wrote', path)
