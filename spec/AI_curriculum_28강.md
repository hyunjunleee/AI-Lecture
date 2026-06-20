# AI 기술의 역사와 현재: 0+28강 통합 심화 커리큘럼 (v14 — 수리 심화 통합판)

> **대상 수준:** 대학원 수준 순수 해석학·측도론적 확률론·선형대수·다변수 미적분·Python — **AI 사전지식 전무** (사양서 §2.11 독자 모델과 동일). "논문 직접 독해 가능"은 *수학 논문을 읽는 능력*을 뜻하며 AI 문헌에 대한 사전 노출을 뜻하지 않는다.
> **무게중심:** 현대 딥러닝/LLM 기술 깊이 중심 (역사적 흐름은 인과적 토대로 포함)
> **범위:** 퍼셉트론(1958)부터 2026년 Harness Engineering·에이전틱 엔터프라이즈까지
> **최종 업데이트:** 2026년 6월 (v14 통합판)
>
> **v14의 지위.** 본 문서는 `AI_curriculum_28강.md`(v13)와 `AI28_부록커리큘럼_수학적의도.md`를 **단일 커리큘럼으로 통합**한 판이다 — 각 강의 주제·요지·본강 수식 유도 항목은 유지하고, 구 부록의 "수리 심화"(근본 원리·증명할 정리)와 신설 "무정지 전제"(순수 수학자의 순차 독해를 위해 그 강에서 명시적으로 정의·정착할 개념 목록)를 각 강에 내장했다. 사양서 §0.2 권위 서열의 ②(정식화 1차 기준)·③(콘텐츠 시드)을 본 문서가 단독 승계하며, 구 부록 문서는 이력으로 보존될 뿐 첨부 불요다. v13의 M-노트는 본문 통합으로 대체되었다.

---

## 사용법 — 각 강의 구획과 공통 무정지 규약

**구획(콘텐츠 분류 — 제시 순서·구조의 강제가 아니다; 사양서 §0.0-2).** 각 강은 다음 콘텐츠를 가진다: ① **이론**(인과 서사) · ② **수식 유도 — 본강**(원 커리큘럼 항목) · ③ **수식 유도 — 수리 심화**(구 부록 통합: 그 장치의 필연성·작동 원리를 증명하는 정리들) · ④ **무정지 전제**(이 강에서 정의·정착할 것) · ⑤ **추천 논문/자료**([본강]/[심화] 표기) · ⑥ **실습**(기본+심화) · ⑦ **연결**(§2.15 다리).

**공통 무정지 규약.**
1. 모든 강은 0강 표준 무대 $S_0$의 재정착(무대 블록, 사양서 §2.6A-5)으로 자신의 무대를 조립한다.
2. ④ "무정지 전제"는 **비포괄 시드**다 — 사양서 §0.0 원칙 (A)–(C)가 최종 판정 기준이며, 목록에 없어도 정의 전 사용은 멈춤이다. 목록의 각 항목은 "이 강 PDF가 그 개념을 *판정 가능한 정의·진술*로 박아야 한다"는 콘텐츠 의무다.
3. 모든 전방 참조는 roadmap(논리 무게 없음)으로만 — 본 문서가 의존 순서를 설계해 두었다(예: 상호정보·전변동거리는 0강, Fano 부등식은 7강, 회로 복잡도·TC⁰의 정의는 8강(17강은 재정착), MDP·가치함수는 15강, 최적 수송의 정의는 21강(19강의 Schrödinger bridge 언급은 roadmap), 정지시각은 25강).
4. 비정식 시드 표현("~의 직관", "~의 분석", "트레이드오프 모델", "~의 관계")은 그대로 산출하지 않는다 — 같은 강의 ③·④가 1차 정식화 기준이다(사양서 §0.2).
5. `[epistemic: 검색 미수행]` 라벨이 붙은 2024–2026 서지는 집필 시 1차 출처로 검증한다(부록 E).

---

## 목차

| Part | 강의 | 주제 |
|------|------|------|
| **0. 수리적 정초** | 0 | 코스 표준 무대 $S_0$ — 측도론적 정착 |
| **I. 기초 토대** | 1–4 | 역사, 학습이론, 최적화, 역전파 |
| **II. 딥러닝 아키텍처** | 5–9 | MLP/CNN, 정규화, 시퀀스/Attention, Transformer, 위치표현 |
| **III. 언어 모델과 스케일** | 10–14 | LM 기초, 사전학습, 스케일링 법칙, 분산학습, PEFT |
| **IV. 정렬·추론** | 15–20 | RLHF, DPO, 추론, RAG/도구, 멀티모달, 안전·해석 |
| **V. 현대 프런티어 (2024–2026)** | 21–25 | MoE, 효율 어텐션, 추론 최적화, 에이전트, 멀티모달 통합 |
| **VI. Harness Engineering & 에이전틱 업무 (2025–2026)** | 26–28 | 하니스 엔지니어링, 프로덕션 하니스, 에이전틱 엔터프라이즈 |

---

# Part 0 — 수리적 정초

## 0강. 기계학습의 측도론적 정초 — 코스 표준 무대 $S_0$

**위상.** 본 강은 독자가 모르는 수학을 가르치지 않는다(독자는 측도론적 확률론을 안다). 대신 **코스 전체가 사용할 표준 무대 $S_0$를 한 번, 코스의 기호로 조립**하여, 이후 모든 강의가 사양서 §2.6A·§2.11-5에 따라 한 줄 재정착으로 부착할 유일한 좌표계를 제공한다. "모델", "학습", "손실", "데이터"라는 공학 어휘가 처음으로 *완전한 수학적 대상*으로 박히는 곳이 여기다. 분량은 본강 평균보다 짧아도 되나, §0.0 무정지 기준·§2 증명 완전성은 동일하게 적용된다.

**이론**
"기계가 학습한다"는 공학 문장을 측도론의 문장으로 번역한다 — 데이터는 확률공간 위의 과정, 모델은 가측사상의 매개족, 학습은 위험 범함수에 대한 적응 확률 과정. 이 번역이 왜 필요한가: 이후 강의의 모든 정리(일반화 경계·수렴·정합성·정확 보존)가 정확히 이 무대의 성질이며, 무대 없이 진술된 정리는 정리가 아니기 때문임을 인과로 제시한다.

**수식 유도 — 본강** (조립할 표준 대상 목록 — 각각 정의와 잘 정의됨의 확인·증명)
- 확률공간과 데이터 과정: $(\Omega,\mathcal F,\mathbb P)$, 표준 Borel 공간 $\mathcal X,\mathcal Y$, i.i.d. 열 $(X_i,Y_i)_{i\ge1}$의 구성(곱측도 정리), 경험측도 $\widehat{\mathcal D}_n$과 SLLN의 한 적용.
- 가설족과 위험: $\Theta\subseteq\mathbb R^p$, $(\theta,x)\mapsto f_\theta(x)$의 결합 가측성 조건, 손실 $\ell$의 가측성, 위험 $R(\theta)=\mathbb E_{\mathcal D}[\ell(f_\theta(X),Y)]$의 잘 정의(가적분 상시 가정), 경험위험 $\widehat R_n(\theta)$이 확률변수임의 확인.
- 학습 알고리즘의 형식화: 필트레이션 $(\mathcal F_t)$, 확률적 gradient $g_t=\nabla R(\theta_t)+M_{t+1}$(마팅게일 차분 잡음 모델), 갱신열 $(\theta_t)$의 적응성. **명제+증명:** 지배함수 가정 하 $\nabla_\theta\,\mathbb E=\mathbb E\,\nabla_\theta$(적분 기호 아래 미분) — 이후 전 강의가 사양서 §2.16-2에서 인용할 표준 출처.
- 조건부 구조: 표준 Borel 위 정칙 조건부 분포의 존재, 조건부 모델 $p(\cdot\mid x)$ = Markov kernel, disintegration.
- 절대연속성과 정보량: $\mu\ll\nu$, Radon–Nikodym 정리, $\mathrm{KL}(\mu\,\|\,\nu)=\int\log\frac{d\mu}{d\nu}\,d\mu$ ($\mu\not\ll\nu$이면 $+\infty$ 규약); **전변동거리** $\mathrm{TV}(\mu,\nu)=\sup_A|\mu(A)-\nu(A)|$와 Pinsker 부등식(진술); **상호정보** $I(X;Y)=\mathrm{KL}(P_{XY}\,\|\,P_X\otimes P_Y)$; cross-entropy의 측도론적 정의와 이산(계수측도) 특례. *(v14: TV·MI를 0강으로 승격 — 7강 Fano, 18강 InfoNCE, 23강 coupling이 재정착한다.)*
- 열 공간 위의 측도: 조건부 pmf 족(자기회귀 모델)으로부터 $\mathcal V^{\mathbb N}$ 위 유일 확률측도의 구성(Ionescu–Tulcea)과 유한열 결합 pmf와의 정합 — 10·11강의 "언어 모델 $p$"가 사는 곳.
- (포인터) 연속시간 대상: SDE 해의 존재·유일성과 시간역행은 진술·출처만 제시 — 본격 전개는 19강.

**무정지 전제 — 이 강에서 정의·정착할 것**
- 위 목록 자체가 전제 목록이다. 추가로: "모델이 $\mathcal D$를 학습한다"는 술어의 1차 바인딩(위험 최소화 열 $(\theta_t)$의 수렴으로), "표본을 뽑는다"의 의미($\Omega$ 위 좌표 사상의 실현), 확률변수/분포/실현의 표기 구분 규약.

**추천 논문/자료**
- Kallenberg (2021), *Foundations of Modern Probability*, 3rd ed. — kernel·disintegration·Ionescu–Tulcea.
- Shalev-Shwartz & Ben-David (2014), *Understanding Machine Learning* — 학습 문제의 형식적 정의(측도론 보강은 본 강이 담당).
- Çinlar (2011), *Probability and Stochastics* — 조건부·kernel 관점 보강.

**실습 과제:** (a) push-forward 정의대로 변환 표본의 경험분포가 이론 분포에 수렴(KS 거리 실측), (b) Monte Carlo 기댓값의 SLLN 수렴, (c) Markov kernel 합성으로 구현한 자기회귀 표집의 유한차원 주변분포가 Ionescu–Tulcea 구성과 일치함을 확인. (코드: `lab00_foundations.py`)

**연결.** 모든 후속 강의의 무대 블록(§2.6A)이 $S_0$를 재정착한다 — 특히 2강(표본공간·가설족), 3강(필트레이션·$\nabla\mathbb E$ 교환), 7강(MI→Fano), 10–11강(열 공간 측도), 15–16강(RN/KL·정책=kernel), 18강(MI), 19강(정칙 조건부·SDE 포인터), 23강(TV·coupling), 25강(필트레이션→정지시각).

---

# Part I — 기초 토대

## 1강. AI의 역사적 궤적과 패러다임 전환

**이론**
기호주의(GOFAI) → 연결주의 → 통계적 학습 → 딥러닝 → 스케일링 시대로 이어지는 인과적 흐름. 퍼셉트론의 등장과 한계, AI 겨울, 역전파의 부활, AlexNet 충격(2012), Transformer 혁명(2017)까지의 전환점을 다룬다. 각 전환이 *왜* 일어났는지(데이터·연산·알고리즘의 상호작용)에 초점을 둔다.

**수식 유도 — 본강**
- 퍼셉트론 수렴 정리: 선형 분리 가능한 데이터에서 업데이트 횟수가 $\frac{R^2}{\gamma^2}$로 유계임을 마진 $\gamma$와 반경 $R$로 유도.
- XOR의 선형 분리 불가능성: 단일 선형 결정경계로 XOR을 분리할 수 없음을 증명.

**수식 유도 — 수리 심화** *(구 부록 통합: 분리 가능성의 기하·확률과 마진의 쌍대성)*
- **정리(Cover, 1965).** $\mathbb R^d$ 일반 위치의 $N$개 점의 선형 분리 가능 dichotomy 수는 $C(N,d)=2\sum_{k=0}^{d-1}\binom{N-1}{k}$; 무작위 라벨이 분리 가능할 확률 $C(N,d)/2^N$은 $N\le d{+}1$에서 1, $N=2(d{+}1)$에서 $1/2$. ⟹ 차원을 올리면(특징 사상) 분리 가능성이 *확률적으로* 보장됨 — "고차원으로 올리기"가 작동하는 이유.
- **정리(Novikoff).** 마진 $\gamma$·반경 $R$의 분리 가능 데이터에서 갱신 횟수 $\le(R/\gamma)^2$ — 증명은 〈가중치·최적해〉 내적의 선형 증가 vs 노름의 $\sqrt{\cdot}$ 증가의 충돌. 이 한계가 hard-margin SVM 쌍대와 같은 양 $1/\gamma^2$를 본다(online↔margin 쌍대).
- **Minsky–Papert의 진짜 내용.** parity 술어의 차수(order)가 입력 크기에 비유계 — 8강 §심화(단일 attention 층의 PARITY 한계)의 1958년 선행.

**무정지 전제 — 이 강에서 정의·정착할 것**
- 무대: 유한 표본 $S=\{(x_i,y_i)\}_{i=1}^N\subset\mathbb R^d\times\{-1,+1\}$의 **결정론적** 설정임을 명시(2강의 확률 설정과의 §2.15 분기 예고).
- "분류기"=사상 $h:\mathbb R^d\to\{-1,+1\}$, "결정경계"=초평면, "선형 분리 가능"·마진 $\gamma$·반경 $R$의 엄밀 정의(엄격 부등식, $\min/\max$의 유한성).
- 퍼셉트론을 *가중치열의 이산 동역학계*로 — 갱신 사상을 함수로 먼저 정의(§2.11-6), "학습"=무오류 고정점 도달로 바인딩(§2.11-9). "뉴런·활성화"는 affine 사상+$\operatorname{sign}$ 합성의 *이름*임을 표기 바인딩.
- 일반 위치(general position)·dichotomy의 정의(Cover 셈의 전제), online mistake-bound 모형의 정의(Novikoff 쌍대 진술의 무대), hinge loss·hard-margin 쌍대 문제의 정식화.
- 술어(predicate)와 그 차수(order)의 정의(Minsky–Papert 진술용); 특징 사상 $\phi$(lift)의 정의와 XOR의 $\phi(x)=(x_1,x_2,x_1x_2)$ 분리.
- 역사 서사의 모든 인과 주장("~때문에 겨울이 왔다")은 판정 가능한 사실(연도·결과·한계 정리)로 지지(§2.14-2).

**추천 논문/자료**
- [본강] Rosenblatt (1958), *The Perceptron*; Minsky & Papert (1969), *Perceptrons*; Rumelhart, Hinton & Williams (1986), *Learning representations by back-propagating errors*
- [심화] Cover (1965, *IEEE EC*); Novikoff (1962); Cortes & Vapnik (1995, *SVM*); Freund & Schapire (1999, perceptron의 large-margin 해석)

