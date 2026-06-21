#!/usr/bin/env python3
from __future__ import annotations
import csv, json, math, statistics, hashlib
from pathlib import Path

BENCHMARK_MEV = {
    'proton': 938.2720813,
    'neutron': 939.5654133,
    'lambda': 1115.683,
    'sigma_plus': 1189.37,
    'sigma_zero': 1192.642,
    'xi_zero': 1314.86,
    'omega_minus': 1672.45,
    'pion_plus': 139.57039,
    'kaon_plus': 493.677,
}

EXPECTED_V59_FINGERPRINT = '4b7e39882f06ce105c5e12b7c068165973baca4624815fce505ed445ca06fbe9'
MODULE = '60_hadron_ratio_benchmark_v6_0A'
CREATED_UTC = '2026-06-21T09:00:00Z'


def sha256_text(s: str) -> str:
    return hashlib.sha256(s.encode('utf-8')).hexdigest()


def median(xs):
    return statistics.median(xs) if xs else None


def pearson(x, y):
    n=len(x)
    if n < 2:
        return None
    mx=sum(x)/n; my=sum(y)/n
    vx=sum((a-mx)**2 for a in x); vy=sum((b-my)**2 for b in y)
    if vx == 0 or vy == 0:
        return None
    return sum((a-mx)*(b-my) for a,b in zip(x,y))/math.sqrt(vx*vy)


def rankdata(vals):
    pairs=sorted((v,i) for i,v in enumerate(vals))
    ranks=[0.0]*len(vals)
    k=0
    while k < len(pairs):
        j=k
        while j+1 < len(pairs) and pairs[j+1][0] == pairs[k][0]:
            j += 1
        r=(k+1+j+1)/2
        for _,i in pairs[k:j+1]:
            ranks[i]=r
        k=j+1
    return ranks


def spearman(x, y):
    return pearson(rankdata(x), rankdata(y))


def metrics(rows, mode, state_filter=None):
    selected = [r for r in rows if r['hadron'] != 'proton' and (state_filter is None or r['state_class'] == state_filter)]
    errors = [r[f'{mode}_absolute_relative_error'] for r in selected]
    return {
        'count': len(selected),
        'mean_absolute_relative_error': sum(errors)/len(errors) if errors else None,
        'median_absolute_relative_error': median(errors),
        'max_absolute_relative_error': max(errors) if errors else None,
        'within_21pct_count': sum(1 for e in errors if e <= 0.21),
        'within_21pct_fraction': (sum(1 for e in errors if e <= 0.21)/len(errors)) if errors else None,
    }


def correlations(rows, mode, state_filter=None):
    selected = [r for r in rows if state_filter is None or r['state_class'] == state_filter]
    xs = [r[f'{mode}_ratio_prediction'] for r in selected]
    ys = [r['benchmark_mass_ratio_to_proton'] for r in selected]
    logx = [math.log(max(v, 1e-300)) for v in xs]
    logy = [math.log(max(v, 1e-300)) for v in ys]
    return {
        'pearson_ratio': pearson(xs, ys),
        'spearman_ratio': spearman(xs, ys),
        'pearson_log_ratio': pearson(logx, logy),
        'spearman_log_ratio': spearman(logx, logy),
    }


