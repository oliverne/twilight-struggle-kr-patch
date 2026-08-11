#!/usr/bin/env python3
"""Common_Strings 235행 수동 번역 적용 스크립트"""

import json
from pathlib import Path

BASE = Path(__file__).resolve().parent.parent.parent

# ── 번역 맵 ──
TRANSLATIONS: dict[str, str] = {
    # ── 메인 메뉴 / 네비게이션 ──
    "Play Offline": "오프라인 플레이",
    "Play Online": "온라인 플레이",
    "Main Menu": "메인 메뉴",
    "Menu": "메뉴",
    "Options": "설정",
    "Settings": "환경 설정",
    "Tutorial": "튜토리얼",
    "Tutorials": "튜토리얼",
    "Start Menu": "시작 메뉴",
    "Exit": "종료",
    "Play": "플레이",
    "View Cards": "카드 보기",
    "Purchase": "구매",
    "Buy": "구매",
    "Details": "상세",
    "Purchased": "구매함",
    "Clear Purchases": "구매 내역 초기화",
    "Coming Soon": "출시 예정",
    "Owned": "보유함",
    "Now Available": "구매 가능",

    # ── 게임 로비 / 설정 ──
    "New": "새로 만들기",
    "Game": "게임",
    "View Game": "게임 보기",
    "Delete Game": "게임 삭제",
    "Delete Your Game": "게임 삭제",
    "Add Computer Player": "컴퓨터 플레이어 추가",
    "Add Human Player": "인간 플레이어 추가",
    "Drag below to add": "아래로 드래그하여 추가",
    "Please enter a name": "이름을 입력하세요",
    "Player 1": "플레이어 1",
    "Player 2": "플레이어 2",
    "Player 3": "플레이어 3",
    "Player 4": "플레이어 4",
    "Player 5": "플레이어 5",
    "Accept": "확인",
    "Online": "온라인",
    "Offline": "오프라인",
    "Online Create Game": "온라인 게임 만들기",
    "Offline Create Game": "오프라인 게임 만들기",
    "Online Lobby": "온라인 로비",
    "Offline Lobby": "오프라인 로비",
    "Return to Lobby": "로비로 돌아가기",
    "Online Game List": "온라인 게임 목록",
    "Offline Game List": "오프라인 게임 목록",
    "Online Record": "온라인 전적",
    "Offline Record": "오프라인 전적",
    "2 Players": "2인 플레이",
    "3 Players": "3인 플레이",
    "4 Players": "4인 플레이",
    "2 Players:": "2인 플레이:",
    "3 Players:": "3인 플레이:",
    "4 Players:": "4인 플레이:",
    "Remote Player": "원격 플레이어",
    "AI Player 1": "AI 플레이어 1",
    "AI Player 2": "AI 플레이어 2",
    "AI Player 3": "AI 플레이어 3",
    "AI Player 4": "AI 플레이어 4",
    "Human": "인간",
    "AI Opponent": "AI 상대",
    "AI Difficulty": "AI 난이도",
    "Ready to Start": "시작 준비 완료",

    # ── 게임 상태 ──
    "Invited": "초대됨",
    "Waiting for Start": "시작 대기 중",
    "Waiting for Players": "플레이어 대기 중",
    "Waiting for Player": "플레이어 대기 중",
    "Waiting": "대기 중",
    "In Progress": "진행 중",
    "Completed": "완료",
    "Game Completed": "게임 완료",
    "Game Paused": "일시 정지",
    "Resume": "계속하기",
    "Forfeit": "기권",
    "Forfeits": "기권",
    "Finish": "종료",
    "Locked": "잠김",
    "Empty": "비어 있음",
    "(Open)": "(열림)",
    "(Closed)": "(닫힘)",
    "View": "보기",
    "Withdraw": "철회",
    "Reject": "거절",
    "Delete": "삭제",
    "Invite": "초대",
    "Start": "시작",
    "Join": "참가",
    "Confirm": "확인",
    "Done": "완료",
    "Continue": "계속",
    "Tap to Continue": "탭하여 계속",
    "Double Tap to Continue…": "두 번 탭하여 계속…",
    "No Card Selected": "선택된 카드 없음",

    # ── 온라인 / 연결 ──
    "Connecting to Server": "서버에 연결 중",
    "Failed to Connect to Server": "서버 연결 실패",
    "Connection Lost": "연결 끊김",
    "Creating Game . . .": "게임 생성 중...",
    "Successfully Created Game!": "게임 생성 완료!",
    "Unable to create.": "생성할 수 없습니다.",
    "Searching for Games . . .": "게임 검색 중...",
    "Joining Game . . .": "게임 참가 중...",
    "Successfully Joined Game!": "게임 참가 완료!",
    "Retrieving Profile . . .": "프로필 불러오는 중...",
    "Enter Name for Player": "플레이어 이름 입력",
    "Lobby Chat": "로비 채팅",
    "Game Chat": "게임 채팅",
    "Game Log": "게임 로그",
    "Please wait...": "잠시 기다려주세요...",
    "Creating a Quick Match game...": "빠른 매칭 게임 생성 중...",
    "Quick Match": "빠른 매칭",
    "Quick Match Request": "빠른 매칭 요청",
    "Request Match": "매치 요청",
    "Delete Matchmaking": "매치메이킹 삭제",
    "Accept Invite": "초대 수락",
    "Timer: Any": "타이머: 상관없음",
    "Any Rating": "모든 레이팅",

    # ── 계정 / 로그인 ──
    "Online Login": "온라인 로그인",
    "Create New Account": "새 계정 만들기",
    "Log Out": "로그아웃",
    "Email": "이메일",
    "User Name:": "사용자 이름:",
    "Enter Email": "이메일 입력",
    "Enter Password": "비밀번호 입력",
    "Enter Username": "사용자 이름을 입력하세요",
    "Enter text...": "텍스트 입력...",
    "Forgot Login?": "로그인 정보를 잊으셨나요?",
    "Verify:": "인증:",
    "Send Login Info": "로그인 정보 보내기",
    "Enter your Email or User Name": "이메일 또는 사용자 이름 입력",
    "Creating Account...": "계정 생성 중...",
    "Account error.": "계정 오류.",
    "Account creation failed.": "계정 생성 실패.",
    "Login failed": "로그인 실패",
    "Username already in use.": "이미 사용 중인 사용자 이름입니다.",
    "Invalid Password": "잘못된 비밀번호",
    "Invalid Email": "잘못된 이메일",
    "Invalid Characters": "이름에 잘못된 문자가 포함되어 있습니다",
    "Check your password again": "비밀번호를 다시 확인하세요",
    "Passwords do not match": "비밀번호가 일치하지 않습니다",
    "You must provide a password": "비밀번호를 입력해야 합니다",
    "An account with this e-mail address is already in use": "이 이메일 주소는 이미 사용 중입니다",
    "Please enter a valid E-mail address": "유효한 이메일 주소를 입력하세요",
    "Please enter a Username": "사용자 이름을 입력하세요",
    "I Agree": "동의합니다",
    "Newsletter Sign-Up": "뉴스레터 구독",
    "Privacy Policy": "개인정보 처리방침",
    "Notifications": "알림",
    "Email Notifications": "이메일 알림",
    "iOS Notifications": "iOS 알림",
    "Android Notifications": "Android 알림",

    # ── 친구 / 프로필 ──
    "Friends": "친구",
    "Friend Request": "친구 요청",
    "Profiles": "프로필",
    "Add Profile": "프로필 추가",
    "Remove Profile": "프로필 삭제",
    "Remove Friend": "친구 삭제",
    "Avatar Select": "아바타 선택",
    "On the Web": "웹에서 보기",
    "Opponent Stats": "상대 전적",
    "Rating": "레이팅",
    "Rating Difference": "레이팅 차이",
    "Previous Rating": "이전 레이팅",
    "Change": "변동",
    "New Rating": "새 레이팅",
    "Head to Head": "맞대결",
    "Wins Versus": "상대 전적 승",
    "Losses Versus": "상대 전적 패",
    "Viewing Player": "플레이어 보기",
    "No Player Data": "플레이어 데이터 없음",

    # ── 설정 ──
    "Languages": "언어",
    "Select Language": "언어 선택",
    "Resolution": "해상도",
    "Resolutions": "해상도",
    "Fullscreen": "전체 화면",
    "Windowed Mode": "창 모드",
    "Theme Selection": "테마 선택",
    "Key Bindings": "키 설정",
    "Audio Levels": "오디오 레벨",
    "Ambient Volume": "배경 음량",
    "Restore Defaults": "기본값 복원",
    "Help Enabled": "도움말 켜기",
    "Confirmation Pause": "확인 창 일시 정지",
    "Confirmation Pop-ups": "확인 팝업",
    "Game Speed": "게임 속도",
    "Auto Play": "자동 진행",
    "None": "없음",
    "Don't show this warning again": "이 경고를 다시 표시하지 않음",
    "Announcements": "공지사항",

    # ── 시간 / 요일 ──
    "Minute": "분",
    "Minutes": "분",
    "Hour": "시간",
    "Hours": "시간",
    "Day": "일",
    "Days": "일",
    "Second": "초",
    "Seconds": "초",
    "Sec": "초",
    "Min": "분",
    "HR": "시간",
    "Hrs": "시간",
    "Sunday": "일요일",
    "Sun": "일",
    "Monday": "월요일",
    "Mon": "월",
    "Tuesday": "화요일",
    "Tues": "화",
    "Wednesday": "수요일",
    "Wed": "수",
    "Thursday": "목요일",
    "Thurs": "목",
    "Friday": "금요일",
    "Fri": "금",
    "Saturday": "토요일",
    "Sat": "토",

    # ── 크레딧 ──
    "Programming": "프로그래밍",
    "Art Director": "아트 디렉터",
    "Production": "프로덕션",
    "Music and Sound": "음악 및 사운드",
    "Marketing and Community": "마케팅 및 커뮤니티",
    "QA Analysts ": "QA 분석가",

    # ── 로딩 / 기타 ──
    "Loading Cards": "카드 로딩 중",
    "Loading": "로딩 중",
    "In-App Store": "인앱 스토어",
    "Expire Timer": "만료 타이머",
    "No Card Selected": "선택된 카드 없음",
    "Game Stats": "게임 통계",
    "Game Type": "게임 유형",

    # ── 확인 메시지 ──
    "Do you want to delete this game?": "이 게임을 삭제하시겠습니까?",
    "Are you sure you want to forfeit this game?": "정말로 기권하시겠습니까?",
    "Are you sure you want to exit the game?": "정말로 게임을 종료하시겠습니까?",
    "Are you sure you want to withdraw from this game?": "정말로 이 게임에서 철회하시겠습니까?",
    "Are you sure you want to delete this Quick Match request?": "이 빠른 매칭 요청을 삭제하시겠습니까?",
    "Are you sure you want to delete this profile?": "이 프로필을 삭제하시겠습니까?",
    "Would you like to play the Tutorial?": "튜토리얼을 플레이하시겠습니까?",
    "Would you like to add this player to your friend list?": "이 플레이어를 친구 목록에 추가하시겠습니까?",
    "Change resolution to {0}x{1}?": "해상도를 {0}x{1}(으)로 변경하시겠습니까?",
    "Keep this resolution?": "이 해상도를 유지하시겠습니까?",
    "Confirm Change": "변경 확인",
    "Tap opponent  to view their profile": "상대를 탭하여 프로필 보기",
    "Press the new key for": "새 키를 누르세요:",

    # ── 포맷 포함 긴 메시지 ──
    "An update is available.<br>Please download the latest<br>version to play online.":
        "업데이트가 있습니다.<br>온라인 플레이를 위해<br>최신 버전을 다운로드하세요.",
    "You have been Disconnected<br> from the Server":
        "서버와의 연결이<br>끊어졌습니다",
    "Unable to create.<br>Too many games created.":
        "생성할 수 없습니다.<br>너무 많은 게임이 생성되었습니다.",
    "Unable to create.<br>Unknown error":
        "생성할 수 없습니다.<br>알 수 없는 오류",
    "Unable to join.<br>Game no longer exists.":
        "참가할 수 없습니다.<br>게임이 더 이상 존재하지 않습니다.",
    "Unable to join.<br>Game is full.":
        "참가할 수 없습니다.<br>게임이 가득 찼습니다.",
    "Unable to join.<br>Lost connection to server.":
        "참가할 수 없습니다.<br>서버 연결이 끊어졌습니다.",
    "Unable to join.<br>Unknown error.":
        "참가할 수 없습니다.<br>알 수 없는 오류",
    "You must be logged<br>in to Game Center<br>to play online":
        "온라인 플레이를 위해<br>Game Center에<br>로그인해야 합니다",
    "Account Created.<br>Enter your Password to Login.":
        "계정이 생성되었습니다.<br>비밀번호를 입력하여 로그인하세요.",
    "Successfully added\xa0\"{0}\"\xa0as a friend.":
        "\"{0}\" 님을 친구로 추가했습니다.",
    "Successfully removed friend.":
        "친구를 삭제했습니다.",
    "Removing \"{0}\" as a friend.":
        "\"{0}\" 님을 친구에서 삭제하는 중...",
    "Adding\xa0\"{0}\"\xa0as a friend.":
        "\"{0}\" 님을 친구로 추가하는 중...",
    "User\xa0\"{0}\"\xa0not found.":
        "사용자 \"{0}\" 님을 찾을 수 없습니다.",
    "{0} is already your friend.":
        "{0} 님은 이미 친구입니다.",
    "All opponents have forfeited.\xa0You win!":
        "모든 상대가 기권했습니다.\xa0승리!",
    "Unable to connect to the server":
        "서버에 연결할 수 없습니다",
    "Account is not yet activated. Please follow the account activation instructions that were sent to your e-mail.":
        "계정이 아직 활성화되지 않았습니다. 이메일로 전송된 계정 활성화 안내를 따라주세요.",
    "The Password and Confirmation fields do not match":
        "비밀번호와 확인 필드가 일치하지 않습니다",
    "Please check your email for your account information":
        "계정 정보를 위해 이메일을 확인하세요",
    "Name contains invalid characters":
        "이름에 허용되지 않는 문자가 포함되어 있습니다",
    "You must accept the Terms of Use Agreement before creating an account":
        "계정을 생성하기 전에 이용약관에 동의해야 합니다",
    "A profile with this name already exists":
        "이 이름의 프로필이 이미 존재합니다",
    "Creating this Quick Match failed.<br>Too many games open.":
        "빠른 매칭 생성 실패.<br>열려 있는 게임이 너무 많습니다.",
}


def main():
    strings_path = BASE / "translation/strings.json"
    strings = json.loads(strings_path.read_text("utf-8"))

    applied = 0
    missing = 0

    for row in strings["rows"]:
        if row["en"] == "EN":
            continue
        if row.get("ko"):
            continue

        en = row["en"]
        if en in TRANSLATIONS:
            row["ko"] = TRANSLATIONS[en]
            row["ko_source"] = "manual"
            applied += 1
        else:
            missing += 1
            print(f"  [MISS] {row['key']}: {repr(en)}")

    strings_path.write_text(
        json.dumps(strings, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )

    total_cs = sum(1 for r in strings["rows"] if r["en"] != "EN")
    cs_with_ko = sum(1 for r in strings["rows"] if r["en"] != "EN" and r.get("ko"))

    print(f"\n=== 결과 ===")
    print(f"적용: {applied}")
    print(f"누락: {missing}")
    print(f"Common_Strings: {cs_with_ko}/{total_cs} ({cs_with_ko/total_cs*100:.1f}%)")
    print(f"→ {strings_path}")


if __name__ == "__main__":
    main()
