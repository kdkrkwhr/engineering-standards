# <PROJECT_NAME> 에이전트 작업 지침

이 파일은 **복사한 프로젝트의 루트 `AGENTS.md`**로 사용합니다. 적용 전 모든 자리표시자를 실제 값으로 채우고, 사용하지 않는 선택 문서 행은 삭제합니다. 이 파일만 복사해 두고 아래 표준 경로가 없는 상태로 사용하지 않습니다.

## 먼저 확인할 계약과 문서

- 프로젝트 요구·기존 계약: `<PROJECT_CONTRACT>`
- 프로젝트별 구조·용어·예외: `docs/engineering-profile.md`
- 공통 기본값: `docs/engineering-standards/standards/core.md`, `docs/engineering-standards/standards/naming.md`
- 에이전트 결과 기준: `docs/engineering-standards/agents/implementation.md`
- 선택한 언어: `<LANGUAGE_PROFILE_PATH>`
- 선택한 프레임워크: `<FRAMEWORK_PROFILE_PATH_OR_DELETE_LINE>`
- API·DTO 작업일 때: `<API_DTO_PATH_OR_DELETE_LINE>`
- DB 트랜잭션 작업일 때: `<TRANSACTION_PATH_OR_DELETE_LINE>`

**MUST** 위 경로가 이 프로젝트에 실제 있는지 확인합니다. 관련 작업에 필요한 문서와 부분만 읽습니다. 이 표준 묶음의 `README.md`나 선택하지 않은 프로필을 전부 읽을 필요는 없습니다. 최신 명시 사용자 요구와 프로젝트 계약·기존 관례·프로젝트별 선택을 일반 기본값보다 우선하고, 플랫폼 권한·안전 제약을 지킵니다.

## 이 프로젝트의 빠른 길찾기와 명령

- 입력·진입점: `<ENTRYPOINT_PATH>` — 나머지 흐름은 `docs/engineering-profile.md`의 코드 읽기 지도를 따릅니다.
- 빌드 또는 정적 검사: `<BUILD_COMMAND_OR_NONE>`
- 테스트: `<TEST_COMMAND>`
- 실제 통합 검증: `<INTEGRATION_COMMAND_OR_NONE>`

명령은 현재 프로젝트에서 확인한 뒤 채웁니다. 항목이 없다면 `없음`과 이유를 적고 명령을 만들어 내지 않습니다.

## 작업 방식과 보고

1. **MUST** 구현 전에 요청 범위·입력·출력·수용 조건과 불확실한 가정을 짧게 파악합니다. 요구를 임의로 추가·삭제하지 않고, 사용자의 단계 제어를 따릅니다. 형식적인 설계 승인 게이트를 새로 만들지 않습니다.
2. **MUST** 기존 진입점 → 처리·정책 → 저장·외부 연동 → 응답을 찾아 변경합니다. 외부 API 스키마, API 키·인증 조건, 원본 데이터 보존 범위는 확인 없이 확정하지 않습니다. README를 읽었다는 말만 하지 말고 실제 계약과 구현·검증 증거를 대조합니다.
3. **MUST** 결과에 요구사항 → 파일·심볼 → 테스트의 연결, 짧은 코드맵, 변경 이유, 실행 명령과 실제 `통과/실패/미실행` 결과를 남깁니다. 작은 수정은 표 대신 몇 줄로 충분합니다. 미실행 통합 검증을 통과로 표시하지 않습니다.
4. **MUST** 커밋 전 관련 경로만 명시적으로 스테이징하고 `git status --short`, `git diff --cached --name-status`와 `python3 docs/engineering-standards/scripts/check_hygiene.py --staged`로 먼저 대상을 확인합니다. 통과한 뒤 staged diff를 검토합니다. `git add .`는 사용하지 않습니다. 비밀 의심 값은 출력·공유하지 않습니다. 이 검사는 실제 비밀 전체를 찾아내거나 이미 원격에 올라간 내용을 취소하지 않습니다.

좋음: “없는 항목은 실패” 요구를 조회 함수·경계 테스트와 연결. 나쁨: 임의 응답만 만든 뒤 실제 연동을 검증했다고 보고. 작업 크기에 비해 문서나 도구 호출을 늘리지 않습니다.
