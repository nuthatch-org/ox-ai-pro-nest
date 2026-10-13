> **Stood down, 13 October 2026.**
>
> Lodestar is offline, and so is everything else I was running for The Graph.
>
> I answered 55 support issues, wrote over 50 forum posts, built and tested over 100 open repos, and helped subgraph devs, indexers and Lodestar users nearly every day. Alone, and unpaid.
>
> Every ask for funding, from a tiny grant ([GIP-0090](https://forum.thegraph.com/t/gip-0090-community-allocation-of-0-1-of-issuance-to-the-nights-watch/7083/2)) to part-time work for the Foundation, was met with hostility. I cant keep going without funding.
>
> To follow my work: [nuthatch-indexer.com](https://nuthatch-indexer.com/)

---

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
./nuthatch dev --dir . --listen 127.0.0.1:8288 --seal-direct --window 2000 --poll-interval 5m --no-admin
```

GraphQL is at `/subgraphs/id/QmbzwJnre963f9wT9VCJPede69vaniAKWVHzUEsAmBfrHG`.
Wait for `/ready` to report ready and a small lag before relying on current event history.
RPC credentials belong in the environment, never in the nest.

## Verification

`tests/verify-events.py` independently decodes raw Polygon logs and compares each exposed field with the GraphQL endpoint. The initial 100,000-block sample matched 2,450 records without differences. A recent sample matched another 962 records, including 102 campaign payouts. A monthly-snapshot block matched one snapshot. All 3,413 comparisons and accounting-query refusal checks passed. Deposit has no rows in the indexed history; its values have not had a live-data comparison.

```sh
export NEST_ENDPOINT="https://subgraphs.nuthatch-indexer.com/subgraphs/id/QmbzwJnre963f9wT9VCJPede69vaniAKWVHzUEsAmBfrHG"
python3 tests/verify-events.py
```

## Handback

This is temporary. Once an independent indexer serves current data through the Graph gateway,
compare event records at the same indexed block and switch the app's supported queries back.
The accounting queries still need the original subgraph throughout.