**실습 과제:** 기본 — NumPy 퍼셉트론 구현·XOR 실패 재현. 심화 — (a) $d$ 고정·$N$ 스윕의 무작위 라벨 분리 성공률 vs Cover 곡선, (b) 갱신 수 vs $(R/\gamma)^2$ 상한, (c) $\phi$-lift 후 XOR 분리. (코드: `lab01_perceptron.py`)

**연결(§2.15).** parity 차수 → 8강 심화(PARITY/TC⁰)의 선행. 마진·kernel lift → 14강(저랭크)·22강(kernel attention). 결정론적 표본 → 2강에서 확률 무대로 일반화(분기 유형: 일반화·정련).

---

## 2강. 학습 이론의 수학적 기반

**이론**
경험적 위험 최소화(ERM), 편향-분산 분해, VC 차원, 일반화 경계, 그리고 고전 통계학습이론을 깨뜨린 이중 하강(double descent) 현상. 과매개변수화(overparameterization) 영역에서 일반화가 다시 좋아지는 현대적 관찰을 고전 이론과 대비.

**수식 유도 — 본강**
- ERM 정식화와 Hoeffding 부등식 기반 일반화 경계 유도.
- 제곱오차의 bias² + variance + irreducible noise 분해.

**수식 유도 — 수리 심화** *(구 부록 통합: 보간의 통계역학 — 이중 하강의 기전)*
- **명제(임계 첨두).** 선형/랜덤특징 모형에서 ridgeless($\lambda\to0^+$) test risk는 $\mathbb E[\sigma_{\min}^{-2}]$ 류 항을 포함하고, $\gamma=p/n\to1$에서 Marchenko–Pastur 스펙트럼의 하단 모서리 $(1-\sqrt\gamma)^2\to0$로 발산 — 첨두의 위치·발산이 랜덤행렬 이론으로 *유도*됨.
- **정리(benign overfitting; Bartlett–Long–Lugosi–Tsybakov 2020).** 공분산의 effective rank 조건($r_k(\Sigma)$, $R_k(\Sigma)$) 하에 최소노름 보간자의 초과위험이 0으로 — "보간=과적합"이 거짓일 수 있는 정확한 스펙트럼 조건.
- **implicit bias.** GD/최소노름 보간자의 특성화(의사역행렬 해), uniform convergence 틀의 설명 실패(Nagarajan–Kolter)의 지위(반례 기반).

**무정지 전제 — 이 강에서 정의·정착할 것**
- 무대: 0강 $S_0$ 재정착 — $(\Omega,\mathcal F,\mathbb P)$·i.i.d. 과정·가설족의 가측성·위험; 1강의 결정론적 표본과의 §2.15 분기(같은 "데이터"라는 이름, 다른 대상).
- "모델 복잡도"의 바인딩: VC 차원의 정의(shattering 포함) — 파라미터 수·노름 기반 복잡도와의 구분 명시. "일반화"=초과위험 $R(\hat\theta)-\inf_\Theta R$, "과적합"의 정의.
- bias–variance의 **삼중 기대 구조**: 각 기댓값이 무엇에 대한 것인지(훈련집합 $\sim\mathcal D^{\otimes n}$ / 표적 잡음 / 테스트점) 매 식에서 측도 명시(§2.6A-3a).
- 보간자·최소-$\ell_2$노름 해(Moore–Penrose)의 정의; Rademacher 복잡도·uniform convergence의 정의.
- 경험 스펙트럼 분포의 정의와 Marchenko–Pastur 법칙의 진술(수렴 양상 — 약수렴 a.s. — 을 §2.16-7로 명시), 조건수 $\kappa$, effective rank $r_k(\Sigma)$의 정의.
- Hoeffding 부등식은 본 강에서 완전 증명(26강 Chernoff 증폭이 재정착할 표준 출처).

**추천 논문/자료**
- [본강] Vapnik (1998), *Statistical Learning Theory*; Belkin et al. (2019, *PNAS*)
- [심화] Bartlett, Long, Lugosi, Tsybakov (2020, *PNAS*); Hastie, Montanari, Rosset, Tibshirani (2022, *Ann. Stat.*); Mei & Montanari (2022); Nagarajan & Kolter (2019, *NeurIPS*)

**실습 과제:** 기본 — 복잡도 스윕으로 이중 하강 곡선 재현. 심화 — 랜덤특징 ridgeless 회귀의 $p/n$ 스윕에서 이중 하강과 $\sigma_{\min}(\frac1n\Phi^\top\Phi)\to0$ 동시 표시, ridge $\lambda$의 첨두 완화 실측. (코드: `lab02_double_descent.py`)

**연결(§2.15).** 조건수·RMT → 14강(Hessian/NTK 스펙트럼). 최소노름 implicit bias → 3강(SGD의 implicit regularization). Hoeffding → 17강(다수결 꼬리)·26강(증폭).

---

## 3강. 최적화의 핵심

**이론**
SGD, 모멘텀, Adam/AdamW, 학습률 스케줄(warmup·cosine), 손실 지형(loss landscape)과 평탄 최소값(flat minima) 가설. AdamW가 weight decay를 L2 정규화에서 분리하는 이유.

**수식 유도 — 본강**
- SGD의 수렴 분석(볼록 가정 하).
- Adam 갱신식과 1·2차 모멘트 편향 보정 유도.
- AdamW의 decoupled weight decay 유도.

**수식 유도 — 수리 심화** *(구 부록 통합: 확률적 흐름으로서의 학습)*
- **명제(선형 안정성; Wu–Ma–E 2018).** 최소값 $\theta^\star$가 학습률 $\eta$·배치 $B$의 SGD에 선형 안정이려면 $\lambda_{\max}(H)\le 2/\eta$ 류 곡률 조건 + 잡음 분산 제약 — *날카로운* 최소값은 큰 $\eta$에서 불안정해 SGD가 평탄한 쪽을 선택(정성적 양상 일반, 정확 상수는 모형 특수 — §2.6 좁힘 동반).
- **정리(Adam 비수렴; Reddi et al. 2018).** 적응률 $v_t$ 비단조성으로 regret $\Theta(T)$인 볼록 online 반례 존재; $\hat v_t=\max$ 보정(AMSGrad)으로 $O(\sqrt T)$ 회복.
- **SGD-as-SDE.** 잡음 공분산이 만드는 정상분포(Mandt–Hoffman–Blei; Li–Tai–E) — 근사의 지위(약수렴 차수·가정)를 명시.

**무정지 전제 — 이 강에서 정의·정착할 것**
- 무대: $S_0$ 재정착 — 필트레이션·마팅게일 차분 잡음, 가정(불편성 $\mathbb E[g_t\mid\mathcal F_{t-1}]=\nabla R(\theta_{t-1})$, 분산 조건)을 상시 가정으로. $\nabla_\theta\mathbb E=\mathbb E\nabla_\theta$는 0강 명제 인용(§2.16-2).
- 볼록·$\beta$-smooth의 정의(6강·15강이 재정착할 표준 출처), GD를 이산 동역학계로; 수렴 결론의 양상(기대 수렴/a.s./고확률)을 §2.16-7로 구분 명시.
- momentum=상태 확장 1차 점화식으로, Adam은 다섯 줄 갱신식 *전체*를 정의 블록으로(사양서 §2.6·§2.7 Algorithm theorem) — $\beta_1,\beta_2,\varepsilon,\eta,\lambda$와 $m_t,v_t,\hat m_t,\hat v_t$ 전수 정의.
- "loss landscape"·"평탄/날카로움"의 바인딩(§2.11-9): $R$의 그래프·Hessian 스펙트럼·선형 안정성 — "가설"로서의 지위 라벨(§2.14-6).
- online convex 최적화·regret의 정의(Reddi 반례·AMSGrad 진술의 무대).
- "warmup이 필요/효과적" 류는 경험 라벨(§2.8b); RAdam 설명은 *한* 설명임을 명시.

**추천 논문/자료**
- [본강] Kingma & Ba (2015), *Adam*; Loshchilov & Hutter (2019), *AdamW*; Li et al. (2018), *Visualizing the Loss Landscape*
- [심화] Mandt, Hoffman, Blei (2017); Li, Tai, E (2019, *JMLR*); Wu, Ma, E (2018); Reddi, Kale, Kumar (2018, *ICLR*); Keskar et al. (2017)

**실습 과제:** 기본 — SGD/Momentum/Adam/AdamW 수렴 비교·손실 지형 2D 투영. 심화 — (a) 2D 손실의 SGD 잡음 공분산↔정상분포 산점, (b) 날카로운/평탄 최소값의 lr 스윕 선형 안정 경계 실측, (c) Reddi 반례의 Adam vs AMSGrad regret. (코드: `lab03_optimizers.py`)

**연결(§2.15).** implicit regularization → 2강(최소노름). 적응 전처리 → 8강 심화(ICL=전처리 경사하강). $\beta$-smooth → 6강(평활성), natural gradient → 15강.

---

## 4강. 역전파와 자동 미분

**이론**
계산 그래프, reverse-mode automatic differentiation, 기울기 소실/폭발, gradient checkpointing의 시간-메모리 트레이드오프.

**수식 유도 — 본강**
- 연쇄법칙의 행렬 형태 유도.
- Jacobian-vector product(JVP)와 vector-Jacobian product(VJP)의 구분.

**수식 유도 — 수리 심화** *(구 부록 통합: 미분의 대수 복잡도와 쌍대성)*
- **정리(Baur–Strassen, 1983).** 직선 프로그램으로 주어진 유리함수 $f:\mathbb R^n\to\mathbb R$의 *모든* 편미분 $\nabla f$의 산술 비용은 $f$ 계산 비용의 상수배(통상 $\le5$)로 유계 — reverse-mode("출력 1개의 $n$개 gradient를 한 번의 backward로")의 점근 최적성.
- **명제(쌍대).** 합성 $f=f_L\circ\cdots\circ f_1$에서 JVP는 $\prod J_l\,v$의 오른쪽 누적(pushforward), VJP는 $u^\top\prod J_l$의 왼쪽 누적(pullback/수반) — 비용이 입·출력 차원비로 갈림.
- **따름(소실/폭발).** $\|\partial h_t/\partial h_{t-k}\|\approx\prod\|J\|$가 1에서 벗어나면 $k$에 지수적 — 6·7강 필연성의 backward 판본.

**무정지 전제 — 이 강에서 정의·정착할 것**
- 계산 그래프=연산 DAG의 정의(노드=기본 연산, 간선=데이터 의존; straight-line program), 그래프의 평가 사상과 함수의 동일성.
- Fréchet 도함수=선형사상, Jacobian=그 행렬 표현; JVP=pushforward, VJP=내적에 대한 수반(전치)으로 *정의*(기호 $J^\top$의 의미 고정).
- 산술 복잡도 모형(기본 연산 단위 비용)의 정의 — Baur–Strassen 진술이 사는 곳.
- "기울기가 잘/안 흐른다" 금지 — $\|\prod_t J_t\|$의 $e^{\pm\Theta(L)}$ 거동으로 치환(§2.14-5).
- checkpointing: 평가 스케줄(저장/재계산 집합)의 정의와 시간–메모리 $O(\sqrt L)$ 절충의 정식화.
- (심화 라벨) 미분=functor(pushforward/pullback) 관점은 개념 비고로 — 논리 무게를 싣지 않음.

**추천 논문/자료**
- [본강] Baydin et al. (2018), *Automatic Differentiation in ML: a Survey*
- [심화] Baur & Strassen (1983, *TCS*); Griewank & Walther (2008, *Evaluating Derivatives*); Fong, Spivak, Tuyéras (2019, *Backprop as Functor*); Chen et al. (2016, checkpointing)

**실습 과제:** 기본 — 스칼라 autodiff 엔진(micrograd 스타일) 구현. 심화 — (a) forward/reverse 비용을 입·출력 차원비로 측정, (b) 깊은 선형망 $\prod J_l$의 $\sigma_{\max}$ 지수 거동, (c) $\sqrt L$ checkpointing 메모리 곡선. (코드: `lab04_autograd.py`)

**연결(§2.15).** Jacobian 곱 → 6강(분산 점화식 backward)·7강(BPTT). 쌍대 → 22강(재귀–합성곱 이중성과 개념 평행). 이산 gradient 추정 → 21강(STE).

---
# Part II — 딥러닝 아키텍처

## 5강. MLP·CNN과 표현 학습

**이론**
보편 근사 정리, 합성곱의 귀납 편향(평행이동 불변성·국소성·파라미터 공유), 잔차 연결(residual)이 깊은 망 학습을 가능케 한 원리.

**수식 유도 — 본강**
- Cybenko 보편 근사 정리의 직관적 스케치. *(v14 승격: "스케치"는 시드 표현일 뿐 — 가정 완비 진술 + 완전 증명(또는 Stone–Weierstrass 경로의 증명 가능한 약화판)으로 다루고, 남기는 부분은 §2.14-6으로 명시 인정한다.)*
- 합성곱 연산의 순전파·역전파, 수용 영역(receptive field) 계산.

**수식 유도 — 수리 심화** *(구 부록 통합: 깊이의 표현 이득·합성곱의 유일성·잔차의 연속 극한)*
- **정리(depth separation; Telgarsky 2016).** 깊이 $\Theta(L^2)$·폭 $O(1)$로 표현되는 1차원 함수 중, 깊이 $O(L)$·폭 $\le 2^L$의 어떤 망으로도 $\Omega(1)$ 오차 미만 근사 불가한 것이 존재 — 깊이의 이득이 *증명*됨.
- **정리(등변 ⟹ 합성곱).** 유한군 $G$ 위 $G$-등변 선형사상은 정확히 $G$-합성곱; $\mathbb R^d$ 평행이동에 대해서는 (정칙성 가정 하) 평행이동과 가환인 유계 선형작용소가 합성곱(Fourier multiplier) — conv는 설계가 아니라 *대칭의 귀결*.
- **명제(residual=ODE).** $h^{(l)}=h^{(l-1)}+\mathcal F_l(h^{(l-1)})$는 $\dot h=f(h,t)$의 단위-step Euler; 깊이 극한·adjoint의 지위 명시.
- **Barron 공간.** 차원무관 $n^{-1/2}$ 근사율의 정확한 의미(어느 노름·어느 함수류).

