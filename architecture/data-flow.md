# Data Flow

Synthetic CSV files land in `data/raw`, load into DuckDB, pass contract validation, feed metric calculations, produce scorecards, and become accessible through API/dashboard layers.
