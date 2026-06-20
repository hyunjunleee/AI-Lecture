# AI 28강 — source-fidelity 이론 파이프라인 오케스트레이터

이 프로젝트는 강의 이론 PDF를 만들기 위한 Claude Code agent pipeline이다. 목표는 다음 세 가지를 동시에 만족하는 것이다.

1. 문헌 주장을 한 줄 요약에서 임의로 재구성하지 않는다.
2. LaTeX 문서는 처음부터 끝까지 무정지 순차 독해 가능해야 한다.
3. PASS 판정은 현재 파일 digest에 묶여야 하며 stale PASS를 허용하지 않는다.

## 0. 핵심 원칙

### 0.1 Prompt is not enforcement

프롬프트 지시는 agent가 무엇을 시도할지를 정한다. 실제 실행 경계는 다음 계층이 강제한다.

```text
subagent tools
+ .claude/settings.json permissions
+ .claude/hooks/pipeline_policy.py PreToolUse hook
+ optional OS sandbox/container
```

이 파이프라인에서 hook은 optional hardening이 아니라 required enforcement layer다.

### 0.2 PASS is about current inputs

`PASS` 문자열만으로 완료하지 않는다. 각 PASS log가 현재 입력 파일들의 sha256과 일치해야 한다.

### 0.3 Source fidelity와 internal math를 분리한다

```text
literature-gate     = 원문 ↔ theory.md ↔ lecture.tex source-fidelity 감사
mathematician-gate  = lecture.tex 내부 수학 전수 감사
```

`mathematician-gate`는 웹 검색으로 자신의 멈춤을 해소하지 않는다. 문헌 원문 확인은 `literature-gate` 또는 `researcher`/`theory-curator` 쪽으로 보낸다.

---

## 1. 에이전트 구성

| 에이전트 | 모델 | 역할 | 주요 산출물 | 웹 | Bash |
|---|---:|---|---|---:|---:|
| `researcher` | sonnet | 넓은 자료조사, source registry, 후보 claim 수집 | `work/lectureNN_research.md` | 예 | 아니오 |
| `theory-curator` | opus | 본문에 실제 사용할 claim-level evidence dossier 작성 | `work/lectureNN_theory.md` | 예 | 아니오 |
| `literature-gate` | opus | 원문-source fidelity 감사 | `output/literature_gate_NN.jsonl` | 예 | hash-only |
| `tex-writer` | sonnet | `theory.md` 기반 LaTeX 집필·재집필 | `output/lectureNN.tex` | 아니오 | 아니오 |
| `typeset-checker` | haiku | 기계적 조판·컴파일·pdftotext·preview | `output/typeset_check_NN.md`, pdf/txt | 아니오 | 제한적 |
| `mathematician-gate` | opus | 내부 수학 전수 감사 | `output/gate_log_NN.jsonl` | 아니오 | hash-only |

### 1.1 Agent별 파일 소유권

| 파일 패턴 | 유일 작성자 |
|---|---|
| `work/lecture*_research*.md` | `researcher` |
| `work/lecture*_theory*.md` | `theory-curator` |
| `output/literature_gate_*.jsonl` | `literature-gate` |
| `output/lecture*.tex` | `tex-writer` |
| `output/typeset_check_*.md` | `typeset-checker` |
| `output/final_pdftotext_check_*.md` | `typeset-checker` |
| `output/gate_log_*.jsonl` | `mathematician-gate` |

`spec/**`, `template/**`, `.claude/**`는 agent가 수정하지 않는다.

---

## 2. 파일 명명 규칙

`NN`은 2자리 강의 번호다. 예: 11강 → `11`.

```text
work/lecture{NN}_research.md
work/lecture{NN}_research_supplement_{RR}.md
work/lecture{NN}_theory.md
work/lecture{NN}_theory_supplement_{RR}.md
output/lecture{NN}.tex
output/lecture{NN}.pdf
output/lecture{NN}.log
output/lecture{NN}.txt
output/lecture{NN}_final.txt
output/typeset_check_{NN}.md
output/typeset_check_{NN}_round{RR}.md
output/final_pdftotext_check_{NN}.md
output/gate_log_{NN}.jsonl
output/literature_gate_{NN}.jsonl
output/build/lecture{NN}_round{RR}/
output/preview/lecture{NN}_round{RR}/
```

