#!/usr/bin/env python3
"""
Student Grade Manager - Demonstration Script
============================================

This script demonstrates the key features of the Student Grade Manager
by automatically creating sample data and showing various operations.

Perfect for:
- Classroom demonstrations
- Testing the application
- Understanding the API
- Quick setup with sample data

Run this script to see the system in action!
"""

import json
import os
from student import Student
from grade_manager import GradeManager


def create_sample_data() -> GradeManager:
    """
    Create a GradeManager with comprehensive sample data.
    
    Returns:
        GradeManager: Manager with sample students and grades
    """
    print("🎓 Creating sample student data...")
    
    manager = GradeManager()
    
    # Sample student data with realistic information
    sample_students = [
        {
            "name": "Alice Johnson",
            "id": "STU001",
            "email": "alice.johnson@school.edu",
            "grades": {
                "Mathematics": 92.5,
                "Science": 88.0,
                "English": 95.5,
                "History": 87.0,
                "Art": 91.0
            }
        },
        {
            "name": "Bob Smith",
            "id": "STU002", 
            "email": "bob.smith@school.edu",
            "grades": {
                "Mathematics": 78.5,
                "Science": 82.0,
                "English": 75.0,
                "History": 80.5,
                "Physical Education": 95.0
            }
        },
        {
            "name": "Carol Davis",
            "id": "STU003",
            "email": "carol.davis@school.edu",
            "grades": {
                "Mathematics": 95.0,
                "Science": 93.5,
                "English": 89.0,
                "History": 92.0,
                "Art": 88.5,
                "Music": 96.0
            }
        },
        {
            "name": "David Wilson",
            "id": "STU004",
            "email": "david.wilson@school.edu",
            "grades": {
                "Mathematics": 65.0,
                "Science": 70.5,
                "English": 68.0,
                "History": 72.0,
                "Physical Education": 85.0
            }
        },
        {
            "name": "Emma Brown",
            "id": "STU005",
            "email": "emma.brown@school.edu",
            "grades": {
                "Mathematics": 88.5,
                "Science": 91.0,
                "English": 92.5,
                "History": 85.0,
                "Art": 94.0,
                "Music": 89.0,
                "Physical Education": 87.5
            }
        },
        {
            "name": "Frank Miller",
            "id": "STU006",
            "email": "frank.miller@school.edu",
            "grades": {
                "Mathematics": 55.0,
                "Science": 58.5,
                "English": 62.0,
                "History": 59.0
            }
        },
        {
            "name": "Grace Lee",
            "id": "STU007",
            "email": "grace.lee@school.edu",
            "grades": {
                "Mathematics": 97.0,
                "Science": 95.5,
                "English": 93.0,
                "History": 96.0,
                "Art": 92.5,
                "Music": 98.0
            }
        },
        {
            "name": "Henry Taylor",
            "id": "STU008",
            "email": "henry.taylor@school.edu",
            "grades": {
                "Mathematics": 73.0,
                "Science": 76.5,
                "English": 71.0,
                "Physical Education": 90.0
            }
        }
    ]
    
    # Create and add students
    for student_data in sample_students:
        student = Student(student_data["name"], student_data["id"], student_data["email"])
        
        # Add grades
        for subject, grade in student_data["grades"].items():
            student.add_grade(subject, grade)
        
        manager.add_student(student)
        print(f"✅ Added {student.name} with {len(student_data['grades'])} grades")
    
    print(f"\n🎉 Created {len(manager)} students with sample data!")
    return manager


def demonstrate_basic_operations(manager: GradeManager):
    """Demonstrate basic operations with the sample data."""
    print("\n" + "="*60)
    print("🔍 DEMONSTRATING BASIC OPERATIONS")
    print("="*60)
    
    # Show all students
    print("\n📚 All Students:")
    print("-" * 30)
    for i, student in enumerate(manager.get_all_students(), 1):
        avg = student.get_average_grade()
        print(f"{i}. {student.name} - Average: {avg:.1f}% ({student.get_letter_grade()})")
    
    # Find a specific student
    print("\n🔍 Finding specific student (STU003):")
    student = manager.find_student("STU003")
    if student:
        print(f"Found: {student.name}")
        print(f"Email: {student.email}")
        print(f"Subjects: {', '.join(student.get_subjects())}")
        highest_subject, highest_grade = student.get_highest_grade()
        print(f"Best subject: {highest_subject} ({highest_grade}%)")
    
    # Show grade distribution
    print("\n📊 Students by Letter Grade:")
    print("-" * 30)
    for grade in ['A', 'B', 'C', 'D', 'F']:
        students = manager.get_students_by_letter_grade(grade)
        print(f"Grade {grade}: {len(students)} students")
        for student in students:
            print(f"  - {student.name}")


