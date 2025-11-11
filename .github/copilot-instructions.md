## Purpose

This file gives an AI coding agent (or a new contributor) the minimum, actionable context to be productive in this repository.

## Big picture (what this project is)

- A single-page Streamlit app (`app.py`) that loads a saved sklearn pipeline/artifacts and predicts "RainTomorrow" for Australian weather.
- The model and preprocessing artifacts are stored in a joblib payload named `aussie_rain.joblib` (the app expects it under `models/aussie_rain.joblib`).

## Key files and artifact contract

- `app.py` — Streamlit UI, input collection, single-row DataFrame construction, preprocessing, and prediction flow.
- `aussie_rain.joblib` — a joblib dictionary expected to contain these keys:
  - `model` (sklearn estimator exposing `predict` and `predict_proba`)
  - `imputer` (transformer with `.transform` for numeric columns)
  - `scaler` (transformer with `.transform` for numeric columns)
  - `encoder` (OneHotEncoder-like object; `.transform` returns a sparse matrix)
  - `input_cols` (list of column names — order matters)
  - `numeric_cols` (list of numeric column names)
  - `categorical_cols` (list of categorical column names)

Do not change the names or the shapes of these keys without updating `app.py` accordingly.

## Data flow & important patterns (from `app.py`)

1. UI fields → `build_input_df()` produces a one-row DataFrame with columns ordered exactly as `input_cols`.
2. `preprocess(df_row)` does:
   - select `numeric_cols`, run `imputer.transform` then `scaler.transform`;
   - select `categorical_cols`, cast to object and call `encoder.transform` (returns sparse → call `.toarray()`);
   - combine with `np.hstack([X_num, X_cat.toarray()])` to produce final model input.
3. Model call: `model.predict_proba(X_final)[0,1]` and `model.predict(X_final)[0]`.

Edge cases the agent must respect:
- Column order is enforced by `input_cols` when creating the DataFrame; changing order breaks preprocessing.
- Encoder returns a sparse matrix — the app calls `.toarray()` before hstack.
- The app is written for a one-row input (interactive Streamlit form). Batch changes require careful reshaping.

## Running & debugging (developer workflow)

Recommended dependencies (create `requirements.txt` if missing):

streamlit
pandas
numpy
scikit-learn
joblib

To create a Python venv and install dependencies (PowerShell):

```powershell
python -m venv .venv; .\.venv\Scripts\Activate.ps1; python -m pip install -r requirements.txt
```

Run the app (PowerShell):

```powershell
streamlit run "app.py"
```

Quick checks when something fails:
- Verify the joblib file location: `app.py` currently loads `models/aussie_rain.joblib` — if `aussie_rain.joblib` is at the repo root, either move it into a `models/` folder or change `load_artifacts()` to load from the actual path.
- If preprocessing errors occur, inspect `input_cols`, `numeric_cols`, and `categorical_cols` inside the joblib object (they must match the DataFrame columns and dtypes expected by the saved transformers).

## Common edits the agent may need to do (how-to examples)

- Add a new input feature:
  1. Add a Streamlit input in `app.py` and a default value (follow existing unit conventions: °C, mm, km/h, hPa).
  2. Update the model artifact (retrain/export) so `input_cols`, `numeric_cols`/`categorical_cols`, and transformers reflect the new feature.
  3. Ensure `build_input_df()` inserts the new field and that `input_cols` order is preserved.

- Fix model path mismatch (example patch):
  - Replace `path = os.path.join("models", "aussie_rain.joblib")` with `path = os.path.join(os.path.dirname(__file__), "aussie_rain.joblib")` if the file lives next to `app.py`.

## Tests & small automation notes

- There are no tests currently. For a quick smoke test, create a pytest that:
  - loads `aussie_rain.joblib`,
  - builds a single-row DataFrame matching `input_cols`,
  - calls `preprocess` (imported from `app.py`) and asserts the output shape matches `len(numeric_cols) + encoder_output_dim`.

## Implementation constraints and conventions

- Keep the artifact keys stable; other code relies directly on those keys.
- Keep UI labels and units consistent (users expect specific units).
- Use `@st.cache_resource` for artifact loading (already used in `app.py`) to avoid repeated loads.

If any part of this file looks incomplete or you want more examples (tests, CI, or a sample `requirements.txt`), tell me which area to expand and I will update it.
