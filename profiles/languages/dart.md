# Dart 언어 프로필

**범위:** Dart 코드를 쓰는 프로젝트에서만 선택합니다. 프레임워크와 폴더 구조는 별도로 정합니다. 아래는 [Effective Dart](https://dart.dev/effective-dart/style)를 따른 초기 제안이며, 사용자 프로젝트의 확정 관례라고 주장하지 않습니다.

- **MUST:** 기존 프로젝트의 공개 API와 파일 이름을 먼저 확인하고, 변경 범위 밖의 이름을 일괄 변경하지 않습니다.
- **SHOULD:** 타입·클래스·enum은 `UpperCamelCase`, 변수·함수·메서드는 `lowerCamelCase`, 파일·디렉터리는 `lowercase_with_underscores`를 사용합니다. 단위와 복수형은 [공통 명명 규칙](../../standards/naming.md)에 따라 의미를 드러냅니다.
- **SHOULD:** `lib/`의 기능을 찾을 수 있는 이름을 쓰고 테스트를 `test/`에 대응시킵니다. 예: `lib/catalog/catalog_entry.dart`와 `test/catalog/catalog_entry_test.dart`. 이는 예시이며 모든 프로젝트에 계층 구조를 강제하지 않습니다.
- **MAY:** 라이브러리 범위의 비공개 식별자에 `_`를 사용합니다. 불필요한 `library` 이름은 만들지 않습니다. [Dart 라이브러리 설명](https://dart.dev/language/libraries)을 참고합니다.

좋은 예: `loadCatalogEntries()`와 `catalog_entries.dart`는 역할을 드러냅니다. 나쁜 예: `CatalogManager.dart`와 `doIt()`은 파일 표기와 동작 의미를 흐립니다. 기존 공개 API와 생성 코드가 다르면 프로젝트 프로필에 예외를 기록합니다. 테스트는 [에이전트 구현 지침](../../agents/implementation.md)의 독립 기대값 원칙을 따릅니다.
