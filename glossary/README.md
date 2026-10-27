# 용어사전 원본과 파생 위키

`common.json`은 공개 가능한 **언어·프레임워크 공통 개념**의 원본입니다. `profile-examples.json`은 특정 스택에서 관찰한 이름을 담는 별도 원본입니다. `id`는 범위가 드러나는 안정된 식별자이며, 같은 단어라도 역할이 다른 Spring Data 저장소와 Python 저장 모듈을 합치지 않습니다. `observed`는 링크된 공개 저장소의 이름·구조를 관찰했다는 뜻이지 모든 프로젝트에 적용할 규칙이라는 뜻이 아닙니다. `proposed` 관계는 이 저장소의 선택 가능한 설명이며, 확정된 코드 호출 그래프가 아닙니다. 적용 규칙은 각 용어의 `related_rule` 문서에서 확인합니다.

공통 개념은 이 저장소의 고정된 원본 규칙을 근거로 삼습니다. `confirmed`는 **이 저장소에서 채택한 의미**일 뿐 모든 프로젝트에 강제한다는 뜻이 아닙니다. 별도 예시는 공개 [Spring 코드](https://github.com/kdkrkwhr/auction-spot-api/tree/d2f769eff1a0fd8b7389d0db854bdd68ac6724fe/src/main/java/com/auctionspot/domain/item)의 controller/service/repository/dto 이름과 공개 [Python 코드](https://github.com/kdkrkwhr/agent-hub/blob/cfe0ac6b341f6edebbf25655fc2e7867492740bd/src/agent_hub/storage.py)의 모듈 함수 형태를 근거로 골랐습니다. 전자는 기존 코드의 기능별 묶음이며, 새 Spring 프로젝트에서 선호하는 네 계층 선택과 동일한 구조라고 주장하지 않습니다. 후자를 Spring Data Repository와 같은 개념으로 이름만 맞추지도 않습니다.

MUST: 소비 프로젝트의 도메인 용어와 실제 코드 노드는 해당 프로젝트에 [프로젝트 용어 템플릿](../templates/glossary/project.json)을 복사해 **그 프로젝트 안에서만** 기록합니다. 공개 여부를 확인하지 않은 이름, 코드, 파일 경로, 로그, 비밀값은 여기에 옮기지 않습니다. 별칭은 검색을 돕지만 코드 명명을 자동 변경하지 않습니다. 충돌하면 프로젝트의 기존 용어와 계약을 먼저 확인합니다.

프로젝트 원본의 항목은 `common.json`의 `id`, 한·영 이름, 의미·범위, 별칭·혼동어, 코드명 예시, 상태, 근거 경로, 관련 규칙을 본떠 실제 값으로 채웁니다. 예를 들어 새로 만든 목록 도메인의 ID는 `catalog-entry`처럼 정할 수 있습니다. `source`는 그 프로젝트의 실제 요구 문서나 검토된 코드 위치를 가리키게 하고, `updated`는 갱신일로 바꿉니다. 빈 템플릿 자체는 용어를 확정하지 않습니다.

`python3 scripts/check_glossary.py`는 두 원본의 중복 ID, 상태, 근거 링크, 관계 대상과 규칙 경로를 검사합니다. `python3 scripts/build_wiki.py --out .site-build`는 두 원본에서 HTML과 Markdown 설명을 만듭니다. 생성 파일은 수정하지 말고 원본 JSON 또는 연결된 규칙 문서를 고칩니다. 위키 설명은 표준을 재정의하지 않으며 관계의 `proposed` 표시는 추론·제안과 관찰 근거를 구분합니다.

[Graphify 공식 README](https://github.com/Graphify-Labs/graphify/blob/v8/README.md)의 코드 분석은 Pages 작업에서 허용한 공개 Python 스크립트에만 적용합니다. `relations`는 여전히 수동으로 검토한 용어 관계이며 Graphify 출력이 아닙니다. Graphify 자동 문서와 사람이 작성한 표준 설명은 구분합니다. 외부 모델을 사용한 위키 생성은 실행하지 않습니다. 모델·비용·전송 범위가 필요한 작업은 별도 결정이 필요합니다. 생성 캐시·로그와 큰 HTML은 커밋하지 않고 검증한 사이트 산출물만 배포합니다.
