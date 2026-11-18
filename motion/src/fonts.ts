import {continueRender, delayRender, staticFile} from 'remotion';

// Local house fonts (repo fonts/), loaded once per page before any frame is captured.
const FACES: [string, string][] = [
  ['Anton', 'fonts/Anton-Regular.ttf'],
  ['Poppins', 'fonts/Poppins-ExtraBold.ttf'],
  ['PoppinsSemi', 'fonts/Poppins-SemiBold.ttf'],
  ['Playfair', 'fonts/PlayfairDisplay.ttf'],
  ['Doto', 'fonts/Doto.ttf'],
];
let started = false;
export const loadFonts = () => {
  if (started) return;
  started = true;
  const h = delayRender('fonts');
  Promise.all(FACES.map(([name, file]) => new FontFace(name, `url(${staticFile(file)})`).load().then((f) => document.fonts.add(f))))
    .then(() => continueRender(h))
    .catch((e) => { console.error(e); continueRender(h); });
};
