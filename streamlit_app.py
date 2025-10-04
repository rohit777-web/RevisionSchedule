"""
Revision Schedule Manager - Streamlit Web UI
A modern, interactive web interface for managing your revision schedule
"""

import streamlit as st
import datetime
import json
import pandas as pd
from pathlib import Path
from typing import List, Dict
import plotly.express as px
import plotly.graph_objects as go

class RevisionScheduler:
    def __init__(self, data_file: str = "revision_data.json"):
        """Initialize the revision scheduler with data persistence."""
        self.data_file = Path(data_file)
        self.topics = []
        self.revision_intervals = [1, 7, 15, 30, 90, 180]  # Days: 1d, 7d, 15d, 1m, 3m, 6m
        self.load_data()
    
    def add_topic(self, topic_name: str, learned_date: str = None) -> bool:
        """Add a new topic with learning date."""
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
        
        # Calculate first revision date (1 day after learning)
        learned = datetime.datetime.strptime(learned_date, "%Y-%m-%d").date()
        first_revision = learned + datetime.timedelta(days=1)
        topic_entry['next_revision'] = first_revision.strftime("%Y-%m-%d")
        
        self.topics.append(topic_entry)
        self.save_data()
        return True
    
    def mark_revised(self, topic_name: str, revision_date: str = None) -> bool:
        """Mark a topic as revised and schedule next revision."""
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
                return True
        
        return False
    
    def get_due_topics(self, date: str = None) -> List[Dict]:
        """Get topics that are due for revision on or before specified date."""
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
        """Get revision schedule for the next specified number of days."""
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
        """Delete a topic from the scheduler."""
        for i, topic in enumerate(self.topics):
            if topic['name'].lower() == topic_name.lower():
                del self.topics[i]
                self.save_data()
                return True
        
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
    
    def get_statistics(self) -> Dict:
        """Get statistics about topics and revisions."""
        total_topics = len(self.topics)
        due_today = len(self.get_due_topics())
        completed_topics = sum(1 for topic in self.topics if topic['revision_count'] >= 6)
        
        stats = {
            'total_topics': total_topics,
            'due_today': due_today,
            'completed': completed_topics,
            'in_progress': total_topics - completed_topics,
            'avg_revisions': sum(topic['revision_count'] for topic in self.topics) / total_topics if total_topics > 0 else 0
        }
        
        return stats

# Initialize session state
if 'scheduler' not in st.session_state:
    st.session_state.scheduler = RevisionScheduler()

