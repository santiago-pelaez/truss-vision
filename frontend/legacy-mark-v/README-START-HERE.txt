TRUSSVISION.AI // MARK V
NETLIFY EDITION — QUICK INSTALL (MAC-FRIENDLY)

WHAT YOU DO:
1. Unzip trussvision-mark-v-netlify.zip.
2. Open Netlify -> your existing TrussVision site -> Deploys.
3. Deploy the WHOLE folder named "trussvision-mark-v" (NOT "public" alone).
   This package includes netlify.toml, public/, and netlify/functions/.
4. Open your site, enter your Google AI Studio API key under GEMINI AUTH,
   select 3.8 FLASH • FAST, upload a picture, then press SCAN.
5. Try LOAD DEMO -> 3D shaft / bearings or 3D cable forces to see the auto orbit.
   Drag to orbit manually, scroll to zoom, click AUTO ORBIT to pause/resume.

FASTEST IMAGE SCAN:
- Crop the picture to ONE engineering question. PNG/JPEG/WebP supported.
- App compresses big photos to approx 1800px before sending (faster and under Netlify limit).
- Small PDFs (under 3 MB) accepted; for multi-page exams crop/screenshot ONE question.
- 3.8 FLASH is faster than 4 ARGON for many routine extractions, but speed varies.
- Deeper analysis checkbox raises thinking effort (usually slower).
- Netlify synchronous functions cannot run longer than 60 seconds.
  The app stops waiting at 53 seconds. It cannot promise instantaneous response.

WHAT WORKS:
- Keeps the original TrussVision multi-panel HUD, load controls, telemetry and editable JSON.
- 2D problems stay in 2D; genuine 3D cable/vector/machine problems automatically
  switch to a rotating spatial projection with smooth entry/exit and pause/resume.
- Broader recognition of beams, trusses, frames, friction, pulleys, 3D cables,
  spatial moments, gear shafts/bearings, and composite shapes.
- Truss member force calculations for ideal 2D pin-jointed systems with known input.
- Shear, moments and support reactions for ONE simply-supported beam with vertical
  point loads or uniform distributed loads (no applied couples or varying UDLs).
- Known 3D applied-force and applied-moment RESULTANTS. It does NOT solve unknown
  3D cable tensions, bearing reactions or full machinery mechanics.
- All other subjects: reconstruction/visual exploration & study prompts only.
  DO NOT interpret preview geometry as an independently verified engineering solution.

SAFETY/ACCURACY:
- Review extracted coordinates, sign conventions, loads, supports and units before
  relying on any output. An AI scan is NOT verified just because a solver ran.
- Input-key mode sends the key to the site's Netlify Function; do not share it.
  If you ever publish the website, use an environment variable GEMINI_API_KEY
  in Netlify Site configuration, and add authentication/abuse protection for public
  access. An environment variable by itself does not prevent strangers using
  your site's API quota via your publicly reachable function.
- Gemini 4 Argon may require a paid account and can be significantly slower.
- No real API end-to-end test was run in this package; connect your own key.

TROUBLESHOOTING:
- Is the page showing but SCAN 404s? You only uploaded public/, or Netlify did
  not deploy netlify/functions/. Check Functions in the Netlify dashboard.
- Gemini timed out? Use 3.8 Flash, crop one problem, turn off deeper analysis.
- Only a photo and notes appear? The model could not reliably reconstruct
  geometry. Try a clearer crop; do not assume the image has been solved.
- 'Solver limitation' is intentional for unsupported equations; it is not a crash.

No professor/homework PDFs are bundled into this public deploy. For private
benchmarks, keep your original class files and their usage restrictions private.
