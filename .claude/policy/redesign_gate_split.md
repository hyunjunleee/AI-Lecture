# 재설계: mathematician-gate → 3개 집중 게이트 분리

> 상태: **구현·라이브 검증 완료**. (step 2~8 적용, hook `py_compile` 통과, lecture07로 3게이트 라이브 실행 검증.)
> 검증 결과: 3게이트 각자 자기 로그만 Read 허용(audit trail 855–860 "X-gate Read whitelisted")·sha256sum만 Bash·digest 바인딩·repair_channel=tex-writer·append-only 전부 hook 강제 확인. **단일 math-gate가 PASS시킨 lecture07에서 8 stall 신규 검출**(read 5·claim 1·model 2), 그 중 BiLSTM/인코더 불일치·Hopfield async/저장패턴은 사용자가 지목한 결함 — 분할의 실증.
> 남은 것: ① `.claude/schemas/{read,claim,model}-gate.schema.json` 생성(선택 — hook `validate_gate`가 실 강제이고 CLAUDE §7.1 표가 문서화하므로 reference용), ② `! rm .claude/agents/mathematician-gate.md`(현재 deprecation stub), ③ lecture07 재빌드로 3 게이트 라이브 검증(§11 체크리스트).
> 이 문서가 구현의 단일 기준이다. 누락·충돌 발견 시 이 문서를 먼저 갱신한다.

---

## 1. 배경·동기 (왜 분리하는가)

단일 `mathematician-gate`가 한 번의 백지상태 순차 독해로 §6.1~§6.8 **8개 차원**(이름바인딩 · load-bearing 주장 · 무대 · 계산 적법성 · 누출 ×2 · 교과서 구조 · 모델 완결성)을 *동시에* 점검한다. 실측상 이 부하가 과했다 — 서로 다른 차원이 반복해서 새어나갔다:

| 놓친 결함 | 차원 | 통과한 iter | 잡힌 계기 |
|---|---|---|---|
| f_t "완화"의 무근거 전제 | 주장(claim) | iter1·iter3 | §6.1a #5 강화 |
| BiLSTM/인코더 §4↔§5 불일치 | 모델 완결(§2.9) | iter4·iter5 | §6.8 추가 |
| §2.6A-5·claim_id 누출 | 누출 | iter1·iter2 | §6.5/6.6 검출기 |

**근본 원인**: ① 한 번의 독해로 8개 병렬 점검 시 주의 분산, ② 백지상태 억제 자체가 무거운데 juggling이 겹치면 auto-fill 반사 복귀, ③ 사양서 §8이 이미 "기계 추출 인벤토리 + 역할 분리 최종 패스"로 멀티패스를 함의, ④ 연속 독해(흐름)·적대적 반박(주장)·구조 완결성(모델)은 심리적으로 다른 렌즈.

**해법**: 연속 독해가 *필요한* 부분만 한 reader로 남기고, 표적 분석(주장·모델)을 독립 에이전트로 분리. perspective-diverse verification — 중복이 아니라 *다른 렌즈*가 더 많이 잡는다.

---

## 2. 설계 원칙 (불변)

- **3 게이트 모두 백지상태**: 각자 `output/lectureNN.tex`와 *자기 자신의* gate log만 Read(hook 강제). theory.md·typeset·spec·서로의 로그 차단. AI 지식 끄고 지면만 본다.
- **매 iteration 백지 재독해**: 이전 PASS에 기대지 않는다.
- **모든 stall → `repair_channel="tex-writer"`** (hook 강제). 자료조사 필요 판단은 tex-writer 단일(§5.5).
- **독립 append-only 로그**: 게이트별 별도 파일 → 병렬 실행 시 write 충돌 없음, 소유권 단순.
- **완료 = 3 게이트 전부 현재 digest 바인딩 PASS** (기존 단일 PASS를 3-PASS로 교체).
- 기존 hook 불변식(append-only prefix·schema·digest 일치·fail-closed·repair_channel) 전부 유지.

---

## 3. 3-게이트 구조

