import React, {useMemo} from 'react';
import {AbsoluteFill, Easing, interpolate, spring, useCurrentFrame, useVideoConfig} from 'remotion';
import {ThreeCanvas} from '@remotion/three';
import {useThree} from '@react-three/fiber';
import * as THREE from 'three';
import {RoomEnvironment} from 'three/examples/jsm/environments/RoomEnvironment.js';
import {RoundedBoxGeometry} from 'three/examples/jsm/geometries/RoundedBoxGeometry.js';

export type Hero3DProps = {
  object: 'globe' | 'bars' | 'coin';
  values?: number[];                 // bars: heights (any units, normalised)
  colors?: string[];                 // bars: per-bar colour
  arcs?: [number, number, number, number][];   // globe: [lat1, lon1, lat2, lon2]
  tone?: string;                     // main colour
  spin?: number;                     // degrees over the clip
  zoom?: number;                     // camera distance multiplier
};

// Every motion here is a function of the frame (Remotion rule: no useFrame, nothing animates on its own).
const Env: React.FC = () => {
  const {gl, scene} = useThree();
  useMemo(() => {
    const pm = new THREE.PMREMGenerator(gl);
    scene.environment = pm.fromScene(new RoomEnvironment(), 0.04).texture;
    (scene as any).environmentIntensity = 0.55;
  }, [gl, scene]);
  return null;
};

const ll = (lat: number, lon: number, r: number) => {
  const p = (90 - lat) * Math.PI / 180, t = (lon + 180) * Math.PI / 180;
  return new THREE.Vector3(-r * Math.sin(p) * Math.cos(t), r * Math.cos(p), r * Math.sin(p) * Math.sin(t));
};

const Globe: React.FC<Hero3DProps> = ({arcs = [], tone = '#e0b25a'}) => {
  const frame = useCurrentFrame();
  const {fps} = useVideoConfig();
  const dots = useMemo(() => {
    const n = 2600, pts: number[] = [];
    for (let i = 0; i < n; i++) {                           // Fibonacci sphere: even dots, no map outline
      const y = 1 - (i / (n - 1)) * 2, r = Math.sqrt(1 - y * y), th = Math.PI * (3 - Math.sqrt(5)) * i;
      pts.push(Math.cos(th) * r * 1.5, y * 1.5, Math.sin(th) * r * 1.5);
    }
    const g = new THREE.BufferGeometry();
    g.setAttribute('position', new THREE.Float32BufferAttribute(pts, 3));
    return g;
  }, []);
  const tubes = useMemo(() => arcs.map(([a, b, c, d]) => {
    const p0 = ll(a, b, 1.5), p2 = ll(c, d, 1.5);
    const mid = p0.clone().add(p2).multiplyScalar(0.5).normalize().multiplyScalar(1.5 + p0.distanceTo(p2) * 0.45);
    return new THREE.QuadraticBezierCurve3(p0, mid, p2);
  }), [JSON.stringify(arcs)]);
  const face = useMemo(() => {                             // turn the globe so the first arc faces the camera
    if (!arcs.length) return 0;
    const c = ll((arcs[0][0] + arcs[0][2]) / 2, (arcs[0][1] + arcs[0][3]) / 2, 1);
    return -Math.atan2(c.x, c.z);
  }, [JSON.stringify(arcs)]);
  return (
    <group rotation={[0.3, face - 0.35 + frame / fps * 0.12, 0]}>
      <mesh><sphereGeometry args={[1.47, 64, 64]} /><meshStandardMaterial color="#0d1626" roughness={0.6} metalness={0.2} /></mesh>
      <points geometry={dots}><pointsMaterial color="#9fb4d8" size={0.022} sizeAttenuation /></points>
      {tubes.map((cv, i) => {
        const p = interpolate(frame, [fps * (0.4 + i * 0.35), fps * (1.4 + i * 0.35)], [0.001, 1],
                              {extrapolateLeft: 'clamp', extrapolateRight: 'clamp', easing: Easing.bezier(0.65, 0, 0.35, 1)});
        const pts = cv.getPoints(80).slice(0, Math.max(2, Math.round(80 * p) + 1));
        const g = new THREE.TubeGeometry(new THREE.CatmullRomCurve3(pts), 64, 0.026, 8, false);
        return (
          <group key={i}>
            <mesh geometry={g}><meshBasicMaterial color={tone} toneMapped={false} /></mesh>
            <mesh position={cv.getPoint(0)}><sphereGeometry args={[0.04, 16, 16]} /><meshBasicMaterial color={tone} toneMapped={false} /></mesh>
            <mesh position={pts[pts.length - 1]}><sphereGeometry args={[0.045, 16, 16]} /><meshBasicMaterial color="#fff6dd" toneMapped={false} /></mesh>
          </group>
        );
      })}
    </group>
  );
};

