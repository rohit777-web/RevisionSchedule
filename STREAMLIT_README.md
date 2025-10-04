# 📚 Revision Schedule Manager - Streamlit Web App

A beautiful, interactive web application for managing your study topics and revision schedules using spaced repetition principles.

## 🎨 Features

### Modern Web Interface
- **Interactive Dashboard** - Real-time statistics and visual analytics
- **Topic Management** - Easy add, view, and delete topics
- **Smart Scheduling** - Automatic revision scheduling based on spaced repetition
- **Visual Charts** - Progress tracking with beautiful charts and graphs
- **Export Options** - Download schedules as CSV or Excel files

### Key Capabilities
✅ Add topics with custom learning dates  
✅ Mark revisions with one click  
✅ View due topics with urgency indicators  
✅ See 7-day and 30-day schedules  
✅ Track progress with visual analytics  
✅ Filter topics by status  
✅ Export data to CSV/Excel  

## 🚀 Quick Start

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

Or install individually:
```bash
pip install streamlit pandas openpyxl plotly
```

### 2. Run the Application

**Option A: Using Batch File (Windows)**
```bash
run_web_app.bat
```

**Option B: Using Command Line**
```bash
streamlit run streamlit_app.py
```

### 3. Access the App
The app will automatically open in your browser at: `http://localhost:8501`

## 📱 User Interface

### 🏠 Dashboard
- **Statistics Cards**: Total topics, due today, completed, average revisions
- **Due Topics**: List of topics needing revision with quick "Mark Done" buttons
- **Upcoming Schedule**: 7-day preview of upcoming revisions
- **Visual Analytics**: Pie charts and bar graphs showing your progress

### ➕ Add Topic
- Enter topic name
- Select learning date
- Automatic first revision scheduling

### ✅ Mark Revised
- Select topic from dropdown
- Choose revision date
- Instant feedback on next revision date

### 📅 Schedule
- Adjustable timeline (7-90 days)
- Color-coded urgency (red = overdue, yellow = this week, green = later)
- Timeline visualization
- Download schedule as CSV

### 📊 All Topics
- Complete topic list with details
- Filter options: All, Due Today, In Progress, Completed
- Export to CSV or Excel

### 🗑️ Delete Topic
- Select and remove topics
- View details before deletion
- Confirmation for safety

## 🎯 Revision Intervals

The app uses scientifically-proven spaced repetition:

| Revision | Interval After Previous |
|----------|------------------------|
| 1st | 1 day |
| 2nd | 7 days |
| 3rd | 15 days |
| 4th | 30 days (1 month) |
| 5th | 90 days (3 months) |
| 6th | 180 days (6 months) |
| 7th+ | 180 days (every 6 months) |

## 🎨 Visual Features

- **Color-Coded Urgency**: 
  - 🔴 Red = Overdue
  - 🟡 Yellow = Due this week
  - 🟢 Green = Future revisions

- **Interactive Charts**:
  - Progress pie chart
  - Revision count bar chart
  - Timeline scatter plot

- **Responsive Design**: Works on desktop and tablet

## 💾 Data Storage

- All data saved automatically to `revision_data.json`
- Persistent across sessions
- Easy to backup or transfer

## 🛠️ Troubleshooting

### Streamlit not found?
```bash
pip install streamlit
```

### Port already in use?
```bash
streamlit run streamlit_app.py --server.port 8502
```

### Browser doesn't open automatically?
Manually visit: `http://localhost:8501`

## 📚 Tips for Best Results

1. **Daily Routine**: Check the dashboard every day
2. **Mark Promptly**: Mark topics as revised as soon as you complete them
3. **Use Filters**: Focus on "Due Today" topics first
4. **Track Progress**: Review the analytics to stay motivated
5. **Export Data**: Download schedules for offline reference

## 🔄 Updating the App

If you add new topics or mark revisions, the interface updates immediately. Simply interact with the app and your changes are saved automatically!

## 📖 Example Workflow

1. **Add Topics**: Add "Python Functions" learned on Oct 1
2. **Dashboard**: See it due for first revision on Oct 2
3. **Mark Revised**: Click "Mark Done" on Oct 2
4. **Schedule**: View next revision scheduled for Oct 9
5. **Track**: Watch your progress grow in the analytics

## 🎉 Benefits

- **Better Retention**: Spaced repetition is scientifically proven
- **Visual Motivation**: See your progress in real-time
- **Easy to Use**: Intuitive interface, no learning curve
- **Portable**: Access from any browser on your computer
- **Data Control**: Your data stays on your machine

## 🌟 Advanced Tips

- Use the timeline slider to plan weeks ahead
- Export data regularly as backup
- Filter by "In Progress" to focus on active learning
- Check "Completed" topics to celebrate your achievements!

## 📞 Support

If you encounter any issues:
1. Make sure all dependencies are installed
2. Check that you're using Python 3.6+
3. Ensure `revision_data.json` has write permissions

---

**Happy Learning! 📚✨**

Built with ❤️ using Streamlit, Pandas, and Plotly