| 게이트 | 한 줄 책임 | 흡수한 기존 §6.x | 감사 모드 | 출력 |
|---|---|---|---|---|
| **read-gate** | 무정지 순차 독해 — 이름·적형·흐름·누출 | §6.1(A)(B)(C) · §6.5 스캐폴딩 누출 · §6.6 claim_id 누출 · §6.7 교과서 구조/브릿지/파편화/메타침입 | 처음→끝 *한 번의 연속 백지 독해* (실제 독자가 하는 것) | `output/read_gate_NN.jsonl` |
| **claim-gate** | load-bearing 주장 적대적 감사 | §6.1a 5테스트(자동채움·지우기·선언≠논증·special↛general·정당화안된전제) | *주장만 표적* — 비교·인과·양상·평가·기제·도입동기·유의성 주장을 열거하고 각각 반박 시도 | `output/claim_gate_NN.jsonl` |
| **model-gate** | 구체 모델·계산 완결성 | §6.2 무대/공간 정착 · §6.3 §2.16 4요소·해석학적 적법성 · §6.8 객체-before-부분/도메인용어/목적-before-메커니즘/아키텍처 정합/§2.11-9 술어 | *정의된 모델·객체·2줄+ 계산 블록만 표적* | `output/model_gate_NN.jsonl` |

공통(3 게이트 모두 def에 포함): 백지상태 격리, 매 iter 재독해, repair_channel=tex-writer, 기계 추출 전수화(§8), JSONL append 규칙, digest 절차.

도구: `Read, Write, Bash, Glob` (각 게이트). Web 금지. Bash는 `sha256sum`만.

---

## 4. 전체 영향 맵 (flow-by-flow — 깐깐한 체크)

### 4.1 `.claude/hooks/pipeline_policy.py` (원본 정책)

| 위치 | 현재 | 변경 |
|---|---|---|
| `WRITE_OWNERS` | `("output/gate_log_[0-9][0-9].jsonl", "mathematician-gate")` | 3 항목으로 교체: `read_gate_NN`→read-gate, `claim_gate_NN`→claim-gate, `model_gate_NN`→model-gate. (구 `gate_log_NN`는 **owner 제거** → 누구도 못 씀 = lecture07 기존 로그 동결.) |
| `MATH_READ_RE` + `handle_read` | mathematician-gate만 tex+gate_log로 제한 | **GATE_READ 맵**으로 일반화: `{read-gate: read_gate_NN, claim-gate: claim_gate_NN, model-gate: model_gate_NN}`. 각 게이트는 `output/lectureNN.tex` + *자기* 로그만 Read 허용, 그 외 deny. |
| `validate_math` | 단일 math 스키마 검증 | **3 검증기**(또는 schema_version으로 분기하는 1 함수). 공통: lecture==NN·iter≥1·verdict·stall_count==len·stall 필드·**repair_channel=tex-writer 강제**·PASS면 stall 0·global_checks no-false·revision_directives·evidence. 차이: schema_version·게이트별 global_checks 키·stall 필수 필드(아래 §7). |
| `handle_bash` | `agent in {mathematician-gate, literature-gate}: sha256sum only` | `{read-gate, claim-gate, model-gate, literature-gate}`로 확장. |
| `is_gate()` | `gate_log\|literature_gate` | `read_gate\|claim_gate\|model_gate\|literature_gate` 추가. (구 `gate_log`도 인식 유지 → orchestrator-deny·sha256sum 허용; owner만 없음.) |
| `check_sha` | gate 로그 sha256sum 허용 | `is_gate` 갱신으로 자동 반영. 게이트는 lecture_tex·typeset_report(+자기로그) sha256sum — 전부 이미 허용. |

핵심 불변: orchestrator(unknown)의 게이트 로그 직접 쓰기 deny(`is_gate`), digest 일치 검사, append-only prefix — 3 로그 모두 동일 적용.

### 4.2 `.claude/hooks/pipeline_policy_main_free.py` (wrapper)