**무정지 전제 — 이 강에서 정의·정착할 것**
- 이미지·텐서의 정의: $x\in\mathbb R^{C\times H\times W}$ — 채널·공간 인덱스의 의미; "tensor"는 *다중첨자 배열*로 표기 바인딩(텐서곱 공간의 원소가 아님을 명시 — abuse 차단, §0.0-B).
- 이산 합성곱/교차상관의 정의($\mathbb Z^2$ 위 유한 지지), padding=정의역 확장 사상·stride=부분표집 사상으로 정식화; `Conv2d`가 계산하는 것은 교차상관임을 §2.5와 일치시켜 명시.
- 평행이동 작용소 $T_v$, 등변성·불변성의 정의(둘의 구분!); "귀납 편향"의 바인딩(§2.11-9: 가설족의 구조 제약으로).
- $C(K)$·sup-norm·조밀성의 정의, Cybenko 가정(판별적 시그모이드)의 완전 진술.
- 수용 영역=출력 좌표가 의존하는 입력 인덱스 집합으로 정의(계산 규칙 포함).
- "표현(representation)/특징(feature) 학습"의 바인딩: 중간 표현 사상 $x\mapsto h^{(l)}(x)$와 그 좌표 범함수로 — 정의 없는 사용 금지(§2.11-9).
- ResNet forward 합성식 $f_\theta=\text{head}\circ\text{GAP}\circ\mathcal B_B\circ\cdots\circ\mathcal B_1\circ\text{stem}$과 각 사상의 차원(사양서 §2.9 예시 그대로).

**추천 논문/자료**
- [본강] Cybenko (1989); LeCun et al. (1998), *LeNet*; He et al. (2016), *ResNet*
- [심화] Telgarsky (2016); Eldan & Shamir (2016, *COLT*); Cohen & Welling (2016, group equivariant CNN); E (2017, dynamical systems); Chen et al. (2018, *Neural ODE*); Barron (1993)

**실습 과제:** 기본 — ResNet 기본 블록 구현·CIFAR-10 학습(축소 모드 §2.12). 심화 — (a) Telgarsky 톱니($2^L$ 진동)를 얕은 망이 못 맞춤, (b) 무작위 평행이동-가환 선형사상이 수치적으로 Toeplitz/순환(=conv)로 수렴, (c) residual의 step 수에 따른 Euler 수렴. (코드: `lab05_resnet.py`)

**연결(§2.15).** 등변성 → 8강(순열 등변성)·9강(위치=등변성 깨기). ODE 관점 → 22강(SSM 연속계). 깊이 분리 → 8강 심화(회로 깊이)와 개념 평행.

---

## 6강. 정규화와 학습 안정화

**이론**
BatchNorm, LayerNorm, RMSNorm, 드롭아웃. Transformer에서 Pre-LN vs Post-LN의 학습 안정성 차이.

**수식 유도 — 본강**
- BatchNorm의 순전파와 역전파 유도.
- LayerNorm vs RMSNorm 비교(평균 제거 항의 유무).

**수식 유도 — 수리 심화** *(구 부록 통합: normalization의 최적화 기하 — 필요성(분산 점화식, 사양서 §2.10 예시) 너머)*
- **명제(scale invariance ⟹ 유효 lr 자동 감쇠).** $f(cw)=f(w)$이면 $\langle\nabla f(w),w\rangle=0$(Euler 항등)이고 GD 하에 $\|w_t\|^2$ 단조 증가 ⟹ 구면 위 유효 보폭 $\eta/\|w_t\|^2$ 감소.
- **명제(평활성; Santurkar et al.).** BN 통과 손실의 gradient·Hessian 작용소 노름의 균일 상계 — 넓은 안정 lr 영역의 *기전*. "internal covariate shift" 설명은 반박된 가설임을 명시(§2.8b).
- **해소 메커니즘(§2.10).** 정규화는 gain $g$를 1로 *교정*하지 않는다($W$ 불변) — 점화식 $q_l=g_lq_{l-1}$의 곱셈 *결합을 끊는다*; $g\approx1$을 *겨냥*하는 Fixup/NFNets와 메커니즘이 다름.

**무정지 전제 — 이 강에서 정의·정착할 것**
- 미니배치 통계의 확률적 지위: 배치 추출의 무작위성이 무대 어디에 사는지(부분집합 균등 추출의 정의), $\hat\mu_B,\hat\sigma_B^2$=경험 모멘트(어느 측도의).
- BatchNorm을 **두 개의 사상**으로 정의 — train(배치 의존 확률적 사상)/eval(EMA 고정 결정론 사상): 같은 이름·다른 함수임을 §2.15-4(동명이물)로 다리.
- 분산 점화식 $q_L=g^Lq_0$의 유도(필요성 — 사양서 §2.10 예시 충실 이행)와 그 가정(독립성·모멘트)의 명시.
- Lipschitz·$\beta$-smoothness는 3강 재정착; 구면 $\mathbb S^{d-1}$ 위 Riemannian gradient의 정의.
- Pre-LN/Post-LN=합성 *순서*의 차이로 정식화하고 깊이별 gradient 척도 진술(Xiong)을 결과로.
- Dropout=베르누이 마스크 곱 사상(train)과 기대 보정(eval)의 정의 — train/eval 의미 분기 명시(§2.5-3 연결).

**추천 논문/자료**
- [본강] Ioffe & Szegedy (2015); Ba et al. (2016); Zhang & Sennrich (2019), *RMSNorm*; Xiong et al. (2020, Pre-LN)
- [심화] Santurkar, Tsipras, Ilyas, Madry (2018); Arora, Li, Lyu (2019); Li & Arora (2019, exponential LR); Zhang, Dauphin, Ma (2019, *Fixup*)

**실습 과제:** 기본 — 정규화 교체·제거 ablation. 심화 — (a) BN 유/무 gradient 변동(평활성) 측정, (b) scale-invariant 망의 $\|w_t\|$ 증가↔유효 lr 감소, (c) Pre/Post-LN 초기 gradient 척도 vs 깊이. (코드: `lab06_normalization.py`)

**연결(§2.15).** 분산 점화식 backward → 4강(Jacobian 곱). Pre-LN 깊이 척도 → 8강 심화(랭크 붕괴를 LN이 못 막음).

---

## 7강. 시퀀스 모델과 Attention의 등장

**이론**
RNN/LSTM/GRU의 장기 의존성 한계, seq2seq의 정보 병목, Bahdanau additive attention이 병목을 해소한 방식.

**수식 유도 — 본강**
- LSTM 게이트 방정식과 BPTT(시간에 대한 역전파).
- Additive attention 가중치 유도.

**수식 유도 — 수리 심화** *(구 부록 통합 — 기제작 PDF "Continuous Hopfield · Nadaraya–Watson" 흡수: "하나의 식, 두 렌즈")*
- **렌즈 1(Hopfield).** 연속 Hopfield 에너지의 정의, CCCP 1스텝 = attention 갱신 명제, 지수적 저장 용량 정리 — attention이 에너지 하강의 *정확한 재현*임.
- **렌즈 2(Nadaraya–Watson).** 핵·대역폭 $h$·NW 추정량의 정의, 편향–분산 절충, 온도 $\beta=1/h^2$ 대응 — softmax(점수)=Gaussian 핵 가중의 동일성.
- *(기제작 7강 심화 PDF는 본강 재제작 시 해당 절로 흡수한다 — 통합판 기준.)*

**무정지 전제 — 이 강에서 정의·정착할 것**
- 시퀀스 공간의 정의: $\bigcup_{T\ge1}(\mathbb R^p)^T$(가변 길이의 처리 규약 포함).
- RNN/LSTM cell을 **함수로 먼저**: 사양서 §2.11-6의 예시 그대로 — 가중치 거론 전에 $\mathbb R^p\times(\mathbb R^q\times\mathbb R^q)\to\mathbb R^q\times\mathbb R^q$ 사상으로; unroll=합성, BPTT=그 합성의 연쇄법칙(4강 재정착).
- "장기 의존성 한계"의 바인딩: $\|\partial h_t/\partial h_{t-k}\|$의 지수 감쇠(4강 따름)로; 게이트=항등 경로 생성의 해소 메커니즘(§2.10 — 점화식의 곱셈 결합을 덧셈 경로로 우회).
- "정보 병목"의 정량화: 상호정보(0강 재정착)와 **Fano 부등식의 정의·진술(본 커리큘럼 최초 등장 지점)** — 고정 차원 벡터를 거치는 채널의 한계.
- attention=softmax 가중 볼록결합 *사상*의 정의 — 점수 함수는 역할·성질로 먼저(§2.11-7), additive($\tanh$ 망)는 특수화로 나중.
- 확률변수/실현의 구분: 학습 말뭉치 문장쌍의 지위(경험분포) 명시.

**추천 논문/자료**
- [본강] Hochreiter & Schmidhuber (1997), *LSTM*; Bahdanau et al. (2015)
- [심화] Ramsauer et al. (2020, *Hopfield Networks is All You Need*); Nadaraya (1964)/Watson (1964); Yuille & Rangarajan (2003, CCCP)

**실습 과제:** 기본 — LSTM+attention 소형 기계번역. 심화 — (a) attention 반복 적용=에너지 단조 하강 실측, (b) NW 대역폭 스윕의 편향–분산, (c) softmax(내적)↔Gaussian 핵 가중 동일성 수치 확인. (코드: `lab07_seq2seq_attention.py`)

**연결(§2.15).** NW 줄기 → 12강($n^{-4/(d+4)}$ 차원의 저주)·18강(RAG=NW)·22강(softmax=Gaussian 핵 random feature) — 본 커리큘럼 상호참조의 척추 1. Bahdanau↔8강 scaled dot-product는 동명이물(유형 4): 공통점(softmax 볼록결합)·차이점(점수 형태·self·recurrence 제거)을 8강 진입 전 다리로.

---

## 8강. Transformer 해부

**이론**
self-attention, multi-head attention, 위치 인코딩, position-wise FFN, residual+norm 스택. "왜 attention만으로 충분한가"의 핵심.

**수식 유도 — 본강**
- scaled dot-product attention $\text{softmax}(QK^\top/\sqrt{d_k})V$, $\sqrt{d_k}$ 스케일링의 분산 근거.
- multi-head 분할·결합의 행렬 형태.

**수식 유도 — 수리 심화** *(구 부록 통합 — 기제작 PDF "트랜스포머의 수리 이론" 흡수)*
- **등변성.** 순열군 작용의 정의, 정리(self-attention의 순열 등변성)와 따름(위치 정보의 필연 — PE 없는 모델의 한계, §2.10).
- **표현력.** 문맥 사상 클래스에 대한 보편 근사 진술; **랭크 붕괴** — Dobrushin 수축 계수의 정의와 attention 층 합성 하 수축 진술(LayerNorm·residual의 역할 한계 포함).
- **계산 능력.** 회로 복잡도·균일성·**TC⁰의 정의(본 커리큘럼 최초 정의 지점 — 17강이 재정착)**, 고정 깊이 Transformer의 한계(PARITY 등)와 Chomsky 위계 대응; 1강 Minsky–Papert 차수와의 다리.
- **회로·동역학.** QK/OV 회로·귀납 헤드의 정의; ICL=경사하강 대응 진술(가정·범위 라벨); NTK·평균장 극한의 정의와 지위.
- *(기제작 8강 심화 PDF는 본강 재제작 시 해당 절들로 흡수한다.)*

**무정지 전제 — 이 강에서 정의·정착할 것**
- 토큰 임베딩=행 추출 $E_x$(AI 관습 표기 — §0.0-B 명시), $Q,K,V$=선형상(차원 전수 명시).
- scaled dot-product의 **완전 행렬형**: row-wise softmax의 명시, causal mask=상삼각 $-\infty$ 가산의 정확한 정의, $\sqrt{d_k}$ 분산 계산의 가정(성분 평균0·분산1·독립)을 가정으로.
- multi-head=부분공간 분해·재결합 사상의 정의(분할이 *어느 공간*의 직합인지).
- 기호 충돌 규약(§2.15-5): $h$ — 7강 hidden state ↔ 본강 head 수 — 를 새 기호로 분리하거나 재정의 명시.
- "attention이 정보를 끌어온다" 류 금지 — $\partial(\cdot)/\partial h_j$의 직접 항 $\alpha_{tj}I$ 존재로 치환(§2.14-5).
- 7강 Bahdanau와의 동명이물 다리(공통점/차이점)를 본격 사용 *전에*(§2.15 의무).

**추천 논문/자료**
- [본강] Vaswani et al. (2017), *Attention Is All You Need*
- [심화] Yun et al. (2020, 보편 근사); Dong, Cordonnier, Loukas (2021, 랭크 붕괴); Merrill & Sabharwal (2023, TC⁰); Elhage et al. (2021, *A Mathematical Framework for Transformer Circuits*); von Oswald et al. (2023, ICL=GD); Jacot et al. (2018, NTK)

**실습 과제:** 기본 — Transformer 인코더-디코더 전체 구현. 심화 — (a) 순열 등변성의 수치 검증(PE 유/무), (b) 깊이에 따른 표현 랭크 붕괴 실측, (c) toy ICL의 GD 대응 곡선. (코드: `lab08_transformer.py`)

**연결(§2.15).** TC⁰/회로 줄기 → 17강(CoT=깊이)·20강(회로 해석) — 상호참조의 척추 2. 등변성 → 5강·9강. ICL=GD → 3강(전처리 경사하강).

---

## 9강. 위치 표현과 장문맥

**이론**
절대 vs 상대 위치, RoPE(회전 위치 임베딩), ALiBi, 길이 외삽(length extrapolation).

**수식 유도 — 본강**
- RoPE의 회전 행렬 형태와 내적이 상대 위치만에 의존함을 유도.

**수식 유도 — 수리 심화** *(구 부록 통합: 위치 부호화의 조화해석)*
- **정리(RoPE 상대성).** $\langle R(\theta_j m)q,\;R(\theta_j n)k\rangle=\langle q,\;R(\theta_j(n-m))k\rangle$ — $m\mapsto R(\theta_j m)$가 $(\mathbb R,+)$의 1-매개변수 유니타리 표현(군 준동형)이라는 사실의 직접 귀결로 증명; RoPE = $\bigoplus_j SO(2)$ 블록 표현.
- **명제(외삽 실패).** 학습 길이 $L_{\mathrm{tr}}$ 밖 위치의 회전각이 미학습 위상으로 진입 → 저주파 분리능 저하; YaRN/NTK-aware = 주파수 재척도 $\theta_j\mapsto\theta_j/s$로 위상 분포를 학습 영역에 정합.
- **ALiBi = Toeplitz 거리 커널.** 선형 bias의 행렬 구조와 암묵적 recency 가중.

**무정지 전제 — 이 강에서 정의·정착할 것**
- 군 표현(특히 1-매개변수 유니타리 표현)의 정의와 준동형성 — 정리의 무대.
- 주파수 대역 $\theta_j=10000^{-2j/d}$의 정의·역할(스케일별 분리능); "외삽(extrapolation)"의 정식화 — 길이 일반화를 분포 지지 밖 평가로(§2.11-9 바인딩).
- Toeplitz 행렬의 정의(ALiBi 진술용).
- 8강 등변성 다리: 위치 표현=순열 등변성을 *의도적으로 깨는* 설계(따름정리 재정착).
- sinusoidal(절대)→RoPE(상대)의 §2.15-2 일반화 분기 — 무엇을 포함·확장하는지 식으로.

