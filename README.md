# Project Sentinel

Project Sentinel은 대표님의 개인 투자 판단을 보조하기 위한 AI 투자 어시스트 프로젝트입니다.

## 핵심 목표

자동매매가 아닌, 시장 감시와 전략 검증을 통해 대표님의 매매 판단을 돕는 시스템을 만든다.

## 절대 원칙

1. 자동매매는 하지 않는다.
2. 최종 매수·매도 판단은 항상 사람이 한다.
3. 추천보다 검증을 우선한다.
4. 성공 데이터뿐 아니라 실패 데이터도 저장한다.
5. 왜 성공했는지, 왜 실패했는지 원인을 기록한다.
6. 처음부터 확장 가능한 구조로 만든다.
7. 기능보다 신뢰를 먼저 만든다.

## V1 목표

- 관심종목 감시
- 조건 충족 시 알림
- 알림 당시 데이터 저장
- 1시간 / 2시간 / 종가 결과 추적
- 성공 / 실패 / 무효 판정
- 성공·실패 원인 저장

## 기술 구성

- Backend: Python, FastAPI
- Mobile: React Native / Expo
- Data: 한국투자증권 Open API
- Notification: Push Notification
- Database: PostgreSQL 또는 SQLite 검토
- AI Analysis: OpenAI API 예정

## Project Philosophy

AI가 매매를 대신하는 것이 아니라, AI가 판단 근거를 정리하고 전략을 검증한다.

> 추천보다 검증.
> 감이 아니라 데이터.