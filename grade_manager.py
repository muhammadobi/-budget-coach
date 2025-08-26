"""
Grade Manager Class Module
==========================

This module defines the GradeManager class which handles collections of students
and provides various operations for managing and analyzing student data.

Key Concepts Demonstrated:
- Class composition (using Student objects)
- List and dictionary operations
- File I/O with JSON
- Data analysis and statistics
- Exception handling
- Data visualization (optional)
"""

import json
import os
from datetime import datetime
from typing import List, Dict, Optional, Any
from student import Student


class GradeManager:
    """
    Manages a collection of students and provides operations for
    grade management, statistics, and data persistence.
    
    This class demonstrates:
    - Managing collections of objects
    - Data persistence with JSON
    - Statistical calculations
    - Report generation
    """
    
    def __init__(self):
        """Initialize an empty grade manager."""
        self.students: List[Student] = []
    
    def add_student(self, student: Student) -> bool:
        """
        Add a student to the manager.
        
        Args:
            student (Student): The student to add
        
        Returns:
            bool: True if added successfully, False if student ID already exists
        """
        # Check if student ID already exists
        if self.find_student(student.student_id):
            return False
        
        self.students.append(student)
        return True
    
    def remove_student(self, student_id: str) -> bool:
        """
        Remove a student by ID.
        
        Args:
            student_id (str): The student ID to remove
        
        Returns:
            bool: True if removed, False if not found
        """
        student = self.find_student(student_id)
        if student:
            self.students.remove(student)
            return True
        return False
    
    def find_student(self, student_id: str) -> Optional[Student]:
        """
        Find a student by ID.
        
        Args:
            student_id (str): The student ID to search for
        
        Returns:
            Optional[Student]: The student if found, None otherwise
        """
        for student in self.students:
            if student.student_id == student_id:
                return student
        return None
    
    def get_all_students(self) -> List[Student]:
        """
        Get all students.
        
        Returns:
            List[Student]: List of all students
        """
        return self.students.copy()
    
    def get_students_by_letter_grade(self, letter_grade: str) -> List[Student]:
        """
        Get all students with a specific letter grade.
        
        Args:
            letter_grade (str): The letter grade to filter by (A, B, C, D, F)
        
        Returns:
            List[Student]: Students with the specified letter grade
        """
        return [student for student in self.students 
                if student.get_letter_grade() == letter_grade.upper()]
    
    def get_passing_students(self, passing_threshold: float = 60.0) -> List[Student]:
        """
        Get all students with passing grades.
        
        Args:
            passing_threshold (float): Minimum grade to pass (default: 60.0)
        
        Returns:
            List[Student]: Students with passing grades
        """
        return [student for student in self.students 
                if student.has_passing_grade(passing_threshold)]
    
    def get_failing_students(self, passing_threshold: float = 60.0) -> List[Student]:
        """
        Get all students with failing grades.
        
        Args:
            passing_threshold (float): Minimum grade to pass (default: 60.0)
        
        Returns:
            List[Student]: Students with failing grades
        """
        return [student for student in self.students 
                if not student.has_passing_grade(passing_threshold)]
    
    def get_top_students(self, count: int = 5) -> List[Student]:
        """
        Get the top performing students.
        
        Args:
            count (int): Number of top students to return
        
        Returns:
            List[Student]: Top students sorted by average grade
        """
        # Filter students with grades and sort by average
        students_with_grades = [s for s in self.students if s.get_grade_count() > 0]
        students_with_grades.sort(key=lambda s: s.get_average_grade(), reverse=True)
        
        return students_with_grades[:count]
    
    def get_class_statistics(self) -> Dict[str, Any]:
        """
        Calculate comprehensive class statistics.
        
        Returns:
            Dict[str, Any]: Dictionary containing various statistics
        """
        if not self.students:
            return {}
        
        students_with_grades = [s for s in self.students if s.get_grade_count() > 0]
        
        if not students_with_grades:
            return {
                'total_students': len(self.students),
                'students_with_grades': 0
            }
        
        # Calculate basic statistics
        all_averages = [s.get_average_grade() for s in students_with_grades]
        class_average = sum(all_averages) / len(all_averages)
        
        # Grade distribution
        grade_distribution = {'A': 0, 'B': 0, 'C': 0, 'D': 0, 'F': 0}
        for student in students_with_grades:
            letter_grade = student.get_letter_grade()
            grade_distribution[letter_grade] += 1
        
        # Subject statistics
        all_subjects = set()
        subject_grades = {}
        
        for student in students_with_grades:
            for subject in student.get_subjects():
                all_subjects.add(subject)
                if subject not in subject_grades:
                    subject_grades[subject] = []
                subject_grades[subject].append(student.get_grade(subject))
        
        subject_averages = {}
        for subject, grades in subject_grades.items():
            subject_averages[subject] = sum(grades) / len(grades)
        
        return {
            'total_students': len(self.students),
            'students_with_grades': len(students_with_grades),
            'class_average': round(class_average, 2),
            'highest_grade': round(max(all_averages), 2),
            'lowest_grade': round(min(all_averages), 2),
            'grade_distribution': grade_distribution,
            'total_subjects': len(all_subjects),
            'subject_averages': {k: round(v, 2) for k, v in subject_averages.items()},
            'passing_rate': round((len(self.get_passing_students()) / len(students_with_grades)) * 100, 1)
        }
    
    def generate_report(self) -> str:
        """
        Generate a comprehensive text report.
        
        Returns:
            str: Formatted report string
        """
        report = []
        report.append("=" * 60)
        report.append("STUDENT GRADE MANAGEMENT SYSTEM - COMPREHENSIVE REPORT")
        report.append("=" * 60)
        report.append(f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        report.append("")
        
        # Class overview
        stats = self.get_class_statistics()
        if stats:
            report.append("CLASS OVERVIEW")
            report.append("-" * 20)
            report.append(f"Total Students: {stats['total_students']}")
            report.append(f"Students with Grades: {stats['students_with_grades']}")
            
            if stats['students_with_grades'] > 0:
                report.append(f"Class Average: {stats['class_average']}%")
                report.append(f"Highest Grade: {stats['highest_grade']}%")
                report.append(f"Lowest Grade: {stats['lowest_grade']}%")
                report.append(f"Passing Rate: {stats['passing_rate']}%")
                report.append("")
                
                # Grade distribution
                report.append("GRADE DISTRIBUTION")
                report.append("-" * 20)
                for grade, count in stats['grade_distribution'].items():
                    percentage = (count / stats['students_with_grades']) * 100
                    report.append(f"{grade}: {count} students ({percentage:.1f}%)")
                report.append("")
                
                # Subject performance
                if stats['subject_averages']:
                    report.append("SUBJECT PERFORMANCE")
                    report.append("-" * 20)
                    for subject, avg in sorted(stats['subject_averages'].items()):
                        report.append(f"{subject}: {avg}%")
                    report.append("")
                
                # Top performers
                top_students = self.get_top_students(5)
                if top_students:
                    report.append("TOP PERFORMERS")
                    report.append("-" * 20)
                    for i, student in enumerate(top_students, 1):
                        avg = student.get_average_grade()
                        report.append(f"{i}. {student.name}: {avg}% ({student.get_letter_grade()})")
                    report.append("")
        
        # Individual student details
        if self.students:
            report.append("INDIVIDUAL STUDENT DETAILS")
            report.append("-" * 30)
            
            for student in sorted(self.students, key=lambda s: s.name):
                report.append(f"\nStudent: {student.name}")
                report.append(f"ID: {student.student_id}")
                report.append(f"Email: {student.email}")
                report.append(f"Enrolled: {student.enrollment_date}")
                
                if student.get_grade_count() > 0:
                    report.append(f"Average Grade: {student.get_average_grade()}% ({student.get_letter_grade()})")
                    report.append("Grades by Subject:")
                    for subject in sorted(student.get_subjects()):
                        grade = student.get_grade(subject)
                        report.append(f"  {subject}: {grade}%")
                else:
                    report.append("No grades recorded")
                
                report.append("-" * 30)
        
        return "\n".join(report)
    
    def save_to_file(self, filename: str) -> None:
        """
        Save all student data to a JSON file.
        
        Args:
            filename (str): The filename to save to
        
        Raises:
            IOError: If file cannot be written
        """
        data = {
            'students': [student.to_dict() for student in self.students],
            'saved_date': datetime.now().isoformat(),
            'total_students': len(self.students)
        }
        
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
        except IOError as e:
            raise IOError(f"Could not save data to {filename}: {e}")
    
    def load_from_file(self, filename: str) -> None:
        """
        Load student data from a JSON file.
        
        Args:
            filename (str): The filename to load from
        
        Raises:
            IOError: If file cannot be read
            ValueError: If file format is invalid
        """
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                data = json.load(f)
        except IOError as e:
            raise IOError(f"Could not load data from {filename}: {e}")
        except json.JSONDecodeError as e:
            raise ValueError(f"Invalid JSON format in {filename}: {e}")
        
        if 'students' not in data:
            raise ValueError("Invalid file format: missing 'students' key")
        
        # Clear existing students and load new ones
        self.students.clear()
        
        for student_data in data['students']:
            try:
                student = Student.from_dict(student_data)
                self.students.append(student)
            except Exception as e:
                print(f"Warning: Could not load student {student_data.get('name', 'Unknown')}: {e}")
    
    def create_visualizations(self) -> None:
        """
        Create various data visualizations using matplotlib.
        
        Raises:
            ImportError: If matplotlib is not installed
        """
        try:
            import matplotlib.pyplot as plt
            import numpy as np
        except ImportError:
            raise ImportError("Matplotlib is required for visualizations. Install with: pip install matplotlib")
        
        students_with_grades = [s for s in self.students if s.get_grade_count() > 0]
        
        if not students_with_grades:
            print("No student data available for visualization.")
            return
        
        # Set up the plot style
        plt.style.use('default')
        
        # 1. Grade Distribution Pie Chart
        plt.figure(figsize=(10, 8))
        
        grade_counts = {'A': 0, 'B': 0, 'C': 0, 'D': 0, 'F': 0}
        for student in students_with_grades:
            letter_grade = student.get_letter_grade()
            grade_counts[letter_grade] += 1
        
        # Filter out grades with 0 count
        labels = [grade for grade, count in grade_counts.items() if count > 0]
        sizes = [count for count in grade_counts.values() if count > 0]
        colors = ['#2ecc71', '#3498db', '#f39c12', '#e67e22', '#e74c3c'][:len(labels)]
        
        plt.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%', startangle=90)
        plt.title('Grade Distribution', fontsize=16, fontweight='bold')
        plt.axis('equal')
        plt.tight_layout()
        plt.savefig('grade_distribution.png', dpi=300, bbox_inches='tight')
        plt.close()
        
        # 2. Student Averages Bar Chart
        plt.figure(figsize=(12, 6))
        
        names = [s.name[:15] + '...' if len(s.name) > 15 else s.name for s in students_with_grades]
        averages = [s.get_average_grade() for s in students_with_grades]
        
        bars = plt.bar(range(len(names)), averages, color='#3498db', alpha=0.7)
        
        # Color bars based on grade
        for i, (bar, avg) in enumerate(zip(bars, averages)):
            if avg >= 90:
                bar.set_color('#2ecc71')  # Green for A
            elif avg >= 80:
                bar.set_color('#3498db')  # Blue for B
            elif avg >= 70:
                bar.set_color('#f39c12')  # Orange for C
            elif avg >= 60:
                bar.set_color('#e67e22')  # Dark orange for D
            else:
                bar.set_color('#e74c3c')  # Red for F
        
        plt.xlabel('Students', fontsize=12)
        plt.ylabel('Average Grade (%)', fontsize=12)
        plt.title('Student Average Grades', fontsize=16, fontweight='bold')
        plt.xticks(range(len(names)), names, rotation=45, ha='right')
        plt.ylim(0, 100)
        
        # Add value labels on bars
        for i, avg in enumerate(averages):
            plt.text(i, avg + 1, f'{avg:.1f}%', ha='center', va='bottom', fontsize=9)
        
        plt.tight_layout()
        plt.savefig('student_averages.png', dpi=300, bbox_inches='tight')
        plt.close()
        
        # 3. Subject Performance (if multiple subjects exist)
        all_subjects = set()
        for student in students_with_grades:
            all_subjects.update(student.get_subjects())
        
        if len(all_subjects) > 1:
            plt.figure(figsize=(10, 6))
            
            subject_data = {}
            for subject in all_subjects:
                grades = []
                for student in students_with_grades:
                    grade = student.get_grade(subject)
                    if grade is not None:
                        grades.append(grade)
                if grades:
                    subject_data[subject] = grades
            
            if subject_data:
                subjects = list(subject_data.keys())
                averages = [sum(grades) / len(grades) for grades in subject_data.values()]
                
                bars = plt.bar(subjects, averages, color='#9b59b6', alpha=0.7)
                
                plt.xlabel('Subjects', fontsize=12)
                plt.ylabel('Average Grade (%)', fontsize=12)
                plt.title('Subject Performance Overview', fontsize=16, fontweight='bold')
                plt.xticks(rotation=45, ha='right')
                plt.ylim(0, 100)
                
                # Add value labels on bars
                for i, avg in enumerate(averages):
                    plt.text(i, avg + 1, f'{avg:.1f}%', ha='center', va='bottom', fontsize=10)
                
                plt.tight_layout()
                plt.savefig('subject_performance.png', dpi=300, bbox_inches='tight')
                plt.close()
    
    def export_to_csv(self, filename: str) -> None:
        """
        Export student data to CSV format.
        
        Args:
            filename (str): The CSV filename to save to
        """
        import csv
        
        with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
            fieldnames = ['Name', 'Student_ID', 'Email', 'Enrollment_Date', 'Average_Grade', 'Letter_Grade', 'Subjects', 'Grade_Count']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            
            writer.writeheader()
            for student in self.students:
                writer.writerow({
                    'Name': student.name,
                    'Student_ID': student.student_id,
                    'Email': student.email,
                    'Enrollment_Date': student.enrollment_date,
                    'Average_Grade': student.get_average_grade(),
                    'Letter_Grade': student.get_letter_grade(),
                    'Subjects': ', '.join(student.get_subjects()),
                    'Grade_Count': student.get_grade_count()
                })
    
    def __len__(self) -> int:
        """Return the number of students."""
        return len(self.students)
    
    def __str__(self) -> str:
        """String representation of the grade manager."""
        return f"GradeManager with {len(self.students)} students"