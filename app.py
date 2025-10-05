import streamlit as st
import pandas as pd
from functions import (
    add_student, edit_student, delete_student, get_students,
    add_subject, delete_subject, get_subjects,
    add_marks, edit_marks, delete_marks, get_marks,
    get_all_report_cards
)

st.set_page_config(page_title="Student Report Card Management", layout="wide")
st.title("🎓 Student Report Card Management System")

menu = [
    "Add Student", "Edit Student", "Delete Student",
    "Add Subject", "Delete Subject",
    "Add Marks", "Edit Marks", "Delete Marks",
    "Show Report Card (single)", "View All Report Cards", "Download Report Cards CSV"
]
choice = st.sidebar.selectbox("Choose Action", menu)

st.sidebar.markdown("---")
st.sidebar.markdown("Made with ❤️ and Streamlit")

# Add Student
if choice == "Add Student":
    st.header("Add New Student")
    name = st.text_input("Full Name", key="add_name")
    class_name = st.text_input("Class", key="add_class")
    roll_number = st.text_input("Roll Number", key="add_roll")
    if st.button("Add", key="add_btn") and name and class_name and roll_number:
        add_student(name, class_name, roll_number)
        st.success(f"Student '{name}' has been added!")

# Edit Student
elif choice == "Edit Student":
    st.header("Edit Student Details")
    students = get_students()
    if students:
        row = st.selectbox("Select Student", students, format_func=lambda x: f"{x[1]} ({x[2]})", key="edit_select_student")
        name = st.text_input("New Name", value=row[1], key="edit_name")
        class_name = st.text_input("New Class", value=row[2], key="edit_class")
        roll_number = st.text_input("New Roll Number", value=row[3], key="edit_roll")
        if st.button("Save", key="edit_btn") and name and class_name and roll_number:
            edit_student(row[0], name, class_name, roll_number)
            st.success("Details updated!")
    else:
        st.info("No students available.")

# Delete Student
elif choice == "Delete Student":
    st.header("Delete Student")
    students = get_students()
    if students:
        row = st.selectbox("Select Student", students, format_func=lambda x: f"{x[1]} ({x[2]})", key="delete_select_student")
        if st.button("Delete", key="delete_btn"):
            delete_student(row[0])
            st.success("Student deleted!")
    else:
        st.info("No students available.")

# Add Subject
elif choice == "Add Subject":
    st.header("Add Subject")
    subject_name = st.text_input("Subject Name", key="add_subject")
    if st.button("Add", key="add_subject_btn") and subject_name:
        add_subject(subject_name)
        st.success(f"Subject '{subject_name}' added!")

# Delete Subject
elif choice == "Delete Subject":
    st.header("Delete Subject")
    subjects = get_subjects()
    if subjects:
        row = st.selectbox("Select Subject", subjects, format_func=lambda x: x[1], key="delete_subject_select")
        if st.button("Delete", key="delete_subject_btn"):
            delete_subject(row[0])
            st.success("Subject deleted!")
    else:
        st.info("No subjects available.")

# Add Marks
elif choice == "Add Marks":
    st.header("Add Marks")
    students = get_students()
    subjects = get_subjects()
    if students and subjects:
        student = st.selectbox("Student", students, format_func=lambda x: f"{x[1]} ({x[2]})", key="add_marks_student")
        subject = st.selectbox("Subject", subjects, format_func=lambda x: x[1], key="add_marks_subject")
        marks = st.number_input("Marks", min_value=0, max_value=100, key="add_marks_value")
        if st.button("Add", key="add_marks_btn"):
            add_marks(student[0], subject[0], marks)
            st.success("Marks added!")
    else:
        st.info("Need students and subjects to add marks.")

