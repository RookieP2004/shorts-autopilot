import {useLayoutEffect, useRef} from 'react';
import {useCurrentFrame, useVideoConfig} from 'remotion';
import gsap from 'gsap';

// GSAP inside Remotion: build ONE paused timeline after mount, then seek it to the current frame on every render.
// Nothing may play on its own (no ticker), or frames rendered in parallel tabs would disagree.
gsap.ticker.lagSmoothing(0);
export const useGsapTimeline = (build: (tl: gsap.core.Timeline) => void, deps: unknown[] = []) => {
  const frame = useCurrentFrame();
  const {fps} = useVideoConfig();
  const tl = useRef<gsap.core.Timeline | null>(null);
  useLayoutEffect(() => {
    const t = gsap.timeline({paused: true});
    build(t);
    tl.current = t;
    t.seek(frame / fps, false);
    return () => { t.kill(); };
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, deps);
  useLayoutEffect(() => {
    tl.current?.seek(frame / fps, false);
  }, [frame, fps]);
};