**추천 논문/자료**
- [본강] Su et al. (2021), *RoFormer (RoPE)*; Press et al. (2022), *ALiBi*
- [심화] Peng et al. (2023, *YaRN*) `[epistemic: 검색 미수행]`; Vaswani et al. (2017, sinusoidal)

**실습 과제:** 기본 — sinusoidal→RoPE 교체·외삽 성능 측정. 심화 — (a) RoPE 점수의 절대 shift 불변 수치 확인, (b) sinusoidal/RoPE/ALiBi 외삽 오차 곡선, (c) YaRN 재척도 전후 비교. (코드: `lab09_rope.py`)

**연결(§2.15).** 군 표현 → 5강(등변=합성곱). 주파수 분석 → 22강(HiPPO 직교 기저)과 개념 평행.

---
# Part III — 언어 모델과 스케일

## 10강. 언어 모델링 기초와 토큰화

**이론**
자기회귀 언어 모델, perplexity, BPE/WordPiece/Unigram 토큰화, 어휘 크기 설계 트레이드오프.

**수식 유도 — 본강**
- 교차 엔트로피와 perplexity의 관계 $\text{PPL} = e^{H}$.
- BPE 병합 알고리즘의 탐욕적 절차.

**수식 유도 — 수리 심화** *(구 부록 통합: 예측과 압축의 등가성·토큰화의 추정 원리)*
- **정리(예측=압축).** 모델 $p$의 산술 부호화 부호 길이 $\approx-\log_2 p(s)$ bit, 기대 길이=cross-entropy ⟹ perplexity 최소화 $\equiv$ 최적 압축(역도 성립).
- **정리(AEP; Shannon–McMillan–Breiman).** 정상 에르고딕 소스에서 $-\frac1n\log p(X_{1:n})\to H$ a.s. — 실측 perplexity가 모집단 entropy rate로 수렴하는 근거(수렴 양상 §2.16-7 명시).
- **명제(Unigram=EM).** 분할 $z$ 잠재변수의 likelihood를 EM(forward–backward/Viterbi)으로 최대화; **BPE=greedy MDL/사전 부호화**; 어휘 크기 = rate–distortion 절충(왜곡의 정의는 23강 roadmap).

**무정지 전제 — 이 강에서 정의·정착할 것**
- 준비 절(사양서 §2.6·§2.11 제10강 예시 충실 이행): 알파벳 $\Sigma$·문자열 $\Sigma^\ast$·$|s|$·어휘 $\mathcal V$(유한 토큰 집합)·$\mathcal V^\ast$·tokenizer $\tau:\Sigma^\ast\to\mathcal V^\ast$와 복호·**$\mathcal V^\ast$($\mathcal V^{\mathbb N}$) 위 측도로서의 $p$**(0강 (vi) Ionescu–Tulcea 재정착)·조건부 pmf·자기회귀 항등·nat/bit.
- 정상성·에르고딕성의 정의(AEP 진술의 전제), entropy rate의 정의와 극한 존재(subadditivity/Fekete).
- $H$의 지위 구분: 모집단 cross-entropy rate vs 경험 추정량 — PPL 실측은 후자임을 명시.
- Kraft 부등식·산술 부호화=중첩 구간 사상의 정의.
- 코드가 *실제로 계산하는* $p$(add-$k$ 평활·Jelinek–Mercer 보간 추정기)의 완전 정의와 0-확률 발산의 필연(§2.10) — 추상 모델로 끝내지 않음(§2.11-3).
- BPE의 정확한 정의: 다중집합 통계 위 병합 규칙·종료 조건·tie 규칙(§0.0-B); Unigram의 잠재 분할·E/M 단계·단조성.

**추천 논문/자료**
- [본강] Sennrich et al. (2016), *BPE*; Kudo (2018), *Unigram LM*
- [심화] Cover & Thomas, *Elements of Information Theory*(AEP); Shannon (1948); Delétang et al. (2024, *Language Modeling Is Compression*) `[epistemic: 검색 미수행]`

**실습 과제:** 기본 — BPE 구현·코퍼스 perplexity. 심화 — (a) trigram 산술 부호화의 부호 길이 vs $-\log_2 p$, (b) $-\frac1n\log p$의 entropy rate 수렴(AEP), (c) Unigram EM 1스텝 vs BPE 1병합의 likelihood 변화. (코드: `lab10_bpe_tokenizer.py`)

**연결(§2.15).** rate–distortion → 14강(NF4)·23강(양자화). entropy/CE → 11강(목적함수 정합성). $n^{-\alpha/d}$ 줄기 → 12강.

---

## 11강. 사전학습 패러다임

**이론**
GPT(causal LM) vs BERT(masked LM) vs T5(seq2seq, span corruption)의 목적함수 설계 차이와 전이학습.

**수식 유도 — 본강**
- CLM·MLM·span corruption 손실의 비교 정식화.

**수식 유도 — 수리 심화** *(구 부록 통합: 정확 밀도 대 의사가능도)*
- **명제(CLM 정합).** $p_\theta(s)=\prod_t p_\theta(s_t\mid s_{<t})$는 임의 $\theta$에서 정규화된 측도(0강 (vi)) — 잘 정의된 생성모델.
- **명제(MLM 비정합).** 학습된 조건부족 $\{p_\theta(s_i\mid s_{\setminus i})\}$은 일반적으로 어떤 결합분포의 조건부와도 양립하지 않음(compatibility 실패) — MLM은 *pseudolikelihood 추정기*이지 명시적 생성밀도가 아님; 정합 조건은 Hammersley–Clifford 형.
- **다리(denoising).** masking을 noising Markov kernel로 보면 MLM ↔ denoising — 19강 score matching의 이산 사촌(roadmap).

**무정지 전제 — 이 강에서 정의·정착할 것**
- 조건부족의 양립성(compatibility)의 정의 — "BERT가 정의하는 $p(s)$는 무엇인가"라는 질문의 정식화.
- pseudolikelihood(Besag)의 정의; Markov random field·클리크·양수성 가정과 Hammersley–Clifford 정리의 진술.
- masking 절차의 정식화: 마스크 분포·noising kernel(0강 (iv) 재정착); span corruption=구간 마스킹 목적의 정확한 정의(CLM↔MLM 보간으로서의 위치).
- "전이학습"의 바인딩(§2.11-9): 사전학습 해 근방에서의 후속 위험 최소화로 — 정의 없는 사용 금지.
- 세 손실의 비교는 *동일 무대*(같은 $\mathcal V^{\mathbb N}$ 측도 공간) 위에서 — 비교 가능성의 전제 명시.

**추천 논문/자료**
- [본강] Radford et al. (2018/2019), *GPT/GPT-2*; Devlin et al. (2019), *BERT*; Raffel et al. (2020), *T5*
- [심화] Besag (1975, pseudolikelihood); Clifford (1990, Hammersley–Clifford); Wang & Cho (2019, *BERT has a Mouth*)

**실습 과제:** 기본 — 소형 GPT 사전학습(tiny corpus). 심화 — (a) 작은 $\mathcal V$에서 CLM 정규화 합산 확인, (b) 학습된 MLM 조건부의 Gibbs 표집 분포 불일치(비정합)를 TV 거리(0강)로 수치화, (c) pseudolikelihood 일관성 한계. (코드: `lab11_pretrain_gpt.py`)

**연결(§2.15).** denoising → 19강(DSM). 정보량 → 10강. kernel → 0강 (iv).

---

## 12강. 스케일링 법칙

**이론**
멱법칙 스케일링, compute-optimal 학습, Chinchilla의 데이터-파라미터 균형 교훈, 창발(emergence) 능력 논쟁(지표 선택의 영향).

**수식 유도 — 본강**
- Kaplan/Chinchilla 형태의 손실-연산 멱법칙과 최적 배분 유도. *(v14 지위 명시: Chinchilla 배분은 멱법칙 형태를 **가정한 뒤의** Lagrange 유도이고, 멱법칙 자체는 경험적 적합 또는 아래 다양체 모형 **가정 하의** 유도다 — 둘을 §2.14-6으로 분리해 "멱법칙을 유도했다"로 합치지 않는다.)*

**수식 유도 — 수리 심화** *(구 부록 통합: 멱법칙은 왜 멱법칙인가)*
- **정리(차원→지수; resolution-limited).** 매끄러운 타깃을 내재 차원 $d$의 다양체 위 표본으로 보간할 때 test loss $\sim N^{-\alpha/d}$ — 지수가 *데이터의 기하*에서 유도됨(7강 NW $n^{-4/(d+4)}$와 동일 줄기).
- **variance-limited vs resolution-limited** 영역의 정의와 구분.
- **명제(emergence의 지위).** 매끄러운 $L(N)$에 비연속/문턱 metric을 합성하면 겉보기 급변 — 연속 metric(token loss·Brier)에서는 매끄러움 회복: "창발"의 상당수는 측정의 산물.

**무정지 전제 — 이 강에서 정의·정착할 것**
- 멱법칙 ansatz $L(N)=aN^{-\alpha}+c$의 지위: 함수형 *가정*; "적합(fit)"의 통계적 정의(log-log 회귀·잔차).
- 매끄러운 매장 다양체·내재 차원의 정의(또는 채택한 차원 개념을 명시); nonparametric 회귀율 진술의 가정(매끄러움 차수·표본 분포).
- Chinchilla 문제의 완전한 정식화: 목적(최종 손실)·제약($C\approx6ND$)·결정변수·Lagrange 조건 — "compute-optimal"의 바인딩.
- "창발(emergence)"의 바인딩(§2.11-9): metric 사상(연속 vs 문턱)의 합성으로 — 명제로 진술.
- 모든 스케일링 주장에 §2.6 좁힘 선언(어느 모형·어느 영역에서 증명/적합인가).

**추천 논문/자료**
- [본강] Kaplan et al. (2020); Hoffmann et al. (2022), *Chinchilla*; Wei et al. (2022), *Emergent Abilities*; Schaeffer et al. (2023), *Are Emergent Abilities a Mirage?*
- [심화] Sharma & Kaplan (2022, data manifold dimension); Bahri, Dyer, Kaplan, Lee, Sharma (2024, *PNAS*) `[epistemic: 검색 미수행]`

**실습 과제:** 기본 — 소규모 스케일 스윕의 멱법칙 적합. 심화 — (a) 내재 차원 $d$를 바꾼 합성 다양체 회귀에서 $\log L$–$\log N$ 기울기 $\approx-\alpha/d$, (b) 같은 매끄러운 곡선에 연속/문턱 metric을 씌워 "창발" 인공물 재현. (코드: `lab12_scaling_laws.py`)

**연결(§2.15).** $n^{-\alpha/d}$ → 7강(NW 차원의 저주)·18강(고차원 NN). RMT → 2강.

---

## 13강. 효율적 학습과 분산 시스템

**이론**
데이터/텐서/파이프라인 병렬, ZeRO 메모리 분할, mixed precision(AMP), gradient accumulation, FlashAttention의 IO-aware 설계.

**수식 유도 — 본강**
- FlashAttention의 online softmax와 메모리 복잡도 $O(N)$ 유도.

**수식 유도 — 수리 심화** *(구 부록 통합: online softmax의 대수 구조와 통신 하한)*
- **명제(결합성).** 부분상태 $(m,\ell,\mathbf o)$(블록 최댓값·정규화합·가중합)의 결합 연산 $\oplus$는 monoid — 임의 타일링·순서의 reduce가 동일 결과 ⟹ FlashAttention 정확성이 타일 크기와 무관.
- **정리(IO 하한; Hong–Kung 1981).** 크기 $M$ 빠른 메모리에서 $n\times n$ 행렬곱류의 전송량 $\Omega(n^3/\sqrt M)$ — attention 타일링이 하한에 점근 부합: "IO-aware"는 휴리스틱이 아니라 *하한 근접*.

**무정지 전제 — 이 강에서 정의·정착할 것**
- log-sum-exp·$(\max,+)$ 구조: monoid의 정의, 부분상태와 $\oplus$의 명시적 정의(결합법칙 증명의 대상).
- IO 계산 모형의 정의: red–blue pebble game(두 단계 메모리·전송 단위·허용 수) — 정리가 사는 무대.
- arithmetic intensity·roofline의 정의(연산/전송 비).
- 부동소수 형식의 정식화: 유한 표현 집합 + 반올림 사상; AMP에서 의미가 바뀌는 지점(§2.5-4)을 fp16/bf16 범위·정밀도로.
- ZeRO=옵티마이저 상태·gradient·파라미터의 분할 함수 정의와 통신량 모형; "병렬화"의 각 유형(데이터/텐서/파이프라인)을 사상 분해로 정식화.

**추천 논문/자료**
- [본강] Rajbhandari et al. (2020), *ZeRO*; Dao et al. (2022), *FlashAttention*
- [심화] Milakov & Gimelshein (2018, online softmax); Rabe & Staats (2021); Hong & Kung (1981, red-blue pebble)

**실습 과제:** 기본 — checkpointing+AMP 전후 메모리·속도. 심화 — (a) 무작위 타일 순서 reduce의 비트 동일성(결합성), (b) 전체 softmax 대비 $O(N)$ 메모리, (c) roofline 산점. (코드: `lab13_efficient_training.py`)

**연결(§2.15).** log-sum-exp → 7강(명제 동근원). kernel 재결합 $O(N)$ → 22강(linear attention).

---

## 14강. 파라미터 효율 미세조정 (PEFT)

**이론**
LoRA, QLoRA, adapter, prefix tuning. 가중치 갱신이 저랭크라는 가설.

**수식 유도 — 본강**
- LoRA의 $\Delta W = BA$ 저랭크 분해와 파라미터 절감.
- QLoRA의 4-bit NormalFloat 양자화 오차 분석.

**수식 유도 — 수리 심화** *(구 부록 통합: 미세조정의 저차원성)*
- **명제(저랭크 충분성).** 미세조정 곡률(NTK Gram)의 상위 $r$ 고유값이 에너지 $1-\epsilon$을 차지하면 rank-$r$ 갱신으로 손실 감소의 $1-\epsilon$ 회복 — 이차 모형 가정 명시.
- **정리(NF4 최적).** 평균0·분산1 정규 소스의 $2^4$ 레벨 양자화에서 분위수 기반 레벨이 기대 $\ell_2$ 왜곡 최소(Lloyd–Max 고정점) — NormalFloat는 *유도된* 코드북(블록 정규화 가정 명시).
- **LoRA 표현력 정리** 진술 `[epistemic: 검색 미수행 — Zeng & Lee 2024]`; intrinsic dimension(무작위 부분공간 학습)의 결과.

