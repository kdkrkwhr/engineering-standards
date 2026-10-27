# TypeScript 언어 프로필

적용 범위: TypeScript 소스의 이름·파일 표기. 프런트엔드 프레임워크를 가정하지 않는 초기 예시이며, 대표 TypeScript 프로젝트 관례를 확인하지 못한 상태의 **제안 기본값**입니다. 채택 프로젝트의 도구·기존 관례를 먼저 확인합니다.

| 대상 | SHOULD 표기 | 예시 |
| --- | --- | --- |
| 클래스·인터페이스·타입 별칭 | `PascalCase` | `CatalogEntry`, `EntryStore` |
| 함수·메서드·변수 | `camelCase` | `findEntry`, `timeoutSeconds` |
| 재할당하지 않는 일반 `const` | 의미 있는 `camelCase` | `entryCount` |
| 모듈 전역의 고정 설정값 | 필요할 때만 `UPPER_SNAKE_CASE` | `MAX_RETRY_COUNT` |
| 파일·폴더 | 프로젝트에서 하나의 방식 선택; 기본은 `kebab-case` | `entry-parser.ts`, `catalog/` |

**MUST** [공통 의미 규칙](../../standards/naming.md)을 따릅니다. `interface IEntryStore` 같은 기계적인 `I` 접두사나 모든 `const`를 대문자로 만드는 규칙은 두지 않습니다. 입력 경계 함수 → 작업 함수 → 도메인 계산 → API·저장 어댑터 → 테스트 순서로 찾을 수 있게 파일 이름과 export를 맞춥니다.

좋음: `parseEntry`와 `entry-parser.ts`. 나쁨: 여러 책임을 담은 `utils.ts`에 `doThing`을 export.

예외: React 컴포넌트 등 프레임워크 관례, 외부 API 필드, 생성 코드, 기존 공개 이름은 프로젝트 프로필에 명시해 우선합니다. 참고: [TypeScript Handbook](https://www.typescriptlang.org/docs/handbook/intro.html). 이 문서의 파일 표기 선택을 공식 강제 규칙으로 주장하지 않습니다.