---

## 3. 기본 파이프라인

N강 요청을 받으면 아래 순서로 실행한다.

```text
1. researcher
   input: spec/*
   output: work/lectureNN_research.md

2. theory-curator
   input: work/lectureNN_research.md + spec/*
   output: work/lectureNN_theory.md

3. literature-gate, mode=dossier
   input: work/lectureNN_research.md + work/lectureNN_theory.md + 원문
   output append: output/literature_gate_NN.jsonl
   required: current research/theory digest에 묶인 PASS

4. tex-writer
   input: spec/* + template/* + research.md + theory.md + latest gate directives
   output: output/lectureNN.tex

5. typeset-checker, mode=round RR
   input: output/lectureNN.tex
   output: output/typeset_check_NN_roundRR.md + output/typeset_check_NN.md + pdf/log/txt/preview
   required: PASS

6. mathematician-gate
   input: output/lectureNN.tex + work/lectureNN_theory.md + output/typeset_check_NN.md
   output append: output/gate_log_NN.jsonl
   required: current lecture/theory/typeset digest에 묶인 PASS

7. literature-gate, mode=lecture
   input: output/lectureNN.tex + work/lectureNN_theory.md + work/lectureNN_research.md + 원문
   output append: output/literature_gate_NN.jsonl
   required: current lecture/theory/research digest에 묶인 PASS

8. typeset-checker, mode=final
   input: output/lectureNN.pdf
   output: output/final_pdftotext_check_NN.md + output/lectureNN_final.txt
   required: PASS
```

최종 완료 조건은 8단계 모두가 current digest 기준으로 PASS일 때만 만족된다.

---

## 4. research.md와 theory.md의 역할 분리

### 4.1 `research.md`

`research.md`는 넓은 자료조사 파일이다.

허용 용도:

```text
- source registry
- 관련 문헌 목록
- 역사적·맥락적 설명 후보
- source_id 부여
- 원문 확인 상태
- theory-curator에게 넘길 extraction request
```

`tex-writer`는 `research.md`를 읽을 수 있다. 단, 다음 load-bearing claim은 `research.md`에서 직접 가져오면 안 된다.

```text
theorem / proposition / lemma / proof / guarantee / convergence / rate / impossibility / finite-sample / asymptotic formal claim
```

이런 주장은 반드시 `theory.md`의 `claim_id`를 통해서만 사용할 수 있다.

### 4.2 `theory.md`

`theory.md`는 본문 사용 허가 파일이다. 모든 load-bearing 외부 claim은 claim card로 존재해야 한다.

필수 정보:

```text
claim_id
source_id
원문 위치
claim type
use grade
정확한 paraphrase
모든 가정
결론
수렴/확률/위상 양상
상수·차원·rate 의존성
proof skeleton provenance
notation transfer
semantic boundary
non-entailments
overclaim risks
tex-writer contract
```

문구 blacklist를 쓰지 않는다. 대신 의미적 경계를 둔다. 예: “existence result를 training guarantee로 강화하지 않는다.”

---

## 5. 분기 규칙

### 5.1 literature-gate dossier FAIL

`output/literature_gate_NN.jsonl`의 마지막 dossier-mode 판정이 FAIL이면:

| 원인 | 분기 |
|---|---|
| theory claim이 원문보다 강함 | `theory-curator` 수정 |
| source registry 자체가 부족함 | `researcher` 보강 |
| claim 사용 여부가 커리큘럼 판단 문제 | `manual_decision`로 중단 |

이 상태에서는 `tex-writer`를 호출하지 않는다.

### 5.2 typeset-checker FAIL

조판·컴파일·pdftotext round check가 FAIL이면:

```text
tex-writer가 output/typeset_check_NN.md와 round report를 읽고 output/lectureNN.tex를 수정
→ lecture.tex 변경으로 인한 invalidation 적용
→ typeset-checker부터 재시작
```

### 5.3 mathematician-gate FAIL

`repair_channel` 기준으로 분기한다.

| repair_channel | 의미 | 다음 |
|---|---|---|
| `tex-writer` | 내부 정의·논리·표현 보강으로 해결 가능 | tex-writer 재집필 |
| `theory-curator` | theory claim card가 얕거나 notation transfer가 부족 | theory-curator 보강 |
| `researcher` | 새 source 확인 또는 원문 확인 필요 | researcher 보강 후 theory-curator |
| `manual_decision` | 강의 범위·증명 생략·정책 판단 | 즉시 BLOCKED |

### 5.4 literature-gate lecture FAIL

| 원인 | 분기 |
|---|---|
| lecture.tex가 theory.md보다 강하게 말함 | `tex-writer` 수정 |
| theory.md가 원문과 불일치 | `theory-curator` 수정 |
| source 미확인 | `researcher` 보강 |
| 정책 판단 | `manual_decision`로 중단 |

---

## 6. Invalidation graph

이 그래프는 반드시 지킨다.

```text
research.md 변경
  → theory-curator 재실행
  → literature-gate dossier PASS 무효
  → tex-writer 산출 무효
  → typeset/math/literature lecture/final PASS 무효

theory.md 변경
  → literature-gate dossier 재실행
  → tex-writer 재실행
  → typeset/math/literature lecture/final PASS 무효

lecture.tex 변경
  → typeset-checker 재실행
  → mathematician-gate PASS 무효
  → literature-gate lecture PASS 무효
  → final pdftotext PASS 무효

typeset_check_NN.md 변경
  → mathematician-gate PASS 무효
  → final pdftotext PASS 무효

lectureNN.pdf 변경
  → final pdftotext PASS 무효
```

최신 PASS log가 있어도 해당 log의 `inputs.*.sha256`이 현재 파일 digest와 다르면 stale PASS로 간주하고 무효화한다.

---

## 7. JSONL 감사 로그 공통 규칙

두 gate log는 append-only JSONL이다.

```text
output/gate_log_NN.jsonl
output/literature_gate_NN.jsonl
```

각 agent는 다음 순서로만 Write한다.

1. 기존 파일이 있으면 Read한다.
2. 기존 내용을 그대로 prefix로 보존한다.
3. 새 compact JSON object 한 줄만 끝에 추가한다.
4. 전체 문자열로 Write한다.

`.claude/hooks/pipeline_policy.py`가 다음을 강제한다.

```text
- 기존 내용 prefix 보존
- 정확히 한 개의 non-empty JSONL line append
- schema_version 검사
- verdict/stall_count/sections/revision_directives 정합성 검사
- current input digest와 log의 inputs digest 일치 검사
- agent_type 없으면 fail-closed
```

### 7.1 mathematician-gate log schema

`output/gate_log_NN.jsonl`의 새 줄은 compact JSON 한 줄이어야 한다.

```json
{"schema_version":"math-gate-source-fidelity","lecture":"NN","iter":1,"inputs":{"lecture_tex":{"path":"output/lectureNN.tex","sha256":"..."},"theory_md":{"path":"work/lectureNN_theory.md","sha256":"..."},"typeset_report":{"path":"output/typeset_check_NN.md","sha256":"..."}},"verdict":"PASS","stall_count":0,"sections":[{"name":"full-document","status":"PASS","stalls":[]}],"global_checks":{"stage_block":true,"all_objects_attached":true,"compute_decl_complete":true,"analytic_legality":true,"predicate_classified":true,"source_claim_alignment":true},"revision_directives":[],"evidence":{"audited_sections":["full-document"],"checked_claim_ids":[],"note":"..."}}
```

### 7.2 literature-gate log schema

`output/literature_gate_NN.jsonl`의 새 줄은 compact JSON 한 줄이어야 한다.

