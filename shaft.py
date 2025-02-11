import streamlit as st
import pandas as pd

# 페이지 설정
st.set_page_config(
    page_icon="🏌🏻",
    page_title="골프 샤프트 고르기",
    layout="wide",
)

# 세션 상태 초기화
st.session_state.setdefault('page', 'main_page')
st.session_state.setdefault('club_type', None)
st.session_state.setdefault('body_type', None)
st.session_state.setdefault('swing_speed', None)
st.session_state.setdefault('desired_launch', None)
st.session_state.setdefault('spin_rate', None)

# 데이터 업로드
shaft_woods = pd.read_csv('woods.csv')
shaft_irons = pd.read_csv('irons.csv')

def filter_shaft_data(data, club_type, swing_speed, body_type, desired_launch, spin_rate):
    if club_type == "드라이버":
        if swing_speed < 40:
            flex_options = ['R', 'R2', 'SR', '5.0']
            data = data[data['flex'].isin(flex_options)]
        elif 40 <= swing_speed < 54:
            flex_options = ['S', 'X', '5.5', '6.0']
            data = data[data['flex'].isin(flex_options)]
        else:
            flex_options = ['X', '6.0', '6.5', 'TX']
            data = data[data['flex'].isin(flex_options)]
        
        if body_type == '마른 체형':
            data = data[data['weight'] <= 55]
        elif body_type == '보통 체형':
            data = data[(data['weight'] > 55) & (data['weight'] <= 65)]
        else:
            data = data[data['weight'] > 65]
        
        if 'launch' in data.columns:
            if desired_launch == '높은 탄도':
                data = data[data['launch'].isin(['high', 'mid-high'])]
            elif desired_launch == '중간 탄도':
                data = data[data['launch'].isin(['mid', 'mid-low', 'mid-high'])]
            else:
                data = data[data['launch'].isin(['low', 'mid-low'])]
    
    elif club_type == "아이언":
        if swing_speed < 30:
            flex_options = ['L', 'A']
        elif 30 <= swing_speed < 35:
            flex_options = ['RR', 'R']
        elif 35 <= swing_speed < 40:
            flex_options = ['S', 'X']
        else:
            flex_options = ['X', 'TX']
        data = data[data['flex'].isin(flex_options)]

        if body_type == '마른 체형':
            data = data[data['weight'] <= 110]
        elif body_type == '보통 체형':
            data = data[data['weight'] <= 125]
        else:
            data = data[data['weight'] > 125]
        
        if 'launch' in data.columns:
            if desired_launch == '높은 탄도':
                data = data[data['launch'].isin(['high', 'mid-high'])]
            elif desired_launch == '중간 탄도':
                data = data[data['launch'].isin(['mid', 'mid-low', 'mid-high'])]
            else:
                data = data[data['launch'].isin(['low', 'mid-low'])]
        
        if 'spin' in data.columns:
            if spin_rate == '높은 스핀량':
                data = data[data['spin'].isin(['mid-high', 'high'])]
            elif spin_rate == '중간 스핀량':
                data = data[data['spin'].isin(['mid-high', 'mid', 'mid-low'])]
            else:
                data = data[data['spin'].isin(['low', 'mid-low'])]
    
    return data

# 페이지 UI 렌더링
if st.session_state['page'] == 'main_page':
    st.header("나에게 맞는 샤프트 찾기 🏌🏻")

    # **1. 클럽 선택**
    st.subheader("1️⃣ 사용할 클럽을 선택하세요")
    st.session_state['club_type'] = st.radio("클럽 타입", ('드라이버', '아이언'))

    # **2. 체형 선택**
    st.subheader("2️⃣ 체형을 선택하세요")
    st.session_state['body_type'] = st.radio("체형", ('마른 체형', '보통 체형', '다부진 체형'))

    # **3. 스윙 스피드 입력**
    st.subheader("3️⃣ 스윙 스피드를 입력하세요 (m/s)")
    swing_speed = st.text_input("스윙 스피드 (숫자로 입력)", value="0")
    try:
        st.session_state['swing_speed'] = int(swing_speed)
    except ValueError:
        st.warning("올바른 숫자를 입력하세요.")
        st.session_state['swing_speed'] = 0

    # **4. 희망 탄도 선택**
    st.subheader("4️⃣ 희망하는 탄도를 선택하세요")
    st.session_state['desired_launch'] = st.radio("희망 탄도", ('높은 탄도', '중간 탄도', '낮은 탄도'))

    # **5. 아이언 선택 시 스핀량 추가 선택**
    if st.session_state['club_type'] == '아이언':
        st.subheader("5️⃣ 희망하는 스핀량을 선택하세요")
        st.session_state['spin_rate'] = st.radio("희망 스핀량", ('높은 스핀량', '중간 스핀량', '낮은 스핀량'))
    else:
        st.session_state['spin_rate'] = None  # 드라이버의 경우 스핀 데이터 제외

    # **결과 보기 버튼**
    if st.button("🔍 결과 보기"):
        st.session_state['page'] = 'results'
        st.experimental_rerun()

# 결과 페이지
elif st.session_state['page'] == 'results':
    st.header("추천 샤프트 결과 📊")

    # 사용자 선택값 불러오기
    club_type = st.session_state['club_type']
    body_type = st.session_state['body_type']
    swing_speed = st.session_state['swing_speed']
    desired_launch = st.session_state['desired_launch']
    spin_rate = st.session_state['spin_rate']

    # 데이터 필터링
    shaft_data = shaft_woods if club_type == "드라이버" else shaft_irons
    filtered_data = filter_shaft_data(shaft_data, club_type, swing_speed, body_type, desired_launch, spin_rate)

    # 필요한 컬럼만 표시 ('company', 'shaft', 'model', 'flex')
    display_columns = ['company', 'shaft', 'model', 'flex']
    
    if filtered_data.empty:
        st.warning("🔍 추천되는 샤프트가 없습니다. 입력한 조건을 다시 확인하세요.")
    else:
        st.dataframe(filtered_data[display_columns])

    # 다시 선택하기 버튼
    if st.button("🔄 다시 선택하기"):
        st.session_state['page'] = 'main_page'
        st.experimental_rerun()