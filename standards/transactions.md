# 트랜잭션과 격리 수준 선택

적용 범위: DB를 사용하는 프로젝트의 선택 가이드. DB·버전·스토리지 엔진이 정해지지 않았다면 격리 수준 하나를 보편적 기본값으로 단정하지 않습니다. 프로젝트의 실제 기본 설정과 변경 이유를 [적용 문서](../templates/project-profile.md)에 적습니다. Spring의 선언적 트랜잭션 사용법은 [Spring Boot 프로필](../profiles/frameworks/spring-boot.md)에 둡니다.

**MUST** 한 작업에서 함께 성공·실패해야 하는 DB 변경을 식별하고 트랜잭션 경계를 정합니다. 읽기 전용 조회와 쓰기를 구분하되, 읽기 후 쓰기의 경쟁 조건을 단순한 조회 트랜잭션으로 해결했다고 가정하지 않습니다. 외부 API 응답을 기다리는 동안 DB 트랜잭션을 오래 열어 두지 않는 것이 기본입니다.

| 수준 | SQL 표준에서 기대하는 주요 보호 | 선택 시 비용·주의 |
| --- | --- | --- |
| `READ UNCOMMITTED` | 커밋 전 데이터를 읽을 수 있음 | 정확성이 중요한 작업의 기본값으로 삼지 않음. DB가 더 강하게 구현할 수도 있음. |
| `READ COMMITTED` (RC) | dirty read 방지. 같은 트랜잭션의 재조회 결과는 바뀔 수 있음 | 읽기마다 새로 확정된 데이터를 보므로 읽기→판단→쓰기 경쟁을 별도 제어해야 함. |
| `REPEATABLE READ` (RR) | 같은 행 재조회 값의 변화 방지. 표준상 phantom은 허용 가능 | 구현에 따라 스냅샷·잠금·phantom 동작이 다름. 모든 경쟁 조건을 없애지는 못함. |
| `SERIALIZABLE` | 성공한 트랜잭션의 효과가 순차 실행과 동등 | 충돌 시 대기·중단·재시도 비용이 생길 수 있어 실제 부하에서 확인. |

`dirty read`는 미커밋 값 읽기, `nonrepeatable read`는 같은 행 재조회 값 변화, `phantom`은 조건에 맞는 행 집합의 변화입니다. 이는 [PostgreSQL의 표준 대비 표](https://www.postgresql.org/docs/current/transaction-iso.html)에 따른 개념 요약입니다. 실제 DB에서는 일반 SELECT와 잠금 읽기, 쿼리·인덱스에 따라 결과가 달라질 수 있습니다.

**공식 문서로 확인한 DB별 예:** PostgreSQL 18의 기본은 RC이고, 요청한 RU는 RC처럼 동작하며 RR에서 phantom을 허용하지 않습니다([공식 격리 문서](https://www.postgresql.org/docs/current/transaction-iso.html)). MySQL 8.4 InnoDB의 기본은 RR이고, 일관된 일반 읽기는 첫 읽기의 스냅샷을 공유하지만 잠금 읽기·범위 조건에는 별도 잠금 동작이 있습니다([공식 InnoDB 문서](https://dev.mysql.com/doc/refman/8.4/en/innodb-transaction-isolation-levels.html)). 이는 **해당 버전의 예시**이며 프로젝트의 연결 설정·실제 서버 기본값을 확인해야 합니다.

격리 수준만으로 중복 생성, lost update, 외부 요청 재시도 문제를 모두 해결했다고 보지 않습니다. **SHOULD** 불변식에 맞춰 unique 제약, 낙관적 버전 검사, 비관적 잠금, 멱등성 키, 충돌 재시도를 각각 검토합니다. 좋음: 같은 항목 중복 등록을 unique 제약과 충돌 응답으로 검증. 나쁨: RR만 켜고 중복 등록이 불가능하다고 가정. 높은 격리 수준의 재시도는 전체 작업의 부작용과 멱등성을 고려합니다.

**MUST** 동시성 주장을 할 때 목표 DB·버전에서 두 연결 이상의 실제 동시 실행을 시험하고 성공·충돌·재시도 결과를 기록합니다. H2 같은 대체 DB 테스트만으로 PostgreSQL이나 MySQL의 잠금·격리 동작이 검증됐다고 보고하지 않습니다. 작은 단일 사용자 도구 등 동시성 위험이 낮으면 DB 기본값을 유지할 수 있지만 선택과 미검증 범위를 기록합니다.
