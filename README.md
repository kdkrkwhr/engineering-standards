# Engineering Standards

프로젝트를 시작하거나 변경할 때 **에이전트에게 작업을 정확히 맡기고, 사람이 구조·코드·판단 이유를 빠르게 파악하기 위한** 선택형 기준입니다. 특정 언어, 프레임워크, 아키텍처를 모든 프로젝트에 강제하지 않습니다. 이 저장소를 만들었다는 사실만으로 다른 저장소에 규칙이 자동 적용되지는 않습니다.

두 가지 사용 흐름이 핵심입니다.

- **에이전트에게 맡길 때:** 적용할 프로필과 작업 범위·입력·출력·수용 조건·실행할 검증을 전달합니다. 결과에는 [요구→구현→테스트 추적표와 코드맵](agents/implementation.md)을 받습니다.
- **사람이 읽을 때:** [프로젝트 적용 문서](templates/project-profile.md)의 진입점에서 요청 → 처리·정책 → 저장·외부 연동 → 응답 → 테스트 순서로 파일을 찾습니다. 이름과 패키지는 그 경로를 드러내야 합니다.

공개 [용어 위키](glossary/README.md)는 이 저장소의 공통 기술 용어를 찾는 보조 지도입니다. 규칙의 원본은 아래 표준 문서이며, 프로젝트 도메인 용어와 실제 코드 노드는 해당 프로젝트에 둡니다.

## 다른 프로젝트에 적용: 세 단계

1. **표준 버전 고정:** 적용할 이 저장소의 커밋 SHA를 정하고, 그 커밋의 문서 구조 전체를 소비 프로젝트의 `docs/engineering-standards/`에 복사합니다. 전체 트리를 복사해야 문서 간 상대 링크가 유지되지만, 에이전트가 모든 문서를 읽어야 한다는 뜻은 아닙니다. 처음 설치할 빈 경로에서만 아래 예시를 사용합니다. 이미 경로가 있으면 덮어쓰지 말고 차이를 먼저 검토합니다.

   ```bash
   (
     set -e
     set -o pipefail
     STANDARDS_REPO=/absolute/path/to/engineering-standards
     STANDARDS_REV=$(git -C "$STANDARDS_REPO" rev-parse HEAD)
     mkdir -p docs
     mkdir docs/engineering-standards
     git -C "$STANDARDS_REPO" archive "$STANDARDS_REV" | tar -xf - -C docs/engineering-standards
   )
   ```

2. **프로젝트 지침 작성:** `docs/engineering-standards/templates/AGENTS.md`를 프로젝트 루트 `AGENTS.md`로, `docs/engineering-standards/templates/project-profile.md`를 `docs/engineering-profile.md`로 복사해 채웁니다. 해당 파일이 이미 있으면 **덮어쓰지 않고**, 기존 지침의 권한·구조·명령을 유지하면서 선택 문서 경로와 결과 보고 항목만 합칩니다. [Spring/Python 가상 예시](examples/agent-template-adoption.md)를 참고합니다.
3. **작업 전달:** 에이전트에게 “루트 `AGENTS.md`와 `docs/engineering-profile.md`를 따르세요. 작업 범위는 …, 입력은 …, 기대 출력은 …, 검증 기준은 …입니다”처럼 지시합니다. 관련 계약과 선택한 프로필만 읽고, 구현·테스트 증거를 요구사항과 대조합니다.

선택한 표준의 **프로젝트 내부 경로**와 고정 SHA를 적용 프로필에 기록합니다. 업데이트는 새 SHA의 파일을 별도 위치에서 비교·검토한 뒤 명시적으로 반영합니다. 자동 동기화, 전역 에이전트 설정 변경, 임의 설치는 하지 않습니다. 복사된 `docs/engineering-standards/AGENTS.md`는 표준 원본 기여 규칙이며 소비 프로젝트 구현 지침은 **프로젝트 루트** `AGENTS.md`입니다.

## 선택할 문서

프로젝트 요구사항·기존 관례를 먼저 읽고 [공통 원칙](standards/core.md)과 [명명 규칙](standards/naming.md)을 기본값으로 고릅니다. 구조 판단이 필요하면 [선택 가이드](standards/architecture.md), 해당할 때만 [API·DTO](standards/api-dto.md)와 [트랜잭션](standards/transactions.md)을 고릅니다. 사용하는 [언어](profiles/languages/)와 [프레임워크](profiles/frameworks/) 프로필만 **각각** 선택합니다. 첫판 언어는 Java, Python, Dart, C#, TypeScript이고 프레임워크 예시는 Spring Boot입니다.

`MUST`는 선택된 범위에서 지켜야 할 규칙, `SHOULD`는 기본 권장, `MAY`는 상황에 따라 택할 수 있는 선택입니다. 선택하지 않은 언어·프레임워크 프로필은 적용되지 않습니다. 플랫폼 안전·권한 제약을 지키고, 최신의 명시적 사용자 요구와 프로젝트 계약·프로젝트별 선택을 이 저장소의 일반 기본값보다 우선합니다. 충돌이 있으면 임의로 계약을 바꾸지 말고 충돌을 드러내어 해결합니다.

## 문서 지도

