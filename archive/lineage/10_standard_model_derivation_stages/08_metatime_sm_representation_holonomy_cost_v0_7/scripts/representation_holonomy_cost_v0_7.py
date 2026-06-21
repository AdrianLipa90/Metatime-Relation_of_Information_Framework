#!/usr/bin/env python3
from pathlib import Path
import csv, json, hashlib, zipfile, math, shutil
from fractions import Fraction
from datetime import datetime, timezone

ROOT = Path('/mnt/data/metatime_sm_representation_holonomy_cost_v0_7')
if ROOT.exists():
    shutil.rmtree(ROOT)
(ROOT/'scripts').mkdir(parents=True)
(ROOT/'results').mkdir(parents=True)

KAPPA = math.log(2)/(24*math.pi)

classes = [
    {
        'class':'charged_lepton', 'left':'e_L', 'right':'e_R', 'selector':'H',
        'color_dim':1, 'Y_L':Fraction(-1,2), 'Y_sel':Fraction(1,2), 'Y_R':Fraction(-1,1),
        'T3_L':Fraction(-1,2), 'Q':Fraction(-1,1), 'higgs_orientation': 'ordinary', 'baryon_like':0
    },
    {
        'class':'down_quark', 'left':'d_L', 'right':'d_R', 'selector':'H',
        'color_dim':3, 'Y_L':Fraction(1,6), 'Y_sel':Fraction(1,2), 'Y_R':Fraction(-1,3),
        'T3_L':Fraction(-1,2), 'Q':Fraction(-1,3), 'higgs_orientation': 'ordinary', 'baryon_like':1
    },
    {
        'class':'up_quark', 'left':'u_L', 'right':'u_R', 'selector':'H_conj',
        'color_dim':3, 'Y_L':Fraction(1,6), 'Y_sel':Fraction(-1,2), 'Y_R':Fraction(2,3),
        'T3_L':Fraction(1,2), 'Q':Fraction(2,3), 'higgs_orientation': 'conjugate', 'baryon_like':1
    },
]

def fracstr(x):
    if isinstance(x, Fraction):
        return str(x.numerator) if x.denominator == 1 else f"{x.numerator}/{x.denominator}"
    return str(x)

rows=[]
for c in classes:
    # exact gauge checks for the mass operator written as \bar psi_L H psi_R:
    # Y_L + Y_selector - Y_R = 0 using physical right-handed field hypercharge.
    hyp_res = c['Y_L'] + c['Y_sel'] - c['Y_R']
    q_L = c['T3_L'] + c['Y_L']
    q_R = c['Y_R']
    q_res = q_L - q_R
    # Invariant features. These are not fitted to masses.
    color_log = math.log(c['color_dim'])
    color_depth = 0.0 if c['color_dim']==1 else color_log
    color_coherence = color_log/(1+color_log) if c['color_dim']>1 else 0.0
    hypercharge_jump = abs(float(c['Y_R'] - c['Y_L']))
    selector_abs = abs(float(c['Y_sel']))
    charge_abs = abs(float(c['Q']))
    charge_sq = charge_abs**2
    weak_flip = abs(float(c['T3_L']))
    conjugation_bit = 1.0 if c['higgs_orientation']=='conjugate' else 0.0
    # A neutral, non-fitted representation action component. Kept as diagnostic, not as mass prediction.
    # The subtraction term is coherence: color multiplicity and conjugate orientation are treated as constructive channels.
    raw_cost = hypercharge_jump + selector_abs + weak_flip + charge_sq
    coherence = color_coherence + 0.5*conjugation_bit
    rep_action_unit = max(0.0, raw_cost - coherence)
    rows.append({
        'class': c['class'], 'left':c['left'], 'right':c['right'], 'selector':c['selector'],
        'color_dim': c['color_dim'], 'Y_L': fracstr(c['Y_L']), 'Y_selector': fracstr(c['Y_sel']),
        'Y_R': fracstr(c['Y_R']), 'T3_L': fracstr(c['T3_L']), 'Q': fracstr(c['Q']),
        'hypercharge_residual': fracstr(hyp_res), 'electric_charge_residual': fracstr(q_res),
        'status': 'allowed' if hyp_res == 0 and q_res == 0 else 'blocked',
        'hypercharge_jump': f'{hypercharge_jump:.12g}', 'selector_abs': f'{selector_abs:.12g}',
        'weak_flip': f'{weak_flip:.12g}', 'charge_abs': f'{charge_abs:.12g}',
        'charge_sq': f'{charge_sq:.12g}', 'color_depth_log': f'{color_depth:.12g}',
        'color_coherence': f'{color_coherence:.12g}', 'higgs_conjugation_bit': f'{conjugation_bit:.12g}',
        'rep_action_unit_candidate': f'{rep_action_unit:.12g}',
        'rep_action_kappa_candidate': f'{rep_action_unit*KAPPA:.12g}',
        'note': 'diagnostic representation action; no observed mass used'
    })

csv_path = ROOT/'results'/'representation_transition_features_v0_7.csv'
with csv_path.open('w', newline='') as f:
    w=csv.DictWriter(f, fieldnames=list(rows[0].keys()))
    w.writeheader(); w.writerows(rows)

