# Revision Schedule Manager

A Python program that helps you manage your study topics and automatically generates revision schedules using spaced repetition principles.

## Features

- **Add Topics**: Track what you've learned with dates
- **Automatic Scheduling**: Generates revision schedule with intervals: 1 day → 7 days → 15 days → 1 month → 3 months → 6 months
- **Due Topics**: View topics that need revision today
- **30-Day Schedule**: See your revision plan for the next month
- **Excel Export**: Export your schedule to Excel files with multiple sheets
- **Data Persistence**: Automatically saves your data in JSON format
- **Statistics**: Track your progress and revision statistics

## Installation

1. Make sure you have Python 3.6+ installed
2. Install required dependencies:
   ```
   pip install -r requirements.txt
   ```

## Usage

Run the program:
```
python revision_scheduler.py
```

### Main Menu Options:

1. **Add New Topic**: Enter a topic name and optional learning date
2. **Mark Topic as Revised**: Update when you've completed a revision
3. **View Due Topics**: See what needs revision today
4. **View 30-Day Schedule**: See upcoming revisions
5. **View All Topics**: Display all tracked topics
6. **Delete Topic**: Remove a topic from tracking
7. **Export to Excel**: Create Excel file with revision schedules
8. **View Statistics**: See your learning progress stats
9. **Exit**: Close the program

## How It Works

The program uses spaced repetition intervals:
- **1st revision**: 1 day after learning
- **2nd revision**: 7 days after 1st revision
- **3rd revision**: 15 days after 2nd revision
- **4th revision**: 30 days after 3rd revision
- **5th revision**: 90 days after 4th revision
- **6th revision**: 180 days after 5th revision
- **Future revisions**: Every 6 months

## Data Storage

- Topics are automatically saved to `revision_data.json`
- Excel exports include three sheets:
  - **All Topics**: Complete topic list with details
  - **Due Today**: Topics needing immediate revision
  - **30-Day Schedule**: Upcoming revision schedule

## Example Usage

1. Add a topic: "Python Functions" learned on 2025-10-01
2. The system automatically schedules:
   - 1st revision: 2025-10-02 (1 day later)
   - 2nd revision: 2025-10-09 (7 days after 1st)
   - 3rd revision: 2025-10-24 (15 days after 2nd)
   - And so on...

## Tips

- Review due topics daily for best results
- Use the Excel export to print physical copies
- Mark revisions promptly to maintain accurate scheduling
- The system is designed for long-term retention using scientifically-proven spaced repetition

## Requirements

- Python 3.6+
- pandas
- openpyxl