| 읽는 사람 | 문서 | 용도 |
| --- | --- | --- |
| 모두 | [공통 원칙](standards/core.md) · [명명 규칙](standards/naming.md) · [구조 선택](standards/architecture.md) | 요구사항, 코드, 변경 판단 |
| API·DB를 쓰는 프로젝트 | [API·DTO](standards/api-dto.md) · [트랜잭션·격리 수준](standards/transactions.md) | 계약과 동시성 선택 |
| Java / Python / Dart / C# / TypeScript 사용자 | [Java](profiles/languages/java.md) · [Python](profiles/languages/python.md) · [Dart](profiles/languages/dart.md) · [C#](profiles/languages/csharp.md) · [TypeScript](profiles/languages/typescript.md) | 언어별 표기와 예외. 해당 언어만 선택 |
| Spring Boot 사용자 | [Spring Boot](profiles/frameworks/spring-boot.md) | 네 계층의 책임과 선택지 |
| 다른 프레임워크 사용자 | [확장 템플릿](profiles/frameworks/TEMPLATE.md) | 새 프로필 추가 |
| 구현 에이전트와 검토자 | [에이전트 구현 지침](agents/implementation.md) | 추적표와 검증 보고 |
| 프로젝트 담당자 | [루트 AGENTS 템플릿](templates/AGENTS.md) · [적용 프로필 템플릿](templates/project-profile.md) · [가상 예시](examples/agent-template-adoption.md) | 실제 적용 범위와 에이전트 지침 기록 |
| 커밋 담당자 | [선택형 ignore 조각](templates/gitignore/README.md) · [위생 검사](scripts/check_hygiene.py) | 불필요한 파일과 명백한 비밀 패턴 점검 |
| 용어를 찾는 사람 | [공통 개념](glossary/common.json) · [스택별 관찰 예시](glossary/profile-examples.json) · [위키 생성 설명](glossary/README.md) | 공통 의미와 범위별 관찰 근거를 구분해 찾기 |
| 이 저장소의 기여자 | [루트 AGENTS.md](AGENTS.md) | **이 저장소만**의 기여 규칙 |

새 언어는 `profiles/languages/<language>.md`에 적용 범위, 표기 규칙, 짧은 예시, 예외와 공식 참고 문서를 적고 이 표에 연결합니다. 새 프레임워크는 [확장 템플릿](profiles/frameworks/TEMPLATE.md)을 사용합니다. 프로젝트의 기존 관례와 다른 제안은 일괄 변경하지 말고 적용 템플릿에 선택 근거와 예외를 남깁니다.

## 커밋 전 점검 범위

이 저장소의 [`.gitignore`](.gitignore)는 로컬 산출물을 제외합니다. 소비 프로젝트에는 [공통/언어별 조각](templates/gitignore/README.md)을 기존 규칙에 맞게 선택해 합칩니다. `.gitignore`는 이미 추적한 파일이나 `git add -f`를 막지 못합니다.

필요한 경로만 `git add -- <경로>`로 스테이징하고 `git add .`는 사용하지 않습니다. 커밋 전 `git status --short`, `git diff --cached --name-status`, `python3 scripts/check_hygiene.py --staged`로 **실제로 올라갈 index**를 먼저 확인합니다. 위생 검사에 걸린 파일의 내용은 출력·공유하지 말고 index에서 제외해 검토합니다. 통과한 뒤 `git diff --cached`와 `git diff --cached --check`로 변경 내용을 봅니다. `python3 scripts/check_hygiene.py --tracked`는 현재 index의 전체 tracked 파일을 확인합니다. 검사는 미추적·미스테이징 파일과 과거 커밋을 보지 않으며 명백한 파일명·비밀 형태만 찾습니다. 비밀값을 완전히 찾아내는 보증이 아닙니다.

문서 구조는 `python3 scripts/check_docs.py`, 복사 후 경로는 `python3 scripts/smoke_adoption.py`, 가짜 문자열 양성·음성 검사는 `python3 scripts/test_hygiene.py`로 확인합니다. [GitHub Actions](.github/workflows/docs.yml)는 **푸시 후** 문서·위생 검사를 실행하므로 원격 업로드 자체를 차단하지 않습니다. 훅 설치, Git 설정, 브랜치 보호 규칙은 자동 변경하지 않습니다. 이 검사는 에이전트 행동이나 예시 코드 실행을 증명하지 않습니다.

## 공개 위키와 GitHub Pages

`python3 scripts/check_glossary.py`로 [공통 개념](glossary/common.json)과 [스택별 예시](glossary/profile-examples.json)를 검사하고 `python3 scripts/build_wiki.py --out .site-build`로 기본 HTML·Markdown을 생성합니다. `python3 scripts/check_site.py .site-build --revision "$(git rev-parse HEAD)"`는 기본 산출물의 허용 파일과 링크를 검사합니다. `.site-build/`는 커밋에서 제외합니다. 위키를 바꿀 때 생성 파일을 직접 고치지 말고 용어 JSON 또는 연결된 규칙을 고칩니다.

[Pages 워크플로](.github/workflows/pages.yml)는 `main` 푸시 후 일회성 실행 환경에서 공개 위키 도구의 Python 스크립트만 `graphifyy==0.9.93`의 **로컬 코드 분석**으로 추출합니다. 생성된 코드 그래프와 자동 문서는 표준 적용 흐름의 사람이 작성한 설명 및 수동 용어 관계와 구분합니다. 외부 LLM 호출, 프로젝트·경력 정보 추출, Mac 영구 설치는 하지 않습니다. `scripts/build_architecture.py`의 입력 허용 목록과 `scripts/check_site.py --graphify`의 공개 파일 검사를 통과한 산출물만 Pages에 올립니다. 실제 배포와 주소 응답을 확인하기 전에는 새 Graphify 산출물이 공개됐다고 간주하지 않습니다. 사이트 주소는 `https://kdkrkwhr.github.io/engineering-standards/`이고 커스텀 도메인은 사용하지 않습니다. [GitHub Pages 공식 안내](https://docs.github.com/en/pages/getting-started-with-github-pages/using-custom-workflows-with-github-pages)를 따릅니다.