def demonstrate_statistics(manager: GradeManager):
    """Demonstrate statistical analysis features."""
    print("\n" + "="*60)
    print("📊 DEMONSTRATING STATISTICAL ANALYSIS")
    print("="*60)
    
    stats = manager.get_class_statistics()
    
    print(f"\n📈 Class Overview:")
    print(f"Total Students: {stats['total_students']}")
    print(f"Students with Grades: {stats['students_with_grades']}")
    print(f"Class Average: {stats['class_average']}%")
    print(f"Highest Grade: {stats['highest_grade']}%")
    print(f"Lowest Grade: {stats['lowest_grade']}%")
    print(f"Passing Rate: {stats['passing_rate']}%")
    
    print(f"\n🎯 Grade Distribution:")
    for grade, count in stats['grade_distribution'].items():
        percentage = (count / stats['students_with_grades']) * 100
        bar = "█" * (count * 2)  # Simple text bar
        print(f"  {grade}: {count:2d} students ({percentage:4.1f}%) {bar}")
    
    print(f"\n📚 Subject Performance:")
    for subject, avg in sorted(stats['subject_averages'].items()):
        print(f"  {subject:<20}: {avg:5.1f}%")
    
    # Top performers
    print(f"\n🏆 Top 3 Students:")
    top_students = manager.get_top_students(3)
    for i, student in enumerate(top_students, 1):
        avg = student.get_average_grade()
        print(f"  {i}. {student.name:<20} - {avg:5.1f}% ({student.get_letter_grade()})")
    
    # Students needing help
    failing_students = manager.get_failing_students()
    if failing_students:
        print(f"\n⚠️  Students Needing Support ({len(failing_students)}):")
        for student in failing_students:
            avg = student.get_average_grade()
            print(f"  - {student.name:<20} - {avg:5.1f}%")


def demonstrate_file_operations(manager: GradeManager):
    """Demonstrate file I/O operations."""
    print("\n" + "="*60)
    print("💾 DEMONSTRATING FILE OPERATIONS")
    print("="*60)
    
    # Save data to JSON
    filename = "demo_student_data.json"
    print(f"\n💾 Saving data to {filename}...")
    try:
        manager.save_to_file(filename)
        print("✅ Data saved successfully!")
        
        # Show file info
        if os.path.exists(filename):
            file_size = os.path.getsize(filename)
            print(f"📄 File size: {file_size} bytes")
    except Exception as e:
        print(f"❌ Error saving data: {e}")
    
    # Generate a comprehensive report
    report_filename = "demo_grade_report.txt"
    print(f"\n📄 Generating report to {report_filename}...")
    try:
        report = manager.generate_report()
        with open(report_filename, 'w', encoding='utf-8') as f:
            f.write(report)
        print("✅ Report generated successfully!")
        print(f"📊 Report contains {len(report.split('\\n'))} lines")
    except Exception as e:
        print(f"❌ Error generating report: {e}")
    
    # Test loading data
    print(f"\n📂 Testing data loading...")
    try:
        test_manager = GradeManager()
        test_manager.load_from_file(filename)
        print(f"✅ Successfully loaded {len(test_manager)} students!")
    except Exception as e:
        print(f"❌ Error loading data: {e}")


def demonstrate_visualizations(manager: GradeManager):
    """Demonstrate data visualization features."""
    print("\n" + "="*60)
    print("📊 DEMONSTRATING DATA VISUALIZATIONS")
    print("="*60)
    
    print("\n🎨 Creating visualizations...")
    try:
        manager.create_visualizations()
        print("✅ Visualizations created successfully!")
        print("📊 Generated files:")
        
        visualization_files = [
            "grade_distribution.png",
            "student_averages.png", 
            "subject_performance.png"
        ]
        
        for filename in visualization_files:
            if os.path.exists(filename):
                file_size = os.path.getsize(filename)
                print(f"  📈 {filename} ({file_size} bytes)")
            else:
                print(f"  ❌ {filename} (not created)")
                
    except ImportError:
        print("⚠️  Matplotlib not installed - visualizations skipped")
        print("💡 Install with: pip install matplotlib")
    except Exception as e:
        print(f"❌ Error creating visualizations: {e}")