| 위치 | 변경 |
|---|---|
| `GATE_LOG_RE` | `(?:gate_log\|literature_gate)` → `(?:gate_log\|literature_gate\|read_gate\|claim_gate\|model_gate)`. orchestrator의 3 새 로그 직접 쓰기를 carve-out(원본 위임 → deny). |

### 4.3 `.claude/agents/`

- **삭제(또는 deprecated)**: `mathematician-gate.md` — 3 게이트가 대체. 내용은 분배(§3 표).
- **신설**: `read-gate.md`, `claim-gate.md`, `model-gate.md`. 각 frontmatter `tools: Read, Write, Bash, Glob`, `model: opus`, `permissionMode: dontAsk`. 공통 본문(백지·매iter·repair_channel·digest 절차·JSONL 규칙) + 게이트별 감사 원칙.

### 4.4 `.claude/settings.json`

- `allow`에 `Agent(read-gate)`·`Agent(claim-gate)`·`Agent(model-gate)` 추가, `Agent(mathematician-gate)` 제거. `Write(output/gate_log_*.jsonl)` → 3 로그 패턴 추가(또는 광역 `Write(**)`가 커버하나 명시 권장).

### 4.5 `CLAUDE.md`

| 절 | 변경 |
|---|---|
| §1 에이전트 표 | math-gate 1행 → read/claim/model 3행. |
| §1.1 파일 소유권 | `gate_log_*` 1행 → `read_gate_*`·`claim_gate_*`·`model_gate_*` 3행. |
| §2 파일 명명 | `read_gate_{NN}.jsonl` 등 3개 추가. |
| §3 파이프라인 | step 6 (math-gate) → **6. read-gate + claim-gate + model-gate (병렬)**, 각 required PASS. |
| §5.3 분기 | "math gate FAIL → tex-writer" → "세 게이트 중 하나라도 FAIL → 그 stall 전부 tex-writer". |
| §6 invalidation | `lecture.tex 변경 → mathematician-gate PASS 무효` → 세 게이트 PASS 무효. |
| §7.1 schema | math 스키마 → 3 스키마(§7). |
| §8 round banner | "최근 math gate" → read/claim/model 3줄. |
| §10 완료조건 C | "latest mathematician-gate PASS" → "latest read/claim/model gate **전부** PASS, current lecture.tex(+typeset_report) digest 일치". |
| §0.3 | 분리 서술 갱신(내부 수학 = 3 게이트). |

### 4.6 `.claude/schemas/`

- `math-gate.schema.json` → `read-gate.schema.json`·`claim-gate.schema.json`·`model-gate.schema.json`(또는 공통+분기). hook의 `validate_*`와 일치.

### 4.7 typeset-checker (final mode)

- §6 final mode가 `sha256sum output/gate_log_NN.jsonl output/literature_gate_NN.jsonl` → `read_gate`·`claim_gate`·`model_gate`·`literature_gate` 4개 로그 digest 기록으로 변경. §7 보고 템플릿의 `math_gate_log` 항목도 3개로.

### 4.8 audit log (`pipeline_policy_main_free.py` 계측)

- 변경 불필요(agent·tool·decision을 기록하므로 새 게이트도 자동 기록). 단 `is_gate_log_mutation`/`GATE_LOG_RE`가 3 로그를 포함하면 carve-out 일관.

---

## 5. 새 파이프라인 흐름

```text
... 5. typeset-checker (round) → typeset_check_NN.md PASS
6. read-gate ∥ claim-gate ∥ model-gate   (병렬, 각 lectureNN.tex 감사)
   - 각 output/{read,claim,model}_gate_NN.jsonl append
   - required: 세 게이트 모두 current lecture.tex digest 바인딩 PASS
   - 하나라도 FAIL → 그 stall(전부 repair_channel=tex-writer) → tex-writer
       → lecture.tex 변경 → typeset부터 재시작 (§6 invalidation)
7. literature-gate (lecture mode)   [변경 없음]
8. typeset-checker (final)          [final이 3 로그 digest 기록]
```

