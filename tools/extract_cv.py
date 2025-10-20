from pdfminer.high_level import extract_text
import re
import json
import os

PDF_PATH = os.path.join(os.path.dirname(__file__), '..', 'Mu_CV.pdf')
OUT_TEXT = os.path.join(os.path.dirname(__file__), '..', 'mu_cv_text.txt')
OUT_JSON = os.path.join(os.path.dirname(__file__), '..', 'mu_cv_data.json')


def normalize_text(s: str) -> str:
    s = s.replace('\r\n', '\n').replace('\r', '\n')
    s = re.sub('[\t\f\v]+', ' ', s)
    s = re.sub('\n{2,}', '\n\n', s)
    return s


def extract_section(text: str, title: str, stops: list[str]) -> str:
    m = re.search(rf'(^|\n)\s*{re.escape(title)}\s*(\n|$)', text, flags=re.IGNORECASE)
    if not m:
        return ''
    start = m.end()
    stop_pos = len(text)
    for k in stops:
        ms = re.search(rf'(^|\n)\s*{re.escape(k)}\s*(\n|$)', text, flags=re.IGNORECASE)
        if ms and ms.start() > start and ms.start() < stop_pos:
            stop_pos = ms.start()
    return text[start:stop_pos].strip()


def lines(section: str) -> list[str]:
    out = []
    for ln in section.split('\n'):
        ln = ln.strip()
        if not ln:
            continue
        ln = re.sub(r'^[-•\u2022\*\d\.\)\(]+\s*', '', ln)
        out.append(ln)
    return out


def main():
    raw = extract_text(PDF_PATH)
    raw = normalize_text(raw)
    with open(OUT_TEXT, 'w', encoding='utf-8') as f:
        f.write(raw)

    first_lines = [l.strip() for l in raw.split('\n') if l.strip()]
    name = next((l for l in first_lines if re.search(r'\bMu\b', l, re.I) and re.search(r'\bJia\b', l, re.I)), first_lines[0] if first_lines else 'Mu Jia')

    email_m = re.search(r'[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}', raw)
    email = email_m.group(0) if email_m else ''

    web_m = re.search(r'(https?://\S+)', raw)
    website = web_m.group(1) if web_m else ''

    # headings and synonyms
    stops = ['Education','Experience','Research Interests','Research Publications','Publications','Awards','Awards and Achievements','Honors','Teaching Experiences']

    education = lines(extract_section(raw, 'Education', stops))

    interests = lines(extract_section(raw, 'Research Interests', stops))

    pubs_root = extract_section(raw, 'Research Publications', stops)
    if not pubs_root:
        pubs_root = extract_section(raw, 'Publications', stops)

    pubs_journal = lines(extract_section(pubs_root, 'Journal Articles', ['Conference Proceedings'] + stops))
    pubs_conf = lines(extract_section(pubs_root, 'Conference Proceedings', ['Journal Articles'] + stops))
    pubs_under = lines(extract_section(pubs_root, 'Under review', ['Journal Articles','Conference Proceedings'] + stops))

    awards = lines(extract_section(raw, 'Awards and Achievements', stops))
    if not awards:
        awards = lines(extract_section(raw, 'Awards', stops)) + lines(extract_section(raw, 'Honors', stops))

    data = {
        'name': name,
        'email': email,
        'website': website,
        'education': education,
        'interests': interests,
        'publications': {
            'under_review': pubs_under,
            'journal': pubs_journal,
            'conference': pubs_conf,
        },
        'awards': awards,
    }

    with open(OUT_JSON, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


if __name__ == '__main__':
    main()