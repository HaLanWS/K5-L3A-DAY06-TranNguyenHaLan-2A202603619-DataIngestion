import json

with open('starter/results/benchmark_trace.json', encoding='utf-8') as f:
    data = json.load(f)

meta = data['metadata']
print('=== METADATA & RESOURCE USAGE ===')
print(f"Model: {meta['embedding_model']} ({meta['dimensions']} dims)")
print(f"Store: {meta['vector_store']}")
print(f"Strategy A: {meta['chunk_counts']['A']} chunks, ingest time: {meta['ingest_time_seconds']['A']}s")
print(f"Strategy B: {meta['chunk_counts']['B']} chunks, ingest time: {meta['ingest_time_seconds']['B']}s")
print(f"Strategy C: {meta['chunk_counts']['C']} chunks, ingest time: {meta['ingest_time_seconds']['C']}s")

def summarize_split(results, split_name):
    subset = [r for r in results if r['split'] == split_name]
    total = len(subset)
    hit1 = sum(1 for r in subset if r['hit_at_1'])
    hit3 = sum(1 for r in subset if r['hit_at_3'])
    
    # filter compliance
    filter_subset = [r for r in subset if r['has_filter']]
    compliant = sum(1 for r in filter_subset if r['filter_compliant']) if filter_subset else 0
    filter_rate = f"{compliant}/{len(filter_subset)}" if filter_subset else "N/A"
    
    return {
        'total': total,
        'hit1': f"{hit1}/{total} ({hit1/total*100:.1f}%)",
        'hit3': f"{hit3}/{total} ({hit3/total*100:.1f}%)",
        'filter_compliance': filter_rate
    }

print('\n=== BENCHMARK RETRIEVAL METRICS ===')
for strat_key, strat_name in [('results_A', 'Strategy A (Fixed)'), ('results_B', 'Strategy B (Structure)'), ('results_C', 'Strategy C (Filtered)')]:
    dev_stat = summarize_split(data[strat_key], 'dev')
    test_stat = summarize_split(data[strat_key], 'test')
    print(f"\n[{strat_name}]")
    print(f"  Dev (15 qs):  Hit@1 = {dev_stat['hit1']} | Hit@3 = {dev_stat['hit3']} | Filter Compliance = {dev_stat['filter_compliance']}")
    print(f"  Test (5 qs):  Hit@1 = {test_stat['hit1']} | Hit@3 = {test_stat['hit3']} | Filter Compliance = {test_stat['filter_compliance']}")
