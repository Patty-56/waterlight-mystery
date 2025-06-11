
import streamlit as st
import os
import json

# 建立資料夾（如不存在）
os.makedirs("data", exist_ok=True)

# 初始化 progress.json（若尚未建立）
def init_progress():
    if not os.path.exists("data/progress.json"):
        with open("data/progress.json", "w") as f:
            json.dump({
                "current_day": 1,
                "story_unlocked": [],
                "last_result": "none",
                "user_data": {}
            }, f, indent=4)

# 載入進度
def load_progress():
    with open("data/progress.json", "r") as f:
        return json.load(f)

# 儲存進度
def save_progress(data):
    with open("data/progress.json", "w") as f:
        json.dump(data, f, indent=4)

# 初始化
init_progress()
progress = load_progress()
current_day = progress["current_day"]
user_data = progress.get("user_data", {})

# Streamlit UI
st.set_page_config(page_title="水色之夜", layout="centered")
st.title("🌌 水色之夜：21天健康解謎遊戲")
st.markdown(f"### 📅 第 {current_day} 天")

# 個人資料輸入
height = st.number_input("請輸入你的身高（cm）", value=user_data.get("height", 160))
weight = st.number_input("請輸入你的體重（kg）", value=user_data.get("weight", 50))
location = st.text_input("請輸入你所在的地區", value=user_data.get("location", "台北"))

if st.button("📌 儲存個人資料"):
    progress["user_data"] = {
        "height": height,
        "weight": weight,
        "location": location
    }
    save_progress(progress)
    st.success("✅ 已儲存個人資料")

# 建議值
suggested_water = weight * 30
suggested_steps = 8000
st.markdown(f"### 💧 今日建議：
- 建議喝水量：{suggested_water:.0f} cc
- 建議步數：{suggested_steps} 步")

# 打卡輸入
real_water = st.number_input("實際喝水量（cc）", min_value=0)
real_steps = st.number_input("實際步數", min_value=0)

# 打卡按鈕
if st.button("✅ 打卡提交"):
    if real_water >= suggested_water and real_steps >= suggested_steps:
        story_path = f"story/day{current_day}.txt"
        teaching_path = f"teaching/day{current_day}.txt"
        puzzle_path = f"puzzle/day{current_day}.txt"

        st.success("🎉 恭喜你打卡成功，進入今日任務")
        if os.path.exists(story_path):
            with open(story_path, "r", encoding="utf-8") as f:
                st.markdown("#### 📖 今日劇情")
                st.info(f.read())

        if os.path.exists(teaching_path):
            with open(teaching_path, "r", encoding="utf-8") as f:
                st.markdown("#### 📘 今日程式教學")
                st.write(f.read())

        answer = ""
        if os.path.exists(puzzle_path):
            with open(puzzle_path, "r", encoding="utf-8") as f:
                st.markdown("#### ❓ 今日問題")
                question = f.read()
                st.write(question)
                answer = st.text_input("請輸入你的答案（例如 A 或 B）").strip().upper()

        if st.button("🧠 提交解答"):
            correct = "B" if current_day % 3 == 1 else "C"  # 模擬答案規則
            if answer == correct:
                st.success("✅ 答對了！獲得今日線索")
                progress["story_unlocked"].append(current_day)
                progress["last_result"] = "success"
                if current_day < 21:
                    progress["current_day"] += 1
                save_progress(progress)
                st.balloons()
            else:
                st.error("❌ 答錯了，請再觀察線索思考")
    else:
        st.error("喝水或步數未達標，已重置至第 1 天")
        progress["current_day"] = 1
        progress["story_unlocked"] = []
        progress["last_result"] = "fail"
        save_progress(progress)
