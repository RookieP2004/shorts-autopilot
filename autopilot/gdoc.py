"""Turn the repo's markdown memory files into the simple HTML that Zapier's Google Docs actions accept."""
import html
import re


def _inline(t):
    t = html.escape(t, quote=False)
    t = re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", t)
    t = re.sub(r"`(.+?)`", r"<i>\1</i>", t)
    return t


def md_to_html(md):
    out = []
    for line in md.splitlines():
        s = line.rstrip()
        if not s:
            out.append("<br>")
        elif s.startswith("### "):
            out.append(f"<h3>{_inline(s[4:])}</h3>")
        elif s.startswith("## "):
            out.append(f"<h2>{_inline(s[3:])}</h2>")
        elif s.startswith("# "):
            out.append(f"<h1>{_inline(s[2:])}</h1>")
        elif s.startswith("|"):
            cells = [c.strip() for c in s.strip("|").split("|")]
            if all(set(c) <= set("-: ") for c in cells):
                continue
            out.append(" · ".join(_inline(c) for c in cells) + "<br>")
        elif re.match(r"^\s*[-*] ", s):
            out.append("• " + _inline(re.sub(r"^\s*[-*] ", "", s)) + "<br>")
        else:
            out.append(_inline(s) + "<br>")
    return "\n".join(out)


if __name__ == "__main__":
    import sys
    print(md_to_html(open(sys.argv[1]).read()))