def main():
    root = Path(__file__).resolve().parents[2]
    v59_path = root/'59_debt9_prime_product_hadron_scale_candidate_v5_9/results/prime_product_hadron_scale_candidate_v5_9.json'
    source = json.loads(v59_path.read_text(encoding='utf-8'))
    fp = source.get('formula_fingerprint_sha256')
    if fp != EXPECTED_V59_FINGERPRINT:
        raise SystemExit(f'v5.9 fingerprint mismatch: {fp}')

    base_mass = BENCHMARK_MEV['proton']
    rows = []
    for r in source['rows']:
        h = r['hadron']
        if h not in BENCHMARK_MEV:
            continue
        carrier = float(r['dimensionless_score_relative_to_proton_structural_base'])
        mass_ratio = BENCHMARK_MEV[h] / base_mass
        direct = carrier
        inverse = 1.0 / carrier if carrier != 0 else float('inf')
        row = {
            'hadron': h,
            'composition': r['composition'],
            'state_class': r['state_class'],
            'v59_carrier_ratio': carrier,
            'benchmark_mass_mev': BENCHMARK_MEV[h],
            'benchmark_mass_ratio_to_proton': mass_ratio,
            'direct_ratio_prediction': direct,
            'direct_absolute_relative_error': abs(direct - mass_ratio)/mass_ratio,
            'inverse_ratio_prediction': inverse,
            'inverse_absolute_relative_error': abs(inverse - mass_ratio)/mass_ratio,
            'benchmark_used_only_after_freeze': True,
            'mev_prediction_claimed': False,
            'absolute_mev_scale_derived': False,
        }
        rows.append(row)

    result = {
        'schema': 'METATIME_DEBT9_HADRON_RATIO_BENCHMARK_V6_0A',
        'module': MODULE,
        'created_utc': CREATED_UTC,
        'source_module': '59_debt9_prime_product_hadron_scale_candidate_v5_9',
        'source_formula_fingerprint_sha256': fp,
        'technical_status': 'PASS',
        'formal_status': 'PASS_SEALED_RATIO_BENCHMARK_WITH_BOUNDARIES',
        'substantive_status': 'DIRECT_CARRIER_FAILS_INVERSE_BARYON_ORIENTATION_PARTIAL_SIGNAL_ABSOLUTE_SCALE_OPEN',
        'debt9_numeric_spectrum': 'OPEN_NOT_CLOSED',
        'canon_allowed': False,
        'current_promotion': 'DENY_CURRENT',
        'mass_prediction_claimed': False,
        'absolute_mev_scale_derived': False,
        'benchmark_performed': True,
        'benchmark_scope': 'ratio_to_proton_after_v5_9_formula_freeze',
        'confinement_residual_budget': 0.21,
        'rows': rows,
        'metrics': {
            'direct_all_nonproton': metrics(rows, 'direct'),
            'inverse_all_nonproton': metrics(rows, 'inverse'),
            'direct_baryon_nonproton': metrics(rows, 'direct', 'baryon_triplet'),
            'inverse_baryon_nonproton': metrics(rows, 'inverse', 'baryon_triplet'),
            'direct_meson_nonproton': metrics(rows, 'direct', 'meson_pair'),
            'inverse_meson_nonproton': metrics(rows, 'inverse', 'meson_pair'),
        },
        'correlations': {
            'direct_baryons': correlations(rows, 'direct', 'baryon_triplet'),
            'inverse_baryons': correlations(rows, 'inverse', 'baryon_triplet'),
            'direct_all': correlations(rows, 'direct'),
            'inverse_all': correlations(rows, 'inverse'),
        },
        'decision': {
            'direct_v59_carrier_as_mass_ratio': 'FAIL',
            'inverse_baryon_orientation': 'PARTIAL_STRUCTURAL_SIGNAL_NOT_PROMOTED',
            'meson_pair_sector': 'SEPARATE_BOUNDARY_REQUIRED',
            'absolute_mev_scale': 'NOT_DERIVED',
            'debt9_closure': 'DENIED',
        },
        'interpretation': [
            'The v5.9 carrier is clean and frozen, but its direct orientation does not reproduce hadron mass ratios.',
            'The inverse orientation gives a partial baryon-ordering signal, especially for Lambda/Sigma/Xi; it still fails neutron and Omega and is not a closure.',
            'Mesons cannot be mixed into the same scoring rule as baryon triplets without a separate pair-state binding operator.',
            'Small errors are not rejected by principle; promotion is denied only where provenance or scale derivation is missing.',
        ],
    }
    result['benchmark_fingerprint_sha256'] = sha256_text(json.dumps({k: result[k] for k in ['source_formula_fingerprint_sha256','benchmark_scope','rows','metrics','correlations','decision']}, sort_keys=True, ensure_ascii=False))

    outdir = root/MODULE/'results'
    outdir.mkdir(parents=True, exist_ok=True)
    (outdir/'hadron_ratio_benchmark_v6_0A.json').write_text(json.dumps(result, indent=2, ensure_ascii=False), encoding='utf-8')
    with (outdir/'hadron_ratio_benchmark_v6_0A.csv').open('w', newline='', encoding='utf-8') as f:
        fields = list(rows[0].keys()) if rows else []
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader(); w.writerows(rows)
    print(json.dumps({'status':'PASS','benchmark_fingerprint_sha256':result['benchmark_fingerprint_sha256']}, indent=2))

if __name__ == '__main__':
    main()
