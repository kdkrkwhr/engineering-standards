# Spring Boot 프로필

적용 범위: **새 Spring Boot 프로젝트의 기본 선택**. 사용자가 선호하는 `presentation / application / domain / infrastructure` 네 계층을 사용합니다. 기존 프로젝트가 기능별 `controller/service/repository/dto` 구조라면 그 구조를 먼저 존중하고, 이동이 실제 이득일 때만 바꿉니다. [프레임워크 중립 선택 가이드](../../standards/architecture.md)와 [Java 표기](../languages/java.md)는 별도로 읽습니다.

## 어디에 무엇을 두는가

| 계층 | 책임과 이름의 단서 | 두지 않을 것 |
| --- | --- | --- |
| `presentation` | HTTP 입력·출력, 요청 검증, 상태 코드·오류 응답. `CatalogEntryController`, `CreateCatalogEntryRequest`, `CatalogEntryResponse`. | 영속성 쿼리, 핵심 정책 |
| `application` | 사용 사례의 순서·권한 판단 연결·트랜잭션 경계. `CreateCatalogEntryService` 또는 `CreateCatalogEntryUseCase`. 외부 저장 계약이 필요하면 `EntryStore` 같은 port. | HTTP 전용 타입, 저장 기술 세부사항 |
| `domain` | 도메인 상태·불변식·계산. `CatalogEntry`, 필요할 때 `EntryPolicy`. | Controller, Spring Data 구현, 외부 API 호출 |
| `infrastructure` | DB·파일·외부 API 구현 및 설정. `JpaEntryStore`, `ExternalCatalogClient`. | 요청 정책 결정, HTTP 응답 조립 |

기본 의존 흐름은 `presentation → application → domain`, `infrastructure → application`의 port 및 `domain`입니다. 시작 설정은 필요한 구현을 연결합니다. **SHOULD** domain을 Spring과 저장 기술에서 독립적으로 유지합니다. port의 위치는 사용 사례 계약이면 `application`, 순수 도메인 계약이면 `domain`도 가능합니다. 어느 한 위치를 모든 프로젝트의 유일한 정답으로 강제하지 않습니다.

가상의 작은 카탈로그 기능에서 **필요한 파일만** 만듭니다:

```text
com.example.catalog/
  CatalogApplication.java
  presentation/catalog/CatalogEntryController.java
  presentation/catalog/CreateCatalogEntryRequest.java
  application/catalog/CreateCatalogEntryService.java
  application/catalog/EntryStore.java          # 분리할 경계가 있을 때
  domain/catalog/CatalogEntry.java
  infrastructure/catalog/JpaEntryStore.java    # 위 계약의 구현이 필요할 때
```

