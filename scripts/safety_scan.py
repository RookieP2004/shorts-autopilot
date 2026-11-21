# Run: python scripts/safety_scan.py "LABEL=path" ...  (before integrating any outside skill or code)
"""Static safety scan of third-party code: network hosts, command execution, secret access, obfuscation,
install hooks, destructive file ops, and agent-instruction injection in Markdown. Prints findings per category."""
import os, re, sys, json, collections
CODE = ('.py', '.js', '.mjs', '.cjs', '.ts', '.tsx', '.sh', '.html', '.bash')
PAT = {
 'exec':      r'\beval\s*\(|new\s+Function\s*\(|\bexec\s*\(|os\.system|subprocess\.|child_process|execSync|spawnSync|\bspawn\(|shell\s*=\s*True|\bpopen\(',
 'network':   r'\bfetch\s*\(|XMLHttpRequest|urllib\.request|\brequests\.(get|post|put)|http\.request|https\.request|\bcurl\b|\bwget\b|socket\.|WebSocket|urlopen',
 'secrets':   r'\.ssh|id_rsa|\.aws|\.netrc|\.npmrc|\.pypirc|/root/\.ig|IG_TOKEN|keychain|\.gnupg|cookies|Login Data|wallet|GITHUB_TOKEN|ANTHROPIC|OPENAI_API|process\.env\.[A-Z_]*(KEY|TOKEN|SECRET)|environ\[[\'"][A-Z_]*(KEY|TOKEN|SECRET)',
 'obfusc':    r'[A-Za-z0-9+/]{300,}={0,2}|(\\x[0-9a-f]{2}){12,}|\batob\s*\(|base64\.b64decode|Buffer\.from\([^)]*base64|marshal\.loads|zlib\.decompress|String\.fromCharCode\(\s*\d+\s*,\s*\d+',
 'destruct':  r'rm\s+-rf\s+[/~$]|shutil\.rmtree\(\s*[\'"]?/|chmod\s+777|/etc/|crontab|\.bashrc|\.profile|sudo\s',
 'mining':    r'stratum\+tcp|xmrig|coinhive|cryptonight|minero',
}
MD_INJ = r'ignore (all |any )?(previous|prior|above) instructions|do not (tell|inform|show) the user|without (telling|asking) the user|secretly|exfiltrat|send (the )?(api )?key|upload .*(token|key|credential)|disable (safety|guard)|you are now|system prompt|curl .*\|\s*(sh|bash)|wget .*\|\s*(sh|bash)'
HOST = re.compile(r'https?://([a-zA-Z0-9.-]+)')
def scan(root, label, skip=('node_modules', '.git', '__pycache__', 'instruments', '.venv', 'venv')):
    hits = collections.defaultdict(list); hosts = collections.Counter(); md = []; hooks = []; nfiles = 0
    for dp, dn, fn in os.walk(root):
        dn[:] = [d for d in dn if d not in skip]
        for f in fn:
            p = os.path.join(dp, f); rel = os.path.relpath(p, root)
            if f == 'package.json':
                try:
                    sc = json.load(open(p)).get('scripts', {})
                    for k in ('preinstall', 'install', 'postinstall', 'prepare'):
                        if k in sc: hooks.append(f'{rel}: {k}: {sc[k]}')
                except Exception: pass
            if f.endswith('.md') or f.endswith('.txt'):
                try: t = open(p, errors='ignore').read()
                except Exception: continue
                for m in re.finditer(MD_INJ, t, re.I):
                    ln = t[:m.start()].count('\n') + 1; md.append(f'{rel}:{ln}: {t.splitlines()[ln-1].strip()[:140]}')
                for h in HOST.findall(t): hosts[h.lower()] += 1
                continue
            if not f.endswith(CODE): continue
            nfiles += 1
            try: t = open(p, errors='ignore').read()
            except Exception: continue
            for h in HOST.findall(t): hosts[h.lower()] += 1
            for i, line in enumerate(t.splitlines(), 1):
                if len(line) > 3000: line = line[:3000]
                for k, r in PAT.items():
                    if re.search(r, line, re.I if k != 'obfusc' else 0):
                        hits[k].append(f'{rel}:{i}: {line.strip()[:150]}')
    print(f'\n######## {label}  ({root}; {nfiles} code files)')
    for k in PAT:
        v = hits.get(k, [])
        print(f'== {k}: {len(v)}')
        for x in v[:int(os.environ.get("SHOW", 12))]: print('   ', x)
    print('== hosts:', ', '.join(f'{h}({n})' for h, n in hosts.most_common(40)))
    print('== install hooks:', hooks or 'none')
    print('== md injection phrases:', len(md)); [print('   ', x) for x in md[:15]]
if __name__ == '__main__':
    for a in sys.argv[1:]:
        lab, path = a.split('=', 1); scan(path, lab)
