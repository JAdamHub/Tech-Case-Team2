---
layout: default
title: Linting Ændringer
permalink: /changes/linting/
---

# 🔍 Linting Ændringer

Her finder du en oversigt over alle automatiske linting forbedringer, der er blevet udført af AI.

<div class="changes-list">
  {% assign linting_changes = site.llm_changes | where: "change_type", "Linting" | sort: 'date' | reverse %}
  {% for change in linting_changes %}
    <div class="change-item">
      <div class="change-header">
        <span class="change-date">{{ change.date | date: "%d-%m-%Y %H:%M" }}</span>
      </div>
      <h3 class="change-title">
        <a href="{{ change.url | relative_url }}">{{ change.title }}</a>
      </h3>
      <div class="change-meta">
        <span class="change-file">{{ change.file }}</span>
      </div>
    </div>
  {% else %}
    <div class="empty-state">
      <p>Ingen linting ændringer fundet endnu.</p>
    </div>
  {% endfor %}
</div>

<style>
.changes-list {
  display: grid;
  grid-template-columns: 1fr;
  gap: 1rem;
  margin-top: 2rem;
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
  justify-content: flex-end;
  margin-bottom: 0.75rem;
}

.change-date {
  font-size: 0.85rem;
  color: #6c757d;
}

.change-title {
  margin: 0.5rem 0;
}

.change-meta {
  font-size: 0.85rem;
  color: #6c757d;
}

.change-file {
  background: #e9ecef;
  padding: 0.25rem 0.5rem;
  border-radius: 4px;
  display: inline-block;
}

.empty-state {
  background: var(--light-bg);
  border-radius: 8px;
  padding: 3rem;
  text-align: center;
  color: #6c757d;
}
</style> 