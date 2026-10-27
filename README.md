# Engineering Standards

프로젝트를 시작하거나 변경할 때 **에이전트에게 작업을 정확히 맡기고, 사람이 구조·코드·판단 이유를 빠르게 파악하기 위한** 선택형 기준입니다. 특정 언어, 프레임워크, 아키텍처를 모든 프로젝트에 강제하지 않습니다. 이 저장소를 만들었다는 사실만으로 다른 저장소에 규칙이 자동 적용되지는 않습니다.

두 가지 사용 흐름이 핵심입니다.

- **에이전트에게 맡길 때:** 적용할 프로필과 작업 범위·입력·출력·수용 조건·실행할 검증을 전달합니다. 결과에는 [요구→구현→테스트 추적표와 코드맵](agents/implementation.md)을 받습니다.
- **사람이 읽을 때:** [프로젝트 적용 문서](templates/project-profile.md)의 진입점에서 요청 → 처리·정책 → 저장·외부 연동 → 응답 → 테스트 순서로 파일을 찾습니다. 이름과 패키지는 그 경로를 드러내야 합니다.

## 사용 순서

1. 프로젝트의 요구사항, 계약, 기존 코드 관례를 먼저 읽습니다.
2. [공통 원칙](standards/core.md), [명명 규칙](standards/naming.md), [구조 선택 가이드](standards/architecture.md)를 읽습니다.
3. 사용하는 [언어](profiles/languages/)와 [프레임워크](profiles/frameworks/) 프로필만 선택합니다. 첫판은 Java, Python, TypeScript와 Spring Boot를 지원합니다. 프로필은 출발점이며 버전·도구·팀 관례는 프로젝트에서 확인합니다.
4. [프로젝트 적용 템플릿](templates/project-profile.md)을 프로젝트 안의 문서로 복사하여 적용 규칙, 용어, 예외를 명시합니다. [짧은 가상 예시](examples/project-profile.md)를 참고할 수 있습니다.
5. 에이전트를 사용한다면 [구현 지침](agents/implementation.md)을 프로젝트의 `AGENTS.md` 또는 작업 지시에서 **명시적으로** 연결합니다. 사람도 같은 문서를 읽고 결과를 검토할 수 있습니다.

`MUST`는 선택된 범위에서 지켜야 할 규칙, `SHOULD`는 기본 권장, `MAY`는 상황에 따라 택할 수 있는 선택입니다. 선택하지 않은 언어·프레임워크 프로필은 적용되지 않습니다. 플랫폼 안전·권한 제약을 지키고, 최신의 명시적 사용자 요구와 프로젝트 계약·프로젝트별 선택을 이 저장소의 일반 기본값보다 우선합니다. 충돌이 있으면 임의로 계약을 바꾸지 말고 충돌을 드러내어 해결합니다.

## 문서 지도

| 읽는 사람 | 문서 | 용도 |
| --- | --- | --- |
| 모두 | [공통 원칙](standards/core.md) · [명명 규칙](standards/naming.md) · [구조 선택](standards/architecture.md) | 요구사항, 코드, 변경 판단 |
| Java / Python / TypeScript 사용자 | [Java](profiles/languages/java.md) · [Python](profiles/languages/python.md) · [TypeScript](profiles/languages/typescript.md) | 언어별 표기와 예외 |
| Spring Boot 사용자 | [Spring Boot](profiles/frameworks/spring-boot.md) | 네 계층의 책임과 선택지 |
| 다른 프레임워크 사용자 | [확장 템플릿](profiles/frameworks/TEMPLATE.md) | 새 프로필 추가 |
| 구현 에이전트와 검토자 | [에이전트 구현 지침](agents/implementation.md) | 추적표와 검증 보고 |
| 프로젝트 담당자 | [적용 템플릿](templates/project-profile.md) · [가상 예시](examples/project-profile.md) | 실제 적용 범위 기록 |
| 이 저장소의 기여자 | [루트 AGENTS.md](AGENTS.md) | **이 저장소만**의 기여 규칙 |

새 언어는 `profiles/languages/<language>.md`에 적용 범위, 표기 규칙, 짧은 예시, 예외와 공식 참고 문서를 적고 이 표에 연결합니다. 새 프레임워크는 [확장 템플릿](profiles/frameworks/TEMPLATE.md)을 사용합니다. 프로젝트의 기존 관례와 다른 제안은 일괄 변경하지 말고 적용 템플릿에 선택 근거와 예외를 남깁니다.

문서 구조 검사는 `python3 scripts/check_docs.py`로 실행합니다. 이는 링크·Markdown 형태만 검사하며 예시 코드의 컴파일이나 실제 서비스 동작을 증명하지 않습니다.
