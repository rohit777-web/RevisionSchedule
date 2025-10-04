"""
Revision Schedule Manager
A program to track topics learned and automatically generate revision schedules
using spaced repetition: 1 day, 7 days, 15 days, 1 month, 3 months, 6 months
"""

import datetime
import json
import csv
import pandas as pd
from pathlib import Path
from typing import List, Dict, Tuple
import os

class RevisionScheduler:
    def __init__(self, data_file: str = "revision_data.json"):
        """Initialize the revision scheduler with data persistence."""
        self.data_file = Path(data_file)
        self.topics = []
        self.revision_intervals = [1, 7, 15, 30, 90, 180]  # Days: 1d, 7d, 15d, 1m, 3m, 6m
        self.load_data()
    
    def add_topic(self, topic_name: str, learned_date: str = None) -> bool:
        """
        Add a new topic with learning date.
        
        Args:
            topic_name: Name of the topic learned
            learned_date: Date when topic was learned (YYYY-MM-DD format)
                         If None, uses current date
        
        Returns:
            True if topic was added successfully, False if already exists
        """
        if learned_date is None:
            learned_date = datetime.date.today().strftime("%Y-%m-%d")
        
        # Check if topic already exists
        for topic in self.topics:
            if topic['name'].lower() == topic_name.lower():
                print(f"Topic '{topic_name}' already exists!")
                return False
        
        # Create new topic entry
        topic_entry = {
            'name': topic_name,
            'learned_date': learned_date,
            'revision_count': 0,
            'last_revised': None,
            'next_revision': None
        }
        
        # Calculate first revision date (1 day after learning)
        learned = datetime.datetime.strptime(learned_date, "%Y-%m-%d").date()
        first_revision = learned + datetime.timedelta(days=1)
        topic_entry['next_revision'] = first_revision.strftime("%Y-%m-%d")
        
        self.topics.append(topic_entry)
        self.save_data()
        print(f"Topic '{topic_name}' added successfully!")
        return True
    
    def mark_revised(self, topic_name: str, revision_date: str = None) -> bool:
        """
        Mark a topic as revised and schedule next revision.
        
        Args:
            topic_name: Name of the topic that was revised
            revision_date: Date when revision was done (YYYY-MM-DD format)
                          If None, uses current date
        
        Returns:
            True if topic was found and updated, False otherwise
        """
        if revision_date is None:
            revision_date = datetime.date.today().strftime("%Y-%m-%d")
        
        for topic in self.topics:
            if topic['name'].lower() == topic_name.lower():
                topic['revision_count'] += 1
                topic['last_revised'] = revision_date
                
                # Calculate next revision date based on revision count
                if topic['revision_count'] < len(self.revision_intervals):
                    days_to_add = self.revision_intervals[topic['revision_count']]
                    revised = datetime.datetime.strptime(revision_date, "%Y-%m-%d").date()
                    next_revision = revised + datetime.timedelta(days=days_to_add)
                    topic['next_revision'] = next_revision.strftime("%Y-%m-%d")
                else:
                    # After 6th revision, schedule 6 months later
                    revised = datetime.datetime.strptime(revision_date, "%Y-%m-%d").date()
                    next_revision = revised + datetime.timedelta(days=180)
                    topic['next_revision'] = next_revision.strftime("%Y-%m-%d")
                
                self.save_data()
                print(f"Topic '{topic_name}' marked as revised!")
                return True
        
        print(f"Topic '{topic_name}' not found!")
        return False
    
    def get_due_topics(self, date: str = None) -> List[Dict]:
        """
        Get topics that are due for revision on or before specified date.
        
        Args:
            date: Date to check (YYYY-MM-DD format). If None, uses current date
        
        Returns:
            List of topics due for revision
        """
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
        
        # Sort by next revision date
        due_topics.sort(key=lambda x: x['next_revision'])
        return due_topics
    
    def get_revision_schedule(self, days_ahead: int = 30) -> List[Dict]:
        """
        Get revision schedule for the next specified number of days.
        
        Args:
            days_ahead: Number of days to look ahead (default: 30)
        
        Returns:
            List of scheduled revisions with dates
        """
        today = datetime.date.today()
        end_date = today + datetime.timedelta(days=days_ahead)
        
        schedule = []
        for topic in self.topics:
            if topic['next_revision']:
                next_rev_date = datetime.datetime.strptime(topic['next_revision'], "%Y-%m-%d").date()
                if today <= next_rev_date <= end_date:
                    schedule.append({
                        'date': topic['next_revision'],
                        'topic': topic['name'],
                        'revision_number': topic['revision_count'] + 1,
                        'days_from_now': (next_rev_date - today).days
                    })
        
        # Sort by date
        schedule.sort(key=lambda x: x['date'])
        return schedule
    
    def get_all_topics(self) -> List[Dict]:
        """Get all topics with their details."""
        return self.topics.copy()
    
    def delete_topic(self, topic_name: str) -> bool:
        """
        Delete a topic from the scheduler.
        
        Args:
            topic_name: Name of the topic to delete
        
        Returns:
            True if topic was found and deleted, False otherwise
        """
        for i, topic in enumerate(self.topics):
            if topic['name'].lower() == topic_name.lower():
                del self.topics[i]
                self.save_data()
                print(f"Topic '{topic_name}' deleted successfully!")
                return True
        
        print(f"Topic '{topic_name}' not found!")
        return False
    
    def save_data(self):
        """Save topics data to JSON file."""
        with open(self.data_file, 'w') as f:
            json.dump(self.topics, f, indent=2)
    
    def load_data(self):
        """Load topics data from JSON file."""
        if self.data_file.exists():
            try:
                with open(self.data_file, 'r') as f:
                    self.topics = json.load(f)
            except (json.JSONDecodeError, FileNotFoundError):
                self.topics = []
        else:
            self.topics = []
    
    def export_to_excel(self, filename: str = None) -> str:
        """
        Export revision schedule to Excel file.
        
        Args:
            filename: Name of the Excel file to create
        
        Returns:
            Path to the created Excel file
        """
        if filename is None:
            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"revision_schedule_{timestamp}.xlsx"
        
        # Create DataFrames for different sheets
        
        # All Topics sheet
        topics_data = []
        for topic in self.topics:
            topics_data.append({
                'Topic Name': topic['name'],
                'Learned Date': topic['learned_date'],
                'Revision Count': topic['revision_count'],
                'Last Revised': topic['last_revised'] or 'Never',
                'Next Revision': topic['next_revision'] or 'Completed'
            })
        
        df_topics = pd.DataFrame(topics_data)
        
        # Due Today sheet
        due_topics = self.get_due_topics()
        due_data = []
        for topic in due_topics:
            due_data.append({
                'Topic Name': topic['name'],
                'Due Date': topic['next_revision'],
                'Revision Number': topic['revision_count'] + 1,
                'Days Overdue': (datetime.date.today() - 
                               datetime.datetime.strptime(topic['next_revision'], "%Y-%m-%d").date()).days
            })
        
        df_due = pd.DataFrame(due_data)
        
        # 30-Day Schedule sheet
        schedule = self.get_revision_schedule(30)
        df_schedule = pd.DataFrame(schedule)
        if not df_schedule.empty:
            df_schedule.columns = ['Date', 'Topic', 'Revision #', 'Days from Now']
        
        # Write to Excel
        with pd.ExcelWriter(filename, engine='openpyxl') as writer:
            df_topics.to_excel(writer, sheet_name='All Topics', index=False)
            df_due.to_excel(writer, sheet_name='Due Today', index=False)
            df_schedule.to_excel(writer, sheet_name='30-Day Schedule', index=False)
        
        print(f"Excel file exported: {filename}")
        return filename
    
    def display_statistics(self):
        """Display statistics about topics and revisions."""
        total_topics = len(self.topics)
        due_today = len(self.get_due_topics())
        completed_topics = sum(1 for topic in self.topics if topic['revision_count'] >= 6)
        
        print(f"\n=== REVISION STATISTICS ===")
        print(f"Total Topics: {total_topics}")
        print(f"Due Today: {due_today}")
        print(f"Completed (6+ revisions): {completed_topics}")
        print(f"In Progress: {total_topics - completed_topics}")
        
        if self.topics:
            avg_revisions = sum(topic['revision_count'] for topic in self.topics) / total_topics
            print(f"Average Revisions per Topic: {avg_revisions:.1f}")

