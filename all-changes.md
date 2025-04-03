---
layout: default
title: All LLM Changes
permalink: /all-changes/
---

# All LLM Changes

<div class="changes-list">
  {% assign all_changes = site.llm_changes | sort: 'date' | reverse %}
  {% for change in all_changes %}
    <div class="change-item" data-type="{{ change.change_type | downcase | replace: ' ', '-' }}">
      <div class="change-header">
        <span class="change-type change-type-{{ change.change_type | downcase | replace: ' ', '-' }}">{{ change.change_type }}</span>
        <span class="change-date">{{ change.date | date: "%d-%m-%Y %H:%M" }}</span>
      </div>
      <h3 class="change-title">
        <a href="{{ change.url | relative_url }}">{{ change.title }}</a>
      </h3>
      <div class="change-meta">
        <span class="change-file">Consolidated Report</span>
        <span class="change-date">Generated: {{ change.date | date: "%d-%m-%Y %H:%M" }}</span>
      </div>
    </div>
  {% endfor %}
</div>

<style>
.changes-list {
  display: grid;
  grid-template-columns: 1fr;
  gap: 1rem;
}

.change-item {
  background: var(--light-bg);
  border-radius: 8px;
  padding: 1.5rem;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
  transition: transform 0.3s ease;
}

.change-item:hover {
  transform: translateY(-3px);
}

.change-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 0.75rem;
}

.change-title {
  margin: 0.5rem 0;
}

.change-meta {
  font-size: 0.85rem;
  color: #6c757d;
  display: flex;
  flex-wrap: wrap;
  gap: 1rem;
}

.change-file,
.change-date {
  background: #e9ecef;
  padding: 0.25rem 0.5rem;
  border-radius: 4px;
}

.change-type {
    font-weight: bold;
    padding: 0.25rem 0.5rem;
    border-radius: 4px;
    background-color: #d3d3d3; /* Default background */
    color: #333;
}

/* Keep specific styles if needed, e.g., for 'Combined Analysis' */
.change-type-combined-analysis {
    background-color: #007bff; /* Blue for combined */
    color: white;
}

@media (max-width: 768px) {
  /* Add any responsive adjustments if necessary */
}

</style> 