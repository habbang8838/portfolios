# portfolios
박지수의 데이터 분석 및 AI 포트폴리오 자료 모음입니다.



# 1. KT 에이블 스쿨 빅 프로젝트 (AI - 딥러닝 시각지능 프로젝트)
카메라에 인식된 사람의 얼굴을 탐지하여 표정을 확률별로 예측하고, 집중도를 계산하는 딥러닝 프로젝트

## 프로젝트 진행 목적
* 보다 솔직한 피드백을 원하는 강연자와 간단하고 신뢰성이 높은 리뷰를 원하는 청중 사이의 양방향 소통 서비스 개발

## 주요 역할
* AI 파트 담당
* FER2013, DAiSEE 데이터셋 크롤링
* 이미지 속 얼굴 탐지 모델 구현 (mediapipe, haarcascade_frontalface 사전학습 모델 사용)
* ConvLSTM, ResNet50, InceptionV3, CNN 2종 모델 구현 및 성능 평가
* 논문 기반 집중도 산출 알고리즘 개발

## 결과값 출력
* 이미지 속 얼굴의 사진을 탐지하고 긍정/부정/중립의 비율과 집중도의 평균값을 결과값으로 출력

## 기대 효과 및 활용 (To-Be)
* 강연자는 청중의 집중도가 저하된 곳을 정확하게 인지하고, 피드백을 받을 수 있다.
* 청중은 간편한 방식으로 강연자에게 피드백을 제공할 수 있다.
* 연설, 영화, 사내 교육 등 다양한 분야로 커스터마이징이 가능할 것이다.

---
# 2. 주별 아토피 위험 지수 예측 프로젝트 (데이터 분석 및 모델링)

## 프로젝트 진행 목적
아토피 피부염은 환경성 질환으로, 날씨 및 대기 오염 물질의 영향을 받아 악화될 수 있기에 위 인자들로 주별 아토피 증상의 악화 위험성이 있는 주간을 예측하는 모델 개발

## 주요 역할
* 모델링 총괄 담당
* 파생변수 생성 및 데이터 그룹화 등의 전처리 작업
* 머신러닝 알고리즘(선형 회귀, 의사결정나무 모델) 사용하여 예측
* shapley value 분석

## 결론 및 시사점
* 기상청 API랑 연동하여 지역을 입력할 때, 자동으로 아토피 위험 지수를 도출 가능
* 날씨 정보와 함께 아토피 위험 지수를 제공하여, 아토피 환자들의 증상 악화를 조기 예방 가능
* 기존 아토피 증상 기록 어플에 주별 환경 인자에 따라 예측되는 아토피 위험 지수를 서비스로 제공하여 개별 환자의 마이데이터를 구축하여 활용 가능
* 아토피를 비롯하여 환경적 요인에 영향을 받는 질병에 대해서도 위험 지수를 개발하여, 종합적인 환경성 질환의 증상 악화를 예측하는 것도 향후에 필요할 것으로 보임

## 아쉬웠던 점
* 꽃가루 농도의 경우 나무별로 특정 월 및 특정 시간대에만 위험 지수를 제공하는 한계로 인해, 예측에 잘 활용하지 못함
* 월은 원-핫 인코딩, 시간대는 데이터 보간법 등을 통해 보완하여 활용 가능
* 본 프로젝트에서는 주로 '환경적 요인'을 기반으로 분석하였으나, 실내위험지수나 개인 건강 데이터 등의 마이데이터에 결합할 수 있다면 보다 정확한 활용 가능

---

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
* 가설을 EDA를 통해 검증해 나가는 방식과 다양한 전처리 시도를 통하여 보다 유의미한 영향을 주는 변수 파악 가능
* 변수 중요도가 가장 높은 변수가 1번 가설에서 생성한 'is_prime_lower_than_avg' 였으며, 이 변수를 제외하고 진행한 경우, 모델링 성능에 많은 영향을 주는 것을 파악 가능
* 임직원과 비임직원 데이터를 각각 나누어 모델링을 진행해본 결과, 임직원은 성능이 높게 나왔지만, 비임직원은 성능이 낮게 나와서, 비임직원에게 많은 영향을 줄 수 있는 변수와 상품, 행사에 대한 정보를 파악하여 분석하여 프라임 회원의 예측 성능을 높일 수 있음

