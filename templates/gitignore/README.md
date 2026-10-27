# 선택형 `.gitignore` 조각

기존 프로젝트의 `.gitignore`를 먼저 읽고 [공통](common.gitignore)에 실제 사용하는 [Java](java.gitignore), [Python](python.gitignore), [Node/TypeScript](node.gitignore) 조각만 **수동으로 합칩니다**. 같은 패턴은 한 번만 두고, 현재 프로젝트의 fixture·생성물·배포 방식에 맞게 좁힙니다. 이 파일들은 자동 설치되거나 전역 설정을 바꾸지 않습니다.

- **SHOULD** OS 파일, 로컬 환경, 캐시, 빌드 산출물, 실행 로그를 제외합니다. 좋은 예: `.venv/`, `node_modules/`, `logs/`. 나쁜 예: `*.json`으로 계약 fixture와 설정까지 전부 제외.
- **MUST** `.env.example` 등 공개 예시에도 실제 키를 넣지 않습니다. 예시 파일 이름은 안전성을 보증하지 않습니다. 선택한 예외 패턴은 내용을 확인한 뒤 유지합니다.
- **MUST** wrapper(`gradlew`, `mvnw` 및 wrapper 파일), 의존성 lockfile, 의도한 테스트 fixture를 확장자만 보고 일괄 제외하지 않습니다. `*.log`에 해당하는 fixture는 명시적 예외를 확인하거나 해당 프로젝트에서 패턴을 제거합니다.

`.gitignore`는 **미추적 파일**에 적용됩니다. 이미 추적한 파일을 제거하지 않고 `git add -f`로 우회할 수도 있습니다([Git 공식 설명](https://git-scm.com/docs/gitignore)). 커밋 전 [위생 검사](../../scripts/check_hygiene.py)를 실행해 index를 확인합니다. 검사도 일부 명백한 패턴만 찾으므로 비밀 유출을 완전히 막는다고 주장하지 않습니다. 예외가 필요한 파일은 역할과 공개 안전성을 검토하고 프로젝트 적용 문서에 이유를 남깁니다.