# Page configuration
st.set_page_config(
    page_title="Revision Schedule Manager",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
    <style>
    .big-font {
        font-size: 24px !important;
        font-weight: bold;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 20px;
        border-radius: 10px;
        text-align: center;
    }
    .stButton>button {
        width: 100%;
    }
    </style>
    """, unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.image("https://em-content.zobj.net/source/animated-noto-color-emoji/356/books_1f4da.gif", width=100)
    st.title("📚 Revision Manager")
    st.markdown("---")
    
    page = st.radio(
        "Navigation",
        ["🏠 Dashboard", "➕ Add Topic", "✅ Mark Revised", "📅 Schedule", "📊 All Topics", "🗑️ Delete Topic"],
        label_visibility="collapsed"
    )
    
    st.markdown("---")
    st.markdown("### 🎯 Revision Intervals")
    st.markdown("""
    - 1️⃣ **1 day**
    - 2️⃣ **7 days**
    - 3️⃣ **15 days**
    - 4️⃣ **30 days**
    - 5️⃣ **90 days**
    - 6️⃣ **180 days**
    """)

scheduler = st.session_state.scheduler

# Main content based on page selection
if page == "🏠 Dashboard":
    st.title("🏠 Dashboard")
    st.markdown("### Welcome to your Revision Schedule Manager!")
    
    # Statistics
    stats = scheduler.get_statistics()
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("📚 Total Topics", stats['total_topics'])
    
    with col2:
        st.metric("⏰ Due Today", stats['due_today'], 
                 delta=f"{stats['due_today']} to review" if stats['due_today'] > 0 else "All caught up!")
    
    with col3:
        st.metric("✅ Completed", stats['completed'])
    
    with col4:
        st.metric("📈 Avg Revisions", f"{stats['avg_revisions']:.1f}")
    
    st.markdown("---")
    
    # Due Topics Section
    col_left, col_right = st.columns([1, 1])
    
    with col_left:
        st.subheader("⏰ Topics Due for Revision")
        due_topics = scheduler.get_due_topics()
        
        if due_topics:
            for topic in due_topics:
                days_overdue = (datetime.date.today() - 
                               datetime.datetime.strptime(topic['next_revision'], "%Y-%m-%d").date()).days
                
                with st.container():
                    col_a, col_b = st.columns([3, 1])
                    with col_a:
                        if days_overdue > 0:
                            st.error(f"🔴 **{topic['name']}** - {days_overdue} days overdue")
                        else:
                            st.warning(f"🟡 **{topic['name']}** - Due today")
                    with col_b:
                        if st.button("Mark Done", key=f"mark_{topic['name']}"):
                            scheduler.mark_revised(topic['name'])
                            st.success(f"✅ {topic['name']} marked as revised!")
                            st.rerun()
        else:
            st.success("🎉 No topics due today! You're all caught up!")
    
    with col_right:
        st.subheader("📅 Upcoming 7-Day Schedule")
        schedule = scheduler.get_revision_schedule(7)
        
        if schedule:
            for item in schedule:
                days = item['days_from_now']
                date_str = item['date']
                
                if days == 0:
                    st.info(f"📌 **Today** - {item['topic']} (Rev #{item['revision_number']})")
                elif days == 1:
                    st.info(f"📌 **Tomorrow** - {item['topic']} (Rev #{item['revision_number']})")
                else:
                    st.info(f"📌 **{date_str}** - {item['topic']} (Rev #{item['revision_number']})")
        else:
            st.info("No revisions scheduled for the next 7 days")
    
    # Charts
    if stats['total_topics'] > 0:
        st.markdown("---")
        st.subheader("📊 Visual Analytics")
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Revision progress pie chart
            fig_pie = go.Figure(data=[go.Pie(
                labels=['Completed (6+ revisions)', 'In Progress'],
                values=[stats['completed'], stats['in_progress']],
                hole=.3,
                marker_colors=['#00cc96', '#636efa']
            )])
            fig_pie.update_layout(title_text="Learning Progress")
            st.plotly_chart(fig_pie, width='stretch')
        
        with col2:
            # Revision count by topic
            topics = scheduler.get_all_topics()
            if topics:
                df_revisions = pd.DataFrame([
                    {'Topic': t['name'][:20] + '...' if len(t['name']) > 20 else t['name'], 
                     'Revisions': t['revision_count']} 
                    for t in sorted(topics, key=lambda x: x['revision_count'], reverse=True)[:10]
                ])
                
                fig_bar = px.bar(df_revisions, x='Topic', y='Revisions', 
                                title="Top Topics by Revision Count",
                                color='Revisions',
                                color_continuous_scale='viridis')
                st.plotly_chart(fig_bar, width='stretch')

elif page == "➕ Add Topic":
    st.title("➕ Add New Topic")
    
    with st.form("add_topic_form"):
        topic_name = st.text_input("Topic Name", placeholder="e.g., Python Functions")
        learned_date = st.date_input("Learned Date", value=datetime.date.today())
        
        submitted = st.form_submit_button("Add Topic", width='stretch')
        
        if submitted:
            if not topic_name:
                st.error("Please enter a topic name!")
            else:
                date_str = learned_date.strftime("%Y-%m-%d")
                if scheduler.add_topic(topic_name, date_str):
                    st.success(f"✅ Topic '{topic_name}' added successfully!")
                    st.info(f"📅 First revision scheduled for: {(learned_date + datetime.timedelta(days=1)).strftime('%Y-%m-%d')}")
                    st.balloons()
                else:
                    st.error(f"Topic '{topic_name}' already exists!")

elif page == "✅ Mark Revised":
    st.title("✅ Mark Topic as Revised")
    
    topics = scheduler.get_all_topics()
    
    if topics:
        topic_names = [t['name'] for t in topics]
        
        with st.form("mark_revised_form"):
            selected_topic = st.selectbox("Select Topic", topic_names)
            revision_date = st.date_input("Revision Date", value=datetime.date.today())
            
            submitted = st.form_submit_button("Mark as Revised", width='stretch')
            
            if submitted:
                date_str = revision_date.strftime("%Y-%m-%d")
                if scheduler.mark_revised(selected_topic, date_str):
                    # Get updated topic info
                    updated_topic = next((t for t in scheduler.get_all_topics() if t['name'] == selected_topic), None)
                    if updated_topic:
                        st.success(f"✅ Topic '{selected_topic}' marked as revised!")
                        st.info(f"📅 Next revision scheduled for: {updated_topic['next_revision']}")
                        st.info(f"🔢 Total revisions: {updated_topic['revision_count']}")
                        st.balloons()
                else:
                    st.error("Failed to mark topic as revised!")
    else:
        st.info("No topics available. Add some topics first!")

elif page == "📅 Schedule":
    st.title("📅 Revision Schedule")
    
    days_ahead = st.slider("Days to look ahead", 7, 90, 30)
    
    schedule = scheduler.get_revision_schedule(days_ahead)
    
    if schedule:
        df_schedule = pd.DataFrame(schedule)
        df_schedule.columns = ['Date', 'Topic', 'Revision #', 'Days from Now']
        
        # Color code based on urgency
        def highlight_urgent(row):
            if row['Days from Now'] <= 1:
                return ['background-color: #ffcccc'] * len(row)
            elif row['Days from Now'] <= 7:
                return ['background-color: #fff4cc'] * len(row)
            else:
                return ['background-color: #ccffcc'] * len(row)
        
        st.dataframe(
            df_schedule.style.apply(highlight_urgent, axis=1),
            width='stretch',
            hide_index=True
        )
        
        # Timeline visualization
        st.subheader("📈 Timeline View")
        
        fig_timeline = px.scatter(df_schedule, x='Date', y='Topic', 
                                 color='Revision #',
                                 size='Revision #',
                                 hover_data=['Days from Now'],
                                 title=f"Revision Schedule ({days_ahead} days)")
        st.plotly_chart(fig_timeline, width='stretch')
        
        # Download button
        csv = df_schedule.to_csv(index=False)
        st.download_button(
            label="📥 Download Schedule as CSV",
            data=csv,
            file_name=f"revision_schedule_{datetime.date.today()}.csv",
            mime="text/csv",
        )
    else:
        st.info(f"No revisions scheduled for the next {days_ahead} days!")

elif page == "📊 All Topics":
    st.title("📊 All Topics")
    
    topics = scheduler.get_all_topics()
    
    if topics:
        # Filter options
        col1, col2 = st.columns([1, 3])
        with col1:
            filter_option = st.selectbox("Filter by", ["All", "Due Today", "In Progress", "Completed"])
        
        # Apply filter
        if filter_option == "Due Today":
            topics = scheduler.get_due_topics()
        elif filter_option == "In Progress":
            topics = [t for t in topics if t['revision_count'] < 6]
        elif filter_option == "Completed":
            topics = [t for t in topics if t['revision_count'] >= 6]
        
        # Display topics
        df_topics = pd.DataFrame([{
            'Topic Name': t['name'],
            'Learned Date': t['learned_date'],
            'Revisions': t['revision_count'],
            'Last Revised': t['last_revised'] or 'Never',
            'Next Revision': t['next_revision'] or 'Completed'
        } for t in topics])
        
        st.dataframe(df_topics, width='stretch', hide_index=True)
        
        # Export options
        col1, col2 = st.columns(2)
        with col1:
            csv = df_topics.to_csv(index=False)
            st.download_button(
                label="📥 Download as CSV",
                data=csv,
                file_name=f"all_topics_{datetime.date.today()}.csv",
                mime="text/csv",
                width='stretch'
            )
        
        with col2:
            # Convert to Excel
            excel_buffer = pd.ExcelWriter('temp.xlsx', engine='openpyxl')
            df_topics.to_excel(excel_buffer, index=False, sheet_name='All Topics')
            excel_buffer.close()
            
            with open('temp.xlsx', 'rb') as f:
                st.download_button(
                    label="📥 Download as Excel",
                    data=f,
                    file_name=f"all_topics_{datetime.date.today()}.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                    width='stretch'
                )
    else:
        st.info("No topics available yet. Start by adding some topics!")

elif page == "🗑️ Delete Topic":
    st.title("🗑️ Delete Topic")
    
    topics = scheduler.get_all_topics()
    
    if topics:
        topic_names = [t['name'] for t in topics]
        
        selected_topic = st.selectbox("Select Topic to Delete", topic_names)
        
        # Show topic details
        topic_details = next((t for t in topics if t['name'] == selected_topic), None)
        if topic_details:
            st.info(f"""
            **Topic Details:**
            - Learned: {topic_details['learned_date']}
            - Revisions: {topic_details['revision_count']}
            - Next Revision: {topic_details['next_revision'] or 'Completed'}
            """)
        
        if st.button("🗑️ Delete Topic", type="secondary"):
            if scheduler.delete_topic(selected_topic):
                st.success(f"✅ Topic '{selected_topic}' deleted successfully!")
                st.rerun()
            else:
                st.error("Failed to delete topic!")
    else:
        st.info("No topics available to delete!")

# Footer
st.markdown("---")
st.markdown("""
    <div style='text-align: center; color: #888;'>
        <p>📚 Revision Schedule Manager | Built with Streamlit | Using Spaced Repetition for Better Learning</p>
    </div>
    """, unsafe_allow_html=True)