# Edit Marks
elif choice == "Edit Marks":
    st.header("Edit Marks")
    students = get_students()
    if students:
        student = st.selectbox("Student", students, format_func=lambda x: f"{x[1]} ({x[2]})", key="edit_marks_student")
        marks_list = get_marks(student[0])
        if marks_list:
            entry = st.selectbox("Select Mark Entry", marks_list, format_func=lambda x: f"{x[1]}: {x[2]}", key="edit_marks_entry")
            new_mark = st.number_input("New Marks", min_value=0, max_value=100, value=entry[2], key="edit_marks_value")
            if st.button("Update", key="edit_marks_btn"):
                edit_marks(entry[0], new_mark)
                st.success("Marks updated!")
        else:
            st.info("No marks for this student.")
    else:
        st.info("No students available.")

# Delete Marks
elif choice == "Delete Marks":
    st.header("Delete Marks")
    students = get_students()
    if students:
        student = st.selectbox("Student", students, format_func=lambda x: f"{x[1]} ({x[2]})", key="delete_marks_student")
        marks_list = get_marks(student[0])
        if marks_list:
            entry = st.selectbox("Select Mark Entry", marks_list, format_func=lambda x: f"{x[1]}: {x[2]}", key="delete_marks_entry")
            if st.button("Delete", key="delete_marks_btn"):
                delete_marks(entry[0])
                st.success("Marks deleted!")
        else:
            st.info("No marks for this student.")
    else:
        st.info("No students available.")

# Show Single Report Card
elif choice == "Show Report Card (single)":
    st.header("Show Student Report Card")
    students = get_students()
    if students:
        student = st.selectbox("Student", students, format_func=lambda x: f"{x[1]} ({x[2]})", key="single_report_student")
        marks_list = get_marks(student[0])
        if marks_list:
            total = sum(x[2] for x in marks_list)
            percentage = total / len(marks_list) if marks_list else 0
            if percentage >= 90:
                grade = "A"
            elif percentage >= 75:
                grade = "B"
            elif percentage >= 60:
                grade = "C"
            elif percentage >= 40:
                grade = "D"
            else:
                grade = "F"
            st.markdown(f"**Total Marks:** {total}")
            st.markdown(f"**Percentage:** {percentage:.2f}%")
            st.markdown(f"**Grade:** {grade}")
            st.write("Marks per subject:")
            for _, subject, marks in marks_list:
                st.write(f"{subject}: {marks}")
            # Chart
            st.subheader("Marks Chart")
            chart_df = pd.DataFrame({
                'Subject': [x[1] for x in marks_list],
                'Marks': [x[2] for x in marks_list]
            })
            st.bar_chart(chart_df.set_index('Subject'))
        else:
            st.info("No marks for this student.")
    else:
        st.info("No students available.")

# View All Report Cards
elif choice == "View All Report Cards":
    st.header("All Students' Report Cards")
    data = get_all_report_cards()
    if data:
        df = pd.DataFrame(data, columns=["ID", "Name", "Class", "Roll", "Subject", "Marks"])
        selected_class = st.selectbox("Filter by Class", ["All"] + sorted(df["Class"].unique().tolist()), key="viewall_class_filter")
        selected_subject = st.selectbox("Filter by Subject", ["All"] + sorted(df["Subject"].unique().tolist()), key="viewall_subject_filter")
        if selected_class != "All":
            df = df[df['Class'] == selected_class]
        if selected_subject != "All":
            df = df[df['Subject'] == selected_subject]
        st.dataframe(df)
        st.subheader("Average Marks by Subject (Chart)")
        avg_df = df.groupby("Subject")["Marks"].mean().reset_index()
        st.bar_chart(avg_df.set_index("Subject"))
    else:
        st.info("No data available.")

# Export to CSV
elif choice == "Download Report Cards CSV":
    st.header("Download All Report Cards")
    data = get_all_report_cards()
    if data:
        df = pd.DataFrame(data, columns=["ID", "Name", "Class", "Roll", "Subject", "Marks"])
        st.download_button("Download as CSV", df.to_csv(index=False), file_name="report_cards.csv", key="export_csv_btn")
    else:
        st.info("No data to download.")
