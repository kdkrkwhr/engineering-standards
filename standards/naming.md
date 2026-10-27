# 명명 규칙: 의미가 먼저, 표기는 언어별

**MUST** 이름에서 역할과 의미를 읽을 수 있게 합니다. 대소문자·밑줄·파일 확장자는 선택한 [언어 프로필](../README.md)의 몫입니다. Java 표기를 Python이나 TypeScript에 강요하지 않습니다.

| 대상 | 공통 의미 규칙 | 좋은 예 / 나쁜 예 |
| --- | --- | --- |
| 클래스·타입 | 표현하는 개념이나 책임을 명사로 씁니다. 구현 기술을 숨겨야 할 때만 추상 이름을 씁니다. | `CatalogEntry`, `EntryParser` / `DataThing`, `CommonClass` |
| 인터페이스·프로토콜 | 제공하는 능력 또는 경계의 역할을 이름으로 드러냅니다. 구현체와 혼동하지 않습니다. | `EntryStore`, `Clock` / `IThing`, `BaseInterface`만으로 의미 대체 |
| 함수·메서드 | 동작은 동사로, 조회는 결과를 알 수 있게, 상태 판단은 불리언임을 드러냅니다. | `calculateTotal`, `findEntry`, `isExpired` / `process`, `handleData` |
| 변수·매개변수 | 값·단위·범위를 드러냅니다. 컬렉션은 복수형, 한 요소는 단수형을 기본으로 합니다. | `entries`, `entry`, `timeoutSeconds` / `data`, `list`, `timeout` |
| 불리언 | 참인 조건이 무엇인지 긍정형으로 표현합니다. 언어 관용 접두사를 사용합니다. | `isActive`, `hasPermission` / `flag`, `notInvalid` |
| 상수 | 변경되지 않는 개념의 뜻을 씁니다. 단순히 재할당하지 않는 지역 값까지 전부 대문자 상수로 만들지 않습니다. | `MAX_RETRY_COUNT` / `THREE` |
| 패키지·모듈 | 그 안의 책임과 경계를 나타냅니다. `common`, `util`은 구체적인 소속을 정할 수 없을 때만 씁니다. | `catalog`, `validation` / 무제한 `helpers` |
| 파일 | 주된 공개 개념이나 역할과 맞춥니다. 테스트 파일은 대응 대상을 찾기 쉽게 둡니다. | `entry_parser.py`, `EntryParser.java` / `misc2.py` |

## 의미를 고르는 순서

1. **MUST** 프로젝트 용어집과 공개 계약의 단어를 먼저 사용합니다. 같은 개념을 `entry`와 `record`로 무심코 섞지 않습니다.
2. **SHOULD** 수량에는 단위를 드러냅니다: `delayMillis`, `sizeBytes`. 타입이 단위를 확실히 표현한다면 중복 접미사는 생략할 수 있습니다.
3. **SHOULD** `items` 같은 복수는 모음에, `item` 같은 단수는 한 값에 씁니다. 집합 자체가 고유한 도메인 개념이면 단수 명사를 쓸 수 있습니다.
4. **SHOULD** 약어는 팀·도메인에서 널리 합의된 것만 사용합니다. `URL`·`ID`의 대소문자 표기는 언어와 기존 코드 관례에 맞춥니다.
5. **SHOULD** 쓰기 동작은 `create`·`update`·`delete`, 읽기는 `find`·`get`·`list`처럼 결과와 실패 조건을 구별합니다. `get`이 없을 때 예외인지 선택값인지 프로젝트에서 정합니다.

`Manager`, `Helper`, `Service`는 **금지어도 필수 접미사도 아닙니다**. `Service`는 애플리케이션 작업을 조정할 때, `Manager`는 실제 수명주기나 자원 관리 책임이 있을 때, `Helper`는 작고 응집된 보조 역할이 명확할 때 사용 가능합니다. `CatalogEntryService`보다 `CreateCatalogEntry`가 더 명확한 작업이라면 후자를 택할 수 있습니다. 반대로 기존 프레임워크·팀에서 `Service`가 명확한 역할을 뜻한다면 유지합니다. 이름만 바꾸려고 동작 범위를 넓히지 않습니다.

예외: 외부 API 필드, DB 스키마, 직렬화 키, 생성 코드, 공개 호환성 이름은 원형을 유지할 수 있습니다. 내부 이름과의 변환 경계를 명시하고 [프로젝트 적용 문서](../templates/project-profile.md)에 기록합니다.
