-- Event-history subset. Mapping inspected statically; accumulated fields are absent.
CREATE VIEW "campaign_win" AS
SELECT tx_hash || '-' || CAST(log_index AS VARCHAR) AS id, block_timestamp AS timestamp, block_number AS block, tx_hash AS "txHash", "userId" AS member, amount FROM ox_ai_pro__campaign_reward;
