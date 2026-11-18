import React from 'react';
import {CalculateMetadataFunction, Composition} from 'remotion';
import {KineticTitle} from './KineticTitle';
import {FlowDiagram} from './FlowDiagram';
import {Hero3D} from './Hero3D';
import {NumberSlam} from './NumberSlam';
import {Stack3D} from './Stack3D';

// Every composition takes its size, fps and length from the input props (set by autopilot/motion.py).
type Meta = {w?: number; h?: number; fps?: number; dur?: number};
const meta: CalculateMetadataFunction<Meta & Record<string, unknown>> = ({props}) => ({
  width: props.w || 1080, height: props.h || 1920, fps: props.fps || 30,
  durationInFrames: Math.max(1, Math.round((props.dur || 3) * (props.fps || 30))),
});

export const Root: React.FC = () => (
  <>
    <Composition id="KineticTitle" component={KineticTitle as any} width={1080} height={1920} fps={30} durationInFrames={90}
                 defaultProps={{lines: ['WHY IS MY', '*CHAI* COSTLIER?']}} calculateMetadata={meta as any} />
    <Composition id="FlowDiagram" component={FlowDiagram as any} width={1080} height={1920} fps={30} durationInFrames={120}
                 defaultProps={{nodes: [{id: 'a', label: 'MONEY', x: 0.3, y: 0.3}, {id: 'b', label: 'PRICES', x: 0.7, y: 0.55}],
                                edges: [['a', 'b']]}} calculateMetadata={meta as any} />
    <Composition id="Hero3D" component={Hero3D as any} width={1080} height={1920} fps={30} durationInFrames={120}
                 defaultProps={{object: 'globe', arcs: [[19, 73, 25, 55]]}} calculateMetadata={meta as any} />
    <Composition id="NumberSlam" component={NumberSlam as any} width={1080} height={1920} fps={30} durationInFrames={75}
                 defaultProps={{text: '$1.92 BILLION'}} calculateMetadata={meta as any} />
    <Composition id="Stack3D" component={Stack3D as any} width={1080} height={1920} fps={30} durationInFrames={90}
                 defaultProps={{n: 30}} calculateMetadata={meta as any} />
  </>
);