def main():
    """Main function to demonstrate the revision scheduler."""
    scheduler = RevisionScheduler()
    
    print("=== REVISION SCHEDULE MANAGER ===")
    print("Welcome to your personal revision scheduler!")
    print("This program helps you track topics and schedules revisions using spaced repetition.")
    
    while True:
        print("\n=== MAIN MENU ===")
        print("1. Add New Topic")
        print("2. Mark Topic as Revised")
        print("3. View Due Topics")
        print("4. View 30-Day Schedule")
        print("5. View All Topics")
        print("6. Delete Topic")
        print("7. Export to Excel")
        print("8. View Statistics")
        print("9. Exit")
        
        choice = input("\nEnter your choice (1-9): ").strip()
        
        if choice == '1':
            topic_name = input("Enter topic name: ").strip()
            if not topic_name:
                print("Topic name cannot be empty!")
                continue
            
            date_input = input("Enter learned date (YYYY-MM-DD) or press Enter for today: ").strip()
            if date_input:
                try:
                    # Validate date format
                    datetime.datetime.strptime(date_input, "%Y-%m-%d")
                    scheduler.add_topic(topic_name, date_input)
                except ValueError:
                    print("Invalid date format! Please use YYYY-MM-DD")
            else:
                scheduler.add_topic(topic_name)
        
        elif choice == '2':
            topic_name = input("Enter topic name to mark as revised: ").strip()
            if topic_name:
                scheduler.mark_revised(topic_name)
        
        elif choice == '3':
            due_topics = scheduler.get_due_topics()
            if due_topics:
                print(f"\n=== TOPICS DUE FOR REVISION ===")
                for topic in due_topics:
                    days_overdue = (datetime.date.today() - 
                                   datetime.datetime.strptime(topic['next_revision'], "%Y-%m-%d").date()).days
                    status = f"{days_overdue} days overdue" if days_overdue > 0 else "Due today"
                    print(f"• {topic['name']} - Due: {topic['next_revision']} ({status})")
            else:
                print("\nNo topics due for revision today! 🎉")
        
        elif choice == '4':
            schedule = scheduler.get_revision_schedule(30)
            if schedule:
                print(f"\n=== 30-DAY REVISION SCHEDULE ===")
                for item in schedule:
                    print(f"• {item['date']} - {item['topic']} (Revision #{item['revision_number']}) - {item['days_from_now']} days from now")
            else:
                print("\nNo revisions scheduled for the next 30 days!")
        
        elif choice == '5':
            topics = scheduler.get_all_topics()
            if topics:
                print(f"\n=== ALL TOPICS ===")
                for topic in topics:
                    status = f"Next: {topic['next_revision']}" if topic['next_revision'] else "Completed"
                    print(f"• {topic['name']} - Learned: {topic['learned_date']} - Revisions: {topic['revision_count']} - {status}")
            else:
                print("\nNo topics added yet!")
        
        elif choice == '6':
            topic_name = input("Enter topic name to delete: ").strip()
            if topic_name:
                confirm = input(f"Are you sure you want to delete '{topic_name}'? (y/N): ").strip().lower()
                if confirm == 'y':
                    scheduler.delete_topic(topic_name)
        
        elif choice == '7':
            filename = input("Enter Excel filename (or press Enter for auto-generated): ").strip()
            if filename and not filename.endswith('.xlsx'):
                filename += '.xlsx'
            scheduler.export_to_excel(filename if filename else None)
        
        elif choice == '8':
            scheduler.display_statistics()
        
        elif choice == '9':
            print("Thank you for using Revision Schedule Manager!")
            break
        
        else:
            print("Invalid choice! Please enter a number between 1 and 9.")

if __name__ == "__main__":
    main()