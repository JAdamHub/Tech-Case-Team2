#!/usr/bin/env python3
"""
Utility script to consolidate multiple reports for the same file into a single report.
This script can be run to clean up the _llm_changes directory and keep only the latest report for each file.
"""

import os
import re
import sys
import shutil
from datetime import datetime
from collections import defaultdict

# Directory for LLM change reports
LLM_CHANGES_DIR = "_llm_changes"
# Backup directory for original reports
BACKUP_DIR = "_llm_changes_backup"


def create_summary_index():
    """
    Create a summary index page with the consolidated reports.
    This function is called from the GitHub Actions workflow.
    """
    # Dictionary to store the latest report for each file
    latest_reports = {}
    files_by_type = defaultdict(list)
    
    print(f"Creating summary index for reports in {LLM_CHANGES_DIR}...")
    
    if not os.path.exists(LLM_CHANGES_DIR):
        print(f"Error: {LLM_CHANGES_DIR} directory does not exist.")
        return False
    
    # First pass: identify all report files and extract their metadata
    reports = []
    for filename in os.listdir(LLM_CHANGES_DIR):
        if not filename.endswith('.md') or filename == 'index.md' or filename.startswith('action_run_marker'):
            continue
            
        report_path = os.path.join(LLM_CHANGES_DIR, filename)
        
        # Extract date from filename (format: YYYYMMDD_HHMMSS_*)
        date_match = re.match(r'^(\d{8}_\d{6})_', filename)
        if not date_match:
            continue
            
        date_str = date_match.group(1)
        try:
            date = datetime.strptime(date_str, '%Y%m%d_%H%M%S')
        except ValueError:
            print(f"Warning: Could not parse date from filename: {filename}")
            continue
            
        # Extract file path and change type from the report front matter
        file_path = None
        change_type = None
        title = None
        
        try:
            with open(report_path, 'r') as f:
                content = f.read()
                
                # Extract from front matter
                file_match = re.search(r'file: "([^"]+)"', content)
                type_match = re.search(r'change_type: "([^"]+)"', content)
                title_match = re.search(r'title: "([^"]+)"', content)
                
                if file_match:
                    file_path = file_match.group(1)
                if type_match:
                    change_type = type_match.group(1)
                if title_match:
                    title = title_match.group(1)
        except Exception as e:
            print(f"Error reading report {filename}: {e}")
            continue
            
        if not file_path or not change_type:
            print(f"Warning: Missing metadata in report: {filename}")
            continue
            
        # Create a report object with all relevant metadata
        report = {
            'filename': filename,
            'path': report_path,
            'date': date,
            'file_path': file_path,
            'change_type': change_type,
            'title': title or f"{change_type} for {os.path.basename(file_path)}"
        }
        reports.append(report)
        
        # Store in the dictionary of files by type
        file_key = file_path
        if file_path not in latest_reports or date > latest_reports[file_path]['date']:
            latest_reports[file_path] = report
            
        # Also group by change type
        files_by_type[change_type].append(report)
    
    # Write the summary index
    summary_path = os.path.join(LLM_CHANGES_DIR, "summary_index.md")
    with open(summary_path, 'w') as f:
        f.write("---\n")
        f.write("layout: page\n")
        f.write("title: Consolidated LLM Changes Summary\n")
        f.write("permalink: /changes/summary/\n")
        f.write("---\n\n")
        
        f.write("# Consolidated LLM Changes Summary\n\n")
        f.write("This page shows a summary of the latest changes for each file, consolidated to avoid duplicates.\n\n")
        
        # Latest changes section
        f.write("## Latest Changes by File\n\n")
        for file_path, report in sorted(latest_reports.items(), key=lambda x: x[1]['date'], reverse=True):
            filename = report['filename']
            date_str = report['date'].strftime("%d-%m-%Y %H:%M")
            f.write(f"- [{report['title']}](../{filename}) - {date_str}\n")
        
        # Changes by type
        f.write("\n## Changes by Type\n\n")
        for change_type, reports in files_by_type.items():
            f.write(f"### {change_type}\n\n")
            for report in sorted(reports, key=lambda x: x['date'], reverse=True):
                filename = report['filename']
                date_str = report['date'].strftime("%d-%m-%Y %H:%M")
                f.write(f"- [{report['title']}](../{filename}) - {date_str}\n")
            f.write("\n")
    
    print(f"Created summary index at {summary_path}")
    return True