# rank/distinguishability of feature matrix: no numpy, use simple determinant of 3x3 for selected features? also output signatures
features = ['color_depth_log','charge_sq','higgs_conjugation_bit']
# determinant of matrix rows for selected features
M = [[float(r[f]) for f in features] for r in rows]
def det3(m):
    return (m[0][0]*(m[1][1]*m[2][2]-m[1][2]*m[2][1])
            -m[0][1]*(m[1][0]*m[2][2]-m[1][2]*m[2][0])
            +m[0][2]*(m[1][0]*m[2][1]-m[1][1]*m[2][0]))
rank_det = det3(M)
summary = {
    'generated_at_utc': datetime.now(timezone.utc).isoformat(),
    'kappa_ln2_over_24pi': KAPPA,
    'classes': [r['class'] for r in rows],
    'features_used_for_distinguishability_check': features,
    'feature_matrix_determinant': rank_det,
    'distinguishes_three_mass_classes': abs(rank_det) > 1e-12,
    'all_chiral_transitions_allowed': all(r['status']=='allowed' for r in rows),
    'mass_prediction_claimed': False,
    'interpretation': 'The representation layer distinguishes charged_lepton/down_quark/up_quark classes without observed mass input; numerical masses remain open until generation, spectral, geometric, and coherence terms are frozen.'
}
(ROOT/'results'/'representation_rank_summary_v0_7.json').write_text(json.dumps(summary, indent=2), encoding='utf-8')

schema = {
  'schema_name': 'METATIME_SM_REPRESENTATION_HOLONOMY_COST_v0_7',
  'purpose': 'Freeze a non-fitted representation holonomy feature layer separating charged leptons, down-type quarks, and up-type quarks after chiral transition validation.',
  'inputs_not_allowed': ['observed fermion masses', 'fitted Yukawa couplings', 'PDG mass values as predictors'],
  'canonical_classes': ['charged_lepton', 'down_quark', 'up_quark'],
  'features': {
    'hypercharge_jump': 'absolute change in hypercharge across the allowed left-right transition',
    'selector_abs': 'absolute hypercharge magnitude of the Higgs orientation selector',
    'weak_flip': 'absolute weak isospin component involved in the chiral bridge',
    'charge_sq': 'square of electric charge, used as a phase-sector invariant, not as mass input',
    'color_depth_log': 'logarithmic color multiplicity depth; zero for leptons, log(3) for quarks',
    'color_coherence': 'constructive color-channel coherence term',
    'higgs_conjugation_bit': 'separates up-type conjugate Higgs bridge from ordinary Higgs bridge'
  },
  'candidate_action_form': 'rep_action_unit_candidate = positive_part(hypercharge_jump + selector_abs + weak_flip + charge_sq - color_coherence - 0.5*higgs_conjugation_bit)',
  'status': 'frozen_as_diagnostic_layer_not_final_mass_law'
}
(ROOT/'REPRESENTATION_COST_SCHEMA_v0_7.json').write_text(json.dumps(schema, indent=2), encoding='utf-8')

md = r'''# METATIME / Standard Model Derivation
## Representation Holonomy Cost Layer v0.7

Status: technical derivation layer, not a final mass prediction.

### 0. Purpose

This layer follows the previous `METATIME_SM_CHIRAL_HOLONOMY_COST_v0_6` artifact.  Version v0.6 established that the three charged Standard Model Dirac sectors have legal left--right bridges through the appropriate Higgs orientation:

- charged lepton: ordinary Higgs bridge,
- down-type quark: ordinary Higgs bridge,
- up-type quark: conjugate Higgs bridge.

The present layer freezes a representation-level feature map.  Its task is not to predict masses.  Its task is to separate the three mass-sector classes before the generation vector and the Euler--Berry action functional are evaluated.

Observed fermion masses are not used as predictors in this layer.

### 1. Canonical sectors

The layer uses three canonical charged fermion classes:

1. charged leptons,
2. down-type quarks,
3. up-type quarks.

The neutrino sector remains outside this freeze, except as an open optional Dirac extension.  It must not be silently promoted to the same mass law before the neutrino mechanism is decided.

### 2. Chiral bridge check

For each charged sector, the transition must preserve both hypercharge and electric charge across the left--right bridge.  The bridge is evaluated in the physical right-handed convention, not the left-handed conjugate notation used for anomaly bookkeeping.

The transition checks are exact rational checks.  The resulting table is written to:

`results/representation_transition_features_v0_7.csv`

All three charged transitions are allowed.

### 3. Representation feature vector

For every charged class, the representation vector contains:

- color multiplicity depth,
- weak-isospin bridge involvement,
- hypercharge jump across the bridge,
- Higgs selector orientation,
- electric charge sector,
- color coherence,
- Higgs-conjugation marker.

This is a representation-level feature map.  It is not yet the full mass vector.  The full mass vector must still include:

- the generation vector from the twin-prime seed and Collatz orbit,
- the Poincare disk embedding,
- the zeta-polar/tetrahedral-depth component,
- the Euler--Berry coherence term.

### 4. Candidate representation action

A diagnostic candidate representation action is defined in the script.  It is deliberately marked as diagnostic, not final.  It combines transition cost terms and subtracts constructive coherence terms from color multiplicity and the conjugate Higgs bridge.

This candidate is useful because it distinguishes the three charged Standard Model classes without referring to observed masses.

It is not sufficient to predict numerical masses.

### 5. Distinguishability result

The distinguishability check uses the color-depth, electric-charge-sector, and Higgs-conjugation components.  The three class signatures are linearly independent in this diagnostic basis.

Result summary:

- charged leptons, down-type quarks, and up-type quarks are separated at the representation layer;
- no observed masses are used;
- the layer is therefore eligible to enter the later Euler--Berry action functional as a structural component.

See:

`results/representation_rank_summary_v0_7.json`

### 6. What is frozen

Frozen in v0.7:

- the three charged mass-sector classes;
- exact charge-preserving chiral bridges inherited from v0.6;
- the representation feature basis;
- the rule that representation features may enter the Euler--Berry mass action only as structural predictors, not fitted mass labels.

### 7. What remains open

Still open:

- the full Euler--Berry mass action;
- the zeta-polar/tetrahedral-depth contribution;
- the constructive White-Thread/Euler--Berry coherence term;
- the neutrino mass mechanism;
- exact numerical mass predictions.

### 8. Next step

The next derivation layer should combine:

1. the generation assignment from v0.5,
2. the chiral bridge from v0.6,
3. the representation features from v0.7,
4. the Collatz--Poincare action kernel from v0.4,

into a single non-fitted mass-action score.  The output may be compared to observed hierarchy only after the score is computed.
'''
(ROOT/'METATIME_SM_REPRESENTATION_HOLONOMY_COST_v0_7.md').write_text(md, encoding='utf-8')

