-- Forward-only migration: record the real network fee (lamports) paid for a
-- transaction, next to the conservative fee_micro estimate.
--
-- fee_micro is intentionally unchanged: it uses the SOL/USD ceiling price so
-- the budget never under-counts spend. This column stores the factual figure
-- reported by the confirmed transaction (res.feeLamports). Existing rows are
-- untouched and remain valid (column is nullable).
ALTER TABLE inference_calls ADD COLUMN fee_lamports INTEGER;
