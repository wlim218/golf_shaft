import streamlit as st
import pandas as pd

# 페이지 설정
st.set_page_config(
    page_icon="🏌🏻",
    page_title="골프 샤프트 고르기",
    layout="wide",
)

# 세션 상태 초기화
st.session_state.setdefault('page', 'club_selection')
st.session_state.setdefault('club_type', None)
st.session_state.setdefault('body_type', None)
st.session_state.setdefault('swing_speed', None)
st.session_state.setdefault('speed_unit', 'm/s')
st.session_state.setdefault('desired_launch', None)
st.session_state.setdefault('spin_rate', None)

def go_to_body_selection():
    st.session_state['page'] = 'body_selection'

def go_to_swing_speed():
    st.session_state['page'] = 'swing_speed'

def go_to_launch_selection():
    st.session_state['page'] = 'launch_selection'

def go_to_spin_rate():
    st.session_state['page'] = 'spin_rate'

def go_to_results():
    st.session_state['page'] = 'results'

# 데이터 업로드
shaft_woods = pd.read_csv('woods.csv')
shaft_irons = pd.read_csv('irons.csv')

def filter_shaft_data(data, club_type, swing_speed, body_type, desired_launch, spin_rate):
    if club_type == "드라이버":
        if swing_speed < 40:
            flex_options = ['R', 'R2', 'SR', '5.0']
            data = data[(data['flex'].isin(flex_options)) & (data['torque'] >= 4.0)]
        elif 40 <= swing_speed < 55:
            flex_options = ['S', 'X', '5.5', '6.0']
            data = data[(data['flex'].isin(flex_options)) & (data['torque'] < 4.0) & (data['torque'] >= 3.0)]
        else:
            flex_options = ['X', '6.0', '6.5', 'TX']
            data = data[(data['flex'].isin(flex_options)) & (data['torque'] < 3.0)]
        
        if body_type == '마른 체형':
            data = data[data['weight'] <= 55]
        elif body_type == '보통 체형':
            data = data[data['weight'] <= 68]
        else:
            data = data[data['weight'] > 68]
        
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
            if desired_launch == '낮은 탄도':
                data = data[data['launch'].isin(['low', 'mid-low'])]
            elif desired_launch == '중간 탄도':
                data = data[data['launch'].isin(['mid', 'mid-low', 'mid-high'])]
            else:
                data = data[data['launch'].isin(['high', 'mid-high'])]
        
        if 'spin' in data.columns:
            if spin_rate == '높은 스핀량':
                data = data[data['spin'].isin(['mid-high', 'high'])]
            elif spin_rate == '중간 스핀량':
                data = data[data['spin'].isin(['mid-high', 'mid', 'mid-low'])]
            else:
                data = data[data['spin'].isin(['low', 'mid-low'])]
    
    return data

# 페이지 이동 함수
def go_to(page):
    st.session_state['page'] = page
    st.experimental_rerun()
    
# 페이지 UI 렌더링
if st.session_state['page'] == 'club_selection':
    st.header("나에게 맞는 샤프트는 무엇일까?")
    club_type = st.radio("사용할 클럽을 선택하세요:", ('드라이버', '아이언'))
    if st.button("다음"):
        st.session_state['club_type'] = club_type
        go_to_body_selection()

elif st.session_state['page'] == 'body_selection':
    st.header("체형 선택")
    body_type = st.radio("체형을 선택하세요:", ('마른 체형', '보통 체형', '다부진 체형'))
    if st.button("이전"):
            go_to('club_selection')
    if st.button("다음"):
        st.session_state['body_type'] = body_type
        go_to_swing_speed()

elif st.session_state['page'] == 'swing_speed':
    st.header("스윙 스피드 입력")

    swing_speed = st.text_input("스윙 스피드를 입력하세요 (m/s)", value="0")
    try:
        swing_speed = int(swing_speed)  # 숫자로 변환
    except ValueError:
        swing_speed = 0  # 잘못된 입력 처리
    if st.button("이전"):
            go_to('body_selection')
    if st.button("다음"):
        st.session_state['swing_speed'] = swing_speed
        go_to_launch_selection()

elif st.session_state['page'] == 'launch_selection':
    st.header("희망하는 탄도 선택")
    desired_launch = st.radio("희망 탄도를 선택하세요:", ('높은 탄도', '중간 탄도', '낮은 탄도'))
    if st.button("이전"):
            go_to('swing_speed')
    if st.button("다음"):
        st.session_state['desired_launch'] = desired_launch
        if st.session_state['club_type'] == '아이언':
            go_to_spin_rate()
        else:
            go_to_results()

elif st.session_state['page'] == 'spin_rate':
    st.header("희망하는 스핀량 선택")
    spin_rate = st.radio("희망 스핀량을 선택하세요:", ('높은 스핀량', '중간 스핀량', '낮은 스핀량'))
    if st.button("이전"):
            go_to('launch_selection')
    if st.button("결과 보기"):
        st.session_state['spin_rate'] = spin_rate
        go_to_results()

elif st.session_state['page'] == 'results':
    st.header("추천 샤프트 결과")
    club_type = st.session_state['club_type']
    body_type = st.session_state['body_type']
    swing_speed = st.session_state['swing_speed']
    desired_launch = st.session_state['desired_launch']
    spin_rate = st.session_state['spin_rate']
    
    shaft_data = shaft_woods if club_type == "드라이버" else shaft_irons
    filtered_data = filter_shaft_data(shaft_data, club_type, swing_speed, body_type, desired_launch, spin_rate)
    
    st.write("📊 **추천 샤프트 목록**")
    if filtered_data.empty:
        st.warning("추천되는 샤프트가 없습니다. 필터 조건을 다시 확인해주세요.")
    else:
        st.dataframe(filtered_data)
    
    if st.button("처음으로 돌아가기"):
        st.session_state['page'] = 'club_selection'
