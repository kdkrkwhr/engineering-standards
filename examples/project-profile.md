# 가상 프로젝트 적용 예시: 카탈로그 항목 API

이 예시는 새로 만든 일반적 도메인입니다. 실제 서비스 코드나 설정을 옮긴 것이 아닙니다.

- 범위: 항목 하나를 등록하고 ID로 조회. 입력은 제목, 출력은 ID·제목. 존재하지 않는 ID의 실패를 구분합니다.
- 선택: [공통 원칙](../standards/core.md), [명명](../standards/naming.md), [API·DTO](../standards/api-dto.md), [트랜잭션](../standards/transactions.md), [Java](../profiles/languages/java.md), [Spring Boot](../profiles/frameworks/spring-boot.md), [에이전트 지침](../agents/implementation.md).
- 사람의 읽기 순서: `presentation/catalog/CatalogEntryController` → `application/catalog/CreateCatalogEntryService` → `domain/catalog/CatalogEntry` → `infrastructure/catalog/JpaEntryStore` → 대응 테스트.
- 용어: `entry`는 등록 항목 하나, `entries`는 목록. `timeoutSeconds`는 초 단위. `record`와 `entry`를 같은 뜻으로 혼용하지 않습니다.
- 적용 규칙: **MUST** 요청 DTO와 응답 DTO의 필드를 요구 계약에 맞춥니다. **SHOULD** 저장 계약 `EntryStore`를 application에 두되 실제 구현이 하나이고 단순 CRUD만 있으면 직접 저장소 사용을 선택할 수 있습니다.
- 예외 기록: 기존 공개 API 필드가 `entry_id`이면 외부 필드는 유지하고 내부 `entryId`와 경계에서 변환합니다. 좋은 예는 변환 위치를 테스트로 고정하는 것, 나쁜 예는 어느 곳에서는 `entryId`, 다른 곳에서는 `entry_id`를 설명 없이 섞는 것입니다.
- API 선택: `POST /catalog-entries`의 입력은 필수 `title`, 생성 응답은 ID·제목, `GET /catalog-entries/{id}`의 없는 ID는 명확한 오류 계약. 중복 요청 정책과 알 수 없는 필드 처리는 API 문서에서 정합니다.
- 트랜잭션 선택: 등록 작업을 쓰기 경계로 두고, 대상 DB·버전 확인 후 실제 기본 격리와 unique 제약·동시성 시험 계획을 기록합니다. DB가 정해지기 전에는 특정 격리 수준을 강제하지 않습니다.
- 검증: 제목 필수, 등록 후 같은 ID 조회, 없는 ID 실패를 독립 fixture로 확인. 실제 저장 통합 검증을 수행하지 않았다면 `미실행`으로 보고합니다.

작업이 더 작다면 선택한 문서와 읽기 순서, 예외만 남겨도 됩니다. 반대로 외부 API가 추가되면 해당 스키마와 실제 통합 검증 근거를 확장합니다.
