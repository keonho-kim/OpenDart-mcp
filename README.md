# OpenDart-MCP

OpenDart-MCP는 DART (Data Analysis, Retrieval and Transfer System) API를 Model-Context Protocol (MCP) 기반으로 제공하여, 다양한 금융 정보 조회 및 분석 기능을 보다 효율적이고 표준화된 방식으로 접근할 수 있도록 돕는 파이썬 라이브러리입니다.

## 주요 기능

OpenDart-MCP는 MCP를 통해 다음과 같은 상세한 금융 정보 조회 및 분석 기능을 제공합니다:

*   **기업 기본 정보 조회**: MCP 인터페이스를 통해 특정 회사 이름이나 코드를 기반으로 기업의 상세 기본 정보(회사명, 영문명, 종목코드, 대표자명, 법인구분, 법인등록번호, 사업자등록번호, 주소, 홈페이지, IR홈페이지, 전화번호, 팩스번호, 설립일, 결산월 등)를 신속하게 조회합니다.
*   **단일 회사 전체 재무제표 조회**: MCP를 이용하여 특정 기업의 특정 사업연도, 보고서 종류(1분기보고서, 반기보고서, 3분기보고서, 사업보고서)에 해당하는 원본 재무제표(개별/연결, XBRL 표준 계정과목 체계)를 요청하고, JSON 형태로 가공된 재무상태표, 손익계산서, 현금흐름표 등의 데이터를 제공받습니다. (IFRS, GAAP 모두 지원 가능)
*   **재무제표 목록 조회**: MCP를 통해 특정 기업이 공시한 과거 재무제표의 목록을 연도별, 분기별로 손쉽게 가져올 수 있으며, 각 재무제표의 상세 조회로 이어지는 연결고리를 제공합니다.
*   **부채 총괄 현황 조회**: MCP를 활용하여 기업의 최근 사업연도 기준 부채 총괄 현황 (유동부채, 비유동부채의 상세 항목 및 금액)을 신속하게 파악하여 재무 건전성 분석에 활용합니다.
*   **타법인 출자 현황 조회**: MCP를 통해 특정 기업의 타 법인에 대한 출자 현황 (출자 대상 회사명, 출자 목적, 최초취득일자, 최초취득금액, 기초 및 기말 지분율, 장부가액 등) 정보를 상세하게 조회하여 기업의 투자 포트폴리오 및 관계사 현황을 분석합니다.
*   **임원 및 직원 현황 조회**: MCP 인터페이스를 통해 기업의 등기임원 및 미등기임원 현황(성명, 생년월일, 직위, 등기/미등기 구분, 재직기간 등)과 직원 현황(직원 수, 평균 근속연수, 연간 급여총액, 1인 평균 급여액 등, 사업부문별/성별 상세 정보 포함)을 조회하여 기업의 인력 구조 및 운영 상태를 파악합니다.
*   **주식 총수 현황 조회**: MCP를 통해 기업이 발행한 주식의 총수, 보통주/우선주 구분, 유통 주식 수, 자기주식 보유 현황 등 주식 관련 핵심 정보를 제공받아 지분 구조 및 시장 유동성 분석에 활용합니다.

## 제공 도구 목록 (src/dart_mcp/tools)

*   `find_company_by_name.py`: 회사 이름으로 회사 정보 검색
*   `get_company_financial_stmt_list.py`: 회사의 재무제표 목록 조회
*   `get_debt_summary.py`: 부채 총괄 현황 조회
*   `get_financial_stmt.py`: 단일회사 전체 재무제표 조회
*   `get_investment_summary.py`: 타법인 출자 현황 조회
*   `get_people_summary.py`: 임원 및 직원 현황 조회
*   `get_stock_summary.py`: 주식 총수 현황 조회

## MCP 설정 가이드

OpenDart-MCP를 Claude Desktop에서 사용하기 위한 단계별 설정 방법입니다.

### 1. 사전 준비사항

#### 1.1 DART API 키 발급
1. [DART 전자공시시스템](https://dart.fss.or.kr/) 접속
2. 우상단 '오픈API' 클릭
3. 'API 신청' → '개발자 등록' 진행
4. 개인정보 입력 후 API 키 발급 (이메일로 전송됨)
5. 발급받은 API 키를 메모장에 저장해 두세요

#### 1.2 Docker 설치
- **Windows**: [Docker Desktop for Windows](https://docs.docker.com/desktop/install/windows-install/) 다운로드 및 설치
- **macOS**: [Docker Desktop for Mac](https://docs.docker.com/desktop/install/mac-install/) 다운로드 및 설치
- **Linux**: 배포판에 맞는 [Docker 설치 가이드](https://docs.docker.com/engine/install/) 참조

### 2. Docker 이미지 빌드


```bash
# 1. 깃허브 복사하기
git clone https://github.com/keonho-kim/OpenDart-mcp.git
```

```bash
# 1. 프로젝트 폴더로 이동
cd OpenDart-mcp

# 2. Docker 이미지 빌드
docker build -t opendart-mcp .
```

> **참고**: 빌드 과정은 몇 분 정도 소요될 수 있습니다.

### 3. Claude Desktop 설정

#### 3.1 설정 파일 찾기
운영체제별 Claude Desktop 설정 파일 위치:

- **Windows**: `%APPDATA%\Claude\claude_desktop_config.json`
- **macOS**: `~/Library/Application Support/Claude/claude_desktop_config.json`
- **Linux**: `~/.config/Claude/claude_desktop_config.json`

#### 3.2 설정 파일 수정
1. 위 경로의 설정 파일을 텍스트 에디터로 열기 (파일이 없다면 새로 생성)
2. 다음 내용을 추가하거나 기존 내용을 수정:

```json
{
  "mcpServers": {
    "opendart-mcp": {
      "command": "docker",
      "args": [
        "run",
        "--rm",
        "-i",
        "--net=host",
        "-e",
        "DART_API_KEY=<PUT_YOUR_DART_API_KEY>",
        "opendart-mcp"
      ]
    }
  }
}
```

3. `<PUT_YOUR_DART_API_KEY>` 부분을 1단계에서 발급받은 실제 API 키로 교체
   - 예시: `"DART_API_KEY=1234567890abcdef1234567890abcdef12345678"`

#### 3.3 설정 파일 예시 (완성된 형태)
```json
{
  "mcpServers": {
    "opendart-mcp": {
      "command": "docker",
      "args": [
        "run",
        "--rm",
        "-i",
        "--net=host",
        "-e",
        "DART_API_KEY=1234567890abcdef1234567890abcdef12345678",
        "opendart-mcp"
      ]
    }
  }
}
```

### 4. Claude Desktop 재시작

설정 파일을 저장한 후 Claude Desktop을 완전히 종료하고 다시 실행하세요.

### 5. 사용 확인

Claude Desktop에서 다음과 같이 테스트해보세요:

```
삼성전자의 2023년 사업보고서를 조회해주세요.
```

### 문제 해결

#### Docker 관련 오류
- Docker가 실행 중인지 확인하세요
- Docker Desktop을 관리자 권한으로 실행해보세요

#### 설정 파일 관련 오류
- JSON 문법이 올바른지 확인하세요 (쉼표, 따옴표 등)
- 설정 파일 경로가 정확한지 확인하세요