**무정지 전제 — 이 강에서 정의·정착할 것**
- 저랭크 갱신·rank의 정의(자명해도 명시), 파라미터 절감의 정확한 셈.
- intrinsic dimension의 *조작적 정의*: 무작위 $r$-부분공간 제한 학습이 목표 성능에 도달하는 최소 $r$ — 프로토콜을 수학적 진술로.
- NTK Gram·Hessian 스펙트럼·effective rank(2강 재정착); "저랭크 가설"의 지위(가설+증거)를 §2.14-6으로.
- 양자화기=유한 코드북으로의 사상, 왜곡 함수의 정의; Lloyd–Max 최적성 조건(중심·경계 조건) — 23강이 재정착.
- "adapter/prefix tuning"=가설족 제한의 정확한 형태(어느 부분공간/어느 입력 확장)로 정식화.

**추천 논문/자료**
- [본강] Hu et al. (2021), *LoRA*; Dettmers et al. (2023), *QLoRA*
- [심화] Li, Farkhoor, Liu, Yosinski (2018, intrinsic dim); Aghajanyan et al. (2021); Zeng & Lee (2024) `[epistemic: 검색 미수행]`; Lloyd (1982)/Max (1960)

**실습 과제:** 기본 — LoRA 레이어 구현·소형 LM 미세조정. 심화 — (a) 무작위 부분공간 학습의 최소 차원 측정, (b) NTK Gram 스펙트럼 집중→rank-$r$ 성능, (c) NF4 분위수 vs 균등 양자화 왜곡. (코드: `lab14_lora.py`)

**연결(§2.15).** rate–distortion → 10강·23강. 스펙트럼 집중 → 2강(RMT).

---

# Part IV — 정렬·추론

## 15강. 명령 튜닝과 RLHF

**이론**
SFT → 보상 모델(RM) → PPO 파이프라인, KL 페널티의 역할, 보상 해킹(reward hacking).

**수식 유도 — 본강**
- 보상 모델의 Bradley-Terry 선호 손실 유도.
- PPO clipped surrogate 목적함수와 KL 페널티.

**수식 유도 — 수리 심화** *(구 부록 통합 15+16 묶음의 15강 분: 정렬의 Gibbs 변분 원리 — 경로 ①)*
- **정리(Gibbs 최적해).** $\max_\pi\;\mathbb E_\pi[r]-\beta\,\mathrm{KL}(\pi\|\pi_{\mathrm{ref}})$의 유일 최적해는 $\pi^\star\propto\pi_{\mathrm{ref}}e^{r/\beta}$ — 증명은 변분/Lagrange 또는 $\mathrm{KL}(\pi\|\pi^\star)\ge0$.
- **명제(식별성).** $r$은 상수 shift·양의 척도에 비식별; 비교 그래프 비연결 시 성분 간 비교 불가(Ford 1957 연결성).
- **Goodhart 과최적화.** 대리/진짜 보상의 분리와 KL 예산 곡선(Gao et al.)의 경험적 지위; PPO 신뢰영역 = natural policy gradient/mirror descent(KL 기하)의 위치.

**무정지 전제 — 이 강에서 정의·정착할 것**
- 정렬 무대: 프롬프트 분포, 정책 $\pi(\cdot\mid x)$=Markov kernel(0강 (iv)), 보상 $r:\mathcal X\times\mathcal Y\to\mathbb R$ 가측 — $S_0$ 재정착.
- 선호 데이터 생성 모형: Bradley–Terry의 정의(random utility/Gumbel 동치 포함), 비교 그래프의 정의.
- KL 목적의 잘 정의: $\pi\ll\pi_{\mathrm{ref}}$ 전제와 $+\infty$ 규약(§2.16-2의 4).
- **PPO의 전제 무대(본 커리큘럼 최초 정의 지점):** (contextual bandit 및) MDP의 정식화 — 상태·행동의 가측 구조, 전이 kernel, 할인 $\gamma$, 가치함수 $V^\pi$·행동가치 $Q^\pi$·advantage $A^\pi$의 정의(이것 없이 surrogate는 공중에 뜬다); importance ratio·clipping의 정의.
- Fisher 정보·KL의 2차 근사·natural gradient의 정의(심화 라벨 가능).
- "보상 해킹"의 바인딩(§2.11-9): 대리 보상 최적화가 진짜 목적과 괴리하는 사건으로 — 정의 후 사용.

**추천 논문/자료**
- [본강] Christiano et al. (2017); Ouyang et al. (2022), *InstructGPT*
- [심화] Bradley & Terry (1952); Ford (1957); Gao, Schulman, Hilton (2023, overoptimization); Kakade (2002, natural PG); Levine (2018, control as inference)

**실습 과제:** 기본 — 선호 쌍으로 보상 모델 학습. 심화 — (a) 합성 보상에서 KL-정규화 최적 정책=Gibbs 형태 일치, (b) KL 예산 스윕의 over-optimization 곡선. (코드: `lab15_reward_model.py`)

**연결(§2.15).** Gibbs/지수 tilt → 16강(DPO)·17강(BoN)·19강(score=energy gradient). KL 기하 → 3강(natural gradient).

---

## 16강. RLHF를 넘어서: DPO와 직접 선호 최적화

**이론**
DPO의 closed-form 유도, RLAIF, 헌법적 AI(Constitutional AI). 보상 모델·RL 루프 없이 선호를 직접 최적화.

**수식 유도 — 본강**
- KL 제약 보상 최대화의 최적 정책이 닫힌 형태를 가지며, 이를 재매개변수화하면 DPO 손실이 됨을 유도.

**수식 유도 — 수리 심화** *(구 부록 통합 15+16 묶음의 16강 분: 경로 ② — 직접 변수변환)*
- **따름(DPO).** $r=\beta\log(\pi^\star/\pi_{\mathrm{ref}})+\beta\log Z$를 Bradley–Terry에 대입하면 $\log Z$ 소거 — 보상모델·RL 루프 없는 손실. 변수변환의 *정확성*(지지집합·측도 0 처리)을 명시.
- **명제(동일 최적해·다른 landscape).** RLHF와 DPO는 같은 표적 $\pi^\star$를 보나 목적함수의 gradient field가 다름 — 'landscape'를 정식 진술로 바인딩.
- **off-support 비결정성.** $\pi_{\mathrm{ref}}$ 지지 밖에서 해가 비결정인 자유도; IPO/Ψ-PO의 위치 `[epistemic: 검색 미수행 — Azar et al. 2024]`.

**무정지 전제 — 이 강에서 정의·정착할 것**
- 15강 Gibbs 정리의 재정착(한 줄+포인터)과, 본강이 그 *변수변환 경로*임의 §2.15-2 분기 명시.
- 변수변환의 적법성 점검 목록: $\pi^\star,\pi_{\mathrm{ref}}>0$ 영역, $\log Z$의 유한성, 소거 한 줄 증명(§2.16).
- "같은 해·다른 경로"의 정식화: 최적해 집합의 동일성 vs 최적화 동역학의 비동일성 — 혼동 금지(§2.14-6).
- RLAIF·Constitutional AI는 시스템 서술로 분리(formal/empirical 라벨, §2.10 frontier 절차).

**추천 논문/자료**
- [본강] Rafailov et al. (2023), *DPO*; Bai et al. (2022), *Constitutional AI*
- [심화] Azar et al. (2024, *IPO/Ψ-PO*) `[epistemic: 검색 미수행]`

**실습 과제:** 기본 — DPO 미세조정·RLHF 비교. 심화 — 같은 데이터에서 RLHF vs DPO가 동일 최적해로 수렴하되 경로·off-support 질량이 다름을 실측. (코드: `lab16_dpo.py`)

**연결(§2.15).** 15강과 "하나의 최적해, 두 경로" 구조(7강의 "하나의 식, 두 렌즈"와 평행). 지수 tilt → 17강 BoN.

---

## 17강. 추론과 테스트타임 연산 (2024–2025 패러다임 전환)

**이론**
o1·DeepSeek R1로 대표되는 패러다임 전환: 추론 중 연산 자원을 동적으로 배분하는 test-time compute scaling. chain-of-thought, self-consistency, s1의 "wait" 토큰을 통한 simple test-time scaling, PRM(Process Reward Model) 기반 MCTS 탐색, best-of-N, multi-round thinking. 학습-시간 스케일링이 둔화되며 추론-시간 스케일링으로 주목 이동.

**수식 유도 — 본강**
- self-consistency 다수결의 정확도 향상 분석. *(v14 정식화: 아래 Condorcet 정리가 이 시드의 1차 기준 — 가정 없는 "분석" 금지.)*
- 추론 길이(생성 토큰 수)와 정확도의 트레이드오프 모델. *(v14 정식화: 가정을 명시한 toy 모형 + §2.6 좁힘 선언으로만.)*

**수식 유도 — 수리 심화** *(구 부록 통합: test-time compute는 왜 정확도를 올리는가 — 투표·선택·깊이)*
- **정리(Condorcet).** 답안별 정답 확률 $p>1/2$·표본 독립이면 다수결 정답 확률 $\to1$($N\to\infty$; 이항 꼬리/Hoeffding — 2강 재정착으로 증명); $p<1/2$면 $\to0$; **오류 상관 시 한계가 $1/2$ 미만에 정체할 수 있음**(공통 실패 모형의 별도 명제) — self-consistency의 이득과 한계.
- **명제(BoN).** best-of-$N$ 분포의 order-statistics 유도와 $\mathrm{KL}(\mathrm{BoN}\,\|\,\mathrm{base})=\log N-\frac{N-1}{N}$; verifier 오차 시 대리 보상 과최적화(15강 Goodhart 동형).
- **다리(CoT=깊이).** 다항 길이 CoT가 고정 깊이(TC⁰, 8강 정의 재정착)를 넘어 본질적으로 순차적인 문제 부류에 도달(Merrill–Sabharwal).

**무정지 전제 — 이 강에서 정의·정착할 것**
- 표본 모형: 답안 공간·정답 사상·모델 조건부에서의 $N$표본 — **독립성은 모형 가정**임을 명시(같은 모델의 표본은 상관 가능).
- 다수결=경험측도의 최빈값으로 정의, **tie 처리 규칙 명시**(§0.0-B).
- order statistics의 정의(이산·연속 각각의 유도 가정), verifier·선택 규칙의 정의.
- "정확도"의 바인딩: 어느 분포에서의 정답 확률인지(문항 분포 명시).
- PRM·MCTS는 정의 또는 24강 roadmap(논리 무게 없음); "wait 토큰" 류 기법은 경험 라벨.
- TC⁰는 8강 재정착(여기서 재정의하지 않음 — 한 줄+포인터).

**추천 논문/자료**
- [본강] Wei et al. (2022), *Chain-of-Thought*; Wang et al. (2023), *Self-Consistency*; Snell et al. (2024); DeepSeek-R1 (2025); Muennighoff et al. (2025, *s1*)
- [심화] Beirami et al. (2024, *best-of-n guarantees*) `[epistemic: 검색 미수행]`; Merrill & Sabharwal (2024)

**실습 과제:** 기본 — CoT+self-consistency의 표본 수–정확도 곡선. 심화 — (a) 독립/상관 오류 모형의 다수결 곡선(Condorcet vs 정체), (b) BoN의 $\mathrm{KL}\approx\log N$ 실측+보상오차 과최적화, (c) toy 순차 문제에서 생각 토큰 길이↑→정확도↑. (코드: `lab17_test_time_scaling.py`)

**연결(§2.15).** CoT/TC⁰ → 8강. BoN/verifier → 24강. KL tilt → 15강. 다수결 증폭 → 26강(von Neumann)과 동형.

---

## 18강. 검색 증강과 도구 사용

**이론**
RAG, dense 임베딩·벡터 검색(ANN), 함수 호출(function calling), ReAct 에이전트 루프, MCP(Model Context Protocol). 2025년의 "슈퍼 에이전트"(Deep Research, Claude Code)와 에이전트 대상 test-time scaling(병렬 샘플링·순차 수정·verifier·rollout 다양화).

**수식 유도 — 본강**
- dense retrieval의 대조 손실(InfoNCE 형태).
- 근사 최근접 탐색(ANN)의 복잡도 직관. *(v14 정식화: "직관"은 §2.14-5상 그대로 둘 수 없는 형식 — 아래 거리 집중·JL 정리의 진술로 대체하거나 frontier 라벨.)*

**수식 유도 — 수리 심화** *(구 부록 통합: 검색의 정보기하와 RAG = Nadaraya–Watson)*
- **정리(InfoNCE 하한).** $I(X;C)\ge\log N-\mathcal L_{\mathrm{NCE}}$ (MI는 0강 (v) 재정착); $N\uparrow$의 bound 조임 vs 추정 분산 증가의 절충.
- **정리(거리 집중).** 적절한 모멘트 조건 하 고차원 i.i.d.에서 $\frac{\max_i\|x-z_i\|-\min_i\|x-z_i\|}{\min_i\|x-z_i\|}\to0$; **JL 보조정리**(상수 포함 진술)와 LSH(해시족·충돌확률의 거리 단조성) — ANN의 정당성과 한계.
- **명제(RAG=NW).** kNN-LM의 다음 토큰 분포 $\propto\sum_i\mathbf 1[v_i=\cdot]\,e^{-d(x,z_i)/\tau}$는 corpus 위 Nadaraya–Watson 가중 = 외부 메모리 attention — 7강 렌즈 2의 *문자 그대로의* 응용.

**무정지 전제 — 이 강에서 정의·정착할 것**
- 임베딩 사상·유사도(내적/코사인)의 정의; "dense retrieval"=최근접 질의의 정식화(corpus·질의·거리).
- 대조 학습의 무대: 양/음성 쌍의 분포(어디서 추출되는가) 명시 — InfoNCE의 기댓값 측도.
- LSH의 정의(해시족·충돌확률), JL의 정확한 진술(차원·왜곡·확률).
- ReAct/agent loop: 상태·행동·관측의 최소 형식 모델(§2.9-4) 또는 frontier 라벨 — MCP·"슈퍼 에이전트"는 시스템 서술로 분리.
- "검색이 성능을 높인다" 류는 경험 라벨(§2.8b).

**추천 논문/자료**
- [본강] Lewis et al. (2020), *RAG*; Yao et al. (2023), *ReAct*; Anthropic MCP (2024)
- [심화] van den Oord et al. (2018, InfoNCE); Poole et al. (2019, MI bounds); HaoChen et al. (2021, spectral contrastive); Beyer et al. (1999); Johnson–Lindenstrauss (1984); Indyk & Motwani (1998, LSH); Khandelwal et al. (2020, kNN-LM)

**실습 과제:** 기본 — 임베딩 검색+생성 RAG 파이프라인. 심화 — (a) 차원↑의 최근접 거리비 집중, (b) JL 사영의 거리 보존 산점, (c) kNN-LM 가중치=softmax(−거리/τ)=NW를 7강 코드와 동일 출력으로 확인. (코드: `lab18_rag.py`)

