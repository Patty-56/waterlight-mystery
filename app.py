import streamlit as st
import os
import json

# 建立資料夾（如不存在）
os.makedirs("data", exist_ok=True)

# 初始化 progress.json
def init_progress():
    path = "data/progress.json"
    if not os.path.exists(path):
        with open(path, "w") as f:
            json.dump({
                "current_day": 1,
                "story_unlocked": [],
                "last_result": "none",
                "user_data": {}
            }, f, indent=4)

# 讀寫進度
def load_progress():
    with open("data/progress.json", "r") as f:
        return json.load(f)

def save_progress(data):
    with open("data/progress.json", "w") as f:
        json.dump(data, f, indent=4)

# 初始化
init_progress()
progress = load_progress()
current_day = progress["current_day"]

# UI
st.set_page_config(page_title="水色之夜", layout="centered")
st.title("🌌 水色之夜")
st.markdown(f"### 📅 第 {current_day} 天")

# 輸入資料
height = st.number_input("請輸入身高（cm）", value=progress["user_data"].get("height", 160))
weight = st.number_input("請輸入體重（kg）", value=progress["user_data"].get("weight", 50))
location = st.text_input("請輸入地區", value=progress["user_data"].get("location", "台北"))

if st.button("📌 儲存個人資料"):
    progress["user_data"] = {
        "height": height,
        "weight": weight,
        "location": location
    }
    save_progress(progress)
    st.success("✅ 已儲存個人資料")

# 建議喝水量與步數
suggested_water = weight * 30
suggested_steps = 8000
real_water = st.number_input("實際喝水量（cc）", min_value=0)
real_steps = st.number_input("實際步數", min_value=0)

# 打卡提交
if st.button("✅ 打卡提交"):
    if real_water >= suggested_water and real_steps >= suggested_steps:
        st.success("🎉 打卡成功，進入今日任務")

        story_path = f"story/day{current_day}.txt"
        teaching_path = f"teaching/day{current_day}.txt"
        puzzle_path = f"puzzle/day{current_day}.txt"

        # 顯示劇情
        if os.path.exists(story_path):
            with open(story_path, "r", encoding="utf-8") as f:
                st.markdown("#### 📖 今日劇情")
                st.info(f.read())

        # 顯示教學
        if os.path.exists(teaching_path):
            with open(teaching_path, "r", encoding="utf-8") as f:
                st.markdown("#### 📘 解題提示")
                st.write(f.read())

        # 顯示題目
        if os.path.exists(puzzle_path):
            with open(puzzle_path, "r", encoding="utf-8") as f:
                st.markdown("#### ❓ 解謎題目")
                st.write(f.read())

            answer = st.text_input("請輸入你的答案（A/B/C）").strip().upper()

            if st.button("🧠 提交解答"):
                correct = "B" if current_day % 3 == 1 else "C"  # 模擬答案
                if answer == correct:
                    st.success("✅ 答對了！獲得今日線索")
                    progress["story_unlocked"].append(current_day)
                    progress["last_result"] = "success"
                    if current_day < 21:
                        progress["current_day"] += 1
                    save_progress(progress)
                    st.balloons()
                else:
                    st.error("❌ 答錯了，請再思考")
    else:
        st.error("喝水或步數未達標，已重置至第 1 天")
        progress["current_day"] = 1
        progress["story_unlocked"] = []
        progress["last_result"] = "fail"
        save_progress(progress)
