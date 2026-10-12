# OX AI PRO event-history stopgap

Limited event-history fallback for Polygon deployment `QmbzwJnre963f9wT9VCJPede69vaniAKWVHzUEsAmBfrHG`.

This does not restore the app's dashboard. Global counters, member balances, ranks and profiles,
referral-tree totals, director reward state and monthly member volume are not reproduced.
A query requesting an unavailable field fails by name, rather than returning a substitute.
Only `Member.id` is available for the relations in the event records.

Hosted endpoint: `https://subgraphs.nuthatch-indexer.com/subgraphs/id/QmbzwJnre963f9wT9VCJPede69vaniAKWVHzUEsAmBfrHG`

Coverage, live status and playground: [nuthatch-indexer.com](https://nuthatch-indexer.com/subgraphs/QmbzwJnre963f9wT9VCJPede69vaniAKWVHzUEsAmBfrHG).

## Exposed event records

- SubscriptionEvent
- Reward
- RankUpEvent
- CampaignWin
- MonthSnapshotEntity
- Transfer
- Withdrawal
- Deposit

The original schema is preserved in `graph/schema.graphql`. The matching read views expose the
fields of the eight immutable entity types above; mutable types have no accounting columns.
Examples are in `queries/`. The `refusal.graphql` query must fail.

## Source and verification

Contract: `0x5f511f9ad5c7b3d68d1f86444a5b7a32459fbb5a`, from block `88711689` on Polygon.
The manifest pins ABI CID `QmRRhZdXPwdpXnrEGePuLtjYVWGJQh3bL7WnUZe2dw8wqW` and mapping
CID `QmWXWj91zUYgRf19ZbJCqEMsAXhxUfotPth1gRT51Mv8Fn`. The compiled handlers were read
statically. They are not executed. Transaction-log ids are transaction hash, a hyphen and decimal
log index. Month snapshots use decimal monthId. `Withdrawal.usdtOut` is tokenAmountOut for
WithdrawPB; tokenOut is also populated there, exactly as the compiled handler does.

## Self-host

Use the nuthatch Graph build, version 5.3.0 or later, with an archive Polygon RPC:

```sh
export NUTHATCH_RPC='YOUR_POLYGON_RPC'
./nuthatch dev --dir . --listen 127.0.0.1:8288 --seal-direct --window 2000 --poll-interval 15s --no-admin
```

GraphQL is at `/subgraphs/id/QmbzwJnre963f9wT9VCJPede69vaniAKWVHzUEsAmBfrHG`.
Wait for `/ready` to report ready and a small lag before relying on current event history.
RPC credentials belong in the environment, never in the nest.

## Verification

`tests/verify-events.py` independently decodes raw Polygon logs and compares each exposed field with the GraphQL endpoint. The initial 100,000-block sample matched 2,450 records without differences. Accounting-query refusal checks passed. CampaignWin, MonthSnapshotEntity and Deposit had no events in that sample; their values are untested by that sample.

```sh
export NEST_ENDPOINT="https://subgraphs.nuthatch-indexer.com/subgraphs/id/QmbzwJnre963f9wT9VCJPede69vaniAKWVHzUEsAmBfrHG"
python3 tests/verify-events.py
```

## Handback

This is temporary. Once an independent indexer serves current data through the Graph gateway,
compare event records at the same indexed block and switch the app's supported queries back.
The accounting queries still need the original subgraph throughout.
