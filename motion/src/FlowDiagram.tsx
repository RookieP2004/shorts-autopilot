import React, {useRef} from 'react';
import {AbsoluteFill, useVideoConfig} from 'remotion';
import gsap from 'gsap';
import {DrawSVGPlugin} from 'gsap/DrawSVGPlugin';
import {MotionPathPlugin} from 'gsap/MotionPathPlugin';
import {useGsapTimeline} from './gsapClock';
import {loadFonts} from './fonts';

gsap.registerPlugin(DrawSVGPlugin, MotionPathPlugin);

type Node = {id: string; label: string; x: number; y: number; color?: string; ink?: string; w?: number};
type Edge = [string, string] | [string, string, string];
export type FlowDiagramProps = {
  nodes: Node[]; edges: Edge[]; step?: number; arrow?: string; pulse?: string; theme?: 'cream' | 'night';
};

// House cream cards (or night chips) that pop in one by one; hand-drawn arrows draw themselves (DrawSVG) and a pulse
// travels along each finished arrow (MotionPath). Positions are frame fractions.
export const FlowDiagram: React.FC<FlowDiagramProps> = ({nodes, edges, step = 0.45, arrow, pulse = '#ffcf33', theme = 'cream'}) => {
  loadFonts();
  const {width, height} = useVideoConfig();
  const k = width / 1080;
  const root = useRef<HTMLDivElement>(null);
  const night = theme === 'night';
  const arrowCol = arrow || (night ? '#e0b25a' : '#1a1410');
  const pos = Object.fromEntries(nodes.map((n) => [n.id, n]));
  const geom = (a: Node, b: Node) => {                     // a gentle curve that stops short of both cards
    const ax = a.x * width, ay = a.y * height, bx = b.x * width, by = b.y * height;
    const dx = bx - ax, dy = by - ay;
    const cx = (ax + bx) / 2 - dy * 0.18, cy = (ay + by) / 2 + dx * 0.18;
    const q = (t: number) => [(1 - t) ** 2 * ax + 2 * (1 - t) * t * cx + t * t * bx, (1 - t) ** 2 * ay + 2 * (1 - t) * t * cy + t * t * by];
    const t0 = 0.2, t1 = 0.8;
    const [sx, sy] = q(t0), [ex, ey] = q(t1);
    const [mx, my] = q(0.5);
    const kx = 2 * mx - (sx + ex) / 2, ky = 2 * my - (sy + ey) / 2;  // control point of the trimmed curve
    const tx = 2 * (1 - t1) * (cx - ax) + 2 * t1 * (bx - cx), ty = 2 * (1 - t1) * (cy - ay) + 2 * t1 * (by - cy);
    return {d: `M${sx},${sy} Q${kx},${ky} ${ex},${ey}`, ex, ey, ang: Math.atan2(ty, tx) * 180 / Math.PI};
  };
  useGsapTimeline((tl) => {
    const el = root.current!;
    nodes.forEach((n, i) => {
      tl.from(el.querySelector(`[data-n="${n.id}"]`), {scale: 0, rotate: -8, duration: 0.5, ease: 'back.out(2.4)'}, 0.1 + i * step);
    });
    edges.forEach((e, i) => {
      const t0 = 0.1 + Math.max(nodes.findIndex((n) => n.id === e[0]), nodes.findIndex((n) => n.id === e[1])) * step + 0.25;
      const p = el.querySelector(`[data-e="${i}"]`);
      tl.from(p, {drawSVG: '0%', duration: 0.6, ease: 'power2.inOut'}, t0);
      const head = el.querySelector(`[data-h="${i}"]`);           // arrowhead lands when the line arrives
      tl.fromTo(head, {opacity: 0, scale: 0.2}, {opacity: 1, scale: 1, duration: 0.2, ease: 'back.out(3)', transformOrigin: '50% 50%'}, t0 + 0.55);
      const dot = el.querySelector(`[data-d="${i}"]`);
      tl.set(dot, {opacity: 1}, t0 + 0.6);
      tl.to(dot, {motionPath: {path: p as SVGPathElement, align: p as SVGPathElement, alignOrigin: [0.5, 0.5]},
                  duration: 1.1, ease: 'none', repeat: 6}, t0 + 0.6);
    });
  }, [JSON.stringify(nodes), JSON.stringify(edges)]);
  return (
    <AbsoluteFill ref={root}>
      <svg width={width} height={height} style={{position: 'absolute', overflow: 'visible'}}>
        <defs>
          <marker id="head" viewBox="0 0 10 10" refX="7" refY="5" markerWidth="5" markerHeight="5" orient="auto-start-reverse">
            <path d="M0,0 L10,5 L0,10 z" fill={arrowCol} />
          </marker>
        </defs>
        {edges.map((e, i) => { const g = geom(pos[e[0]], pos[e[1]]); return (
          <g key={i}>
            <path data-e={i} d={g.d} fill="none" stroke={arrowCol} strokeWidth={9 * k} strokeLinecap="round" />
            <g transform={`translate(${g.ex},${g.ey}) rotate(${g.ang})`}>
              <path data-h={i} d={`M${-22 * k},${-18 * k} L${14 * k},0 L${-22 * k},${18 * k} z`} fill={arrowCol} opacity={0} />
            </g>
            <circle data-d={i} r={13 * k} fill={pulse} stroke={night ? 'none' : '#1a1410'} strokeWidth={4 * k} opacity={0} />
          </g>
        ); })}
      </svg>
      {nodes.map((n) => (
        <div key={n.id} data-n={n.id}
             style={{position: 'absolute', left: n.x * width, top: n.y * height, translate: '-50% -50%',
                     width: (n.w || 0.42) * width, padding: `${18 * k}px ${22 * k}px`, borderRadius: 28 * k, textAlign: 'center',
                     background: night ? 'rgba(8,12,22,0.92)' : (n.color || '#f6efe2'),
                     border: `${6 * k}px solid ${night ? '#e0b25a' : '#1a1410'}`,
                     boxShadow: night ? `0 0 ${24 * k}px rgba(224,178,90,0.45)` : `0 ${10 * k}px 0 rgba(0,0,0,0.22)`,
                     fontFamily: 'Anton', fontSize: 64 * k, lineHeight: 1.05, color: night ? '#efe6d2' : (n.ink || '#1a1410')}}>
          {n.label}
        </div>
      ))}
    </AbsoluteFill>
  );
};