**연결(§2.15).** **7강 NW와 동일 식** — 본 커리큘럼 핵심 다리. InfoNCE → 19강(CLIP). 고차원 → 12강. verifier/rollout → 24강 roadmap.

---

## 19강. 멀티모달과 생성 모델

**이론**
CLIP 대조학습, 비전-언어 융합, 확산 모델(diffusion) 기초, 멀티모달 LLM. (확산/이미지 생성은 본 강의에 압축 — 현 커리큘럼 결정에 따라 별도 확장하지 않음.)

**수식 유도 — 본강**
- CLIP의 대조 손실(InfoNCE, 양방향).
- DDPM의 forward/reverse 과정과 변분 하한(ELBO), 단순화된 노이즈 예측 목적함수 유도.

**수식 유도 — 수리 심화** *(구 부록 통합: 확산 모델의 score·SDE 바닥)*
- **정리(노이즈예측=DSM; Vincent 2011).** $x_t=\sqrt{\bar\alpha_t}x_0+\sqrt{1-\bar\alpha_t}\,\epsilon$에서 $\mathbb E\|\epsilon_\theta-\epsilon\|^2$ 최소화는 $\nabla_{x_t}\log p_t$의 denoising score matching과 동치 — DDPM 목적 = score 학습.
- **정리(시간역행; Anderson 1982).** $dx=f\,dt+g\,dW$의 역행 $dx=[f-g^2\nabla\log p_t]\,dt+g\,d\bar W$; 동일 주변분포의 probability-flow ODE $dx=[f-\frac12g^2\nabla\log p_t]\,dt$ — 본강에서는 진술+가정+출처(증명 전개의 지위 라벨), SDE 존재는 0강 포인터.
- **명제(score의 존재).** 가우시안 convolution은 $t>0$에서 매끄러운 양의 밀도를 보장 ⟹ $\nabla\log p_t$ 잘 정의 — 순수수학 독자에게 결정적인 적법성 진술.
- OT·Schrödinger bridge·flow matching은 **전방 roadmap**(논리 무게 없음 — OT의 정의는 21강) `[epistemic: 검색 미수행 — Lipman et al. 2023]`.

**무정지 전제 — 이 강에서 정의·정착할 것**
- DDPM 무대: $\mathbb R^d$·르베그 지배측도·가우시안 Markov kernel의 명시 구성(0강 (iv) 정칙 조건부 재정착), forward chain의 결합 밀도 인수분해.
- ELBO 유도의 §2.16 전수 적용: Jensen 적용 지점, 조건부 밀도 조작의 RN 근거(0강 (v)), 적분–합 교환의 적법성, $\bar\alpha_t$ 등 모든 보조량 정의.
- "score"의 표기 바인딩: $\nabla_x\log p_t(x)$ — 존재 조건과 함께(위 명제).
- CLIP: 쌍 데이터 분포·양방향 InfoNCE의 정의(18강 재정착); "융합/정렬(alignment)"의 바인딩(§2.11-9: 공동 임베딩 공간에서의 근접으로).
- 역과정 파라미터화(평균/분산 선택)의 지위: 설계 선택임을 명시(§2.14-6 — "유도된 필연"으로 말하지 않음).

**추천 논문/자료**
- [본강] Radford et al. (2021), *CLIP*; Ho et al. (2020), *DDPM*; Liu et al. (2023), *LLaVA*
- [심화] Hyvärinen (2005); Vincent (2011); Anderson (1982); Sohl-Dickstein et al. (2015); Song et al. (2021, *Score-Based SDE*); Lipman et al. (2023, flow matching) `[epistemic: 검색 미수행]`

**실습 과제:** 기본 — CLIP 스타일 제로샷 분류 + 소형 DDPM. 심화 — 1–2D 합성 분포에서 (a) DSM 학습 score vs 해석적 $\nabla\log p$ 대조, (b) 역행 SDE vs prob-flow ODE 표집 비교, (c) ELBO=DSM 항의 수치 동치. (코드: `lab19_clip_diffusion.py`)

**연결(§2.15).** denoising → 11강(MLM 이산판). energy/score → 15강(Gibbs). InfoNCE → 18강. OT/SB → 21강에서 정의 후 재방문.

---

## 20강. 정렬·안전·해석가능성 종합

**이론**
mechanistic interpretability(회로·superposition), 능력 평가, 스케일러블 감독, 현재 한계(환각·견고성·장기 일관성)와 열린 문제.

**수식 유도 — 본강**
- superposition에서 feature가 거의 직교하게 배치되는 기하 직관. *(v14 정식화: 아래 거의-직교 정리의 진술로 대체 — "기하 직관"으로 두지 않는다.)*
- attention/activation patching의 인과적 개입 정식화. *(v14: do-개입의 정의를 먼저 박은 뒤에만 전개 — §2.16 의무 1.)*

**수식 유도 — 수리 심화** *(구 부록 통합: superposition의 압축센싱과 개입의 인과론)*
- **정리(거의 직교 개수).** $\mathbb R^d$에 쌍별 내적 $\le\epsilon$인 단위벡터를 $m=e^{\Omega(\epsilon^2 d)}$개 둘 수 있음(확률적 구성+JL; 상한은 Kabatiansky–Levenshtein 포인터) — 차원보다 지수적으로 많은 특징의 저간섭 중첩 저장.
- **명제(sparse 복원).** 사전의 incoherence/RIP 하에 $\ell_1$ 최소화로 활성에서 특징 복원 — "읽어내기"의 조건; Toy Models의 importance×sparsity 상전이(실험 지위 라벨).
- **명제(patching=개입).** 구조적 인과 모형(SCM)·$\mathrm{do}$ 연산자의 정의 위에서, 활성 치환의 출력 변화 = 인과 매개 효과; causal abstraction으로 회로 가설 검정 `[epistemic: 검색 미수행 — Geiger et al.]`.

**무정지 전제 — 이 강에서 정의·정착할 것**
- "feature"의 바인딩(§2.11-9): 활성 공간의 방향/선형 범함수로; "superposition"의 정의($m>d$ 특징의 선형 중첩 표현 모형).
- JL은 18강 재정착; incoherence·RIP·$\ell_1$ 복원 문제의 정의.
- SCM(변수·구조방정식·개입)의 정의 — patching 진술의 무대; "회로(circuit)"의 바인딩(8강 QK/OV 재정착: 부분 사상들의 합성으로).
- "환각·견고성·장기 일관성"은 §2.10 frontier 절차로: formal 정의가 서면 정의, 아니면 empirical 라벨 — 정의 없는 평가 지표 사용 금지.
- "스케일러블 감독"의 바인딩 또는 frontier 라벨.

**추천 논문/자료**
- [본강] Elhage et al. (2021–22), *Transformer Circuits / Toy Models of Superposition*; 최신 모델 카드·평가 프레임워크 `[epistemic: 검색 미수행 — 집필 시 검증]`
- [심화] Kabatiansky & Levenshtein (1978); Donoho (2006)/Candès–Tao (RIP); Vig et al. (2020, causal mediation); Pearl (2009, *Causality*); Geiger et al. `[epistemic: 검색 미수행]`

**실습 과제:** 기본 — 소형 Transformer의 activation patching 회로 탐색. 심화 — (a) 무작위 단위벡터 내적의 $d\uparrow$ 0-집중, (b) Toy Model sparsity 상전이 재현, (c) toy 회로의 patching 인과 효과 측정. (코드: `lab20_interpretability.py`)

**연결(§2.15).** 회로 → 8강(QK/OV·귀납헤드). JL → 18강. RIP/sparse → 22강(MLA latent).

---
# Part V — 현대 프런티어 (2024–2026)

## 21강. Mixture-of-Experts와 희소 아키텍처

**이론**
top-k 라우팅, 부하 균형(load balancing), expert 용량 제약. 2025–2026년 거의 모든 프런티어 모델(DeepSeek-V3/R1, Llama 4, Mistral Large 3, Gemini)이 MoE를 채택 — 전체 파라미터는 키우되 쿼리마다 일부 expert만 활성화. 2025년 중반 이후 초점이 파라미터 수에서 긴 학습·배포 하의 라우팅 신뢰성으로 이동.

**수식 유도 — 본강**
- top-k 게이팅과 auxiliary load-balancing loss 유도. *(v14 정식화: aux loss는 아래 균형 제약의 완화로 §2.10에 따라 유도한다 — 천하 손실의 무근거 제시 금지.)*
- expert 병렬화의 all-to-all 통신 비용.

**수식 유도 — 수리 심화** *(구 부록 통합: 희소 라우팅의 이산 최적화와 최적 수송)*
- **정리(Sinkhorn).** 비용 $C$, 한계 $\mathbf a,\mathbf b$의 entropy-정규화 OT $\min_{P\in U(\mathbf a,\mathbf b)}\langle C,P\rangle-\tfrac1\lambda H(P)$의 해는 $P=\mathrm{diag}(u)\,e^{-\lambda C}\,\mathrm{diag}(v)$이고 Sinkhorn 반복으로 수렴 — 균형 라우팅(BASE layers)의 닫힌 구조.
- **정리(Birkhoff–von Neumann).** 이중확률행렬의 집합 = 치환행렬들의 볼록포 — "균형 할당"이 사는 다면체.
- **명제(STE/Gumbel).** Gumbel-softmax는 온도 $\tau\to0^+$에서 argmax 표집으로 약수렴; straight-through estimator는 forward 이산·backward 항등의 *편향* gradient — 비미분 라우팅의 학습 가능성과 그 대가.
- **effective capacity.** 활성 파라미터 수 대비 성능의 정확한 셈 — 경험적 지위 라벨.

**무정지 전제 — 이 강에서 정의·정착할 것**
- **최적 수송의 정의(본 커리큘럼 최초 정의 지점 — 19강의 Schrödinger bridge 언급이 재방문한다):** 이산 Monge–Kantorovich 문제 — 한계 분포·결합(수송 계획)·수송 다면체 $U(\mathbf a,\mathbf b)$·비용 범함수; entropy 정규화와 $\lambda$의 역할.
- 라우팅=할당 문제의 정식화: 토큰–expert 비용행렬·용량 제약; top-k 연산의 정의(**tie 규칙 명시**, §0.0-B)와 비미분성의 명시.
- gradient 추정의 세 길(STE·Gumbel-softmax·REINFORCE)의 정의와 편향/분산 비교 — "그냥 흘려보낸다" 류 금지(4강 다리).
- load-balancing aux loss를 균형 제약(이중확률 근접)의 완화로 *유도*(§2.10 해소 메커니즘 — 제약을 직접 부과하지 않고 위반을 벌점화).
- "expert가 전문화된다"·"effective capacity"의 바인딩(§2.11-9) — 정의 또는 경험 라벨.
- all-to-all 통신 비용의 모형(13강 IO·통신 모형 재정착).

**추천 논문/자료**
- [본강] Shazeer et al. (2017), *Sparsely-Gated MoE*; Fedus et al. (2022), *Switch Transformer*; DeepSeek-V3 (2024); Llama 4 (2025)
- [심화] Lewis et al. (2021, *BASE layers*); Cuturi (2013, Sinkhorn); Birkhoff (1946); Jang et al. (2017)·Maddison et al. (2017, Gumbel-softmax); Bengio et al. (2013, STE)

**실습 과제:** 기본 — 소형 MoE 레이어 구현·라우팅 분포·expert 활용도 시각화. 심화 — (a) Sinkhorn 균형 할당의 load balance 개선, (b) Gumbel-softmax 온도↓의 argmax 수렴·gradient 분산, (c) 희소 vs dense의 동일 활성 FLOPs 성능. (코드: `lab21_moe.py`)

**연결(§2.15).** OT/Sinkhorn → 19강 SB 재방문(정규화 OT로서 — 한 줄). 이산 gradient → 4강. 통신 비용 → 13강.

---

## 22강. 효율적 어텐션과 하이브리드 아키텍처

**이론**
quadratic 한계 극복: 선형 어텐션, 상태공간모델(Mamba/SSM), 선형 어텐션(Gated Delta Networks)과 sparse MoE를 결합한 하이브리드(일정한 메모리 복잡도). KV 캐시 압축, MLA(multi-head latent attention).

**수식 유도 — 본강**
- 선형 어텐션의 커널 트릭(softmax 근사).
- SSM의 재귀-합성곱 이중성, MLA의 latent 압축.

**수식 유도 — 수리 심화** *(구 부록 통합: 선형 어텐션의 커널성과 상태공간의 제어이론 이중성)*
- **명제(커널 $O(N)$).** $\mathrm{Attn}_i=\dfrac{\phi(q_i)^\top\sum_{j\le i}\phi(k_j)v_j^\top}{\phi(q_i)^\top\sum_{j\le i}\phi(k_j)}$는 누적합 상태로 $O(N)$; $\phi$가 softmax 커널의 random feature면 softmax attention의 불편 근사(Performer/FAVOR+) — 이차 비용 제거의 *정확한* 대수(13강 결합성·7강 Gaussian↔softmax의 합류점).
- **정리(LTI=합성곱).** $h'=Ah+Bx,\ y=Ch$의 출력은 $y=\bar K*x$, $\bar K_t=C\bar A^t\bar B$(이산) — 재귀(추론)와 합성곱(병렬 학습)이 *동일 사상*의 두 계산법.
- **HiPPO.** $A,B$를 과거 신호의 $L^2(\mu)$ 직교다항식 사영이 최적이 되도록 선택 — 기억 핵의 유도.
- **selective SSM(Mamba).** 입력의존 계수가 LTI를 *파기* — 무엇이 깨지고(합성곱 표현) 무엇이 남는지(재귀 $O(N)$)의 정확한 진술. **MLA**=저랭크 KV 압축 사상 `[epistemic: 검색 미수행 — DeepSeek-V2 2024]`.

**무정지 전제 — 이 강에서 정의·정착할 것**
- 커널·특징사상의 정의(7강 재정착 — softmax(내적)=Gaussian 핵 가중의 명제를 한 줄 회상), random feature 표현의 정의(불편성·분산 진술 포함).
- LTI 시스템의 정의(상태공간 $(A,B,C)$·선형성·시불변성), 임펄스 응답의 정의, 이산화 사상(ZOH/bilinear)의 정의 — 연속↔이산의 다리(5강 ODE 재정착).
- $L^2(\mu)$·직교다항식 기저·사영의 명시(어느 측도 $\mu$에 대한 직교인지 — Legendre/Laguerre의 구분).
- "일정한 메모리 복잡도"·"장문맥 능력"의 바인딩(§2.11-9): 상태 차원 고정·정보 보존의 한계와 함께.
- 누적합 상태의 정의와 결합성(13강 monoid 재정착) — 병렬 scan 가능성의 근거.

**추천 논문/자료**
- [본강] Gu & Dao (2023), *Mamba*; DeepSeek-V2 (2024), *MLA*; Qwen3.5 하이브리드 (2026)
- [심화] Katharopoulos et al. (2020, *Transformers are RNNs*); Choromanski et al. (2021, *Performer*); Gu et al. (2020, *HiPPO*); Gu et al. (2021, *S4*)

