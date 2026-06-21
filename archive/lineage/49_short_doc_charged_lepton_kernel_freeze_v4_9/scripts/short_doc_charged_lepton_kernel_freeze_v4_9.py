#!/usr/bin/env python3
from __future__ import annotations
import csv, hashlib, json, math
from pathlib import Path

MODULE = Path(__file__).resolve().parents[1]
ROOT = MODULE.parents[0]

def load_json(p: Path):
    with p.open() as f: return json.load(f)

def sha_obj(obj) -> str:
    return hashlib.sha256(json.dumps(obj, sort_keys=True, separators=(',', ':'), ensure_ascii=False).encode()).hexdigest()

# Source constants from short documents, not PDG.
OIB = math.log(2) / (24.0 * math.pi)
L3 = 7
THETA = {'e': math.pi/6, 'mu': math.pi/4, 'tau': math.pi/3}

# Pull prior frozen, non-benchmark traces from modules that already exist in the repo.
v45_path = ROOT/'45_debt9_document_collatz_twinprime_tau_v4_5'/'results'/'document_collatz_twinprime_tau_trace_v4_5.json'
v48_path = ROOT/'48_debt9_charged_lepton_generation_review_v4_8'/'results'/'charged_lepton_generation_review_v4_8.json'
v45 = load_json(v45_path)
v48 = load_json(v48_path)
rows45 = {r['slot']: r for r in v45['rows'] if r['slot'] in ('e','mu','tau')}
rows48 = v48['base_rows']

# Strict short-doc Fij: use OIB from ln2/(24pi), not legacy I0=0.009 and not Formal_SM fitted Ci.
def F_short(src: str, dst: str) -> float:
    return math.exp(OIB * (THETA[dst] - THETA[src]))

# Short-doc spinor/identity holonomy justifies half-action amplitude gate:
# step10: identity invariant uses half-phase; step4: spin-1/2 lifted closure; v4.8 tau_v2 actions were frozen earlier.
def half_action_gate(slot: str) -> float:
    return math.exp(0.5 * (rows48[slot]['tau_v2_action'] - rows48['e']['tau_v2_action']))

kernel_rows = []
for slot in ('e','mu','tau'):
    r45 = rows45[slot]
    f = F_short('e', slot)
    gate = half_action_gate(slot)
    # This is a dimensionless frozen kernel, not a MeV mass prediction.
    kernel_value = r45['composite_document_tau_trace'] * f * gate
    kernel_rows.append({
        'slot': slot,
        'generation': r45['generation'],
        'theta_rad': THETA[slot],
        'theta_source': 'short F_ij S2 interpretation table',
        'tau_doc': r45['tau_doc'],
        'composite_document_tau_trace_v45': r45['composite_document_tau_trace'],
        'origin_class_v45': r45['origin_class'],
        'F_short_e_to_slot_from_OIB': f,
        'tau_v2_action_v48': rows48[slot]['tau_v2_action'],
        'spinor_half_action_gate': gate,
        'short_doc_kernel_value_dimensionless': kernel_value,
        'mass_prediction_claimed': False,
        'benchmark_performed': False,
        'pdg_reference_input_used': False,
        'observed_mass_input_used': False,
    })

ke = next(r for r in kernel_rows if r['slot'] == 'e')['short_doc_kernel_value_dimensionless']
for r in kernel_rows:
    r['short_doc_kernel_ratio_to_e'] = r['short_doc_kernel_value_dimensionless'] / ke if ke else None

kernel = {
    'schema': 'METATIME_SHORTDOC_CHARGED_LEPTON_KERNEL_FREEZE_v4_9',
    'module': '49_short_doc_charged_lepton_kernel_freeze_v4_9',
    'technical_status': 'PASS',
    'formal_status': 'PASS_WITH_STRICT_SHORT_DOC_SOURCE_LEDGER',
    'substantive_status': 'FROZEN_SHORT_DOC_KERNEL_NOT_NUMERIC_CLOSURE',
    'created_utc': '2026-06-21T00:00:00Z',
    'constants': {
        'L3_base': L3,
        'OIB_ln2_over_24pi': OIB,
        'legacy_I0_not_used': 0.009,
        'theta_assignments_rad': THETA,
    },
    'formula_frozen_before_benchmark': {
        'strict_F_short': 'F_ij = exp((ln2/(24*pi))*(theta_j-theta_i))',
        'spinor_half_action_gate': 'G_i = exp(0.5*(tau_v2_action_i - tau_v2_action_e))',
        'kernel': 'K_i = composite_document_tau_trace_v45_i * F_short(e,i) * G_i',
        'mass_conversion_to_MeV': 'not defined in v4.9',
        'benchmark': 'not performed in v4.9'
    },
    'rows': kernel_rows,
    'short_doc_diagnostic': {
        'strict_short_doc_Fij_dynamic_range': {
            'e_to_mu': F_short('e','mu'),
            'e_to_tau': F_short('e','tau'),
            'comment': 'Promille-scale Fij from short S2/OIB kernel cannot by itself supply large charged-lepton hierarchy.'
        },
        'large_F_table_status': 'diagnostic clue only; not promoted because v4.9 does not rederive large charged-lepton F_ij from first principles',
        'debt9_numeric_spectrum': 'OPEN_NOT_CLOSED'
    },
    'taint_ledger': {
        'Vandermonde_charged_lepton_fit': 'DENIED_AS_INPUT',
        'Formal_SM_mass_replay_or_exact_fit': 'DENIED_AS_INPUT',
        'large_document_F_table_from_MetaTheory_appendix': 'DIAGNOSTIC_ONLY_NOT_PROMOTED',
        'electron_unit_anchor': 'NOT_USED_FOR_MASS_CLOSURE_IN_V4_9',
        'PDG_reference_masses': 'NOT_USED',
    },
    'canon_allowed': False,
    'current_promotion': 'DENY_CURRENT',
}
kernel['operator_fingerprint_sha256'] = sha_obj({
    'constants': kernel['constants'],
    'formula': kernel['formula_frozen_before_benchmark'],
    'rows': [{k:v for k,v in r.items() if k not in ('mass_prediction_claimed','benchmark_performed','pdg_reference_input_used','observed_mass_input_used')} for r in kernel_rows],
})

out_json = MODULE/'results'/'short_doc_charged_lepton_kernel_freeze_v4_9.json'
out_csv = MODULE/'results'/'short_doc_charged_lepton_kernel_freeze_v4_9.csv'
out_json.write_text(json.dumps(kernel, indent=2, ensure_ascii=False))
with out_csv.open('w', newline='') as f:
    writer = csv.DictWriter(f, fieldnames=list(kernel_rows[0].keys()))
    writer.writeheader(); writer.writerows(kernel_rows)
print(json.dumps({'status':'PASS','fingerprint':kernel['operator_fingerprint_sha256'],'out':str(out_json)}, indent=2))
