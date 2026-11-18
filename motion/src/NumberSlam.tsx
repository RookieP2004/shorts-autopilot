import React, {useRef} from 'react';
import {AbsoluteFill, random, useCurrentFrame, useVideoConfig} from 'remotion';
import gsap from 'gsap';
import {useGsapTimeline} from './gsapClock';
import {loadFonts} from './fonts';

export type NumberSlamProps = {
  text: string;          // e.g. "$1.92 BILLION" - digits roll like a slot machine, then the whole number slams down
  label?: string;        // small line under it
  color?: string;
  accent?: string;       // shockwave + sparks colour
  size?: number;
  y?: number;
  roll?: number;         // seconds the digits roll
};

const DIG = '0123456789';

// The big-number moment: digit reels spin and land one by one (GSAP stagger), the number punches in, a shockwave ring
// and sparks fly out, and the frame shakes and settles. Everything is seeked from the frame (deterministic).
export const NumberSlam: React.FC<NumberSlamProps> = ({text, label, color = '#ffffff', accent = '#ffcf33', size = 250, y = 0.42,
                                                        roll = 0.9}) => {
  loadFonts();
  const frame = useCurrentFrame();
  const {width, height, fps} = useVideoConfig();
  const k = Math.min(width, height * 0.5625) / 1080 * (width > height ? 1.6 : 1);
  const root = useRef<HTMLDivElement>(null);
  const fs = size * k;
  const chars = [...text];
  const land = 0.15 + roll;
  useGsapTimeline((tl) => {
    const el = root.current!;
    el.querySelectorAll('.reel').forEach((r, i) => {
      const d = Number((r as HTMLElement).dataset.d);
      tl.fromTo(r, {yPercent: 0}, {yPercent: -(100 / 21) * (10 + d), duration: roll - 0.05 + i * 0.07, ease: 'power3.out'}, 0.1);
    });
    tl.fromTo(el.querySelector('.num'), {scale: 1.9, opacity: 0}, {scale: 1, opacity: 1, duration: 0.32, ease: 'back.out(2.6)'}, 0.05);
    tl.fromTo(el.querySelector('.ring'), {scale: 0.2, opacity: 0.9}, {scale: 2.6, opacity: 0, duration: 0.7, ease: 'power2.out'}, land);
    tl.fromTo(el.querySelector('.ring2'), {scale: 0.2, opacity: 0.6}, {scale: 3.4, opacity: 0, duration: 0.9, ease: 'power2.out'}, land + 0.06);
    tl.fromTo(el.querySelector('.num'), {scale: 1.12}, {scale: 1, duration: 0.35, ease: 'elastic.out(1.2, 0.4)'}, land);
    el.querySelectorAll('.spark').forEach((s, i) => {
      const a = random(`a${i}`) * Math.PI * 2, r = (0.25 + random(`r${i}`) * 0.4) * width;
      tl.fromTo(s, {x: 0, y: 0, opacity: 1, rotate: 0}, {x: Math.cos(a) * r, y: Math.sin(a) * r * 0.7, opacity: 0, rotate: random(`o${i}`) * 540,
                                                        duration: 0.7 + random(`d${i}`) * 0.4, ease: 'power3.out'}, land);
    });
    if (label) tl.from(el.querySelector('.lab'), {y: 40 * k, opacity: 0, duration: 0.4, ease: 'power3.out'}, land + 0.1);
  }, [text, label]);
  const t = frame / fps - land;                                   // camera shake after the slam, decaying
  const amp = t > 0 ? Math.exp(-t * 7) * 18 * k : 0;
  const sx = amp * (random(`sx${frame}`) - 0.5) * 2, sy = amp * (random(`sy${frame}`) - 0.5) * 2;
  return (
    <AbsoluteFill ref={root} style={{transform: `translate(${sx}px, ${sy}px)`}}>
      <div style={{position: 'absolute', left: '50%', top: `${y * 100}%`}}>
        <div className="ring" style={{position: 'absolute', width: fs * 2.2, height: fs * 2.2, left: -fs * 1.1, top: -fs * 1.1,
                                      borderRadius: '50%', border: `${10 * k}px solid ${accent}`, opacity: 0}} />
        <div className="ring2" style={{position: 'absolute', width: fs * 2.2, height: fs * 2.2, left: -fs * 1.1, top: -fs * 1.1,
                                       borderRadius: '50%', border: `${4 * k}px solid ${accent}`, opacity: 0}} />
        {Array.from({length: 22}).map((_, i) => (
          <div key={i} className="spark" style={{position: 'absolute', width: 18 * k, height: 46 * k, left: -9 * k, top: -23 * k,
                                                 background: i % 3 ? accent : color, borderRadius: 4 * k, opacity: 0}} />
        ))}
      </div>
      <div className="num" style={{position: 'absolute', left: 0, right: 0, top: `${y * 100}%`, translate: '0 -50%', display: 'flex',
                                   justifyContent: 'center', fontFamily: 'Anton', fontSize: fs, lineHeight: 1, color,
                                   WebkitTextStroke: `${Math.max(3, 9 * k)}px #120e0a`, paintOrder: 'stroke fill',
                                   textShadow: `0 ${10 * k}px 0 rgba(0,0,0,0.3)`, opacity: 0}}>
        {chars.map((c, i) => DIG.includes(c) ? (
          <span key={i} style={{display: 'inline-block', height: fs, overflow: 'hidden', verticalAlign: 'top'}}>
            <span className="reel" data-d={c} style={{display: 'flex', flexDirection: 'column'}}>
              {(DIG + DIG + '0').split('').map((d, j) => <span key={j} style={{height: fs, lineHeight: `${fs}px`}}>{d}</span>)}
            </span>
          </span>
        ) : <span key={i} style={{whiteSpace: 'pre'}}>{c}</span>)}
      </div>
      {label ? <div className="lab" style={{position: 'absolute', left: 0, right: 0, top: `calc(${y * 100}% + ${fs * 0.62}px)`, textAlign: 'center',
                                            fontFamily: 'PoppinsSemi', fontSize: 46 * k, color, letterSpacing: 2 * k,
                                            textShadow: `0 ${3 * k}px ${10 * k}px rgba(0,0,0,0.7)`}}>{label}</div> : null}
    </AbsoluteFill>
  );
};
