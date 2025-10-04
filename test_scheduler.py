"""
Test script for the revision scheduler - tests core functionality
without requiring pandas/openpyxl dependencies
"""

import sys
import os
sys.path.append(os.path.dirname(__file__))

# Import just the scheduler class (without pandas dependency)
import datetime
import json
from pathlib import Path

class SimpleRevisionScheduler:
    """Simplified version for testing without pandas dependency"""
    
    def __init__(self, data_file: str = "test_revision_data.json"):
        self.data_file = Path(data_file)
        self.topics = []
        self.revision_intervals = [1, 7, 15, 30, 90, 180]
        self.load_data()
    
    def add_topic(self, topic_name: str, learned_date: str = None) -> bool:
        if learned_date is None:
            learned_date = datetime.date.today().strftime("%Y-%m-%d")
        
        # Check if topic already exists
        for topic in self.topics:
            if topic['name'].lower() == topic_name.lower():
                return False
        
        # Create new topic entry
        topic_entry = {
            'name': topic_name,
            'learned_date': learned_date,
            'revision_count': 0,
            'last_revised': None,
            'next_revision': None
        }
        
        # Calculate first revision date
        learned = datetime.datetime.strptime(learned_date, "%Y-%m-%d").date()
        first_revision = learned + datetime.timedelta(days=1)
        topic_entry['next_revision'] = first_revision.strftime("%Y-%m-%d")
        
        self.topics.append(topic_entry)
        self.save_data()
        return True
    
    def mark_revised(self, topic_name: str, revision_date: str = None) -> bool:
        if revision_date is None:
            revision_date = datetime.date.today().strftime("%Y-%m-%d")
        
        for topic in self.topics:
            if topic['name'].lower() == topic_name.lower():
                topic['revision_count'] += 1
                topic['last_revised'] = revision_date
                
                # Calculate next revision date
                if topic['revision_count'] < len(self.revision_intervals):
                    days_to_add = self.revision_intervals[topic['revision_count']]
                    revised = datetime.datetime.strptime(revision_date, "%Y-%m-%d").date()
                    next_revision = revised + datetime.timedelta(days=days_to_add)
                    topic['next_revision'] = next_revision.strftime("%Y-%m-%d")
                else:
                    revised = datetime.datetime.strptime(revision_date, "%Y-%m-%d").date()
                    next_revision = revised + datetime.timedelta(days=180)
                    topic['next_revision'] = next_revision.strftime("%Y-%m-%d")
                
                self.save_data()
                return True
        return False
    
    def get_due_topics(self, date: str = None):
        if date is None:
            check_date = datetime.date.today()
        else:
            check_date = datetime.datetime.strptime(date, "%Y-%m-%d").date()
        
        due_topics = []
        for topic in self.topics:
            if topic['next_revision']:
                next_rev_date = datetime.datetime.strptime(topic['next_revision'], "%Y-%m-%d").date()
                if next_rev_date <= check_date:
                    due_topics.append(topic)
        
        due_topics.sort(key=lambda x: x['next_revision'])
        return due_topics
    
    def save_data(self):
        with open(self.data_file, 'w') as f:
            json.dump(self.topics, f, indent=2)
    
    def load_data(self):
        if self.data_file.exists():
            try:
                with open(self.data_file, 'r') as f:
                    self.topics = json.load(f)
            except (json.JSONDecodeError, FileNotFoundError):
                self.topics = []
        else:
            self.topics = []