```json
{"schema_version":"literature-gate-source-fidelity","lecture":"NN","iter":1,"mode":"dossier","inputs":{"research_md":{"path":"work/lectureNN_research.md","sha256":"..."},"theory_md":{"path":"work/lectureNN_theory.md","sha256":"..."}},"verdict":"PASS","stall_count":0,"sections":[{"name":"source-fidelity","status":"PASS","stalls":[]}],"global_checks":{"source_locators_traceable":true,"assumptions_not_weakened":true,"conclusions_not_strengthened":true,"proof_provenance_respected":true,"reader_visible_source_notes":true},"revision_directives":[],"evidence":{"checked_source_ids":[],"checked_claim_ids":[],"note":"..."}}
```

lecture mode에서는 `inputs`에 `lecture_tex`, `theory_md`, `research_md`가 모두 필요하다.

---

## 8. Round banner와 정체 감지

매 라운드 시작에 출력한다.

```text
════ 라운드 #RR ════
최근 dossier gate: [PASS/FAIL/stale/missing]
최근 typeset: [PASS/FAIL/stale/missing]
최근 math gate: [PASS/FAIL/stale/missing]
최근 literature lecture gate: [PASS/FAIL/stale/missing]
다음: [agent/mode]
════════════════════
```

최근 3개 FAIL 라운드에서 동일 canonical_key가 남고 stall_count가 감소하지 않으면 BLOCKED한다.

비교 단위:

```text
canonical_key.section
canonical_key.problem_type
canonical_key.target
repair_channel
```

`loc`는 증거일 뿐 signature에 넣지 않는다.

---

## 9. 최종 pdftotext gate

`typeset-checker`가 final mode로 수행한다.

산출물:

```text
output/lectureNN_final.txt
output/final_pdftotext_check_NN.md
```

필수 검사:

```text
1. pdftotext -layout output/lectureNN.pdf output/lectureNN_final.txt
2. final txt 존재와 non-empty 확인
3. "??" 없음
4. "Undefined" 없음
5. replacement character � 없음
6. 주요 절 제목 추출 가능
7. theorem/definition/stage/computebox 제목 추출 가능
8. 한글 문자가 사라지지 않았는지 확인
9. load-bearing source dependency remark가 의도한 경우 PDF 텍스트에 나타나는지 확인
10. final txt, pdf, tex, theory, latest gate log digest 기록
```

최종 PASS는 `output/final_pdftotext_check_NN.md`의 종합 판정이 PASS이고, 현재 pdf/txt/tex digest가 보고서의 digest와 일치할 때만 유효하다.

---

## 10. 완료 조건

완료하려면 모두 필요하다.

```text
A. latest dossier-mode literature-gate PASS
   - current research.md/theory.md digest와 일치

B. latest typeset_check_NN.md PASS
   - current lecture.tex digest와 일치

C. latest mathematician-gate PASS
   - current lecture.tex/theory.md/typeset_report digest와 일치

D. latest lecture-mode literature-gate PASS
   - current lecture.tex/theory.md/research.md digest와 일치

E. final pdftotext gate PASS
   - current pdf/txt/tex/theory digest와 일치
```

하나라도 missing/stale/FAIL이면 완료하지 않는다.

---

## 11. 기본값

- 강의 콘텐츠 기본값: 이론 전용. 코드 실습 제외.
- 논문 장문 직접 인용 금지. 짧은 식별용 anchor만 허용.
- 관련 문헌 나열과 역사적 맥락은 `research.md`를 근거로 쓸 수 있다.
- formal claim은 `theory.md`의 `claim_id`를 가져야 한다.
- load-bearing 외부 claim은 comment-only source tag로 충분하지 않다. 독자에게 보이는 source dependency remark 또는 macro가 필요하다.

---

## 12. 권위 문서 위치

```text
spec/AI28_강의제작_사양서_v13-2.md
spec/AI_curriculum_28강.md
spec/curriculum_decisions_log.md
template/lecture_template.tex
```
