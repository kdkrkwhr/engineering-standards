# 이 저장소의 기여 규칙

이 파일은 **engineering-standards 저장소를 편집하는 사람과 에이전트**에게만 적용됩니다. 복사된 표준 묶음 안에서도 그 문서 자체의 편집 범위에만 해당합니다. 소비 프로젝트의 구현 지침은 별도 [루트 AGENTS 템플릿](templates/AGENTS.md)을 프로젝트 루트에 적용하고 [프로젝트 적용 프로필](templates/project-profile.md)을 채워야 생깁니다.

- MUST: 일반 규칙과 언어·프레임워크별 선택을 분리하고, 기존 프로젝트 관례와 최신 명시 요구를 먼저 확인합니다.
- MUST: 실제 과제 코드, 시험 문제, 개인 정보, 비밀값, 내부 대화를 예시나 이력에 넣지 않습니다. 예시는 새로 만든 일반적 도메인만 사용합니다.
- MUST: 규칙을 고칠 때 이유, 짧은 좋은/나쁜 예, 필요한 예외를 함께 검토합니다. `MUST`/`SHOULD`/`MAY`의 강도를 명확히 합니다.
- MUST: 필요한 경로만 `git add -- <경로>`로 스테이징하고 `git add .`를 사용하지 않습니다. 커밋 전 상태·staged 목록과 위생 검사 결과를 먼저 보고, 통과하면 `git diff --cached`로 내용을 확인합니다. 비밀 의심 값은 출력·공유하지 않습니다.
- MUST: `python3 scripts/check_docs.py`, `python3 scripts/smoke_adoption.py`, `python3 scripts/test_hygiene.py`, `python3 scripts/check_glossary.py`, `python3 scripts/test_wiki.py`, `python3 scripts/check_hygiene.py --staged`, `git diff --cached --check`를 실행하고 결과를 보고합니다. 예시 코드를 실행하지 않았다면 실행했다고 주장하지 않습니다.
- MUST: 공개 위키에는 공개 확인된 기술 용어와 일반 예시만 넣습니다. 생성 Pages 산출물은 `scripts/check_site.py`로 허용 파일을 확인하고, 실제 배포 전에는 공개되었다고 말하지 않습니다.
- SHOULD: 새 언어·프레임워크 프로필은 적용 범위와 현재 공식 문서 링크를 적습니다. 버전에 따라 달라지는 주장은 해당 버전의 공식 자료로 확인합니다.
- SHOULD: 새 규칙이 작은 프로젝트에 불필요한 추상화나 파일을 늘리지 않는지 확인합니다.

예: 프로젝트별 선택을 프로필로 기록하는 것은 좋고, 한 프로젝트의 패키지 이름을 모든 언어의 필수 구조로 옮기는 것은 나쁩니다. 예외는 이 저장소의 문서에서 일반화하지 말고 해당 프로젝트 적용 문서에 기록합니다.
