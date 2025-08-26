#!/usr/bin/env python3
"""
Student Grade Manager - A Comprehensive Python Teaching Project
===============================================================

This project demonstrates:
- Object-Oriented Programming (Classes, Objects, Inheritance)
- File I/O and Data Persistence
- Data Structures (Lists, Dictionaries)
- Error Handling and Input Validation
- Data Visualization
- Menu-driven Programming
- String Formatting and Manipulation

Author: Teaching Assistant
Purpose: Educational demonstration for coding students
"""

import json
import os
import sys
from datetime import datetime
from typing import List, Dict, Optional

# Import custom modules
from student import Student
from grade_manager import GradeManager
from utils import clear_screen, get_valid_input, print_header, print_separator


def display_main_menu():
    """Display the main menu options"""
    clear_screen()
    print_header("🎓 STUDENT GRADE MANAGER 🎓")
    print("1. Add New Student")
    print("2. View All Students")
    print("3. Add Grade to Student")
    print("4. View Student Details")
    print("5. Calculate Class Statistics")
    print("6. Generate Grade Report")
    print("7. Visualize Grades")
    print("8. Save Data")
    print("9. Load Data")
    print("0. Exit")
    print_separator()


def main():
    """Main program loop"""
    # Initialize the grade manager
    manager = GradeManager()
    
    # Load existing data if available
    if os.path.exists("students_data.json"):
        try:
            manager.load_from_file("students_data.json")
            print("✅ Previous data loaded successfully!")
        except Exception as e:
            print(f"⚠️  Could not load previous data: {e}")
    
    print("Welcome to the Student Grade Manager!")
    print("This system helps you manage student information and grades.")
    input("Press Enter to continue...")
    
    # Main program loop
    while True:
        display_main_menu()
        
        choice = get_valid_input(
            "Enter your choice (0-9): ",
            input_type="int",
            min_val=0,
            max_val=9
        )
        
        try:
            if choice == 1:
                add_new_student(manager)
            elif choice == 2:
                view_all_students(manager)
            elif choice == 3:
                add_grade_to_student(manager)
            elif choice == 4:
                view_student_details(manager)
            elif choice == 5:
                show_class_statistics(manager)
            elif choice == 6:
                generate_grade_report(manager)
            elif choice == 7:
                visualize_grades(manager)
            elif choice == 8:
                save_data(manager)
            elif choice == 9:
                load_data(manager)
            elif choice == 0:
                # Auto-save before exit
                try:
                    manager.save_to_file("students_data.json")
                    print("✅ Data saved automatically!")
                except Exception as e:
                    print(f"⚠️  Could not save data: {e}")
                
                print("Thank you for using Student Grade Manager! 👋")
                sys.exit(0)
                
        except KeyboardInterrupt:
            print("\n\n👋 Goodbye!")
            sys.exit(0)
        except Exception as e:
            print(f"\n❌ An error occurred: {e}")
            input("Press Enter to continue...")


def add_new_student(manager: GradeManager):
    """Add a new student to the system"""
    clear_screen()
    print_header("ADD NEW STUDENT")
    
    # Get student information
    name = get_valid_input("Enter student name: ", input_type="str", min_length=2)
    student_id = get_valid_input("Enter student ID: ", input_type="str", min_length=1)
    
    # Check if student ID already exists
    if manager.find_student(student_id):
        print(f"❌ Student with ID '{student_id}' already exists!")
        input("Press Enter to continue...")
        return
    
    email = get_valid_input("Enter student email: ", input_type="email")
    
    # Create and add student
    student = Student(name, student_id, email)
    manager.add_student(student)
    
    print(f"✅ Student '{name}' added successfully!")
    input("Press Enter to continue...")


def view_all_students(manager: GradeManager):
    """Display all students in the system"""
    clear_screen()
    print_header("ALL STUDENTS")
    
    students = manager.get_all_students()
    
    if not students:
        print("📭 No students found in the system.")
    else:
        print(f"📊 Total Students: {len(students)}")
        print_separator()
        
        for i, student in enumerate(students, 1):
            avg_grade = student.get_average_grade()
            grade_count = len(student.grades)
            
            print(f"{i}. {student.name}")
            print(f"   ID: {student.student_id} | Email: {student.email}")
            print(f"   Grades: {grade_count} | Average: {avg_grade:.1f}%" if grade_count > 0 else "   No grades yet")
            print()
    
    input("Press Enter to continue...")


def add_grade_to_student(manager: GradeManager):
    """Add a grade to a specific student"""
    clear_screen()
    print_header("ADD GRADE TO STUDENT")
    
    if not manager.get_all_students():
        print("📭 No students found. Please add students first.")
        input("Press Enter to continue...")
        return
    
    # Show all students
    print("Available students:")
    students = manager.get_all_students()
    for i, student in enumerate(students, 1):
        print(f"{i}. {student.name} (ID: {student.student_id})")
    
    print_separator()
    
    # Get student selection
    student_choice = get_valid_input(
        f"Select student (1-{len(students)}): ",
        input_type="int",
        min_val=1,
        max_val=len(students)
    )
    
    selected_student = students[student_choice - 1]
    
    # Get grade information
    subject = get_valid_input("Enter subject: ", input_type="str", min_length=1)
    grade = get_valid_input("Enter grade (0-100): ", input_type="float", min_val=0, max_val=100)
    
    # Add the grade
    selected_student.add_grade(subject, grade)
    
    print(f"✅ Grade {grade}% in {subject} added to {selected_student.name}!")
    input("Press Enter to continue...")


