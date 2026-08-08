# 번역 소스 스키마

`translation/strings.json`과 `translation/cards.json`은 원본 TextAsset에서
재생성 가능한 행 기반 번역 소스다. Phase 4 주입기는 행 번호나 문자열 일부가
아닌 `asset_name`과 `key`로 행을 찾고, 해당 행의 `ko`만 한국어 대상 열에 쓴다.

## 행 필드

| 필드 | 필수 | 설명 |
|---|---|---|
| `row` | 예 | 원본 TextAsset의 행 번호. 검증·디버그용 보조 식별자 |
| `key` | 예 | TextAsset의 열 1 키. 주입 시 기본 식별자 |
| `en` | 예 | 원문 EN 열 값. 절대 덮어쓰지 않음 |
| `ko` | 아니오 | 확정된 한글 번역. 없는 행은 미번역 또는 검토 대기 |
| `translation_source` | `ko`가 있으면 예 | 번역 출처와 매칭 근거 |

## `translation_source` 필드

```json
{
  "source": "runtime-20260315",
  "match_mode": "exact",
  "runtime_source_lines": [227]
}
```

- `source`: 번역 출처 식별자. 현재는 `runtime-20260315`을 사용한다.
- `match_mode`: `exact`(원문 전체 동일) 또는 `runtime_escape_decoded`(런타임
  TSV의 이스케이프를 한 번 해석한 뒤 원문 전체 동일)이다.
- `runtime_source_lines`: 출처 TSV의 행 번호다. 같은 원문·번역이 여러 번
  있을 수 있으므로 배열로 유지한다.

## 주입 규칙

1. `en`은 보존한다.
2. `ko`가 있는 행만 한국어 교체 대상 언어 열에 셀 단위로 쓴다.
3. `ko`가 없는 행은 건너뛴다. 원문 부분 치환·유사도 매칭으로 채우지 않는다.
4. `translation_source`가 다른 수동 번역은 자동 스크립트가 덮어쓰지 않는다.
