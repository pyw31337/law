# Let's Law (렛츠로) 에이전트 공통 인수인계 계약

> 이 문서는 Codex, Claude, Gemini 및 로컬 에이전트가 렛츠로 법률·판례 데이터베이스를 이어서 운영하기 위한 단일 계약서입니다.

## 1. 정본 및 저장소 원칙
- **정본 경로**: `/Users/pyw31337/Developer/law`
- **단일 진실 공급원(SSOT)**: 판례, 헌법재판소 결정례, 대법원 양형기준 데이터는 오직 이 레포지토리에서만 수정·확장한다.
- **연합 소비**: 뉴스보드 등 타 서비스는 이 레포지토리의 `data/precedents_db.json`을 온디맨드 fetch하여 표시한다.

## 2. 데이터 스키마 및 URN 규정
- **판례 URN**: `urn:law:precedent:{case_no}`
- **필수 필드**: `case_no`, `court`, `date`, `case_name`, `crime_type`, `statute`, `summary`, `factors`, `sentencing_guideline`, `verdict` (`sentence`, `key_takeaway`).
- **가중/감경 인자**: 대법원 양형위원회 기준에 따라 객관적 사실(초범, 합의, 공탁금, 피해금액, 범죄집단 여부)에 기반하여 작성하며 추정치를 배제한다.
