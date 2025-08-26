#!/usr/bin/env python3
"""
Basic Tests for Student Grade Manager
=====================================

This module contains basic tests to verify the core functionality
of the Student Grade Manager application.

Perfect for demonstrating:
- Unit testing concepts
- Test-driven development
- Quality assurance
- Debugging techniques

Students can run these tests to verify their code works correctly.
"""

import os
import json
import tempfile
from student import Student
from grade_manager import GradeManager


def test_student_creation():
    """Test basic student creation and properties."""
    print("🧪 Testing student creation...")
    
    # Test valid student creation
    student = Student("John Doe", "STU001", "john@example.com")
    
    assert student.name == "John Doe"
    assert student.student_id == "STU001"
    assert student.email == "john@example.com"
    assert len(student.grades) == 0
    
    print("  ✅ Basic student creation works")
    
    # Test input validation
    try:
        Student("", "STU001", "john@example.com")
        assert False, "Should have raised ValueError for empty name"
    except ValueError:
        print("  ✅ Empty name validation works")
    
    try:
        Student("John Doe", "", "john@example.com")
        assert False, "Should have raised ValueError for empty ID"
    except ValueError:
        print("  ✅ Empty ID validation works")


def test_grade_operations():
    """Test grade addition and calculations."""
    print("\n🧪 Testing grade operations...")
    
    student = Student("Jane Smith", "STU002", "jane@example.com")
    
    # Test adding grades
    student.add_grade("Math", 85.0)
    student.add_grade("Science", 92.0)
    student.add_grade("English", 78.0)
    
    assert len(student.grades) == 3
    assert student.get_grade("Math") == 85.0
    assert student.get_grade("Science") == 92.0
    
    print("  ✅ Grade addition works")
    
    # Test average calculation
    expected_average = (85.0 + 92.0 + 78.0) / 3
    assert abs(student.get_average_grade() - expected_average) < 0.01
    
    print("  ✅ Average calculation works")
    
    # Test letter grade
    assert student.get_letter_grade() == "B"  # Average is ~85
    
    print("  ✅ Letter grade calculation works")
    
    # Test invalid grade
    try:
        student.add_grade("Invalid", 150.0)
        assert False, "Should have raised ValueError for grade > 100"
    except ValueError:
        print("  ✅ Grade validation works")


def test_grade_manager():
    """Test the GradeManager class functionality."""
    print("\n🧪 Testing grade manager...")
    
    manager = GradeManager()
    
    # Test adding students
    student1 = Student("Alice Johnson", "STU001", "alice@example.com")
    student1.add_grade("Math", 95.0)
    student1.add_grade("Science", 88.0)
    
    student2 = Student("Bob Wilson", "STU002", "bob@example.com")
    student2.add_grade("Math", 75.0)
    student2.add_grade("Science", 82.0)
    
    assert manager.add_student(student1) == True
    assert manager.add_student(student2) == True
    
    print("  ✅ Student addition works")
    
    # Test duplicate prevention
    duplicate = Student("Charlie Brown", "STU001", "charlie@example.com")
    assert manager.add_student(duplicate) == False
    
    print("  ✅ Duplicate prevention works")
    
    # Test finding students
    found = manager.find_student("STU001")
    assert found is not None
    assert found.name == "Alice Johnson"
    
    not_found = manager.find_student("STU999")
    assert not_found is None
    
    print("  ✅ Student search works")
    
    # Test statistics
    stats = manager.get_class_statistics()
    assert stats['total_students'] == 2
    assert stats['students_with_grades'] == 2
    
    print("  ✅ Statistics calculation works")


def test_file_operations():
    """Test file save and load operations."""
    print("\n🧪 Testing file operations...")
    
    # Create test data
    manager = GradeManager()
    student = Student("Test Student", "TEST001", "test@example.com")
    student.add_grade("Math", 90.0)
    student.add_grade("Science", 85.0)
    manager.add_student(student)
    
    # Test saving
    with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
        temp_filename = f.name
    
    try:
        manager.save_to_file(temp_filename)
        assert os.path.exists(temp_filename)
        
        print("  ✅ File saving works")
        
        # Test loading
        new_manager = GradeManager()
        new_manager.load_from_file(temp_filename)
        
        assert len(new_manager) == 1
        loaded_student = new_manager.find_student("TEST001")
        assert loaded_student is not None
        assert loaded_student.name == "Test Student"
        assert loaded_student.get_grade("Math") == 90.0
        
        print("  ✅ File loading works")
        
    finally:
        # Clean up
        if os.path.exists(temp_filename):
            os.unlink(temp_filename)


def test_edge_cases():
    """Test edge cases and error conditions."""
    print("\n🧪 Testing edge cases...")
    
    # Test empty manager statistics
    empty_manager = GradeManager()
    stats = empty_manager.get_class_statistics()
    assert stats == {}
    
    print("  ✅ Empty manager handling works")
    
    # Test student with no grades
    student = Student("No Grades", "STU999", "no@grades.com")
    assert student.get_average_grade() == 0.0
    assert student.get_letter_grade() == "F"
    
    print("  ✅ No grades handling works")
    
    # Test grade removal
    student.add_grade("Math", 85.0)
    student.add_grade("Science", 90.0)
    
    assert student.remove_grade("Math") == True
    assert student.get_grade("Math") is None
    assert student.remove_grade("NonExistent") == False
    
    print("  ✅ Grade removal works")


def test_string_representations():
    """Test string representations and formatting."""
    print("\n🧪 Testing string representations...")
    
    student = Student("Test Student", "TEST001", "test@example.com")
    student.add_grade("Math", 85.0)
    
    # Test __str__ method
    str_repr = str(student)
    assert "Test Student" in str_repr
    assert "TEST001" in str_repr
    assert "85.0%" in str_repr
    
    print("  ✅ String representation works")
    
    # Test __repr__ method
    repr_str = repr(student)
    assert "Student(" in repr_str
    assert "Test Student" in repr_str
    
    print("  ✅ Repr representation works")


def run_all_tests():
    """Run all tests and report results."""
    print("🧪 RUNNING BASIC TESTS FOR STUDENT GRADE MANAGER")
    print("=" * 60)
    
    tests = [
        test_student_creation,
        test_grade_operations,
        test_grade_manager,
        test_file_operations,
        test_edge_cases,
        test_string_representations
    ]
    
    passed = 0
    failed = 0
    
    for test in tests:
        try:
            test()
            passed += 1
        except AssertionError as e:
            print(f"  ❌ Test failed: {e}")
            failed += 1
        except Exception as e:
            print(f"  ❌ Test error: {e}")
            failed += 1
    
    print("\n" + "=" * 60)
    print("🎯 TEST RESULTS")
    print("=" * 60)
    print(f"✅ Passed: {passed}")
    print(f"❌ Failed: {failed}")
    print(f"📊 Total:  {passed + failed}")
    
    if failed == 0:
        print("\n🎉 All tests passed! The code is working correctly.")
    else:
        print(f"\n⚠️  {failed} test(s) failed. Check the code for issues.")
    
    print("\n💡 Teaching note:")
    print("These tests demonstrate how to verify code correctness!")
    print("Students can add more tests to cover additional scenarios.")


if __name__ == "__main__":
    run_all_tests()