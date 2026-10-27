# 적용 예시: Spring Boot와 Python

두 경우 모두 **가상 프로젝트**입니다. 아래 경로·클래스·명령은 실제 저장소에서 확인한 값이 아닙니다. 복사한 표준 묶음의 실제 경로와 해당 프로젝트의 코드·명령으로 바꿉니다. 적용 순서는 [README의 세 단계](../README.md)를 따릅니다.

## Spring Boot: 새 네 계층 프로젝트

- 루트 `AGENTS.md`의 언어 선택: `docs/engineering-standards/profiles/languages/java.md`; 프레임워크 선택: `docs/engineering-standards/profiles/frameworks/spring-boot.md`.
- API와 DB를 실제 사용하는 경우에만 `standards/api-dto.md`, `standards/transactions.md`를 추가합니다.
- `docs/engineering-profile.md`의 가상 코드맵: `presentation/catalog/CatalogEntryController` → `application/catalog/CreateCatalogEntryService` → `domain/catalog/CatalogEntry` → `infrastructure/catalog/JpaEntryStore` → 해당 테스트. 포트·DTO는 실제 필요할 때만 만듭니다.
- `<ENTRYPOINT_PATH>`와 `<TEST_COMMAND>`는 프로젝트의 실제 파일과 명령으로 채웁니다. 예를 들어 `./gradlew test`는 **설명용 명령**이며 이 가상 프로젝트에서 실행·검증하지 않았습니다.

## Python: 작은 모듈 프로젝트

- 루트 `AGENTS.md`의 언어 선택: `docs/engineering-standards/profiles/languages/python.md`; 프레임워크 행은 삭제합니다. API·DB가 없다면 두 선택 행도 삭제합니다.
- `docs/engineering-profile.md`의 가상 코드맵: `catalog.py`의 `create_entry` → 저장 함수 또는 파일 경계(있는 경우) → `tests/test_catalog.py`. Spring의 네 계층이나 Java식 camelCase를 가져오지 않습니다.
- `<ENTRYPOINT_PATH>`와 `<TEST_COMMAND>`는 프로젝트에서 확인해 채웁니다. `python -m pytest`는 **설명용 명령**이며 의존성·설치 여부나 실행 결과를 보증하지 않습니다.

기존 프로젝트에 루트 `AGENTS.md`가 있으면 덮어쓰지 않습니다. 기존 권한·테스트·구조 지침을 읽고, 필요한 문서 경로와 결과 보고 항목만 합치며 충돌은 프로젝트 선택에 기록합니다.