**실습 과제:** 기본 — Mamba 블록 구현·Transformer와 장문맥 메모리·속도 비교. 심화 — (a) FAVOR+의 softmax attention 근사 오차 vs 특징 수·누적합 $O(N)$, (b) 같은 SSM의 재귀 출력=합성곱 출력(비트 일치), (c) HiPPO 사영 vs 임의 $A$의 장기 기억. (코드: `lab22_mamba.py`)

**연결(§2.15).** 7강(Gaussian↔softmax)·13강(재결합)·5강(ODE) — NW 줄기의 종착. 저랭크 KV → 14강(저랭크)·20강(RIP/latent).

---

## 23강. 추론 최적화와 양자화

**이론**
"프런티어 vs 효율 모델 클래스" 시대: 연산을 무한히 키울 수 없으니 효율을 키운다. 양자화(INT8/INT4, Blackwell의 NVFP4), speculative decoding, KV 캐시 관리(PagedAttention), 증류, 엣지 배포.

**수식 유도 — 본강**
- 양자화 오차와 스케일 선택.
- speculative decoding의 기대 가속(수용률 기반) 유도.

**수식 유도 — 수리 심화** *(구 부록 통합: 추론 최적화의 확률 구조 — 양자화와 무손실 추측 디코딩)*
- **정리(추측 디코딩 정확성).** draft $q$로 표집한 토큰을 확률 $\min(1,p/q)$로 수용하고, 거부 시 $\propto\max(0,p-q)$에서 재표집하면 출력은 **정확히** target $p$ 분포(maximal coupling 구성) — *근사 없는* 가속. 완전 증명(이산), 연속 일반화는 가정 명시.
- **명제(기대 가속).** draft 블록당 기대 수용 토큰 수 $=\sum$ 누적 수용확률; 전체 가속 = 수용률 $\alpha$와 draft 비용비의 renewal-reward 비 — 가속이 $\alpha$의 명시적 함수.
- **양자화 = rate–distortion/Lloyd–Max(14강 재정착).** outlier feature의 heavy-tail이 per-channel/group 스케일을 강제(LLM.int8()) — 분포 사실은 경험 라벨, 왜곡 분해는 정리.

**무정지 전제 — 이 강에서 정의·정착할 것**
- TV 거리(0강 (v) 재정착)·**coupling의 정의·maximal coupling 정리(본 커리큘럼 최초 정의 지점)** — "정확 보존"의 의미를 $\mathrm{TV}=0$으로 박는다.
- 수정 rejection sampling 절차의 완전 정의(수용 확률·잔차 분포의 정규화 확인 — §2.16 계산 선언으로).
- renewal 과정의 정의와 renewal-reward 정리의 진술(가정 포함) — "기대 가속"이 사는 무대.
- 양자화기·왜곡(14강 재정착), per-channel/per-tensor의 정의; "outlier/heavy-tail"의 바인딩(사용하는 지표 — 첨도·꼬리 지수 등 — 의 정의, §2.11-9).
- PagedAttention=결정론적 메모리 관리의 시스템 서술 분리(formal 주장 없음을 명시).
- draft/target 모델 쌍의 무대: 같은 $\mathcal V$ 위 두 조건부(0강 (vi)) — 분포 비교의 전제.

**추천 논문/자료**
- [본강] Frantar et al. (2023), *GPTQ*; Leviathan et al. (2023), *Speculative Decoding*; Kwon et al. (2023), *vLLM/PagedAttention*
- [심화] Chen et al. (2023, speculative sampling); Dettmers et al. (2022, *LLM.int8()*); Lindvall, *Lectures on the Coupling Method*(coupling 표준 출처)

**실습 과제:** 기본 — INT4 양자화·정확도-지연 트레이드오프. 심화 — (a) toy 분포에서 추측 디코딩 출력=target($\mathrm{TV}\approx0$) 확인, (b) 수용률 vs 기대 가속 곡선, (c) outlier 주입 시 per-tensor vs per-channel 오차. (코드: `lab23_quantization.py`)

**연결(§2.15).** rate–distortion → 10강·14강. coupling → 19강(SDE coupling — 개념 평행). TV → 0강·11강(Gibbs 불일치 측정과 동일 거리).

---

## 24강. 에이전트 시스템과 도구 통합 프런티어

**이론**
오케스트레이션: 계획·인식·추론·도구사용·검색에 특화된 에이전트들을 오케스트레이터가 조율. 다단계 도구 호출, Tool Search 아키텍처, MCP, 장기 메모리, 멀티에이전트 협업, 자율적으로 작업을 완수하는 multimodal digital workers.

**수식 유도 — 본강**
- 에이전트 test-time scaling의 정확도-rollout 관계. *(v14 정식화: 아래 formal 부분 — UCB regret·verifier 선택 위험 — 만 정리로 제시하고, 나머지는 `[epistemic: 경험적 보고]`로 분리한다 — §2.10 frontier 절차.)*
- verifier 기반 선택의 best-of-N 분석. *(v14: 17강 BoN 명제의 재정착 + verifier 오류율 $\eta$ 항 추가로만.)*

**수식 유도 — 수리 심화** *(구 부록 통합: 에이전트 탐색의 증명 가능한 핵심 — `[대부분 frontier]`, formal만 정리로)*
- **명제(UCB regret).** UCB1의 누적 후회 $O\!\big(\sum_{i:\Delta_i>0}\frac{\log T}{\Delta_i}\big)$; UCT가 트리 탐색으로 확장 — rollout 예산 증가의 이득에 *후회 한계*가 있음.
- **명제(verifier 선택 위험).** verifier 오류율 $\eta$ 하의 $N$ 후보 best 선택은 selective-prediction의 위험–커버리지 절충을 따름 — 17강 BoN과 동형.
- **명제(계획 난해성).** STRIPS 계획 결정 문제는 PSPACE-complete(Bylander) — 최적 도구 시퀀싱의 본질적 하한.
- Tool Search·장기 메모리·멀티에이전트 이득은 `[epistemic: 경험적 보고]`.

**무정지 전제 — 이 강에서 정의·정착할 것**
- (확률적) bandit의 정식화: 팔·보상 분포·정책·누적 후회의 정의 — 15강 MDP와의 관계(상태 없는 특수화)를 §2.15 분기로 명시.
- UCB1 지수의 정의와 regret 증명의 골격(신뢰 폭 — 2강 Hoeffding 재정착).
- selective prediction의 정의: 기권 규칙·커버리지·선택 위험 — "verifier로 거른다"의 정식화.
- 결정 문제·PSPACE의 정의(8강 회로 복잡도 재정착 + 공간 복잡도 한 줄 정의) — STRIPS 진술의 무대; STRIPS 자체의 정의(상태·연산자·목표).
- "오케스트레이션"·"장기 메모리"·"digital workers"의 지위: 시스템 서술·경험 라벨로 분리 — 정의 없는 수학적 주장 금지.

**추천 논문/자료**
- [본강] Yao et al. (2023), *ReAct*; Anthropic MCP (2024); *Scaling Test-time Compute for LLM Agents* (2025) `[epistemic: 검색 미수행]`
- [심화] Auer, Cesa-Bianchi, Fischer (2002, UCB1); Kocsis & Szepesvári (2006, UCT); Bylander (1994); El-Yaniv & Wiener (2010, selective prediction)

**실습 과제:** 기본 — 멀티스텝 도구 사용 에이전트 + verifier. 심화 — (a) 다중 도구 bandit의 UCB regret $\sim\log T$, (b) verifier 오류율별 best-of-N 선택 위험, (c) 소형 계획 문제의 탐색 폭발. (코드: `lab24_agent_verifier.py`)

**연결(§2.15).** BoN/verifier → 17강. MCTS → 17강 PRM·MCTS. bandit↔MDP → 15강. PSPACE → 8강 회로 줄기.

---

## 25강. 멀티모달 통합 모델과 현재 상태 종합 (2026)

**이론**
vision-language MoE 변형으로 긴 interleaved 멀티모달 문맥에서 지연-품질 제어. 언어·비전·행동을 연결하는 multisensory 생성 모델. 프롬프트를 지능적으로 라우팅하는 통합 시스템(간단한 질문은 빠른 모델, 복잡한 문제는 깊은 "thinking" 모델로 에스컬레이션). 현재 프런티어 지형(GPT-5 계열, Gemini, Claude, 오픈소스 DeepSeek/Qwen/Llama)과 미해결 문제.

**수식 유도 — 본강**
- 통합 멀티모달 손실의 결합.
- 라우팅 의사결정(난이도 추정 → 모델 선택)의 기대 비용. *(v14 정식화: 비용·오류율·정지 규칙을 정의한 뒤에만 — 아래 SPRT·cascade가 1차 기준; '난이도'는 §2.11-9 바인딩 후 사용.)*

**수식 유도 — 수리 심화** *(구 부록 통합: 적응 라우팅의 순차검정과 정지 — `[frontier]`, formal만 정리로)*
- **정리(SPRT 최적성; Wald–Wolfowitz).** 두 단순가설 사이 순차확률비 검정은 주어진 두 오류율에서 기대 표본 수 최소 — "쉬우면 빨리, 어려우면 깊게"의 최적 정지 규칙.
- **명제(cost-sensitive cascade).** 단계별 비용 $c_k$·정확도 하에서 기대비용 최소 라우팅은 임계기반 cascade(Viola–Jones 형).
- adaptive computation time(ACT)의 halting — 미분 가능 완화로서의 지위 라벨; 통합 멀티모달 품질·VL-MoE 이득은 `[epistemic: 공식 발표 기준/2차 출처]`.

**무정지 전제 — 이 강에서 정의·정착할 것**
- **정지시각(stopping time)의 정의(본 커리큘럼 최초 정의 지점):** 0강 필트레이션 재정착 위에 $\{\tau\le t\}\in\mathcal F_t$ — 순차검정·26~28강 점검 문제의 공통 무대.
- 순차검정의 정식화: 가설 쌍·우도비 과정·두 오류율 $(\alpha,\beta)$·임계 $(A,B)$ — SPRT의 완전 정의.
- cascade의 비용 모델: 단계·비용·전이(에스컬레이션) 규칙·기대비용 범함수의 정의.
- "난이도"의 바인딩: 관측 가능한 통계량(예: 우도비·불확실도 추정량)으로 — 정의 없는 사용 금지.
- 통합 멀티모달 손실: 각 항이 어느 무대(어느 모달리티의 측도 공간) 위 양인지 부착(§2.6A) — 19강 CLIP·11강 CLM 재정착.
- "프런티어 지형" 서술은 §2.8c 최전선 라벨로 분리.

**추천 논문/자료**
- [본강] Qwen3-VL (2025) `[epistemic: 검색 미수행]`; 최신 프런티어 모델 카드; 2024–2026 추론 LLM 서베이 `[epistemic: 집필 시 검증]`
- [심화] Wald & Wolfowitz (1948); Graves (2016, *ACT*); Viola & Jones (2001, cascade)

**실습 과제:** 기본 — 멀티모달 입력(텍스트+이미지) 통합 추론 파이프라인 + 난이도 기반 라우터. 심화 — (a) SPRT가 고정표본 검정보다 적은 기대표본으로 동일 오류 달성, (b) cost-sensitive cascade의 기대비용 vs 임계값. (코드: `lab25_multimodal_router.py`)

**연결(§2.15).** 정지시각 → 26~28강(점검 문제의 무대). adaptive compute → 17강. cascade↔BoN: 순차 vs 병렬의 test-time 자원 배분 분기.

---

# Part VI — Harness Engineering & 에이전틱 업무 (2025–2026)

## 26강. 프롬프트에서 하니스로: AI 엔지니어링의 진화

**이론**
AI 엔지니어링 성숙도 3단계: Phase 1 프롬프트 엔지니어링(단일 상호작용 최적화) → Phase 2(2024–2025) 컨텍스트 엔지니어링(MCP·RAG로 컨텍스트 큐레이션) → Phase 3(2026) 하니스 엔지니어링(자율성·정확성·통제). 핵심 등식 **Agent = Model + Harness**: 모델은 raw intelligence, 하니스가 이를 신뢰 가능·실행 가능하게 만든다. 최근 배포의 핵심 발견: 프로젝트 실패 원인은 reasoning 결핍이 아니라 컨텍스트·도구·런타임·신원·관측가능성이라는 비모델 운영 계층. 용어 출처(Hashimoto, OpenAI, Karpathy의 context/agentic engineering 구분).

**수식 유도 — 본강**
- Plan–Execute–Verify 루프의 형식적 정의. *(v14 정식화: 아래 상태기계 정식화가 1차 기준.)*
- 검증 통과율 $p$와 안전하게 위임 가능한 자율성 수준의 관계. *(v14 정식화: 아래 von Neumann 증폭 정리로 — '신뢰도'·'자율성'은 정의 없는 사용 금지(§2.11-9).)*

**수식 유도 — 수리 심화** *(구 부록 통합 26–28 묶음의 26강 분: 신뢰성 증폭 — 불신뢰 모델로부터 신뢰 시스템, `[frontier]` formal만 정리로)*
- **정리(신뢰성 증폭; von Neumann 1956 / Chernoff).** 부품 오류율 $p<1/2$의 출력을 $k$중 다수결(또는 독립 검증 $k$회)하면 시스템 오류율 $\le e^{-\Theta(k(1/2-p)^2)}$로 지수 감소 — 2강 Hoeffding/Chernoff 재정착으로 증명. **오류 독립성 가정이 핵심 한계**(§2.14-6 명시); 상관 오류 시 증폭 실패는 17강 Condorcet 정체와 *동형*.
- Agent = Model + Harness의 골격: 모델=확률적으로 틀리는 부품, 하니스의 게이트·검증 루프=신뢰성을 증폭하는 외곽 구조(restoring organ)로 읽는 정식화.

**무정지 전제 — 이 강에서 정의·정착할 것**
- 시스템 무대: 모델=오류율 $p$의 베르누이 부품(이 모형화 자체가 *가정*임을 명시 — 작업 동질성·정의된 정답), 검증기=1종/2종 오류율 있는 시험 — 무엇이 확률적이고 무엇이 결정론적인지 부착(§2.6A).
- Plan–Execute–Verify의 상태기계 정식화: 상태·전이·게이트·종료 조건의 정의(시드의 "형식적 정의"를 실제로 수행).
- "신뢰도"=시스템 오류율, "자율성 수준"=통과율 임계 규칙(예: $k$회 연속 통과 시 위임)으로 바인딩 — 그 외 의미로의 확장은 경험 라벨.
- $k$중 검증의 독립성: 어떤 무작위성에 대한 독립인지(재표집·다른 검증기) 명시 — 17강 표본 상관 논의 재정착.
- Phase 1→3 서사·"실패 원인" 진단은 §2.8b 경험·보고 라벨(출처 명시).

