# Python 언어 프로필

적용 범위: Python 이름·모듈·테스트 파일. 특정 런타임 버전이나 웹 프레임워크를 요구하지 않는 초기 예시입니다. [PEP 8](https://peps.python.org/pep-0008/)을 기본 참고로 삼고 프로젝트의 기존 공개 API를 우선합니다.

| 대상 | SHOULD 표기 | 예시 |
| --- | --- | --- |
| 클래스·예외·프로토콜 | `CapWords` | `CatalogEntry`, `EntryParseError`, `EntryStore` |
| 함수·메서드·변수 | `snake_case` | `find_entry`, `timeout_seconds` |
| 모듈·패키지 | 소문자 `snake_case`, 역할별 | `entry_parser.py`, `catalog/` |
| 모듈 수준 상수 | `UPPER_SNAKE_CASE` | `MAX_RETRY_COUNT` |
| 테스트 파일 | `test_*.py` | `test_entry_parser.py` |

**MUST** [공통 의미 규칙](../../standards/naming.md)을 적용합니다. `is_active`, `has_permission`처럼 참 조건을 드러냅니다. `Protocol`이나 추상 클래스는 외부 경계 또는 복수 구현이 실제로 필요할 때 선택합니다. 인터페이스를 만들기 위해 모듈을 쪼개지 않습니다.

작은 프로젝트는 `catalog.py`와 `tests/test_catalog.py`로 시작할 수 있습니다. 역할이 커지면 `catalog/api.py` → `catalog/service.py` → `catalog/store.py`와 관련 테스트 순으로 읽을 수 있게 나눕니다. 이것은 가상 예시이며 계층 패키지를 강제하지 않습니다.

좋음: `entries = load_entries()`와 `for entry in entries`. 나쁨: `data = get_data()`만 반복해 값의 의미를 감춤.

예외: 기존 혼합 표기, 외부 JSON 키, 프레임워크 콜백 이름, 생성 코드는 호환성을 우선하고 변환 지점을 명시합니다. `Manager`/`Service`는 [역할 기준](../../standards/naming.md)으로 판단합니다.