**invalidation 추가**: `lecture.tex 변경 → read/claim/model gate PASS 전부 무효`. `typeset_check_NN.md 변경 → (각 게이트가 typeset_report를 inputs에 바인딩하면) 무효`.

**완료조건 C(신)**: latest read-gate PASS ∧ latest claim-gate PASS ∧ latest model-gate PASS, 셋 다 current `lecture.tex`(+`typeset_check_NN.md`) digest와 일치.

---

## 6. 게이트 로그 inputs 바인딩 (설계 결정)

각 게이트 로그 `inputs`:
```json
"inputs": {
  "lecture_tex": {"path":"output/lectureNN.tex","sha256":"..."},
  "typeset_report": {"path":"output/typeset_check_NN.md","sha256":"..."}
}
```
- **theory_md 드롭**: 게이트는 백지상태(theory를 안 읽음)이고, 내부 수학 판정은 lecture.tex에만 의존한다. theory.md 변경은 tex-writer 재집필 → lecture.tex 변경으로 전이 무효화되므로 직접 바인딩 불요. (구 math-gate는 theory_md를 바인딩했으나 이는 잉여였음.)
- typeset_report 유지: 감사한 tex가 *컴파일된 버전*임을 묶는다. (drop도 가능 — 미해결 결정 §9.)

---

## 7. JSONL 스키마 (3종)

공통 골격:
```json
{"schema_version":"<gate>-v1","lecture":"NN","iter":1,
 "inputs":{"lecture_tex":{...},"typeset_report":{...}},
 "verdict":"PASS|FAIL","stall_count":0,
 "sections":[{"name":"...","status":"PASS|FAIL","stalls":[...]}],
 "global_checks":{...},"revision_directives":[...],
 "evidence":{"audited_sections":["..."],"note":"..."}}
```
stall 공통 필수(hook `check_stall`): `stall_id·loc·why·fix·repair_channel(=tex-writer)·canonical_key`.

| 게이트 | schema_version | global_checks 키 | stall 추가 필수 |
|---|---|---|---|
| read-gate | `read-gate-v1` | `names_bound · expressions_wellformed · claims_follow · no_scaffolding_leak · no_claimid_leak · textbook_flow` | `principle∈{A,B,C}` |
| claim-gate | `claim-gate-v1` | `auto_fill_checked · erase_test · declaration_vs_argument · scope_match · premise_justified` | `claim_text · trigger_type · failed_test` |
| model-gate | `model-gate-v1` | `objects_before_parts · domain_terms_defined · purpose_before_mechanism · architecture_consistent · compute_decl_4elem · analytic_legality · predicates_classified` | `object_or_block · principle∈{A,B,C}` |

hook `validate_*`: schema_version·inputs·verdict·stall_count·repair_channel=tex-writer·PASS면 stall0&no-false·evidence.audited_sections(read/model) 검사. (claim-gate evidence는 audited_claims 등.)

---

## 8. 마이그레이션

- **lecture07 기존 `output/gate_log_07.jsonl`**(math-gate 5 iter): 동결(owner 제거 → 불변 history). 삭제하지 않음. 새 빌드는 3 새 로그를 만든다.
- 기존 `gate_log_*` 패턴은 hook `is_gate`에 남겨 orchestrator-deny·sha256sum 인식 유지.
- 첫 적용 강의(lecture07 재빌드 또는 다음 강의)에서 3 로그 라이브 검증.

### 8.1 게이트 로그 append 메커니즘 (lecture07 완주 중 추가)

