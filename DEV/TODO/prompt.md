 Since I can't share the entire codebase all at once due to token limits per message; I rely on you to ask explicitly for the file you need to make an informed decision. Like who determines the target value and the size of the array.

My objective for this session is to update the README.md based on the current codebase, since it has not been updated since the Proof of Concept stage, when we were visualizing a single algorithm (Interval Coverage). The current vision is to create a platform for visualizing algorithms.


***

**Role:** You are a Senior Technical Documentation Specialist and Software Architect.

**Task:** Completely rewrite the project's `README.md` file. The current version describes an "Interval Coverage Visualization PoC," but the codebase has evolved into a generic **"Algorithm Visualization Platform"** capable of supporting multiple algorithms (currently Interval Coverage and Binary Search) via a registry-based architecture.

**Context:**
The project adheres to a strict philosophy: *Backend does ALL the thinking (trace generation), Frontend does ALL the reacting (visualization).* This philosophy remains, but the implementation has shifted from hardcoded endpoints to a dynamic registry system.

**Required Updates & Sections:**

1.  **Project Title & Overview:**
    *   Rename the project to **"Algorithm Visualization Platform"**.
    *   Update the status to reflect that the platform architecture is complete and supports multiple algorithms.

2.  **Project Structure:**
    *   Update the file tree diagram to reflect the new architecture.
    *   **Backend:** Highlight `backend/algorithms/registry.py`, `base_tracer.py`, and the `binary_search.py` implementation.
    *   **Frontend:** Highlight the `visualizations/` folder (containing `ArrayView`, `TimelineView`, `CallStackView`) and `AlgorithmSwitcher.jsx`.

3.  **Key Architecture Decisions (Crucial Update):**
    *   **The Registry Pattern:** Explain that new algorithms are added via `backend/algorithms/registry.py` and automatically discovered by the frontend.
    *   **Unified API:** Explain that `app.py` now uses a single generic endpoint (`/api/trace/unified`) that routes requests based on the registry.
    *   **Dynamic Visualization:** Explain how the frontend uses `visualizationRegistry.js` to dynamically select the correct component (e.g., `ArrayView` vs `TimelineView`) based on metadata sent from the backend.

4.  **API Documentation:**
    *   **New Primary Endpoint:** Document `POST /api/trace/unified`. Show the JSON structure: `{"algorithm": "name", "input": {...}}`.
    *   **Discovery Endpoint:** Document `GET /api/algorithms` which lists available algorithms and their example inputs.
    *   **Legacy:** Mark the old `/api/trace` endpoint as deprecated/legacy.

5.  **Contributing (Adding a New Algorithm):**
    *   *This is the most important instruction change.*
    *   Rewrite the "Adding a New Algorithm" guide. It should no longer say "Add endpoint in app.py".
    *   **New Steps:**
        1.  Inherit from `AlgorithmTracer` (`backend/algorithms/base_tracer.py`).
        2.  Implement `execute()` and `get_prediction_points()`.
        3.  Register the class in `backend/algorithms/registry.py`.
        4.  (Frontend) Ensure a compatible visualization component exists in `frontend/src/components/visualizations/`.

6.  **Compliance & Standards:**
    *   Add a new section referencing the **Tenant Guide** (`docs/TENANT_GUIDE.md`).
    *   Mention that all new algorithms must pass the **Compliance Checklists** (Backend, Frontend, QA) found in `docs/compliance/`.

7.  **Active Learning Features:**
    *   Generalize the description of "Prediction Mode." Use Binary Search (predicting "Search Left" vs "Search Right") as a second example alongside the existing Interval Coverage example.

**Tone:**
Professional, educational, and architecturally focused.

**Input Files for Reference:**
*   `backend/algorithms/registry.py` (For understanding the new backend architecture)
*   `backend/app.py` (For the new API endpoints)
*   `frontend/src/utils/visualizationRegistry.js` (For the frontend dynamic rendering)
*   `docs/compliance/CHECKLIST_SYSTEM_OVERVIEW.md` (For the new compliance section)

---

Before you begin updating the README.md, generate a plan that you can follow later when I give you the final approval to proceed with the rewrite.
