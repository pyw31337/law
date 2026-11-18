# 렛츠로 (Let's Law) — 대한민국 법률·판례·형량 인텔리전스 독립 원장

> 대한민국 헌법재판소 결정례, 대법원 전원합의체, 하급심 양형기준 및 선고형 가중치 시뮬레이터를 전담 수집·분석·관리하는 독립 법률 서비스 및 정본 원장입니다.
> 컬처플로우(CultureFlow)가 공연 데이터를 제공하듯, 뉴스보드(NewsBoard) 및 패밀리 서비스에 법률 온톨로지 데이터를 공식 공급합니다.

---

## 1. 글로벌 온톨로지 식별자 체계 (Global Federated URN)
모든 법률 데이터는 타 서비스와의 크로스 온톨로지 매핑을 위해 고유 URN(Uniform Resource Name)을 가집니다:

- **판례 식별자**: `urn:law:precedent:{사건번호}` (예: `urn:law:precedent:2016헌나1`, `urn:law:precedent:2019도11626`)
- **법령/조문 식별자**: `urn:law:statute:{법령명}:{조문번호}` (예: `urn:law:statute:특경법:제3조`)
- **재판부/법조인 식별자**: `urn:people:person:{p_id}` 연동

---

## 2. 제공 엔드포인트 및 데이터 정본
- **전방위 리딩 판례 원장**: `data/precedents_db.json`
- **양형 시뮬레이터 웹 서비스**: `index.html`
- **액티브 크롤링 엔진**: `scripts/crawler.py`

## 3. 외부 서비스(뉴스보드 등) 데이터 연동 방식
타 서비스에서는 아래 방식으로 렛츠로의 원장 데이터를 비동기 fetch하여 사용합니다:

```javascript
// 뉴스보드 또는 외부 서비스에서 렛츠로 데이터 연동 예시
async function loadLetLawPrecedents() {
  const url = 'https://pyw31337.github.io/law/data/precedents_db.json';
  // 로컬 개발 환경 폴백
  const localFallback = '../law/data/precedents_db.json';
  try {
    const res = await fetch(url);
    return await res.json();
  } catch (e) {
    const fallbackRes = await fetch(localFallback);
    return await fallbackRes.json();
  }
}
```

---

## 4. 라이선스 및 관리 주체
- 본 서비스는 독립 마이크로서비스로 배포·운영되며, 단일 진실 공급원(Single Source of Truth, SSOT) 원칙에 따라 법률 데이터의 수정과 보강은 오직 이 레포지토리에서만 수행됩니다.
