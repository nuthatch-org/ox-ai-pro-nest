-- Event-history subset. Mapping inspected statically; accumulated fields are absent.
CREATE VIEW "rank_up_event" AS
SELECT tx_hash || '-' || CAST(log_index AS VARCHAR) AS id, block_timestamp AS timestamp, block_number AS block, tx_hash AS "txHash", "userId" AS member, CAST("newRank" AS INTEGER) AS "newRank" FROM ox_ai_pro__rank_up;
