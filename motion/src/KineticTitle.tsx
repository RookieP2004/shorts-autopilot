import React, {useRef} from 'react';
import {AbsoluteFill, useVideoConfig} from 'remotion';
import gsap from 'gsap';
import {DrawSVGPlugin} from 'gsap/DrawSVGPlugin';
import {useGsapTimeline} from './gsapClock';
import {loadFonts} from './fonts';

gsap.registerPlugin(DrawSVGPlugin);

export type KineticTitleProps = {
  lines: string[];            // "*word*" = accent colour + hand-drawn underline
  size?: number;              // px at 1080 wide
  color?: string;
  accent?: string;
  stroke?: string;            // house text: white fill + dark stroke
  font?: 'Anton' | 'Playfair' | 'Poppins';
  style?: 'rise' | 'pop' | 'wave' | 'slam';
  stagger?: number;           // seconds between letters
  y?: number;                 // 0..1 vertical centre
  sub?: string;
  out?: number;               // seconds when it leaves (0 = stays)
};

const parse = (line: string) => {
  const out: {ch: string; acc: boolean}[] = [];
  let acc = false;
  for (const ch of line) {
    if (ch === '*') { acc = !acc; continue; }
    out.push({ch, acc});
  }
  return out;
};

export const KineticTitle: React.FC<KineticTitleProps> = ({
  lines, size = 120, color = '#ffffff', accent = '#ffcf33', stroke = '#1a1410', font = 'Anton', style = 'rise',
  stagger = 0.028, y = 0.3, sub, out = 0,
}) => {
  loadFonts();
  const {width} = useVideoConfig();
  const k = width / 1080;
  const root = useRef<HTMLDivElement>(null);
  useGsapTimeline((tl) => {
    const el = root.current!;
    const chars = el.querySelectorAll('.ch');
    const from = style === 'pop' ? {scale: 0, rotate: -12, opacity: 0}
      : style === 'wave' ? {yPercent: 60, rotate: 8, opacity: 0}
        : style === 'slam' ? {scale: 2.6, opacity: 0, filter: 'blur(10px)'} : {yPercent: 110};
    tl.from(chars, {...from, duration: style === 'slam' ? 0.38 : 0.55, ease: style === 'slam' ? 'power4.out' : 'back.out(2.2)',
                    stagger}, 0.05);
    const uls = el.querySelectorAll('.ul');
    if (uls.length) tl.from(uls, {drawSVG: '0%', duration: 0.5, ease: 'power2.inOut'}, '-=0.15');
    if (sub) tl.from(el.querySelector('.sub'), {y: 30 * k, opacity: 0, duration: 0.45, ease: 'power3.out'}, '-=0.25');
    tl.to(el.querySelectorAll('.acc'), {scale: 1.08, duration: 0.18, yoyo: true, repeat: 1, ease: 'power1.inOut', stagger: 0.03}, '-=0.1');
    if (out > 0) tl.to(chars, {yPercent: -110, opacity: 0, duration: 0.35, ease: 'power2.in', stagger: stagger * 0.5}, out);
  }, [JSON.stringify(lines), style]);
  const fam = font === 'Playfair' ? 'Playfair' : font === 'Poppins' ? 'Poppins' : 'Anton';
  return (
    <AbsoluteFill>
      <div ref={root} style={{position: 'absolute', left: 0, right: 0, top: `${y * 100}%`, translate: '0 -50%', textAlign: 'center'}}>
        {lines.map((ln, li) => {
          const ch = parse(ln);
          return (
            <div key={li} style={{overflow: style === 'rise' ? 'hidden' : 'visible', lineHeight: 1.05, padding: `0 ${20 * k}px`,
                                  position: 'relative', display: 'block'}}>
              {ch.map((c, i) => (
                <span key={i} className={'ch' + (c.acc ? ' acc' : '')}
                      style={{display: 'inline-block', fontFamily: fam, fontSize: size * k, color: c.acc ? accent : color,
                              WebkitTextStroke: `${Math.max(2, 7 * k)}px ${stroke}`, paintOrder: 'stroke fill',
                              whiteSpace: 'pre', textShadow: `0 ${6 * k}px 0 rgba(0,0,0,0.25)`}}>{c.ch}</span>
              ))}
              {ch.some((c) => c.acc) ? (
                <svg width="100%" height={size * k * 0.28} viewBox="0 0 1000 40" preserveAspectRatio="none"
                     style={{position: 'absolute', left: '22%', width: '56%', bottom: -size * k * 0.12}}>
                  <path className="ul" d="M10,30 C200,8 420,34 600,18 S880,10 990,22" fill="none" stroke={accent}
                        strokeWidth={10} strokeLinecap="round" />
                </svg>
              ) : null}
            </div>
          );
        })}
        {sub ? <div className="sub" style={{fontFamily: 'PoppinsSemi', fontSize: 40 * k, color, marginTop: 24 * k,
                                            textShadow: `0 ${3 * k}px ${8 * k}px rgba(0,0,0,0.6)`}}>{sub}</div> : null}
      </div>
    </AbsoluteFill>
  );
};