**추천 논문/자료**
- [본강] Martin Fowler (2026), *Harness Engineering for coding agent users* `[epistemic: 검색 미수행]`; OpenAI Codex harness 사례; LangChain, *Agent = Model + Harness*
- [심화] von Neumann (1956, *Probabilistic Logics and the Synthesis of Reliable Organisms from Unreliable Components*); Pippenger (1985)

**실습 과제:** 기본 — 단일 프롬프트 에이전트에 검증 루프 추가·신뢰도 변화 정량 측정. 심화 — 부품 오류율 $p<1/2$에서 $k$중 검증의 시스템 오류율 지수 감소(독립) vs 상관 시 정체. (코드: `lab26_harness_basics.py`)

**연결(§2.15).** 증폭=Condorcet의 시스템 판본 → 17강. 검증기 선택 → 24강. 게이트 메커니즘 → 27강. 점검 빈도 → 28강(25강 정지시각 위에서).

---

## 27강. 프로덕션 하니스 설계: 제약·피드백·관측가능성

**이론**
핵심 원리: 에이전트가 실수할 때마다 다시는 같은 실수를 못 하도록 하니스를 엔지니어링한다. 프롬프트로 "표준을 따르라"는 확률적 준수 vs 위반 시 PR을 차단하는 린터의 결정론적 강제. 5계층 하니스(도구·미들웨어·메모리·가드레일·관측가능성), AGENTS.md, CI 통합 검증, 샌드박스 실행. ablation 결과 성능 향상은 도구·미들웨어·장기 메모리에 기인(산문 전략은 전이되지 않음). AI 생성 코드의 보안 결함 급증이 하니스 필요성의 실증적 근거.

**수식 유도 — 본강**
- 결정론적 게이트의 오류 차단율과 잔여 위험. *(v14 정식화: 아래 게이트 명제 — 조건부 분포와 잔여 오류 — 가 1차 기준.)*
- observability-driven 하니스 자동 진화의 목적함수. *(v14: 정식화 가능하면 정의, 아니면 frontier 라벨로 분리.)*

**수식 유도 — 수리 심화** *(구 부록 통합 26–28 묶음의 27강 분)*
- **명제(결정론적 게이트의 메커니즘; §2.10 해소 구분).** 게이트(린터·테스트) $G$는 모델의 출력 분포 $P$를 *교정하지 않는다* — 위반 사건 $\{G=\text{fail}\}$의 출력을 *차단*하여, 시스템 출력 분포가 **조건부 분포 $P(\cdot\mid G=\text{pass})$**가 되게 한다; 잔여 오류는 $P(\mathrm{err}\mid\mathrm{pass})\le P(\mathrm{err}\cap\mathrm{pass})/P(\mathrm{pass})$로 게이트의 검출력이 직접 제한.
- **명제(확률적 준수와의 차이).** 프롬프트 지시는 출력 분포를 $P\to P'$로 *이동*시킬 뿐 위반 사건에 질량을 남긴다 — "상태가 제약을 만족"(차단) vs "병리를 일으킨 양을 교정"(이동)의 §2.10 구분이 두 강제 방식의 수학적 차이.
- observability-driven 자동 진화·5계층의 이득은 `[epistemic: 경험적 보고]`.

**무정지 전제 — 이 강에서 정의·정착할 것**
- 게이트의 정식화: 출력 공간 위 가측 지시함수(또는 시험) $G$, 통과 사건, **조건부 분포 $P(\cdot\mid\mathrm{pass})$의 정의**(0강 (iv) 정칙 조건부 재정착 — $P(\mathrm{pass})>0$ 전제 명시, §2.16).
- "잔여 위험"=$P(\mathrm{err}\mid\mathrm{pass})$로 바인딩; 게이트의 1종/2종 오류(과차단·누락)의 정의와 절충.
- "확률적 준수"=프롬프트 조건화에 의한 분포 변화로 정식화 — 위반 질량 잔존 명제의 무대.
- 피드백 루프("같은 실수를 못 하도록")의 정식화: 게이트 집합의 단조 증가 열로 — 잔여 오류의 단조성 진술(가정 포함) 또는 경험 라벨.
- 5계층·AGENTS.md·샌드박스는 시스템 서술로 분리; ablation 주장에는 출처·라벨.

**추천 논문/자료**
- [본강] *Agentic Harness Engineering: Observability-Driven Automatic Evolution of Coding-Agent Harnesses* (arXiv, 2026) `[epistemic: 검색 미수행]`; awesome-harness-engineering; IEEE CAI 2026, *Engineering Trustworthy Multi-Agent Systems* `[epistemic: 검색 미수행]`
- [심화] (조건화·검정의 표준 출처는 0강 Kallenberg 재사용)

**실습 과제:** 기본 — 린터·테스트·pre-commit 훅을 결정론적 가드레일로 결합, 회귀 차단 검증 루프. 심화 — 결정론적 게이트 통과 분포의 잔여 오류 ≈ 0 vs 확률적 준수(프롬프트)의 잔여 위반 질량 비교 실측. (코드: `lab27_production_harness.py`)

**연결(§2.15).** 게이트=조건화 → 0강 (iv). 증폭과의 결합(게이트 $k$회) → 26강. 차단 vs 이동의 §2.10 구분 → 6강(정규화의 해소 메커니즘)과 원리 평행.

---

## 28강. 코딩을 넘어: 에이전틱 엔터프라이즈와 디지털 동료

**이론**
2025년 에이전틱 AI가 코드 작성 방식을 바꿨고, 2026년은 그 변화가 SDLC 전반을 재구성하며 코딩이 사이버보안·운영·디자인·데이터 사이언스 등 비전통적 사용자에게 민주화. 2025년이 데이터와 "대화"였다면 2026년은 제안을 넘어 행동하는 "디지털 동료"의 통합. 전문화 에이전트(연구자·기획자·실행자·QA)를 오케스트레이터가 조율, CRM·ERP·티켓팅·CI/CD에 권한 기반 접근, 세션 간 상태 유지. 실무 적용: 언더라이팅 데이터 수집, 재무 대사, 법무 문서 검토 등 저가치 작업 자동화.

**거버넌스(핵심 한계)**
대부분의 에이전틱 시도가 파일럿을 넘지 못하는 이유는 모델 품질이 아니라 시스템 수준 문제 — 권한 정의, 멀티에이전트 체인의 관측가능성, 신뢰성(엣지 케이스·재시도·안전한 실패), 프로세스 오너십(책임 소재). EU AI Act가 투명성·위험 분류·인간 감독 요구를 강화. 표준 자동화를 "에이전틱"으로 리브랜딩하는 과장 경계.

**수식 유도 — 본강**
- human-in-the-loop 체크포인트 빈도와 자율성-위험 트레이드오프. *(v14 정식화: 아래 점검 문제로 정식화하거나, 못 하면 frontier 라벨 — 정의 없는 '위험'·'자율성 수준' 사용 금지.)*
- 멀티에이전트 오케스트레이션의 비용·지연 모델. *(v14: 아래 최소 대기열 모형으로만 — 적용 범위 명시.)*

**수식 유도 — 수리 심화** *(구 부록 통합 26–28 묶음의 28강 분)*
- **명제(점검 빈도).** 오류 누적 과정·점검 비용 $c$·발견 시 복구의 절충에서 최적 human-in-the-loop 빈도는 inspection/optimal-stopping 문제의 해(임계형 해의 구조 진술) — 25강 정지시각 무대 위에서.
- **비용·지연의 최소 모형.** 도착·서비스의 대기열 모형과 **Little의 법칙 $L=\lambda W$**(진술·적용 가정) — 멀티에이전트 파이프라인 지연의 1차 산식; 그 이상의 스케줄링 주장은 `[epistemic: 경험적 보고]`.
- 거버넌스(권한·책임·EU AI Act)는 **규범적 진술**로 수학 주장과 분리(§2.14-6) `[epistemic: 공식 발표 기준]`.

**무정지 전제 — 이 강에서 정의·정착할 것**
- 점검 문제의 정식화: 누적 오류(또는 위험) 과정의 정의, 점검·복구 비용, 허용 정책(정지/점검 규칙 — 25강 정지시각 재정착), 기대비용 범함수 — "체크포인트 빈도"가 사는 무대.
- 대기열의 최소 정의(도착 과정·서비스 시간·시스템 내 개수 $L$·체류 시간 $W$)와 Little 법칙의 진술·적용 가정(정상성) — 과장 없는 적용 범위.
- "자율성-위험 트레이드오프"의 바인딩: 위 기대비용에서 점검 간격을 늘릴 때의 비용 곡선으로.
- "디지털 동료"·"민주화"·산업 적용 서사는 §2.8b/c 경험·최전선 라벨(출처 명시); "에이전틱 리브랜딩 경계"는 정의 문제로 — 본 강의 형식 모델(26강 상태기계)에 부합하는지로 판정.
- 권한·감사 로그: 접근 제어의 최소 정식화(주체·자원·허용 관계) 또는 시스템 서술 분리.

**추천 논문/자료**
- [본강] Anthropic, *2026 Agentic Coding Trends Report* `[epistemic: 검색 미수행]`; Camunda, 엔터프라이즈 에이전틱 자동화(EAA); MCP/A2A 프로토콜 문헌 `[epistemic: 검색 미수행]`
- [심화] Little (1961); (inspection/optimal stopping 표준 교재 — 예: Ross, *Applied Probability Models*); EU AI Act `[epistemic: 공식 발표 기준]`

**실습 과제:** 기본 — 다중 도구·권한 경계 업무 자동화 에이전트(문서 검토→요약→티켓 생성) + human-in-the-loop 게이트·감사 로그. 심화 — (a) 점검 비용–누적오류 절충의 최적 빈도 곡선, (b) 토이 파이프라인에서 Little 법칙 $L=\lambda W$ 실측. (코드: `lab28_enterprise_agent.py`)

**연결(§2.15).** 정지시각·SPRT → 25강. 증폭·게이트 → 26·27강. 전체 코스의 종착: $S_0$(0강) 위에서 모델(10강)→정렬(15–16강)→추론(17강)→시스템(26–28강)으로 이어진 무대의 일관성 점검.

---

# 부록

## 부록 A. 실습 코드 정책

- 각 강의 실습은 **전체 솔루션 코드**를 제공하며, 모든 주요 함수에 대해 **함수별 상세 설명**(입력·출력·핵심 로직·수식 대응)을 포함한다.
- 코드는 별도 파일(`lab00_*.py` ~ `lab28_*.py`)로 단계적으로 제공 예정.
- **v14 통합:** 구 부록 실습(`labAXX`)은 같은 강의 lab 파일에 **심화 항목**으로 흡수한다 — 각 강 "실습 과제"의 기본/심화 구분이 그 대응이다. 자원 제약 시 사양서 §2.12(축소·확장 정책)에 따라 기본 항목을 우선 보존한다.
- 외부 의존성은 최소화하며, 개념 증명용 소형 데이터/모델을 사용한다.

## 부록 B. 선행 권장 사항

선형대수(고유분해·SVD), 확률·정보이론(엔트로피·KL), 다변수 미적분(연쇄법칙), Python·NumPy·PyTorch 숙련. 논문 독해를 전제로 하므로 각 강의의 추천 논문을 사전 또는 병행 독해할 것을 권장한다. *(정합: 본 항목은 최소 권장이며, 강의 집필의 독자 모델은 헤더의 사양서 §2.11 기준 — 대학원 순수 해석학·측도론적 확률론, AI 무경험 — 을 따른다.)*

## 부록 C. 시드 지위와 정식화 기준 (v14)

1. 각 강 "수식 유도 — 본강" 항목은 **시드**다. 시드의 비정식 표현("~의 직관", "~의 분석", "트레이드오프 모델", "~의 관계")은 산출물의 비정식성을 정당화하지 않는다(사양서 §0.2).
2. 시드의 정식화 기준은 — ① 사양서 §2.6A(무대)·§2.9(구체 모델)·§2.10(필연성)·§2.16(계산 선언·적법성), ② **같은 강의 "수식 유도 — 수리 심화"의 정리 진술·가정과 "무정지 전제" 목록** — 순으로 우선한다. v13의 M-노트는 이 본문 통합으로 대체되었다.
3. "무정지 전제" 목록은 **비포괄 시드**다 — 사양서 §0.0 원칙 (A)–(C)가 최종 판정 기준이며, 목록 통과가 무정지 독해를 대신하지 않는다.
4. 제0강의 표준 무대 $S_0$는 모든 강의 무대 블록의 재정착 표적이다(사양서 §2.6A-5). 본 문서가 설계한 최초 정의 지점 — TV·MI(0강), Hoeffding(2강), Fano(7강), TC⁰(8강), MDP·가치함수(15강), OT(21강), coupling(23강), 정지시각(25강) — 이후의 사용은 모두 §2.11-5 재정착으로 처리한다.
5. 기존 1–28강의 주제·순서·요지는 v14에서 삭제·변경되지 않았다 — 구 부록 내용의 강별 내장과 "무정지 전제"의 추가만 있었다. 제7·8강의 기제작 심화 PDF는 본강 재제작 시 해당 절로 흡수한다.

## 부록 D. 제작 우선순위 (구 부록 티어의 v14 재해석 — 심화 절의 비중·성숙도 기준)

| 티어 | 강 | 비고 |
|---|---|---|
| A (심화 절이 풍부·확립) | 1, 2, 3, 4, 5, 9, 10, 11, 12, 19, 22 | 고전 정리 중심 — 우선 제작 |
| B | 6, 13, 14, 15, 16, 17, 18, 20, 21, 23 | 확립 정리 + 일부 라벨 필요 |
| C (frontier — formal/empirical 분리 필수) | 24, 25, 26, 27, 28 | formal 핵심(UCB·SPRT·von Neumann·게이트·Little)만 정리로 |
| 기제작 흡수 | 7, 8 | 심화 PDF 완료분 — 본강 재제작 시 흡수 |

## 부록 E. 서지 검증 의무 (불가침)

본 문서의 `[epistemic: 검색 미수행]`·`[epistemic: 공식 발표 기준]` 라벨이 붙은 2024–2026 항목(YaRN, Delétang, Bahri, Zeng–Lee, Azar, Beirami, Lipman, Geiger, DeepSeek-V2 MLA, Qwen3-VL, Fowler, *Agentic Harness Engineering*, *Scaling Test-time Compute for LLM Agents*, Anthropic Trends Report, MCP/A2A, EU AI Act 등)은 **각 강 PDF 제작 시 검색으로 1차 출처(arXiv·venue·DOI·공식 문서)를 확정**한 뒤에만 인용한다. 고전 정리(Cover·Novikoff·Baur–Strassen·Anderson·Vincent·HiPPO·von Neumann·Wald–Wolfowitz·Little 등)는 표준 출처로 충분하다.
