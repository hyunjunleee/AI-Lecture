---
name: mathematician-gate
description: >
  DEPRECATED — read-gate / claim-gate / model-gate 3개로 분리됨. dispatch하지 말 것.
  내부 수학 감사는 .claude/agents/{read,claim,model}-gate.md 를 사용한다.
tools: Read
model: opus
---

# mathematician-gate (DEPRECATED — 사용 중지)

이 단일 게이트는 한 번의 백지 독해로 8개 차원을 점검하다 서로 다른 차원을 반복해서 놓쳤다.
세 개의 집중 게이트로 분리되었다:

- `read-gate` — 무정지 순차 독해(이름·적형·흐름·누출)
- `claim-gate` — load-bearing 주장 적대적 5테스트
- `model-gate` — 구체 모델·계산 완결성(객체 before 부분, §2.16 4요소)

분리 동기·구조·전체 영향 맵은 `.claude/policy/redesign_gate_split.md` 참조.
이 파일은 호환을 위해 남겨둔 것이며 dispatch하지 않는다(hook도 더 이상 이 agent에 gate log
소유권을 주지 않는다). 완전 제거는 `! rm .claude/agents/mathematician-gate.md`.
