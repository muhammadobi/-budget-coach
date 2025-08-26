"""
Student Class Module
===================

This module defines the Student class which represents a student in the grade management system.

Key Concepts Demonstrated:
- Class definition and constructor (__init__)
- Instance attributes and methods
- Data encapsulation
- String representation (__str__ and __repr__)
- Property methods and data validation
- Dictionary manipulation
- Date/time handling
"""

from datetime import datetime
from typing import Dict, Optional


class Student:
    """
    Represents a student with personal information and academic grades.
    
    This class demonstrates object-oriented programming concepts including:
    - Encapsulation of data and methods
    - Instance variables and methods
    - Data validation
    - String formatting
    """
    
    def __init__(self, name: str, student_id: str, email: str):
        """
        Initialize a new Student object.
        
        Args:
            name (str): The student's full name
            student_id (str): Unique identifier for the student
            email (str): Student's email address
        
        Raises:
            ValueError: If any required field is empty
        """
        # Input validation
        if not name or not name.strip():
            raise ValueError("Student name cannot be empty")
        if not student_id or not student_id.strip():
            raise ValueError("Student ID cannot be empty")
        if not email or not email.strip():
            raise ValueError("Email cannot be empty")
        
        # Instance attributes
        self.name = name.strip()
        self.student_id = student_id.strip()
        self.email = email.strip().lower()
        self.enrollment_date = datetime.now().strftime("%Y-%m-%d")
        self.grades: Dict[str, float] = {}  # Subject -> Grade mapping
    
    def add_grade(self, subject: str, grade: float) -> None:
        """
        Add a grade for a specific subject.
        
        Args:
            subject (str): The subject name
            grade (float): The grade value (0-100)
        
        Raises:
            ValueError: If grade is not between 0 and 100
        """
        if not 0 <= grade <= 100:
            raise ValueError("Grade must be between 0 and 100")
        
        if not subject or not subject.strip():
            raise ValueError("Subject name cannot be empty")
        
        # Store the grade (overwrites if subject already exists)
        self.grades[subject.strip().title()] = round(grade, 2)
    
    def remove_grade(self, subject: str) -> bool:
        """
        Remove a grade for a specific subject.
        
        Args:
            subject (str): The subject name to remove
        
        Returns:
            bool: True if grade was removed, False if subject not found
        """
        subject_key = subject.strip().title()
        if subject_key in self.grades:
            del self.grades[subject_key]
            return True
        return False
    
    def get_grade(self, subject: str) -> Optional[float]:
        """
        Get the grade for a specific subject.
        
        Args:
            subject (str): The subject name
        
        Returns:
            Optional[float]: The grade if found, None otherwise
        """
        return self.grades.get(subject.strip().title())
    
    def get_average_grade(self) -> float:
        """
        Calculate the average grade across all subjects.
        
        Returns:
            float: Average grade, or 0.0 if no grades exist
        """
        if not self.grades:
            return 0.0
        
        return round(sum(self.grades.values()) / len(self.grades), 2)
    
    def get_letter_grade(self) -> str:
        """
        Convert the average grade to a letter grade.
        
        Returns:
            str: Letter grade (A, B, C, D, F)
        """
        average = self.get_average_grade()
        
        if average >= 90:
            return "A"
        elif average >= 80:
            return "B"
        elif average >= 70:
            return "C"
        elif average >= 60:
            return "D"
        else:
            return "F"
    
    def get_gpa(self) -> float:
        """
        Calculate GPA based on average grade.
        
        Returns:
            float: GPA on a 4.0 scale
        """
        average = self.get_average_grade()
        
        if average >= 90:
            return 4.0
        elif average >= 80:
            return 3.0
        elif average >= 70:
            return 2.0
        elif average >= 60:
            return 1.0
        else:
            return 0.0
    
    def has_passing_grade(self, passing_threshold: float = 60.0) -> bool:
        """
        Check if student has a passing average grade.
        
        Args:
            passing_threshold (float): Minimum grade to pass (default: 60.0)
        
        Returns:
            bool: True if student is passing, False otherwise
        """
        return self.get_average_grade() >= passing_threshold
    
    def get_subjects(self) -> list:
        """
        Get a list of all subjects the student has grades for.
        
        Returns:
            list: List of subject names
        """
        return list(self.grades.keys())
    
    def get_grade_count(self) -> int:
        """
        Get the total number of grades recorded.
        
        Returns:
            int: Number of grades
        """
        return len(self.grades)
    
    def get_highest_grade(self) -> tuple:
        """
        Get the highest grade and its subject.
        
        Returns:
            tuple: (subject, grade) or (None, 0.0) if no grades
        """
        if not self.grades:
            return None, 0.0
        
        subject = max(self.grades, key=self.grades.get)
        return subject, self.grades[subject]
    
    def get_lowest_grade(self) -> tuple:
        """
        Get the lowest grade and its subject.
        
        Returns:
            tuple: (subject, grade) or (None, 0.0) if no grades
        """
        if not self.grades:
            return None, 0.0
        
        subject = min(self.grades, key=self.grades.get)
        return subject, self.grades[subject]
    
    def to_dict(self) -> dict:
        """
        Convert student object to dictionary for serialization.
        
        Returns:
            dict: Student data as dictionary
        """
        return {
            'name': self.name,
            'student_id': self.student_id,
            'email': self.email,
            'enrollment_date': self.enrollment_date,
            'grades': self.grades
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> 'Student':
        """
        Create a Student object from a dictionary.
        
        Args:
            data (dict): Dictionary containing student data
        
        Returns:
            Student: New Student object
        """
        student = cls(data['name'], data['student_id'], data['email'])
        student.enrollment_date = data.get('enrollment_date', student.enrollment_date)
        student.grades = data.get('grades', {})
        return student
    
    def __str__(self) -> str:
        """
        String representation for user-friendly display.
        
        Returns:
            str: Formatted student information
        """
        avg_grade = self.get_average_grade()
        grade_count = len(self.grades)
        
        return (f"Student: {self.name} (ID: {self.student_id})\n"
                f"Email: {self.email}\n"
                f"Enrolled: {self.enrollment_date}\n"
                f"Grades: {grade_count} subjects, Average: {avg_grade:.1f}% ({self.get_letter_grade()})")
    
    def __repr__(self) -> str:
        """
        Technical representation for debugging.
        
        Returns:
            str: Technical representation
        """
        return f"Student(name='{self.name}', student_id='{self.student_id}', email='{self.email}')"
    
    def __eq__(self, other) -> bool:
        """
        Check equality based on student ID.
        
        Args:
            other: Another Student object
        
        Returns:
            bool: True if student IDs match
        """
        if not isinstance(other, Student):
            return False
        return self.student_id == other.student_id
    
    def __hash__(self) -> int:
        """
        Hash function based on student ID.
        
        Returns:
            int: Hash value
        """
        return hash(self.student_id)