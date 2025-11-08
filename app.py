import streamlit as st 
import random

# --------------------------
# بيانات داخلية لتوليد الأسئلة
# --------------------------

concepts = [
    "variables", "loops", "functions", "recursion", "OOP", "arrays",
    "conditions", "exceptions", "strings", "dictionaries"
]

# --------------------------
# أسئلة MCQ مع مستوى صعوبة: "easy", "medium", "hard"
# --------------------------
mcq_templates = [
    ("What is the output of the following code?\n\n{code}\n\nA) {a}\nB) {b}\nC) {c}\nD) {d}\n", "A", "easy"),
    ("Which of the following is TRUE about {concept}?\nA) {a}\nB) {b}\nC) {c}\nD) {d}\n", "B", "medium")
]

true_false_templates = [
    ("{concept}: {statement} (True/False)", "True", "easy"),
    ("Is the following statement correct?\n{statement} (True/False)", "False", "medium")
]

debug_templates = [
    ("Find the error in this code and fix it:\n\n{code}", None, "hard"),
    ("What will cause this code to crash?\n\n{code}", None, "hard")
]

# --------------------------
# دوال توليد البيانات
# --------------------------

def random_code_snippet():
    snippets = [
        "x = 5\nprint(x * 2)",
        "for i in range(3):\n    print(i)",
        "def add(a, b):\n    return a + b\nprint(add(2, 3))",
        "nums = [1, 2, 3]\nprint(nums[1])",
        "s = 'hello'\nprint(s.upper())"
    ]
    return random.choice(snippets)

def random_answers():
    return {
        "a": str(random.randint(1, 20)),
        "b": str(random.randint(1, 20)),
        "c": str(random.randint(1, 20)),
        "d": str(random.randint(1, 20)),
    }

def generate_mcq():
    template, correct, difficulty = random.choice(mcq_templates)
    code = random_code_snippet()
    ans = random_answers()
    concept = random.choice(concepts)
    text = template.format(code=code, concept=concept, **ans)
    return text, correct, difficulty

def generate_true_false():
    template, correct, difficulty = random.choice(true_false_templates)
    statement = random.choice([
        "A loop always runs at least once",
        "A function can return multiple values",
        "Strings are immutable",
        "Python uses indentation to define blocks"
    ])
    concept = random.choice(concepts)
    text = template.format(concept=concept, statement=statement)
    return text, correct, difficulty

def generate_debug():
    code = random.choice([
        "for i in range(5)\n    print(i)",
        "x = [1, 2, 3]\nprint(x[3])",
        "def f()\n    return 10",
        "print(unknown_var)"
    ])
    template = random.choice(debug_templates)
    if "{code}" in template[0]:
        text = template[0].format(code=code)
    else:
        text = template[0]
    return text, None, "hard"

def generate_test(num_questions=5):
    questions = []
    difficulties = ["easy", "medium", "hard"]
    # تقسيم الأسئلة بالتساوي حسب الصعوبة
    for i in range(1, num_questions + 1):
        q_type = random.choice(["mcq", "tf", "debug"])
        if q_type == "mcq":
            q, a, d = generate_mcq()
        elif q_type == "tf":
            q, a, d = generate_true_false()
        else:
            q, a, d = generate_debug()
        questions.append((i, q, a, d))
    return questions

# --------------------------
# واجهة Streamlit + التصحيح
# --------------------------

st.title("✅ مولّد اختبارات برمجية تلقائيًا مع مستويات صعوبة")
st.write("اضغط زر التوليد لإنشاء اختبار جديد بدون أي API خارجية.")

num = st.slider("عدد الأسئلة:", 3, 20, 7)

if st.button("✨ توليد اختبار"):
    questions = generate_test(num)

    user_answers = {}
    correct_answers = {}
    difficulties = {}

    for idx, q, a, d in questions:
        st.subheader(f"Q{idx} (Difficulty: {d.capitalize()})")
        st.code(q)

        if a:
            user_answers[idx] = st.text_input(f"إجابتك للسؤال {idx}:", key=f"ans_{idx}")
            correct_answers[idx] = a
        else:
            st.info("🔧 هذا السؤال للتصحيح ولا يحتاج إجابة.")
            correct_answers[idx] = None

        difficulties[idx] = d
        st.markdown("---")

    # زر التصحيح
    if st.button("✅ تصحيح الإجابات"):
        st.subheader("نتيجة التصحيح:")

        total = 0
        correct_count = 0
        total_questions = len(user_answers)

        progress_bar = st.progress(0)

        for idx, qindex in enumerate(user_answers):
            user = user_answers[qindex].strip().lower()
            correct = correct_answers[qindex].strip().lower()

            if user == correct:
                st.success(f"✅ سؤال {qindex}: إجابة صحيحة!")
                correct_count += 1
            else:
                st.error(f"❌ سؤال {qindex}: إجابة خاطئة. الصحيحة هي: **{correct_answers[qindex]}**")

            total += 1

            # تحديث شريط التقدم وتلوينه حسب النسبة
            pct = int((idx + 1) / total_questions * 100)
            if pct >= 80:
                progress_bar.progress(pct)
            elif 50 <= pct < 80:
                progress_bar.progress(pct)
            else:
                progress_bar.progress(pct)

        # النتيجة النهائية
        score = correct_count
        percentage = (correct_count / total) * 100 if total > 0 else 0

        st.write("---")
        st.subheader("📊 النتيجة النهائية")
        st.info(f"✅ الدرجة: **{score} / {total}**")
        st.info(f"📈 نسبة النجاح: **{percentage:.2f}%**")