긴 누적 로그(한국어+LaTeX 수 KB)는 LLM이 exact-prefix를 바이트-정확 재현 불가 → append 막힘(read-gate가 PASS 판정해도 기록 실패). hook이 세 방식을 *동일 검증*하도록 확장:
- **(a) 전체 Write append**(기존) · **(b) Edit-append**(마지막 줄 짧은 말미만 `old_string`으로 재현 → hook이 결과 파일을 재구성해 prefix·1줄·schema·digest 동일 검증) · **(c) 라운드 파일** `output/{gate}_gate_NN_rRR.jsonl`(신규 단일-라인, prefix 불필요).
- hook 변경: `gate_append_content`(Write/Edit 분기) + WRITE_OWNERS(glob)·validate_gate/validate_lit·handle_write·handle_read·is_gate·wrapper `GATE_LOG_RE`에 `(?:_r\d+)?` 추가.
- **Edit 범위 제한(명시 가드)**: 블랭크 게이트(read/claim/model)는 hook이 Write·Edit를 *자기 로그(베이스·라운드)로만* 허용 — 타 로그·`.tex`·기타 일절 불가. literature-gate는 소유권으로 동일하게 confined.
- **주의**: 에이전트 도구 집합은 *등록 시 고정* — Edit는 def frontmatter에 미리 있어야 다음 세션부터 작동(세션 도중 추가는 미반영). 그래서 lecture07 완주 자체는 (c) 라운드 파일로 진행했다.
- 문서: CLAUDE.md §7(3 방식)·§2(라운드 명명), 각 게이트 def §2/§8, literature-gate frontmatter에 Edit 추가.

---

## 9. 미해결 설계 결정 (구현 전 확정)

1. **병렬 vs 순차**: 3 게이트를 한 메시지로 병렬 dispatch(빠름, 독립 로그라 충돌無) 권장. 순차도 가능.
2. **typeset_report 바인딩 유지 vs 드롭**: 유지(컴파일 버전 묶기) 권장.
3. **mathematician-gate.md 삭제 vs deprecated 보존**: 삭제 후 이 문서가 분배 기록 권장.
4. **스키마 파일 3분리 vs 공통+분기**: hook 가독성상 3분리 권장.
5. **claim-gate read 격리**: tex만(theory 차단) 유지 — "지면에서 정당화되는가"가 본질이므로.

---

## 10. 구현 순서 (mid-flight 파손 방지)

순서가 중요하다 — hook과 agent를 동시에 바꾸지 않으면 중간 상태가 deny를 유발한다.

1. **이 설계 문서** (현재).
2. 신규 3 agent def 작성(`read/claim/model-gate.md`) — 아직 hook이 모르면 settings allow도 없어 dispatch 불가하나 파일 작성은 무해.
3. **hook 한 번에**: `pipeline_policy.py`(WRITE_OWNERS·GATE_READ·validate_*·handle_bash·is_gate) + `pipeline_policy_main_free.py`(GATE_LOG_RE) 동시 수정 → `py_compile` 검증.
4. `settings.json` Agent allow 3개 추가.
5. `CLAUDE.md`(§1·1.1·2·3·5.3·6·7.1·8·10·0.3) 일괄.
6. `.claude/schemas/` 3종.
7. typeset-checker final mode 3 로그 digest.
8. `mathematician-gate.md` 삭제.
9. lecture07 재빌드로 라이브 검증(read/claim/model 3 PASS until).

각 단계 후 `py_compile`(hook)·구조 점검. **3·5는 breaking이므로 그 사이에 게이트를 dispatch하지 않는다.**

---

## 11. 검증 체크리스트 (구현 완료 판정)

- [ ] hook `py_compile` 통과(양 파일).
- [ ] 3 게이트 각각 자기 로그만 Read, 타 로그·theory·spec Read시 deny (라이브).
- [ ] 3 게이트 sha256sum 외 Bash deny.
- [ ] orchestrator의 3 로그 직접 Write deny(wrapper carve-out → 원본 deny).
- [ ] 잘못된 repair_channel(≠tex-writer) stall Write deny.
- [ ] digest 불일치 시 Write deny.
- [ ] 병렬 dispatch 시 3 로그 각각 append-only 유지(충돌無).
- [ ] CLAUDE.md 완료조건 C가 3-PASS로, invalidation이 3 게이트로.
- [ ] typeset final이 3 로그 digest 기록.
- [ ] mathematician-gate 잔존 참조 0(agent registry·CLAUDE·schemas·typeset).
