---
layout: default
title: LLM Code Automation Hub
---

# LLM Code Automation Hub

Welcome to LLM Code Automation Hub - a central place where you can follow all AI-generated code changes, tests, and improvements in the project.

## Recent Changes

<div class="recent-changes-container">
  {% assign sorted_changes = site.llm_changes | sort: 'date' | reverse %}
  {% for change in sorted_changes limit:10 %}
    <div class="change-card">
      <div class="change-header">
        <span class="change-type change-type-{{ change.change_type | downcase | replace: ' ', '-' }}">{{ change.change_type }}</span>
        <span class="change-date">{{ change.date | date: "%d-%m-%Y %H:%M" }}</span>
      </div>
      <div class="change-title">
        <a href="{{ change.url | relative_url }}">{{ change.title }}</a>
      </div>
      {% if change.file_name %}
      <div class="change-file">
        <span class="file-icon">📄</span> {{ change.file_name }}
      </div>
      {% endif %}
    </div>
  {% endfor %}
</div>

<div class="view-all-changes">
  <a href="{{ site.baseurl }}/all-changes" class="view-all-button">View all changes</a>
</div> 