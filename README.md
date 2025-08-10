# DragonBall Chess — Local 2-Player (with AI)

A single-file React app that mashes up classic chess with Dragon Ball transformations. Pieces “power up” on captures, can be “damaged” (lose a form) on hits, and promotions become the Grand Priest. Runs fully in the browser; optional embedded Stockfish (WASM) gives you a local AI with adjustable strength.

🎮 **[▶ Play it online here](https://anurag9000.github.io/dragonball-chess/)** — works entirely in your browser.


## ✨ Features

* **DBZ x Chess rules**

  * Capture = attacker levels up by multiple forms (based on the victim’s highest form reached).
  * **Hit mechanic**: if a defender has a higher form, it loses exactly one form instead of being captured and **the turn passes**.
  * Promotion → **Grand Priest**.
  * Strict, canonical mapping between chess types and DBZ characters (R=Goku/Vegeta, N=Gohan-Kid/Frieza, B=Majin Boo/Gotenks, Q=Grand Priest, K=Zeno; pawns are named per file).
* **Local AI (Stockfish)** with 4 hardness presets; runs in a Web Worker (no server).
* **Quality of life**

  * Visible **attack beam** trail on captures/hits.
  * **Fog of war** toggle.
  * Material tally + capture history.
  * **Undo** with DBZ-aware history.
  * **Boot log** overlay for quick diagnostics.

---

## 🗂️ Project structure

```
.
├── index.html                # This file (app boot + UI)
├── assets/
│   └── pieces/
│       ├── goku/base.png, kaioken.png, ssj.png, ...
│       ├── vegeta/base.png, ssj.png, ssj2.png, ssb.png, ultra_ego.png
│       ├── zeno/zeno.png
│       ├── grand_priest/grand_priest.png
│       └── ... (see “Sprites” below)
└── vendor/
    ├── react.development.js
    ├── react-dom.development.js
    ├── babel.min.js
    └── lichess/
        ├── stockfish-17-lite-single.js
        ├── stockfish-17-lite-single.wasm
        └── (any other files the worker expects)
```

> The app currently pulls **chess.js** from a CDN at runtime. See **Offline/air-gapped mode** to make it 100% local.

---

## 🚀 Quick start

1. Put this repository on any static web server (or open `index.html` directly).

   * Easiest: `python -m http.server` then visit `http://localhost:8000`.
2. Ensure sprites exist under `assets/pieces/<character>/<form>.png`. Missing files simply hide the image (the game still works).
3. (Optional AI) Drop the Stockfish worker + `.wasm` into `vendor/lichess/` (filenames as above).
4. Open the page. You should see “Boot: Mounted OK” in the bottom-right **bootlog**.

---

## 🎮 Gameplay & DBZ rules

* **Power-up on kill:** when a piece captures, it gains `victim.maxForm + 1` forms (capped at its own max).
  The app tracks `formIdx` (current stage) and `maxForm` (highest reached).
* **Hit, not kill:** if you attack a defender that’s **above base** (formIdx > 0), the defender **drops one form** instead of being removed; **turn flips** to the opponent. This is drawn as a beam on the board.
* **Promotion:** any pawn that promotes becomes **Grand Priest** (single-form sprite).
* **Strict mapping:** every square’s DBZ character is auto-normalized to match the underlying chess **type** (k, q, r, b, n, p). If a roster entry is missing/invalid, it is repaired according to canonical mapping.
* **Back rank (both colors)**

  * a/h-files (Rooks): **Goku / Vegeta**
  * b/g-files (Knights): **Gohan-Kid / Frieza**
  * c/f-files (Bishops): **Majin Boo / Gotenks**
  * d-file (Queen): **Grand Priest**
  * e-file (King): **Zeno**
* **Pawn files (a→h):** Saibaman, Chiaotzu, Krillin, Tien, Whis, Yamcha, Piccolo, Android 18.

> **Note on “❤ life”:** the badge under each piece currently shows `life` which increments on **kills** (a “win streak” stat). **It is not used as HP** in combat resolution; the *forms* are the actual “health.” (This matches the code and the power-up logic.)

---

## 🧠 AI (Stockfish WASM)

* Toggle **AI as White/Black** in the side panel.
* Choose a **Hardness** profile (Easy / Normal / Hard / Insane). This adjusts:
  `UCI_Elo`, `movetime`, `depth`, and cache `Hash`.
* The engine runs as a **Web Worker**: `vendor/lichess/stockfish-17-lite-single.js` (WASM alongside).
* A small **engine log** shows UCI handshake, best moves, and status.

---

## 🖼️ Sprites (characters & forms)

The app expects PNGs here:

```
assets/pieces/<character>/<form>.png
```

### Included characters (expandable)

* `goku`: `base`, `kaioken`, `ssj`, `ssj2`, `ssj3`, `ssj4`, `ssg`, `ssb`, `ssb_kaioken`, `ui`, `mui`
* `vegeta`: `base`, `great_ape`, `ssj`, `ssj2`, `ssj3`, `ssj4`, `ssg`, `ssb`, `ssb_evolved`, `ultra_ego`
* `zeno`: `zeno`
* `whis`: `angel`
* `grand_priest`: `grand_priest`
* `piccolo`: `base`, `potential`, `orange`
* `krillin`: `base`
* `yamcha`: `base`
* `tien`: `base`
* `chiaotzu`: `base`
* `android_18`: `base`
* `majin_boo`: `fat`, `evil`, `super`, `buutenks`, `buuccolo`, `buuhan`, `kid_buu`
* `frieza`: `1`, `2`, `3`, `final`, `mecha`, `golden`, `black`
* `saibaman`: `base`
* `gohan_kid`: `base`, `ssj`, `ssj2`, `ssj3`, `mystic`, `beast`
* `gotenks`: `base`, `ssj`, `ssj2`, `ssj3`

> Missing images are tolerated: the piece plays normally; only the sprite hides.

---

## 🧩 Tech notes

* **UI:** React 18 (UMD) + in-page Babel transform of the JSX.
* **Chess rules:** `chess.js` (ESM) loaded from CDN; legacy UMD fallback (0.10.3) with shims.
* **Engine:** Lichess Stockfish 17 “lite single” WASM in a Web Worker.
* **Canvas overlay** draws transient attack lines; auto-scales with board.

---

## 🔧 Configuration & switches

* **Fog of War:** per-turn half-board mask (button toggles ON/OFF).
* **Undo:** restores both **FEN** and **roster** (DBZ state), then re-normalizes mappings.
* **Difficulty Apply:** restarts the engine worker to apply fresh options.

---

## 📦 Offline / air-gapped mode

The header claims “no network required,” but **chess.js** is currently fetched from a CDN. To go 100% offline:

1. Download `chess.js` ESM and serve it locally, or switch to the UMD 0.10.3 file locally and keep the included shims.

   * Replace:

     ```html
     import('https://cdn.jsdelivr.net/npm/chess.js@1.4.0/dist/esm/chess.js')
     ```

     with

     ```js
     ChessCtor = await tryImport('/vendor/chess.js'); // your local path
     ```
2. Keep `vendor/react*.js`, `vendor/babel.min.js` local (already referenced).
3. Provide `vendor/lichess/stockfish-17-lite-single.js` and its `.wasm` next to it (already referenced).
   The line:

   ```js
   window.Module = { locateFile: p => 'vendor/lichess/' + p };
   ```

   tells the worker where to find the `.wasm`.

---

## 🧪 Development tips

* Use a local server (avoids `file://` CORS quirks for dynamic `import()` and Workers).
* Open DevTools Console and the **bootlog** (bottom-right) to spot:

  * “Chess ready”, “Mounted OK”, “UCI ok”, etc.
  * Any sprite 404s (harmless; just invisible).
* The overlay canvas resizes on demand; if you change board borders, keep the `border` offset in `drawAttackLine` in sync.

---

## 🐞 Troubleshooting

* **“Chess not loaded” / alert on boot**
  You’re offline or the CDN failed. Switch to a local `chess.js` file (see **Offline**).
* **Engine never gets to “readyok”**
  Check the `vendor/lichess/` paths and the `.wasm` file name. The Web Worker file must be loadable, and `window.Module.locateFile` must point to the correct folder.
* **No sprites showing**
  Confirm the folder/filenames exactly match `spriteUrl(char, form)`:
  `assets/pieces/<char>/<form>.png`.
* **AI does nothing**
  Ensure AI is enabled for the side to move; check the engine log; click **Apply** after changing hardness.
* **Desync after many undos**
  The app re-normalizes roster ↔ chess type every position change; if you edited code, confirm `ensureMappingStrict` is still called in the `[game]` effect.

---

## 🗺️ Extending the rules

* **Add forms**: extend a character’s array in `FORMS`, drop matching PNGs.
* **New characters**: add a key in `FORMS`, then whitelist it in `TYPE_ALLOWED` for the intended chess type(s).
* **Alternate promotion**: change the promotion branch in `doMove` where `moverPrev.char` is set to `'grand_priest'`.

---

## ✅ Known consistency notes (as coded)

* The **“❤ life”** badge is a kill counter, not HP. Combat resolution uses `formIdx` only.
  If you want life to be HP, wire hits to decrement `life` and gate defeat on `life === 0`, or rename the badge (e.g., “KOs”).
* On **castling**, both king and rook roster entries are moved to keep DBZ mapping in sync.
* **En passant** correctly identifies and removes the defender’s pawn in the roster.

---

## 📜 License

Choose a license (MIT/Apache-2.0/AGPL, etc.) and add it here.

---

## 🤝 Credits

* Chess rules by **chess.js**
* Engine by **Stockfish** (Lichess WASM build)
* All Dragon Ball character names/sprites are fan theming; provide your own artwork.

---

## 🧭 Roadmap (suggested)

* Full offline `chess.js` by default.
* Sound effects for hits/captures, per character.
* Per-piece **HP** mode (make “life” actual HP).
* PGN export with DBZ annotations.
* Mobile layout polish & drag-and-drop moves.

---

**Have fun going MUI on the 64 squares.**
