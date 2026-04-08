# GStack

> Claude Code를 AI 개발팀으로 바꾸는 오픈소스 워크플로우 프레임워크

Garry Tan(Y Combinator CEO)이 공개한 **23개 이상의 Claude Code 전용 스킬(슬래시 커맨드) 모음**. 단일 AI 어시스턴트를 CEO, 엔지니어, 디자이너, QA, 보안 전문가 등 역할 기반 팀으로 구성해 전문적인 개발 흐름을 만든다.

---

## 핵심 특징

| 특징 | 내용 |
|------|------|
| 역할 기반 아키텍처 | 각 스킬이 특정 전문가 역할(Staff Engineer, QA, CSO 등)로 Claude를 전환 |
| 설정 기반 | CLAUDE.md 파일로 레이어드 컨텍스트 구성, 별도 GUI 없음 |
| 브라우저 자동화 | Chromium 데몬으로 100~200ms 수준의 빠른 브라우저 명령 지원 |
| 병렬 실행 | 멀티 에이전트로 10~15개 프로젝트 동시 진행 |
| MIT 라이선스 | 완전 오픈소스, 자유롭게 커스터마이징 가능 |

---

## 개발 7단계 워크플로우

```
Think → Plan → Build → Review → Test → Ship → Reflect
```

1. **Think** — 문제 검증
2. **Plan** — 제품 비전 및 기술 아키텍처 확정
3. **Build** — 고정된 플랜 기반 구현
4. **Review** — Staff Engineer 레벨 코드 감사
5. **Test** — QA 및 성능 테스트
6. **Ship** — 자동화된 릴리즈 및 배포
7. **Reflect** — 회고 및 문서화

---

## 주요 스킬 목록

### 기획 · 설계
- `/plan-ceo-review` — 제품 레벨 사고
- `/plan-eng-review` — 아키텍처 및 기술 설계
- `/plan-design-review` — 디자인 리뷰
- `/autoplan` — 자동 계획 수립

### 개발
- `/investigate` — 코드베이스 조사
- `/design-html` — HTML/CSS 구현
- `/pair-agent` — 페어 프로그래밍 에이전트
- `/learn` — 코드 학습 보조

### 품질 보증
- `/review` — 프로덕션 레벨 코드 감사
- `/qa` — 브라우저 자동화 포함 체계적 테스트
- `/cso` — 보안 리뷰

### 배포 · 릴리즈
- `/ship` — 릴리즈 관리
- `/land-and-deploy` — 배포 자동화
- `/canary` — 카나리 배포
- `/benchmark` — 성능 측정

### 안전 장치
- `/careful` — 위험 작업 전 검토 강제
- `/freeze` / `/unfreeze` — 코드 변경 동결
- `/guard` — 보호 모드

---

## 실제 성과

Garry Tan이 50일간 파트타임으로 달성한 수치:

- 주당 평균 **10,000줄** 코드 작성
- 주당 **100개** PR 처리
- 총 **600,000줄** 이상 프로덕션 코드
- GitHub 공개 48시간 내 **10,000 스타** 돌파

---

## 기존 방식과의 차이

| 구분 | 일반 AI 코딩 | GStack |
|------|-------------|--------|
| 역할 | 단일 제너럴리스트 | 전문가 역할 분리 |
| 품질 검증 | 즉흥적 | 단계별 리뷰 프로세스 |
| 배포 | 수동 | 자동화 파이프라인 |
| 안전성 | 없음 | freeze/guard 메커니즘 |
| 적합 대상 | 개인 간단 작업 | MVP 개발, 팀 운영 |

---

## 설치 방법

```bash
# GStack 레포 클론
git clone https://github.com/garrytan/gstack

# Claude Code에 스킬 등록
# ~/.claude/ 디렉토리에 스킬 파일 복사 후 Claude Code 재시작
```

---

## 참고 링크

- [GitHub](https://github.com/garrytan/gstack)
- [공식 사이트](https://gstacks.org/)
- [GStack 설명 — MindStudio](https://www.mindstudio.ai/blog/what-is-gstack-gary-tan-claude-code-framework)
