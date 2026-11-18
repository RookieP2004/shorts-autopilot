import React, {useMemo} from 'react';
import {AbsoluteFill, interpolate, random, spring, useCurrentFrame, useVideoConfig} from 'remotion';
import {ThreeCanvas} from '@remotion/three';
import {useThree} from '@react-three/fiber';
import * as THREE from 'three';
import {RoomEnvironment} from 'three/examples/jsm/environments/RoomEnvironment.js';
import {RoundedBoxGeometry} from 'three/examples/jsm/geometries/RoundedBoxGeometry.js';

export type Stack3DProps = {
  n?: number;            // how many cash bricks (fictional notes) fall into the pile
  color?: string;        // brick colour
  band?: string;         // paper band colour
  every?: number;        // seconds between bricks
  move?: 'orbit' | 'push' | 'rise';
};

const Env: React.FC = () => {
  const {gl, scene} = useThree();
  useMemo(() => {
    const pm = new THREE.PMREMGenerator(gl);
    scene.environment = pm.fromScene(new RoomEnvironment(), 0.04).texture;
    (scene as any).environmentIntensity = 0.6;
  }, [gl, scene]);
  return null;
};

// A pile of banded cash bricks building itself: each brick drops in with a spring bounce onto a growing pyramid while the
// camera orbits / pushes / rises. A big amount made physical (pair it with a hud or NumberSlam for the actual figure).
export const Stack3D: React.FC<Stack3DProps> = ({n = 30, color = '#8fbf98', band = '#e0b25a', every = 0.06, move = 'orbit'}) => {
  const frame = useCurrentFrame();
  const {width, height, fps, durationInFrames} = useVideoConfig();
  const brick = useMemo(() => new RoundedBoxGeometry(1.0, 0.28, 0.5, 3, 0.04), []);
  const bandG = useMemo(() => new THREE.BoxGeometry(0.22, 0.29, 0.51), []);
  const slots = useMemo(() => {                                  // pyramid layers: 4x3, 3x2, 2x2, 1x1 ... repeated wider
    const out: [number, number, number, number][] = [];
    let level = 0;
    while (out.length < n) {
      const cols = Math.max(1, 5 - level), rows = Math.max(1, 3 - Math.floor(level / 2));
      for (let r = 0; r < rows && out.length < n; r++)
        for (let c = 0; c < cols && out.length < n; c++)
          out.push([(c - (cols - 1) / 2) * 1.04, level * 0.29 + 0.14, (r - (rows - 1) / 2) * 0.54, (random(`r${out.length}`) - 0.5) * 0.12]);
      level++;
    }
    return out;
  }, [n]);
  const p = frame / Math.max(1, durationInFrames - 1);
  const fit = Math.max(1, height / width);
  const cam = move === 'push' ? [0, 2.2, interpolate(p, [0, 1], [9, 6]) * fit] as const
    : move === 'rise' ? [2.5, interpolate(p, [0, 1], [0.8, 4.0]), 7.5 * fit] as const
      : [Math.sin(p * 1.2 - 0.6) * 7.5 * fit, 2.6, Math.cos(p * 1.2 - 0.6) * 7.5 * fit] as const;
  return (
    <AbsoluteFill>
      <ThreeCanvas width={width} height={height} gl={{alpha: true, antialias: true, preserveDrawingBuffer: true}}
                   camera={{fov: 32, position: cam as any}} onCreated={({camera}) => camera.lookAt(0, 0.6, 0)} shadows>
        <CamLook />
        <Env />
        <ambientLight intensity={0.25} />
        <spotLight position={[0, 9, 2]} angle={0.5} penumbra={0.4} intensity={160} castShadow color="#fff1da" />
        <directionalLight position={[-5, 2, -4]} intensity={1.4} color="#7fb2ff" />
        <mesh rotation={[-Math.PI / 2, 0, 0]} receiveShadow><circleGeometry args={[5, 64]} /><meshStandardMaterial color="#1a1f2a" roughness={0.85} /></mesh>
        {slots.map(([x, y, z, rot], i) => {
          const s = spring({frame: frame - Math.round(i * every * fps) - 4, fps, config: {damping: 11, mass: 0.6}});
          if (s <= 0.001) return null;
          const yy = y + (1 - s) * 4.5;
          return (
            <group key={i} position={[x, yy, z]} rotation={[0, rot + (1 - s) * 1.2, (1 - s) * 0.4]}>
              <mesh geometry={brick} castShadow receiveShadow><meshPhysicalMaterial color={color} roughness={0.55} clearcoat={0.2} /></mesh>
              <mesh geometry={bandG} castShadow><meshStandardMaterial color={band} roughness={0.4} metalness={0.2} /></mesh>
            </group>
          );
        })}
      </ThreeCanvas>
    </AbsoluteFill>
  );
};

const CamLook: React.FC = () => {
  const {camera} = useThree();
  camera.lookAt(0, 0.7, 0);
  return null;
};