def consolidate_reports():
    """
    Consolidate multiple reports for the same file into a single report.
    Keep only the latest report for each file.
    """
    if not os.path.exists(LLM_CHANGES_DIR):
        print(f"Error: {LLM_CHANGES_DIR} directory does not exist.")
        return False
        
    # Create backup directory
    if not os.path.exists(BACKUP_DIR):
        os.makedirs(BACKUP_DIR)
        print(f"Created backup directory: {BACKUP_DIR}")
    
    # Backup current reports
    backup_timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_path = os.path.join(BACKUP_DIR, f"backup_{backup_timestamp}")
    os.makedirs(backup_path)
    
    for filename in os.listdir(LLM_CHANGES_DIR):
        if filename.endswith('.md') and not filename.startswith('action_run_marker'):
            src = os.path.join(LLM_CHANGES_DIR, filename)
            dst = os.path.join(backup_path, filename)
            shutil.copy2(src, dst)
    
    print(f"Backed up {LLM_CHANGES_DIR} to {backup_path}")
    
    # Dictionary to store file paths and their latest reports
    file_reports = {}
    test_reports = {}
    
    # First pass: gather all reports and identify the latest for each file
    for filename in os.listdir(LLM_CHANGES_DIR):
        if not filename.endswith('.md') or filename == 'index.md' or filename.startswith('action_run_marker'):
            continue
            
        report_path = os.path.join(LLM_CHANGES_DIR, filename)
        
        # Extract date from filename (format: YYYYMMDD_HHMMSS_*)
        date_match = re.match(r'^(\d{8}_\d{6})_', filename)
        if not date_match:
            continue
            
        date_str = date_match.group(1)
        try:
            date = datetime.strptime(date_str, '%Y%m%d_%H%M%S')
        except ValueError:
            print(f"Warning: Could not parse date from filename: {filename}")
            continue
            
        # Extract file path and change type from the report front matter
        file_path = None
        change_type = None
        source_file = None
        
        try:
            with open(report_path, 'r') as f:
                content = f.read()
                
                # Extract from front matter
                file_match = re.search(r'file: "([^"]+)"', content)
                type_match = re.search(r'change_type: "([^"]+)"', content)
                source_match = re.search(r'source_file: "([^"]+)"', content)
                
                if file_match:
                    file_path = file_match.group(1)
                if type_match:
                    change_type = type_match.group(1)
                if source_match:
                    source_file = source_match.group(1)
        except Exception as e:
            print(f"Error reading report {filename}: {e}")
            continue
            
        if not file_path or not change_type:
            print(f"Warning: Missing metadata in report: {filename}")
            continue
            
        # For test reports, use source file as the key
        if change_type == "Test Generation" and source_file:
            # Only store if it's newer than any existing report
            if source_file not in test_reports or date > test_reports[source_file]['date']:
                test_reports[source_file] = {
                    'filename': filename,
                    'path': report_path,
                    'date': date
                }
        else:
            # Only store if it's newer than any existing report
            if file_path not in file_reports or date > file_reports[file_path]['date']:
                file_reports[file_path] = {
                    'filename': filename,
                    'path': report_path,
                    'date': date
                }
    
    # Second pass: delete old reports keeping only the latest for each file
    files_to_keep = set(report['path'] for report in file_reports.values())
    files_to_keep.update(report['path'] for report in test_reports.values())
    
    # Update the filenames with "consolidated_" prefix
    for report_dict in [file_reports, test_reports]:
        for file_key, report in report_dict.items():
            # Add 'consolidated: true' to the front matter if not already there
            report_path = report['path']
            with open(report_path, 'r') as f:
                content = f.read()
                
            if 'consolidated: true' not in content:
                # Add 'consolidated: true' before the last line of the front matter
                content = content.replace('---\n', '---\nconsolidated: true\n', 1)
                with open(report_path, 'w') as f:
                    f.write(content)
                print(f"Updated report {report['filename']} to mark as consolidated")
    
    # Delete old reports
    delete_count = 0
    for filename in os.listdir(LLM_CHANGES_DIR):
        if filename.endswith('.md') and not filename.startswith('action_run_marker'):
            report_path = os.path.join(LLM_CHANGES_DIR, filename)
            if report_path not in files_to_keep:
                # Already backed up, so safe to delete
                os.remove(report_path)
                delete_count += 1
    
    # Create the summary index
    create_summary_index()
    
    print(f"Consolidation complete. Kept {len(files_to_keep)} latest reports, deleted {delete_count} older reports.")
    return True


if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == 'consolidate':
        consolidate_reports()
    else:
        create_summary_index() 