def view_student_details(manager: GradeManager):
    """View detailed information about a specific student"""
    clear_screen()
    print_header("STUDENT DETAILS")
    
    if not manager.get_all_students():
        print("📭 No students found. Please add students first.")
        input("Press Enter to continue...")
        return
    
    # Get student ID
    student_id = get_valid_input("Enter student ID: ", input_type="str")
    student = manager.find_student(student_id)
    
    if not student:
        print(f"❌ Student with ID '{student_id}' not found!")
        input("Press Enter to continue...")
        return
    
    # Display student information
    print(f"👤 Name: {student.name}")
    print(f"🆔 ID: {student.student_id}")
    print(f"📧 Email: {student.email}")
    print(f"📅 Enrolled: {student.enrollment_date}")
    
    print_separator()
    
    if student.grades:
        print("📊 GRADES:")
        total_grade = 0
        for subject, grade in student.grades.items():
            print(f"   {subject}: {grade}%")
            total_grade += grade
        
        avg_grade = student.get_average_grade()
        print(f"\n📈 Average Grade: {avg_grade:.1f}%")
        print(f"🎯 Letter Grade: {student.get_letter_grade()}")
        print(f"📚 Total Subjects: {len(student.grades)}")
    else:
        print("📭 No grades recorded yet.")
    
    input("Press Enter to continue...")


def show_class_statistics(manager: GradeManager):
    """Display class-wide statistics"""
    clear_screen()
    print_header("CLASS STATISTICS")
    
    stats = manager.get_class_statistics()
    
    if not stats:
        print("📭 No data available for statistics.")
        input("Press Enter to continue...")
        return
    
    print(f"👥 Total Students: {stats['total_students']}")
    print(f"📊 Students with Grades: {stats['students_with_grades']}")
    
    if stats['students_with_grades'] > 0:
        print_separator()
        print(f"📈 Class Average: {stats['class_average']:.1f}%")
        print(f"🏆 Highest Grade: {stats['highest_grade']:.1f}%")
        print(f"📉 Lowest Grade: {stats['lowest_grade']:.1f}%")
        
        print_separator()
        print("🎯 GRADE DISTRIBUTION:")
        for grade, count in stats['grade_distribution'].items():
            percentage = (count / stats['students_with_grades']) * 100
            print(f"   {grade}: {count} students ({percentage:.1f}%)")
    
    input("Press Enter to continue...")


def generate_grade_report(manager: GradeManager):
    """Generate and save a detailed grade report"""
    clear_screen()
    print_header("GENERATE GRADE REPORT")
    
    report = manager.generate_report()
    
    # Save report to file
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"grade_report_{timestamp}.txt"
    
    try:
        with open(filename, 'w') as f:
            f.write(report)
        
        print(f"✅ Report generated successfully!")
        print(f"📄 Saved as: {filename}")
        print_separator()
        print("Report Preview:")
        print(report[:500] + "..." if len(report) > 500 else report)
        
    except Exception as e:
        print(f"❌ Error generating report: {e}")
    
    input("Press Enter to continue...")


def visualize_grades(manager: GradeManager):
    """Create visualizations of grade data"""
    clear_screen()
    print_header("VISUALIZE GRADES")
    
    try:
        manager.create_visualizations()
        print("✅ Visualizations created successfully!")
        print("📊 Check the following files:")
        print("   - grade_distribution.png")
        print("   - student_averages.png")
        print("   - subject_performance.png")
    except ImportError:
        print("⚠️  Matplotlib not installed. Install with: pip install matplotlib")
    except Exception as e:
        print(f"❌ Error creating visualizations: {e}")
    
    input("Press Enter to continue...")


def save_data(manager: GradeManager):
    """Save data to file"""
    clear_screen()
    print_header("SAVE DATA")
    
    filename = get_valid_input(
        "Enter filename (or press Enter for default): ",
        input_type="str",
        required=False
    ) or "students_data.json"
    
    try:
        manager.save_to_file(filename)
        print(f"✅ Data saved successfully to '{filename}'!")
    except Exception as e:
        print(f"❌ Error saving data: {e}")
    
    input("Press Enter to continue...")


def load_data(manager: GradeManager):
    """Load data from file"""
    clear_screen()
    print_header("LOAD DATA")
    
    filename = get_valid_input("Enter filename: ", input_type="str")
    
    if not os.path.exists(filename):
        print(f"❌ File '{filename}' not found!")
        input("Press Enter to continue...")
        return
    
    try:
        manager.load_from_file(filename)
        print(f"✅ Data loaded successfully from '{filename}'!")
    except Exception as e:
        print(f"❌ Error loading data: {e}")
    
    input("Press Enter to continue...")


if __name__ == "__main__":
    main()