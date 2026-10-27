# C# 언어 프로필

**범위:** C# 프로젝트에서만 선택합니다. ASP.NET 등의 프레임워크 구조는 별도로 선택합니다. 아래는 [Microsoft C# 식별자 지침](https://learn.microsoft.com/en-us/dotnet/csharp/fundamentals/coding-style/identifier-names)과 [코딩 관례](https://learn.microsoft.com/en-us/dotnet/csharp/fundamentals/coding-style/coding-conventions)를 따른 초기 제안이며, 사용자 프로젝트의 확정 관례라고 주장하지 않습니다.

- **MUST:** 기존 네임스페이스·공개 API·프로젝트 계약을 먼저 확인하고, 변경 범위 밖의 이름을 일괄 변경하지 않습니다.
- **SHOULD:** namespace·클래스·인터페이스·공개 메서드·프로퍼티는 `PascalCase`, 매개변수·지역 변수는 `camelCase`, 비공개 인스턴스 필드는 `_camelCase`로 씁니다. 인터페이스의 `I` 접두사는 C# 생태계 관례로만 적용합니다.
- **SHOULD:** 파일은 주된 타입을 드러내는 이름으로, 네임스페이스는 프로젝트의 기능 범위를 드러내는 이름으로 정합니다. 예: `Catalog/LoadEntries.cs`, `Catalog.Tests/LoadEntriesTests.cs`. 폴더와 네임스페이스가 일치하는지는 실제 프로젝트 구성을 확인합니다.
- **MAY:** 한 파일이 한 네임스페이스를 담는 새 코드에서는 파일 범위 namespace를 사용합니다. 기존 블록 형식을 바꾸기 위한 일괄 수정은 하지 않습니다. [Microsoft namespace 설명](https://learn.microsoft.com/en-us/dotnet/csharp/fundamentals/program-structure/namespaces)을 참고합니다.

좋은 예: `LoadCatalogEntries`와 `entryCount`. 나쁜 예: `Helper`와 `data1`은 책임·단위가 보이지 않습니다. 다른 관례를 쓰는 기존 프로젝트는 [적용 프로필](../../templates/project-profile.md)에 예외와 이유를 적습니다. 테스트는 [공통 원칙](../../standards/core.md)의 요구사항을 독립적으로 검증합니다.
