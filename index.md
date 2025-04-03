---
layout: default
title: LLM Code Automation Hub
---

# LLM Code Automation Hub

Welcome to LLM Code Automation Hub - a central place where you can follow all AI-generated code changes, tests, and improvements in the project.

## Dashboard

<div class="dashboard">
  <div class="dashboard-card">
    <h3>🔍 Linting Fixes</h3>
    <ul>
      {% assign linting_changes = site.llm_changes | where: "change_type", "Linting" %}
      {% for change in linting_changes limit:5 %}
        <li>
          <a href="{{ change.url | relative_url }}">{{ change.title }}</a>
          <small>{{ change.date | date: "%d-%m-%Y %H:%M" }}</small>
        </li>
      {% endfor %}
      {% if linting_changes.size > 5 %}
        <li><a href="{{ '/changes/linting/' | relative_url }}">See all</a></li>
      {% endif %}
    </ul>
  </div>
  
  <div class="dashboard-card">
    <h3>🧪 Test Generation</h3>
    <ul>
      {% assign test_changes = site.llm_changes | where: "change_type", "Test Generation" %}
      {% for change in test_changes limit:5 %}
        <li>
          <a href="{{ change.url | relative_url }}">{{ change.title }}</a>
          <small>{{ change.date | date: "%d-%m-%Y %H:%M" }}</small>
        </li>
      {% endfor %}
      {% if test_changes.size > 5 %}
        <li><a href="{{ '/changes/tests/' | relative_url }}">See all</a></li>
      {% endif %}
    </ul>
  </div>
  
  <div class="dashboard-card">
    <h3>🐛 Bug Fixes</h3>
    <ul>
      {% assign bug_changes = site.llm_changes | where: "change_type", "Bug Fix" %}
      {% for change in bug_changes limit:5 %}
        <li>
          <a href="{{ change.url | relative_url }}">{{ change.title }}</a>
          <small>{{ change.date | date: "%d-%m-%Y %H:%M" }}</small>
        </li>
      {% endfor %}
      {% if bug_changes.size > 5 %}
        <li><a href="{{ '/changes/bugs/' | relative_url }}">See all</a></li>
      {% endif %}
    </ul>
  </div>
  
  <div class="dashboard-card">
    <h3>📝 Code Reviews</h3>
    <ul>
      {% assign review_changes = site.llm_changes | where: "change_type", "Code Review" %}
      {% for change in review_changes limit:5 %}
        <li>
          <a href="{{ change.url | relative_url }}">{{ change.title }}</a>
          <small>{{ change.date | date: "%d-%m-%Y %H:%M" }}</small>
        </li>
      {% endfor %}
      {% if review_changes.size > 5 %}
        <li><a href="{{ '/changes/reviews/' | relative_url }}">See all</a></li>
      {% endif %}
    </ul>
  </div>
</div>

## Recent Changes

<ul class="recent-changes">
  {% for change in site.llm_changes reversed limit:10 %}
    <li>
      <span class="change-type change-type-{{ change.change_type | downcase | replace: ' ', '-' }}">{{ change.change_type }}</span>
      <a href="{{ change.url | relative_url }}">{{ change.title }}</a>
      <span class="change-date">{{ change.date | date: "%d-%m-%Y %H:%M" }}</span>
    </li>
  {% endfor %}
</ul>

<div class="view-all">
  <a href="{{ '/all-changes' | relative_url }}" class="button">View all changes</a>
</div> 