---

# 4. BDA 인사이트 마케팅 공모전
CJ 더마켓 내부 고객의 주문 데이터를 사용하여 월별 구매 패턴 및 재구매 고객 판매 동향을 파악하여 고객별 적절한 마케팅 방법 제시

## 데이터 변수
주문접수 일시, 유입채널, 유입매체, 아이디, 전시상품명, 전시유입코드, 판매가, 수량 등

## 주요 역할
* 코드 작성 총괄
* 데이터 전처리 (월별 데이터 합치기, 불필요한 칼럼 삭제, 유입 채널 분류, 주문 시간)
* 월별로 카테고리별 판매 횟수 및 상관계수 파악 (시각화)
* 고객의 아이디로 그룹화하여, 최다 이용 고객의 주문 패턴 파악(유입채널에 따른 주문 시간, 카테고리별 주문 시간)

## 결론 및 시사점
* 유입채널 별로 파악 : 증정 행사 및 적립 행사, 명절 행사 등이 있을 때 푸시 알림 및 상위 랭킹에 상품을 노출시켜 매출을 향상시키기
* 월별로 파악 : 수요가 높은 제품 및 상관관계 높은 제품을 파악하여, 증정 행사 및 이벤트, 할인 쿠폰 등을 제공하기
* 재구매 패턴 파악 : 특가 이벤트, 증정 행사에 따라 수요가 높은 상품의 트렌드를 오래 따라가는 경향이 높으며, 특정 시간별로 유입하는 채널을 분석하여 특정 시간대에 광고 배너를 활성화하여 재구매 유도

---

# 5. 교통사고 건수 예측 프로젝트
교통 사고에 영향을 주는 주요 변수를 파악하여, 사고 건수를 예측하는 머신러닝 모델 개발

## 문제 파악 및 프로젝트 진행 목적 (AS-IS)
교통사고 잠재 변수 파악을 위한 선행 연구도 수차례 진행되었지만, 근시일의 교통사고 발생을 예측하고 실질적으로 예방하기 위한 노력의 부족

## 사용 데이터
* 9개년(2010~2018년) 서울시 교통 사고 정보 데이터
* 경기도, 광주광역시, 제주도, 세종시 등의 교통 사고 정보 데이터 (시간대가 각각 상이함)
* 훈련 데이터 : 서울시 8개년(2010~2017) 데이터
* 테스트 데이터 : 서울시 1개년(2018) 데이터
* 타겟 데이터 : 발생일, 시군구별로 groupby 하여 사고 건수를 count

## 데이터 변수
발생일자, 시간, 시군구, 사고내용, 법정동명, 사상자수, 사고유형, 노면상태, 기상상태, 도로형태 등

## 주요 역할
* 랜덤 포레스트 모델 구현
* 데이터 재라벨링(라벨 인코딩) 작업 및 5개 지역으로 모델의 일반화 성능 확인
* (이례적 분석) 연령별 교통 사고에 영향을 미치는 유형 분석
* (이례적 분석) 이륜차 및 자전거의 교통사고 유형 분석
* (이례적 분석) 도로 형태별로 교통 사고 사망건 데이터 시각화

## 결론 및 시사점
* 도로 형태, 노면 상태, 기상 상태 3개의 변수가 교통 사고 건수에 높은 영향을 주는 것으로 파악
* 각 변수의 값을 sum()한 모델의 경우, 사고 건수를 사전에 알고 있어야 하므로, mean() 모델을 사용하여 도로 형태별로 그룹화하여 진행하였으나, 위치 정보가 누락되어 해당 위치에 대한 미시적 예측이 어려운 한계가 발생함
* 경기도 교통사고 발생 데이터가 서울특별시와 가장 유사하게 나타났으며, 위 데이터를 합쳐서 예측한다면 모델의 성능을 개선시킬 수 있을 것으로 파악
* 지역별로 특성이 다르게 나타나는 유동인구, 신호등/가로등 분포, LED 표지판 등의 변수를 반영하면 더욱 정확한 예측 모델을 개발할 수 있을 것으로 파악

  
