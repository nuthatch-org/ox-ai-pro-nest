-- Event-history subset. Mapping inspected statically; accumulated fields are absent.
CREATE VIEW "deposit" AS
SELECT tx_hash || '-' || CAST(log_index AS VARCHAR) AS id, block_timestamp AS timestamp, block_number AS block, tx_hash AS "txHash", "from", amount, message FROM ox_ai_pro__usdt_deposited;
