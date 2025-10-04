# 📚 Revision Schedule Manager - Usage Guide

## Quick Start

### Option 1: Full Version (Requires Python + Dependencies)
1. Install Python 3.6+ from python.org
2. Install dependencies: `python -m pip install pandas openpyxl`
3. Run: `python revision_scheduler.py`
4. Features: Full functionality + Excel export

### Option 2: Standalone Version (Python Only)
1. Install Python 3.6+ from python.org
2. Run: `python simple_revision_scheduler.py`
3. Features: Core functionality + CSV export

## 🎯 How to Use

### Adding Topics
1. Select "Add New Topic" from menu
2. Enter the topic name (e.g., "Python Functions")
3. Enter learning date or press Enter for today
4. System automatically schedules first revision for tomorrow

### Managing Revisions
1. Check "View Due Topics" daily
2. Study the topics that are due
3. Use "Mark Topic as Revised" when done
4. System automatically schedules next revision

### Viewing Progress
- **Due Topics**: See what needs revision today
- **30-Day Schedule**: Plan your revision sessions
- **All Topics**: Overview of your learning progress
- **Statistics**: Track your overall progress

## 📅 Revision Schedule

The system uses scientifically-proven spaced repetition:

| Revision | Interval | Example Timeline |
|----------|----------|------------------|
| 1st | 1 day | Learn today → Revise tomorrow |
| 2nd | 7 days | After 1 week |
| 3rd | 15 days | After 2+ weeks |
| 4th | 30 days | After 1 month |
| 5th | 90 days | After 3 months |
| 6th | 180 days | After 6 months |
| 7th+ | 180 days | Every 6 months |

## 💡 Tips for Success

1. **Daily Check**: Review due topics every day
2. **Mark Promptly**: Mark revisions as soon as you complete them
3. **Stay Consistent**: Small daily sessions work better than cramming
4. **Export Data**: Use CSV/Excel export to print physical schedules
5. **Use Demo**: Run option 9 to see how it works with sample data

## 📁 Files Created

- `revision_data.json`: Your topic data (automatically saved)
- `*_all_topics.csv`: Complete topic list export
- `*_due_today.csv`: Topics needing revision
- `*_30_day_schedule.csv`: Upcoming revisions

## 🔧 Troubleshooting

**Python not found?**
- Install Python from python.org
- Enable "Add to PATH" during installation

**Import errors?**
- Full version: `python -m pip install pandas openpyxl`
- Or use: `simple_revision_scheduler.py` (no dependencies)

**Data not saving?**
- Check file permissions in the directory
- Make sure you have write access

## 🎓 Example Usage

1. **Day 1**: Add "Spanish Vocabulary" (learned today)
2. **Day 2**: System reminds you to revise "Spanish Vocabulary"
3. **Day 2**: Mark as revised → Next revision scheduled for Day 9
4. **Day 9**: Revise again → Next revision scheduled for Day 24
5. **Continue the pattern for long-term retention**

## 🚀 Advanced Features

- **Batch Export**: Export all data to multiple CSV files
- **Date Flexibility**: Add topics with custom learning dates  
- **Progress Tracking**: See completion statistics
- **Data Persistence**: All data automatically saved and restored

Remember: Consistency is key! The spaced repetition algorithm is designed to optimize your long-term memory retention. 🧠✨