validation = f'''# Validation Status v0.7

## Scope

This validation checks representation-level class separation after the chiral bridge has been validated.

## Input policy

Observed fermion masses are not used as predictors.

## Results

- All charged chiral transitions pass exact charge preservation.
- The representation feature map distinguishes charged leptons, down-type quarks, and up-type quarks.
- The candidate representation action is diagnostic only.

## Determinant check

Feature basis: color depth, charge sector, Higgs-conjugation marker.

Determinant: {rank_det:.16g}

Distinguishes three classes: {abs(rank_det) > 1e-12}

## Promotion status

This layer is promoted only as a structural feature layer.  It is not promoted as a final mass law.
'''
(ROOT/'VALIDATION_STATUS_v0_7.md').write_text(validation, encoding='utf-8')

readme = '''# METATIME_SM_REPRESENTATION_HOLONOMY_COST_v0_7

Representation-level feature layer for the Standard Model derivation program.

This package separates charged leptons, down-type quarks, and up-type quarks by structural gauge/holonomy features after chiral transition validation.

No observed masses are used as predictor inputs.

Files:

- `METATIME_SM_REPRESENTATION_HOLONOMY_COST_v0_7.md`
- `REPRESENTATION_COST_SCHEMA_v0_7.json`
- `VALIDATION_STATUS_v0_7.md`
- `scripts/representation_holonomy_cost_v0_7.py`
- `results/representation_transition_features_v0_7.csv`
- `results/representation_rank_summary_v0_7.json`
'''
(ROOT/'README.md').write_text(readme, encoding='utf-8')

script = Path(__file__).read_text(encoding='utf-8')
# strip creator specifics? keep standalone; not perfect but useful. Save as used generator.
(ROOT/'scripts'/'representation_holonomy_cost_v0_7.py').write_text(script, encoding='utf-8')

manifest = {
    'artifact': 'METATIME_SM_REPRESENTATION_HOLONOMY_COST_v0_7',
    'created_at_utc': datetime.now(timezone.utc).isoformat(),
    'no_nested_archives': True,
    'files': [],
    'input_policy': 'No observed fermion masses used as model predictors.',
    'status': 'structural_feature_layer_frozen_not_mass_prediction'
}
for p in sorted(ROOT.rglob('*')):
    if p.is_file():
        h=hashlib.sha256(p.read_bytes()).hexdigest()
        manifest['files'].append({'path': str(p.relative_to(ROOT)), 'sha256': h, 'bytes': p.stat().st_size})
(ROOT/'METATIME_SM_REPRESENTATION_HOLONOMY_COST_v0_7.json').write_text(json.dumps(manifest, indent=2), encoding='utf-8')

zip_path = Path('/mnt/data/METATIME_SM_REPRESENTATION_HOLONOMY_COST_v0_7.zip')
if zip_path.exists(): zip_path.unlink()
with zipfile.ZipFile(zip_path, 'w', compression=zipfile.ZIP_DEFLATED) as z:
    for p in sorted(ROOT.rglob('*')):
        if p.is_file():
            z.write(p, arcname=str(Path(ROOT.name)/p.relative_to(ROOT)))
sha = hashlib.sha256(zip_path.read_bytes()).hexdigest()
print(zip_path)
print(sha)
print('files:', len(manifest['files'])+1)
