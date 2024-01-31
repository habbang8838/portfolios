# portfolios
박지수의 데이터 분석 및 AI 포트폴리오 자료 모음입니다.

# 1. KT 에이블 스쿨 빅 프로젝트
카메라에 인식된 사람의 얼굴을 탐지하여 표정을 확률별로 예측하고, 집중도를 계산하는 딥러닝 프로젝트

## 프로젝트를 진행하게 된 목적 및 계기
보다 솔직한 피드백을 원하는 강연자와 간단하고 신뢰성이 높은 리뷰를 원하는 청중 사이의 양방향 소통 서비스 개발

## 주요 역할
* AI 파트 담당
* FER2013, DAiSEE 데이터셋 크롤링
* 이미지 속 얼굴 탐지 모델 구현 (mediapipe, haarcasccade_frontalface 사전학습 모델 사용)
* ConvLSTM, ResNet50, InceptionV3, CNN 2종 모델 구현 및 성능 평가
* 논문 기반 집중도 산출 알고리즘 개발

## 결과값 출력
* 이미지 데이터를 입력받으면, 이미지 속 얼굴의 사진을 탐지하고 긍정/부정/중립의 비율과 집중도의 평균 값을 결과값으로 출력

## 기대 효과 및 활용
* 강연자는 청중의 집중도가 저하된 곳을 정확하게 인지하고, 피드백을 받을 수 있다.
* 청중은 간편한 방식으로 강연자에게 피드백을 제공할 수 있다.
* 연설, 영화, 사내 교육 등 다양한 분야로 커스터마이징이 가능할 것이다.


# 3. BDA 모델링 공모전
CJ 더마켓 주문 내역을 통해 프라임 회원 유무 분류를 진행하는 모델링 프로젝트

## 데이터 설명

<설명 변수(X)>
product_name (주문한 상품명), net_order_qty(주문 수량), net_order_amt(주문 금액 : 정규화된 수치),
gender(성별), age_grp(연령대 그룹), employee_yn(임직원 유무), order_date(주문 날짜)

<종속 변수(Y)>
prime_yn(프라임 회원 유무)

## 분석을 위해 설정한 6가지 가설
1) (상품명, 동일 수량)으로 그룹화 하였을 때, 프라임 회원은 일반 회원보다 할인 혜택으로 인해 저렴한 가격으로 구매할 것이다.
2) 프라임 회원은 가장 경제활동이 활발하며, 주부층이 가장 많이 분포하고 있는 30~40대 연령층에 가장 많이 분포할 것이다.
3) 프라임 회원은 남성 회원보다 여성 회원이 더 많을 것이다.
4) 동일 상품에 대해 프라임 회원의 주문 수량이 더 많을 것이다.
5) 구매 품목 중 인기 상품을 구매하는 회원은 프라임 회원이 비프라임 회원보다 비율이 높을 것이다.
6) 주문 번호로 그룹화 하여, 총 구매 금액을 비교하면 프라임 회원이 비프라임 회원보다 높을 것이다.

### 주요 역할
* 가설을 검정하기 위한 EDA 과정
* 타겟 변수에 유의미한 영향을 주는 파생변수 생성
* 임직원, 비임직원 나누어 프라임 회원 예측 진행

### 인사이트
* 가설을 EDA를 통해 검증해 나가는 방식과 다양한 전처리 시도를 통하여 보다 유의미한 영향을 주는 변수를 파악할 수 있다.
* 변수 중요도가 가장 높은 변수가 1번 가설에서 생성한 'is_prime_lower_than_avg' 였으며, 이 변수를 제외하고 진행한 경우, 모델링 성능에 많은 영향을 주는 것을 알 수 있다.
* 임직원과 비임직원 데이터를 각각 나누어 모델링을 진행해본 결과, 임직원은 성능이 높게 나왔지만, 비임직원은 성능이 낮게 나와서, 비임직원에게 많은 영향을 줄 수 있는 변수와 상품, 행사에 대한 정보를 파악하여 분석한 결과, 프라임 회원 예측의 성능을 높일 수 있었다.