const Bars: React.FC<Hero3DProps> = ({values = [3, 5, 2, 8], colors, tone = '#4aa3ff'}) => {
  const frame = useCurrentFrame();
  const {fps} = useVideoConfig();
  const mx = Math.max(...values);
  const lo = Math.min(...values) * 0.55;                    // baseline: small rises still look like rises
  const geo = useMemo(() => new RoundedBoxGeometry(0.7, 1, 0.7, 4, 0.08), []);
  const n = values.length;
  return (
    <group rotation={[0, interpolate(frame, [0, fps * 4], [-0.5, -0.25]), 0]} position={[0, -1.2, 0]}>
      <mesh rotation={[-Math.PI / 2, 0, 0]} receiveShadow><circleGeometry args={[3.2, 64]} /><meshStandardMaterial color="#1b2333" roughness={0.9} /></mesh>
      {values.map((v, i) => {
        const s = spring({frame: frame - 6 - i * 5, fps, config: {damping: 14, mass: 0.8}});
        const h = Math.max(0.02, ((v - lo) / (mx - lo)) * 2.6 * s);
        return (
          <mesh key={i} geometry={geo} position={[(i - (n - 1) / 2) * 0.95, h / 2, 0]} scale={[1, h, 1]} castShadow>
            <meshPhysicalMaterial color={(colors && colors[i]) || tone} roughness={0.38} clearcoat={0.6} clearcoatRoughness={0.25} />
          </mesh>
        );
      })}
    </group>
  );
};

const Coin: React.FC<Hero3DProps> = ({tone = '#e0b25a', spin = 540}) => {
  const frame = useCurrentFrame();
  const {fps, durationInFrames} = useVideoConfig();
  const a = interpolate(frame, [0, durationInFrames], [0, spin * Math.PI / 180], {easing: Easing.bezier(0.2, 0.8, 0.2, 1)});
  const lift = spring({frame, fps, config: {damping: 12}});
  return (
    <group rotation={[0.25, a, 0.1]} position={[0, (lift - 1) * 2, 0]}>
      <mesh rotation={[Math.PI / 2, 0, 0]}><cylinderGeometry args={[1.2, 1.2, 0.2, 96]} />
        <meshPhysicalMaterial color={tone} metalness={1} roughness={0.22} clearcoat={0.6} /></mesh>
      {[0.105, -0.105].map((z, i) => (
        <mesh key={i} position={[0, 0, z]}><torusGeometry args={[1.05, 0.045, 16, 96]} />
          <meshPhysicalMaterial color={tone} metalness={1} roughness={0.18} /></mesh>
      ))}
    </group>
  );
};

export const Hero3D: React.FC<Hero3DProps> = (p) => {
  const frame = useCurrentFrame();
  const {width, height, fps} = useVideoConfig();
  // step back until the object's width fits the frame's horizontal field of view (portrait clips are narrow)
  const hfov = 2 * Math.atan(Math.tan((32 * Math.PI / 180) / 2) * (width / height));
  const objW = p.object === 'bars' ? (p.values || [1, 1, 1, 1]).length * 0.95 + 1.2 : p.object === 'coin' ? 3.0 : 3.6;
  const need = (objW / 2) / Math.tan(hfov / 2) + 1.5;
  const dist = Math.max(p.object === 'bars' ? 7.5 : 6.2, need) * (p.zoom || 1) * interpolate(frame, [0, fps * 5], [1.08, 0.96]);
  return (
    <AbsoluteFill>
      <ThreeCanvas width={width} height={height} gl={{alpha: true, antialias: true, preserveDrawingBuffer: true}}
                   camera={{fov: 32, position: [0, 0.6, dist]}} shadows>
        <Env />
        <ambientLight intensity={0.25} />
        <directionalLight position={[3, 5, 4]} intensity={1.6} castShadow />
        <directionalLight position={[-4, 2, -3]} intensity={1.2} color="#7fb2ff" />
        {p.object === 'globe' ? <Globe {...p} /> : p.object === 'bars' ? <Bars {...p} /> : <Coin {...p} />}
      </ThreeCanvas>
    </AbsoluteFill>
  );
};
