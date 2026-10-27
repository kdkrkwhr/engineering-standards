# Java 언어 프로필

적용 범위: Java 소스의 이름과 파일·패키지 표기. 선택한 프레임워크의 구조는 별도 문서를 따릅니다. 특정 Java 버전을 전제로 하지 않는 초기 예시입니다.

| 대상 | SHOULD 표기 | 예시 |
| --- | --- | --- |
| 클래스·인터페이스·enum | `UpperCamelCase` | `CatalogEntry`, `EntryStore` |
| 메서드·변수 | `lowerCamelCase` | `findEntry`, `timeoutSeconds` |
| 진짜 상수 | `UPPER_SNAKE_CASE` | `MAX_RETRY_COUNT` |
| 패키지 | 소문자, 짧은 책임·기능 이름 | `catalog`, `validation` |
| 주된 공개 타입 파일 | 타입 이름과 같은 `.java` | `CatalogEntry.java` |

**MUST** [공통 의미 규칙](../../standards/naming.md)을 먼저 적용합니다. 이름만 보고 `CatalogEntryController`가 입력 경계, `CreateCatalogEntryService`가 작업 조정, `EntryStore`가 저장 계약임을 알 수 있어야 합니다. `IEntryStore`처럼 `I`를 기계적으로 붙이지 않습니다. 인터페이스와 구현을 구별할 필요가 있다면 구현의 실제 기술·역할을 `JpaEntryStore`처럼 드러냅니다.

코드를 읽을 때는 호출 진입점 → 애플리케이션 작업 → 도메인 규칙 → 저장·외부 구현 → 대응 테스트 순서를 권장합니다. 패키지 위치는 [구조 선택](../../standards/architecture.md)과 선택한 프레임워크 프로필에서 정합니다.

좋음: `Duration timeout` 또는 `timeoutSeconds`. 나쁨: 단위가 불명확한 `timeout`과 역할이 불명확한 `DataManager`.

예외: 공개 API, 생성 코드, 기존 팀 관례는 유지할 수 있습니다. JavaBeans·직렬화 도구가 요구하는 접근자 이름도 계약에 맞춥니다. 표현 차이는 프로젝트 문서에 기록합니다. 참고: [Java Language Specification의 이름 관례](https://docs.oracle.com/javase/specs/jls/se21/html/jls-6.html#jls-6.1). 링크는 명명 참고 자료이며 이 프로필이 Java 21을 요구한다는 뜻이 아닙니다.
