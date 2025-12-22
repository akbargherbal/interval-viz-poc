# Resilient HUD Design System: The "Vertical Logic" Edition

## 1. Core Philosophy: "Architectural Locking"

The dashboard does not rely on "eyeballing" alignment. It relies on **Architectural Locking**. We do not position elements; we define mathematical relationships between them.

The layout prioritizes **Legible Precision** over maximal density. Labels are large and semantic, data is centered via calculation, and collision is mathematically impossible due to the "Iron Logic" of the grid.

---

## 2. The "Iron Logic" (The Mathematical Core)

The structural integrity of the dashboard rests on a single vertical dimension called the **Instrument Strip**.

```css
:root {
  /* The master variable controlling the height of the middle band */
  --h-strip: 48px;
  /* The footer action height */
  --h-action: clamp(28px, 16cqh, 32px);
}
```

This variable (`--h-strip`) serves three simultaneous masters to ensure alignment never drifts:

1.  **Grid Row 2 Height:** Defines the container for **Zone 3 (Logic)**.
2.  **Zone 5 Overlay Height:** Defines the height of the **Zone 5 (Boundaries)** overlay inside Zone 1.
3.  **Zone 1 Bottom Padding:** Defines the "No-Fly Zone" so the hero value never collides with the overlay.

**Visual Result:** Zone 3 (Logic) and Zone 5 (Overlay) form a continuous horizontal band across the dashboard, despite being in different grid columns.

---

## 3. The 5-Zone Topology

The grid is a **2x3 matrix**, but zones utilize row-spanning, overlays, and flex-direction shifts to create a hierarchy.

### Zone 1: The Primary Focus (The "Stage")

- **Position:** Column 1, Spans Rows 1 & 2 (`grid-row: 1 / 3`).
- **Role:** The active subject (e.g., Current Value, Mid Index).
- **Typography:** `clamp(70px, 45cqh, 110px)`.
- **The "No-Fly Zone":** Zone 1 has `padding-bottom: var(--h-strip)`. This forces the number to center perfectly in the _visible_ space above the overlay.
- **Labeling:** Large, uppercase, colored **Amber-600** (dimmed version of the hero color).

### Zone 2: The Goal (The "North Star")

- **Position:** Column 2, Row 1.
- **Role:** The static target (e.g., Target Value, Max Sum).
- **Labeling:** Large, uppercase, colored **Emerald-600**.

### Zone 3: The Logic (The "Vertical Tab")

- **Position:** Column 2, Row 2 (Height locked to `--h-strip`).
- **Role:** The decision engine (e.g., `TRUE/FALSE`, `x < y`).
- **Structural Change:** Unlike other zones, this is a **Flex Row**.
  - **Left Column:** The Label (Vertical Sidebar).
  - **Right Column:** The Content (Centered Data).
- **Why:** This physically separates the label from the data, making overlap impossible regardless of data length.

### Zone 4: The Action (The "Footer")

- **Position:** Spans Columns 1 & 2, Row 3.
- **Role:** The consequence (e.g., "SWAP INDICES", "SEARCH RIGHT").
- **Height:** Locked to `var(--h-action)`.

### Zone 5: State Boundaries (The "Overlay")

- **Position:** Absolute positioned at the bottom of Zone 1.
- **Role:** Contextual metadata (e.g., Pointers, Indices, Depth).
- **Height:** Locked to `var(--h-strip)`.
- **Visuals:** Semi-transparent backdrop (`backdrop-filter: blur`) allows it to float over the background while obscuring nothing due to the "No-Fly Zone."

---

## 4. Visual Grammar & Semantics

Colors are functional layers. Labels inherit the **Hue** of their parent zone but use specific **Saturation/Lightness** to recede slightly.

| Context    | Main Color (Data)       | Label Color (Meta)      | Meaning                      |
| :--------- | :---------------------- | :---------------------- | :--------------------------- |
| **Focus**  | Amber-400 (`#fbbf24`)   | Amber-600 (`#d97706`)   | Active, Hot, Changing.       |
| **Goal**   | Emerald-400 (`#34d399`) | Emerald-600 (`#059669`) | Stable, Desired, Success.    |
| **Logic**  | White (`#ffffff`)       | Blue-300 (`#93c5fd`)    | Neutral, Boolean, Technical. |
| **Action** | Slate-100 (`#f1f5f9`)   | Slate-400 (`#94a3b8`)   | Instruction, Future State.   |

---

## 5. The "Vertical Tab" Pattern (Zone 3)

To solve the density issue in Zone 3 (which is only ~48px tall), we implement the **Vertical Tab**.

1.  **Orientation:** The label is rotated using `writing-mode: vertical-rl` and `transform: rotate(180deg)`. It reads bottom-to-top.
2.  **Aggression:** To ensure the label is seen despite its position, it uses:
    - **Font Style:** `italic` (Dynamic forward motion).
    - **Font Weight:** `900` (Heavy).
    - **Font Size:** `~12px` (`clamp(11px, 4cqh, 13px)`).
    - **Background:** A dark translucent strip (`rgba(0,0,0,0.25)`) to act as a physical divider.
3.  **Result:** A distinct "technical sidebar" aesthetic that maximizes horizontal space for the logic equation.

---

## 6. Resilience & Scaling (React Implementation)

The dashboard ignores pixels in favor of **Container Query Units (cqh)** and dynamic text scaling.

### Text Scaling Constants

React components must implement dynamic font scaling for values that exceed standard lengths.

```javascript
const Z1_LONG_TEXT = 4; // Threshold for Zone 1 Hero Value
const Z3_LONG_TEXT = 5; // Threshold for Zone 3 Logic Text
```

### CSS Classes

- `.long-text`: Applied to Zone 1 when `value.length > Z1_LONG_TEXT`. Reduces font size by ~30%.
- `.zone3-long-text`: Applied to Zone 3 when `logic.length > Z3_LONG_TEXT`. Reduces font size to fit the strip.

---

## 7. Implementation Checklist

When implementing this dashboard for a new algorithm:

1.  **Graceful Degradation:** Always check `if (!step?.data?.visualization) return ...` first.
2.  **Safe Data Extraction:** Destructure visualization data with default fallbacks (e.g., `const val = data?.val ?? "-"`).
3.  **Logic Derivation:** Calculate `logicText`, `logicSub`, and `actionText` based on `step.type` or data comparison _before_ rendering.
4.  **Zone Mapping:**
    - **Zone 1:** The "Hero" number.
    - **Zone 2:** The "Target" number.
    - **Zone 3:** The "Comparison" (Vertical Tab).
    - **Zone 4:** The "Verb" (Action).
    - **Zone 5:** The "Context" (3 cells max).
5.  **Apply Scaling:** Use `Z1_LONG_TEXT` and `Z3_LONG_TEXT` logic for dynamic class application.
