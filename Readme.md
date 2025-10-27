# 🧑‍💻 SKN17-4th-1Team: Axiom
> SK네트웍스 Family AI캠프 17기 - 4차 프로젝트 1팀  
  개발 기간: 2025.10.24 ~ 2025.10.27

<br>

# 📌 목차
1. [팀 소개](#1️⃣-팀-소개)  
2. [프로젝트 개요](#2️⃣-프로젝트-개요)  
3. [기술 스택](#3️⃣-기술-스택)  
4. [시스템 구성도](#4️⃣-시스템-구성도)  
5. [요구사항 정의서](#5️⃣-요구사항-정의서)  
6. [화면설계서](#6️⃣-화면설계서)  
7. [WBS](#7️⃣-WBS)
8. [테스트 계획 및 결과 보고서](#8️⃣-테스트-계획-및-결과-보고서)  
9. [수행 결과](#9️⃣-수행-결과)  
10. [한 줄 회고](#🔟-한-줄-회고)  

<br>
<br>

# 1️⃣ 팀 소개
#### ✅ **팀명: Axiom**
> 단순함이 궁극의 정교함이다

#### ✅ **팀원 소개**

| [@김주영](https://github.com/samkim7788)                      | [@김준협](https://github.com/use08168)                       |  [@맹지수](https://github.com/happyfrogg)                       | [@이민영](https://github.com/mylee99125)                       | [@조세희](https://github.com/tpgml6513)                       |
|---------------------------------------------------------------|---------------------------------------------------------------------|---------------------------------------------------------------------|---------------------------------------------------------------------|---------------------------------------------------------------------|
| <img src="./images/jy.png" width="150" height="150">         | <img src="images/jh.png" width="150" height="150" />| <img src="images/js.png" width="150" height="150">             |  <img src="images/my.png" width="150" height="150" />|<img src="images/sh.png" width="150" height="150" />|

<br>
<br>


# 2️⃣ 프로젝트 개요

## ✅ 프로젝트 소개: Chative Jobs

**Chative Jobs**는 사용자의 마케팅 기획안에 대해, Apple의 마케팅 전략과 브랜딩 아이디어 기반으로 스티브 잡스에게 직접 컨설팅 받는 듯한 경험을 제공하는 **AI 기반 마케팅 컨설팅 챗봇**입니다.

<br>

## ✅ 프로젝트 필요성
![필요성](./images/int.png)

출처: [https://www.mordorintelligence.kr/industry-reports/marketing-consulting-market](https://www.mordorintelligence.kr/industry-reports/marketing-consulting-market)
> 본 분석에 사용된 모든 수치는 **당사가 52명을 대상으로 진행한 '마케팅 전략 수립 비효율성'에 대한 자체 설문조사 결과**를 기반으로 합니다.

마케팅 컨설팅 시장은 매년 성장하여, 2025년에는 **약 35억 달러** 규모로 추산됩니다. <br>하지만 이러한 외형적 성장에도 불구하고, 기존 컨설팅 서비스는 고질적인 비효율성을 안고 있습니다.


### 아쉬운 점 1. 높은 비용

| 아쉬운 점 | 설문 결과 |
| :--- | :--- |
| **비용 민감도** | AI 기능에 지불 의향 있는 응답자 중 **90.5%가** 월 **10만원 미만을** 선호 (Q6-1)
| **가성비 불만** | 불만족 응답자의 **1순위 불만 사유**는 **매우 높은 비용으로 인한 가성비 부족**이었습니다.
---

### 아쉬운 점 2. 획일적 전략 & 내부 자료 활용 미흡

| 아쉬운 점 | 설문 결과 |
| :---- | :---- |
| **차별화된 전략의 요구** | **82.7%가** '브랜드의 가치와 비전 정의'가 **매우 중요하다**고 응답 (Q5, 4+5점)
| **내부 자료 활용 사각지대** | Q3에서 시간 낭비를 느낀 응답자 중 **85.7%가** '사내 자료 재활용에 어려움'을 겪는다고 응답 (Q3-1, 4+5점)


<br>

## ✅ Chative Job의 솔루션

저희 AI 챗봇은 **혁신성, 신뢰성, 효율성**을 결합하여 기존 컨설팅의 한계를 돌파합니다.

### 목표 1: 혁신적 전략 초안 및 신뢰성 확보

| AI 기능 | 가치 제안 |
| :--- | :--- | 
| **혁신적 전략 제시<br>(스티브잡스 페르소나)**  | 단순 통계 기반을 넘어, **스티브 잡스 페르소나** 기반의 **파괴적 혁신 아이디어**를 초기 전략 초안으로 제공 |
| **신뢰성 & 정확성 확보** |  **RAG 기술**을 활용하여 학술 자료 및 최신 데이터에 기반한 답변의 **신뢰도와 정확성**을 극대화 |

### 목표 2: 사용자 친화적이고 효율적인 마케팅 전략 분석

| AI 기능 | 가치 제안 |
| :--- | :--- | 
| **기획안(PDF) 요약 및 분석** | **복잡한 내부 기획안(PDF)을** 간편하게 업로드하면, AI가 **핵심 요약 및 보완점**을 분석하여 사용자의 질문에 응답하여 사용자 시간을 절약|
| **사용자 중심 가격 정책** | **초기 전략:** 사용자 유입 극대화를 위한 **무료 서비스 배포** 및 **광고 수익 모델** 우선 적용 <br> **향후 전략:** **중소기업/스타트업**이 부담 없이 사용할 수 있는 **합리적인 구독료** 모델을 추후 도입할 수 있는 기반 마련 |
    

<br>
<br>


# 3️⃣ 기술 스택


| 카테고리 | 기술 스택 |
|----------|-------------------------------------------|
| **사용 언어** | ![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=Python&logoColor=white) |
| **프레임워크** | ![Django](https://img.shields.io/badge/Django-092E20?style=for-the-badge&logo=Django&logoColor=white) |
| **LLM** | ![Midm-2.0-Mini-Instruct](https://img.shields.io/badge/Midm%202.0%20Mini%20Instruct-3776AB?style=for-the-badge&logo=Midm-2.0-Mini-Instruct&logoColor=white) |
| **벡터 데이터베이스** | ![FAISS](https://img.shields.io/badge/FAISS-009688?style=for-the-badge&logo=Apache&logoColor=white) |
| **임베딩 모델** | ![OpenAI Embeddings](https://img.shields.io/badge/OpenAI%20Embeddings-8C9E90?style=for-the-badge&logo=OpenAI&logoColor=white) |
| **모델 튜닝/학습 프레임워크** | ![PyTorch](https://img.shields.io/badge/PyTorch-EE4C2C?style=for-the-badge&logo=PyTorch&logoColor=white) ![Transformers](https://img.shields.io/badge/Transformers-FFCC00?style=for-the-badge&logo=HuggingFace&logoColor=black) ![LoRA](https://img.shields.io/badge/LoRA-F76D57?style=for-the-badge&logo=HuggingFace&logoColor=white) |
| **프론트엔드** | <img src="https://img.shields.io/badge/html5-E34F26?style=for-the-badge&logo=html5&logoColor=white"> <img src="https://img.shields.io/badge/css-1572B6?style=for-the-badge&logo=css3&logoColor=white"> <img src="https://img.shields.io/badge/javascript-F7DF1E?style=for-the-badge&logo=javascript&logoColor=black"> |
| **실행 환경** | ![RunPod](https://img.shields.io/badge/RunPod-FF4500?style=for-the-badge&logo=Render&logoColor=white) ![AWS EC2](https://img.shields.io/badge/AWS%20EC2-FF9900?style=for-the-badge&logo=Amazon%20AWS&logoColor=white) |
| **배포 및 컨테이너** | ![Docker](https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=Docker&logoColor=white) ![Docker Compose](https://img.shields.io/badge/Docker--Compose-1488C6?style=for-the-badge&logo=Docker&logoColor=white)  |
| **DB 및 기타** | ![MySQL](https://img.shields.io/badge/MySQL-4479A1?style=for-the-badge&logo=MySQL&logoColor=white) ![python-decouple](https://img.shields.io/badge/python--decouple-3776AB?style=for-the-badge&logo=Python&logoColor=white) |
| **형상 관리 및 협업** | ![Git](https://img.shields.io/badge/Git-F05032?style=for-the-badge&logo=Git&logoColor=white) ![GitHub](https://img.shields.io/badge/GitHub-181717?style=for-the-badge&logo=GitHub&logoColor=white) ![Notion](https://img.shields.io/badge/Notion-000000?style=for-the-badge&logo=Notion&logoColor=white) ![Google Drive](https://img.shields.io/badge/Google%20Drive-4285F4?style=for-the-badge&logo=Google%20Drive&logoColor=white) |
| **테스트** | ![Pytest](https://img.shields.io/badge/pytest-%23ffffff.svg?style=for-the-badge&logo=pytest&logoColor=2f9fe3) |



<br>
<br>


# 4️⃣ 시스템 구성도

![시스템 구성도](./images/system.png)

<br>
<br>


# 5️⃣ 요구사항 정의서

![요구사항 정의서](./images/req.png)

**✅ 사용자 관련 요구사항:**
사용자는 로그인, 회원가입, 개인정보 수정을 할 수 있어야 한다.

**✅ 채팅 관련 요구사항:**
사용자는 Chative Jobs 시스템을 통해 PDF 업로드 및 질의응답 채팅을 할 수 있어야 한다.

**✅ 히스토리 관련 요구사항:**
사용자의 파일 및 채팅 기록은 저장, 접근 가능해야한다.


---

<br>
<br>


# 6️⃣ 화면설계서

[✅ 화면 설계서 바로가기](https://docs.google.com/presentation/d/10oxuHBTXadnlJ9JGtmlaPrudTjYlZZQR/edit?usp=sharing&ouid=103468688069912495528&rtpof=true&sd=true)

<details>
<summary>전체 화면 설계서</summary>
<br>

**- 메인 홈 화면**
![화면설계서1](./images/scr1.png)
<br>

**- 회원가입/로그인/비밀번호 찾기**
![화면설계서2](./images/scr2.png)
![화면설계서3](./images/scr3.png)
![화면설계서4](./images/scr4.png)
![화면설계서5](./images/scr5.png)
![화면설계서6](./images/scr6.png)

<br>

**- 회원 채팅**
![화면설계서10](./images/scr10.png)
![화면설계서11](./images/scr11.png)
![화면설계서12](./images/scr12.png)
<br>


**- 개인정보 설정**
![화면설계서7](./images/scr7.png)
![화면설계서8](./images/scr8.png)
![화면설계서9](./images/scr9.png)
<br>

</details>

<br>
<br>

# 7️⃣ WBS

![WBS](./images/wbs.png)


<br>
<br>


# 8️⃣ 테스트 계획 및 결과 보고서
### 테스트 계획서
![테스트 계획서](./images/test_plan.png) 

<details>
<summary>테스트 시나리오</summary>
<br>

**- 단위 테스트**
![단위 테스트](./images/test_ut.png)
<br>

**- 통합 테스트**
![테스트 시나리오](./images/test_it.png)
<br>

</details>

### 테스트 결과 보고서
![테스트 결과](./images/test_report.png)

<br>

## 한계점 및 향후 개선 계획

---

<br>
<br>

# 9️⃣ 수행 결과

![최종-결과-화면-gif](./img/완성.png)




<br>
<br>
<br>

# 🔟 한 줄 회고
| 항목 | 내용 |
|------|------|
| 김주영 |  |
| 김준협 |  |
| 맹지수 |  |
| 이민영 |  |
| 조세희 |  |

<br>