def test_revision_scheduler():
    """Test the core functionality"""
    print("🧪 Testing Revision Schedule Manager...")
    
    # Create test scheduler
    scheduler = SimpleRevisionScheduler("test_data.json")
    
    # Test 1: Add a topic
    print("\n✅ Test 1: Adding topics")
    success1 = scheduler.add_topic("Python Basics", "2025-10-01")
    success2 = scheduler.add_topic("Data Structures", "2025-10-02")
    success3 = scheduler.add_topic("Python Basics", "2025-10-01")  # Duplicate
    
    print(f"   - Add 'Python Basics': {'✓' if success1 else '✗'}")
    print(f"   - Add 'Data Structures': {'✓' if success2 else '✗'}")
    print(f"   - Add duplicate 'Python Basics': {'✗ (Expected)' if not success3 else '✓ (Unexpected)'}")
    
    # Test 2: Check revision schedules
    print("\n✅ Test 2: Revision schedule generation")
    python_topic = next((t for t in scheduler.topics if t['name'] == 'Python Basics'), None)
    if python_topic:
        expected_first_revision = "2025-10-02"  # 1 day after learning
        actual_first_revision = python_topic['next_revision']
        print(f"   - First revision for 'Python Basics':")
        print(f"     Expected: {expected_first_revision}")
        print(f"     Actual: {actual_first_revision}")
        print(f"     Status: {'✓' if expected_first_revision == actual_first_revision else '✗'}")
    
    # Test 3: Mark as revised
    print("\n✅ Test 3: Marking topics as revised")
    success = scheduler.mark_revised("Python Basics", "2025-10-02")
    print(f"   - Mark 'Python Basics' as revised: {'✓' if success else '✗'}")
    
    # Check second revision date (should be 7 days later)
    python_topic = next((t for t in scheduler.topics if t['name'] == 'Python Basics'), None)
    if python_topic:
        expected_second_revision = "2025-10-09"  # 7 days after first revision
        actual_second_revision = python_topic['next_revision']
        print(f"   - Second revision date:")
        print(f"     Expected: {expected_second_revision}")
        print(f"     Actual: {actual_second_revision}")
        print(f"     Status: {'✓' if expected_second_revision == actual_second_revision else '✗'}")
    
    # Test 4: Due topics
    print("\n✅ Test 4: Getting due topics")
    due_topics = scheduler.get_due_topics("2025-10-02")
    print(f"   - Topics due on 2025-10-02: {len(due_topics)}")
    for topic in due_topics:
        print(f"     - {topic['name']} (due: {topic['next_revision']})")
    
    # Test 5: Complete revision cycle
    print("\n✅ Test 5: Complete revision cycle for 'Data Structures'")
    test_dates = ["2025-10-03", "2025-10-10", "2025-10-25", "2025-11-24", "2026-02-22", "2026-08-21"]
    expected_next_dates = ["2025-10-10", "2025-10-25", "2025-11-24", "2026-02-22", "2026-08-21", "2027-02-17"]
    
    for i, (revision_date, expected_next) in enumerate(zip(test_dates, expected_next_dates)):
        scheduler.mark_revised("Data Structures", revision_date)
        ds_topic = next((t for t in scheduler.topics if t['name'] == 'Data Structures'), None)
        actual_next = ds_topic['next_revision'] if ds_topic else None
        
        interval_name = ["1 day", "7 days", "15 days", "1 month", "3 months", "6 months"][i]
        print(f"   - Revision {i+1} ({interval_name}):")
        print(f"     Revised on: {revision_date}")
        print(f"     Next due: {actual_next} (expected: {expected_next})")
        print(f"     Status: {'✓' if actual_next == expected_next else '✗'}")
    
    # Test 6: Data persistence
    print("\n✅ Test 6: Data persistence")
    original_count = len(scheduler.topics)
    
    # Create new scheduler instance (should load from file)
    new_scheduler = SimpleRevisionScheduler("test_data.json")
    loaded_count = len(new_scheduler.topics)
    
    print(f"   - Original topics: {original_count}")
    print(f"   - Loaded topics: {loaded_count}")
    print(f"   - Persistence: {'✓' if original_count == loaded_count else '✗'}")
    
    # Show final summary
    print("\n📊 Final topic summary:")
    for topic in scheduler.topics:
        print(f"   - {topic['name']}:")
        print(f"     Learned: {topic['learned_date']}")
        print(f"     Revisions: {topic['revision_count']}")
        print(f"     Next due: {topic['next_revision']}")
    
    # Cleanup
    if Path("test_data.json").exists():
        Path("test_data.json").unlink()
    
    print("\n🎉 Testing completed!")

if __name__ == "__main__":
    test_revision_scheduler()