`com.example.catalog`는 임의 예시이고 실제 패키지는 프로젝트의 도메인·조직·기존 코드에 맞춥니다. 기능이 늘어나면 각 계층 안에서 `catalog`, `account`처럼 기능별로 묶어 찾기 쉽게 합니다. 루트의 애플리케이션 클래스는 하위 패키지 탐색을 돕습니다([Spring Boot 공식 구조 안내](https://docs.spring.io/spring-boot/reference/using/structuring-your-code.html)).

## 선택과 읽는 순서

**MUST** 이름과 경로로 `Controller → UseCase/Service → Domain → Repository port/adapter` 흐름을 추적할 수 있게 합니다. 사람이 읽을 때는 요청 DTO와 Controller에서 입력 계약을 확인하고, 작업 클래스에서 처리 순서, domain에서 규칙, infrastructure에서 실제 저장·연동, 마지막으로 테스트를 확인합니다. `Service`와 `UseCase`는 둘 다 가능하되 한 프로젝트에서 역할이 같은 작업의 이름을 일관되게 씁니다.

작은 CRUD에 빈 계층, 모든 클래스의 인터페이스, 불필요한 DDD 객체를 만들지 않습니다. 저장 경계를 분리할 실익이 있으면 `EntryStore` port 하나와 구현을 둡니다. 단순한 프로젝트가 기존 Spring Data repository를 `application`에서 직접 쓰기로 선택할 수도 있습니다. 이는 기본 의존 방향의 **명시적 예외**이므로 이유와 교체·테스트 비용을 프로젝트 문서에 남깁니다. JPA entity와 domain 객체를 분리할지는 불변식의 복잡성·매핑 비용으로 판단합니다.

**SHOULD** 입력 오류는 `presentation`에서 계약에 맞는 응답으로, 작업 실패는 `application`에서 의미 있게 구분하고, domain 규칙 위반은 domain 언어로 표현합니다. 저장·네트워크 오류를 성공 응답으로 삼키지 않습니다. 트랜잭션 범위는 사용 사례의 일관성 경계에 맞춥니다.

테스트는 domain의 규칙 → application 작업 → 필요한 웹·저장 경계 → 중요한 실제 통합 순으로 고릅니다. 모형 테스트와 실제 DB/API 통합 결과를 구별합니다([Spring Boot 공식 테스트 안내](https://docs.spring.io/spring-boot/reference/testing/index.html)). 좋음: 가상 카탈로그 항목 생성의 입력, 불변식, 저장 결과를 각각 검증. 나쁨: Controller 모형 테스트만 통과하고 실제 저장까지 검증했다고 보고.

## 트랜잭션과 API 표현

**SHOULD** DB 트랜잭션을 `application`의 사용 사례 경계에 둡니다. 쓰기 작업은 필요한 변경을 한 경계에 묶고, 읽기 작업은 `@Transactional(readOnly = true)`를 선택할 수 있습니다. `readOnly`는 최적화 힌트이며 쓰기를 막는 보증이 아닙니다([Spring `@Transactional` API](https://docs.spring.io/spring-framework/docs/current/javadoc-api/org/springframework/transaction/annotation/Transactional.html)). 기본 선언은 `REQUIRED`, DB 기본 격리 사용, 런타임 예외·`Error` 롤백이며 checked exception의 롤백은 별도 설정이 필요합니다([Spring 선언적 트랜잭션](https://docs.spring.io/spring-framework/reference/data-access/transaction/declarative/annotations.html)). 프로젝트 버전·설정에서 실제 정책을 확인합니다.

**MUST** 기본 proxy 모드에서 같은 객체 내부의 메서드 호출은 `@Transactional` 경계를 새로 적용하지 않는다는 점을 고려합니다. 전파(`REQUIRES_NEW` 등), 롤백 예외, 격리 수준을 바꾸면 이유와 테스트를 남깁니다. `REQUIRES_NEW`는 별도 연결·풀 여유가 필요할 수 있습니다([Spring 전파 설명](https://docs.spring.io/spring-framework/reference/data-access/transaction/declarative/tx-propagation.html)). 외부 API 응답을 기다리느라 DB 트랜잭션을 오래 붙잡지 않습니다. DB 격리·락·재시도 선택은 [공통 트랜잭션 가이드](../../standards/transactions.md)를 따릅니다.

Request/Response DTO는 기본적으로 `presentation/<feature>`에, 작업 입력 `Command`는 실제 역할이 있을 때 `application/<feature>`에 둡니다. domain 객체와 영속성 entity의 분리는 필요에 따라 선택하고, 외부 API 계약과 DTO 생성·매핑 기준은 [API·DTO 가이드](../../standards/api-dto.md)에 둡니다.

예외: 보안, 프레임워크 설정, 레거시 연동은 위치가 애매할 수 있습니다. 사용자를 향한 정책은 해당 작업·domain에, 기술 구현은 infrastructure에 두는 것을 먼저 검토하고 선택 근거를 [프로젝트 문서](../../templates/project-profile.md)에 기록합니다. Spring Boot 버전별 API·테스트 도구는 사용 중인 버전의 공식 문서에서 확인합니다.
