#!/usr/bin/env python3
"""
Simple analytics viewer for Taofu bot data
Run this to analyze questions and user engagement
"""

import json
from collections import Counter
from datetime import datetime, timedelta
import sys

def load_analytics():
    """Load analytics data from JSON file"""
    try:
        with open('analytics.json', 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        print("No analytics data found. Run the bots first to collect data.")
        return []
    except json.JSONDecodeError:
        print("Error reading analytics.json. File may be corrupted.")
        return []

def analyze_questions(analytics):
    """Analyze the most common questions"""
    if not analytics:
        print("No data to analyze.")
        return
    
    print("=" * 60)
    print("TAOFU BOT ANALYTICS")
    print("=" * 60)
    
    # Basic stats
    total_questions = len(analytics)
    print(f"\n📊 Total Questions: {total_questions}")
    
    # Platform breakdown
    platforms = Counter(item['platform'] for item in analytics)
    print(f"\n📱 Platform Breakdown:")
    for platform, count in platforms.items():
        print(f"  {platform}: {count} questions")
    
    # Time analysis
    if analytics:
        dates = [datetime.fromisoformat(item['timestamp'].split('T')[0]) for item in analytics]
        date_counts = Counter(dates)
        
        print(f"\n📅 Questions by Date:")
        for date, count in sorted(date_counts.items()):
            print(f"  {date.strftime('%Y-%m-%d')}: {count} questions")
    
    # Most common questions
    questions = [item['question'].lower().strip() for item in analytics]
    question_counts = Counter(questions)
    
    print(f"\n❓ Top 10 Most Asked Questions:")
    for i, (question, count) in enumerate(question_counts.most_common(10), 1):
        print(f"  {i}. \"{question}\" ({count} times)")
    
    # User engagement
    users = Counter(item['username'] for item in analytics)
    print(f"\n👥 Top 10 Most Active Users:")
    for i, (username, count) in enumerate(users.most_common(10), 1):
        print(f"  {i}. {username}: {count} questions")
    
    # Recent activity
    if analytics:
        recent = [item for item in analytics 
                 if datetime.fromisoformat(item['timestamp']) > datetime.now() - timedelta(days=7)]
        print(f"\n🕒 Recent Activity (Last 7 Days): {len(recent)} questions")
        
        if recent:
            print("  Recent questions:")
            for item in recent[-5:]:  # Last 5 questions
                timestamp = datetime.fromisoformat(item['timestamp']).strftime('%m-%d %H:%M')
                print(f"    [{timestamp}] {item['username']}: \"{item['question']}\"")

def search_questions(analytics, search_term):
    """Search for specific questions"""
    matching = []
    search_lower = search_term.lower()
    
    for item in analytics:
        if search_lower in item['question'].lower():
            matching.append(item)
    
    if matching:
        print(f"\n🔍 Found {len(matching)} questions containing '{search_term}':")
        for item in matching:
            timestamp = datetime.fromisoformat(item['timestamp']).strftime('%Y-%m-%d %H:%M')
            print(f"  [{timestamp}] {item['username']} ({item['platform']}): \"{item['question']}\"")
    else:
        print(f"\n❌ No questions found containing '{search_term}'")

def export_data(analytics, filename='taofu_analytics_export.json'):
    """Export analytics data to a file"""
    try:
        with open(filename, 'w') as f:
            json.dump(analytics, f, indent=2)
        print(f"\n💾 Data exported to {filename}")
    except Exception as e:
        print(f"\n❌ Error exporting data: {e}")

def main():
    """Main function"""
    analytics = load_analytics()
    
    if not analytics:
        return
    
    # Check for command line arguments
    if len(sys.argv) > 1:
        command = sys.argv[1]
        
        if command == 'search' and len(sys.argv) > 2:
            search_questions(analytics, sys.argv[2])
        elif command == 'export':
            export_data(analytics)
        elif command == 'help':
            print("""
Usage: python analytics_viewer.py [command]

Commands:
  (no args)    - Show full analytics report
  search <term> - Search for questions containing <term>
  export       - Export data to taofu_analytics_export.json
  help         - Show this help message
            """)
        else:
            print("Unknown command. Use 'help' for usage information.")
    else:
        # Show full analytics
        analyze_questions(analytics)

if __name__ == "__main__":
    main() 