def demonstrate_advanced_features(manager: GradeManager):
    """Demonstrate advanced features and edge cases."""
    print("\n" + "="*60)
    print("🚀 DEMONSTRATING ADVANCED FEATURES")
    print("="*60)
    
    # Add a new student programmatically
    print("\n➕ Adding a new student programmatically...")
    new_student = Student("Isabella Garcia", "STU009", "isabella.garcia@school.edu")
    new_student.add_grade("Mathematics", 84.0)
    new_student.add_grade("Science", 89.5)
    new_student.add_grade("English", 91.0)
    
    if manager.add_student(new_student):
        print(f"✅ Added {new_student.name} successfully!")
    else:
        print("❌ Failed to add student (ID might already exist)")
    
    # Demonstrate error handling
    print("\n🛡️  Testing error handling...")
    
    # Try to add duplicate student
    duplicate = Student("Test Student", "STU001", "test@test.com")  # STU001 already exists
    if not manager.add_student(duplicate):
        print("✅ Correctly prevented duplicate student ID")
    
    # Try invalid grade
    try:
        new_student.add_grade("Invalid Subject", 150.0)  # Grade > 100
        print("❌ Should have caught invalid grade")
    except ValueError:
        print("✅ Correctly caught invalid grade (>100)")
    
    # Test empty data scenarios
    empty_manager = GradeManager()
    empty_stats = empty_manager.get_class_statistics()
    if not empty_stats:
        print("✅ Correctly handled empty class statistics")
    
    print("\n🎯 Advanced operations completed!")


def show_summary():
    """Show a summary of what was demonstrated."""
    print("\n" + "="*60)
    print("🎉 DEMONSTRATION COMPLETE!")
    print("="*60)
    
    print("\n✨ What was demonstrated:")
    print("  🎓 Student creation and management")
    print("  📊 Grade tracking and calculations")
    print("  📈 Statistical analysis and reporting")
    print("  💾 File I/O and data persistence")
    print("  📊 Data visualization (if matplotlib available)")
    print("  🛡️  Error handling and validation")
    print("  🚀 Advanced features and edge cases")
    
    print("\n📁 Files created during demo:")
    demo_files = [
        "demo_student_data.json",
        "demo_grade_report.txt",
        "grade_distribution.png",
        "student_averages.png",
        "subject_performance.png"
    ]
    
    for filename in demo_files:
        if os.path.exists(filename):
            file_size = os.path.getsize(filename)
            print(f"  ✅ {filename} ({file_size} bytes)")
    
    print("\n🚀 Next steps:")
    print("  1. Run 'python main.py' to use the interactive application")
    print("  2. Examine the generated files to see the output")
    print("  3. Modify the code to add new features")
    print("  4. Use this as a foundation for your own projects")
    
    print("\n💡 Teaching tip:")
    print("  This demo shows students how all the pieces work together!")


def main():
    """Run the complete demonstration."""
    print("🎓 STUDENT GRADE MANAGER - COMPREHENSIVE DEMONSTRATION")
    print("=" * 60)
    print("This script demonstrates all features of the Student Grade Manager.")
    print("Perfect for classroom presentations and testing!")
    print()
    
    try:
        # Create sample data
        manager = create_sample_data()
        
        # Run demonstrations
        demonstrate_basic_operations(manager)
        demonstrate_statistics(manager)
        demonstrate_file_operations(manager)
        demonstrate_visualizations(manager)
        demonstrate_advanced_features(manager)
        
        # Show summary
        show_summary()
        
    except KeyboardInterrupt:
        print("\n\n👋 Demonstration interrupted by user.")
    except Exception as e:
        print(f"\n❌ An error occurred during demonstration: {e}")
        print("This might be a good teaching moment about debugging!")
    
    print("\n🎉 Thank you for watching the demonstration!")


if __name__ == "__main__":
    main()