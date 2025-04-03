---
layout: default
title: All LLM Changes
permalink: /all-changes/
---

# All LLM Changes

<div class="filters">
  <button class="filter-btn active" data-filter="all">All</button>
  <button class="filter-btn" data-filter="linting">Linting</button>
  <button class="filter-btn" data-filter="test-generation">Tests</button>
  <button class="filter-btn" data-filter="bug-fix">Bug Fixes</button>
  <button class="filter-btn" data-filter="code-review">Code Reviews</button>
</div>

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
        <span class="change-file">{{ change.file }}</span>
        {% if change.source_file %}
        <span class="change-source">Source: {{ change.source_file }}</span>
        {% endif %}
      </div>
    </div>
  {% endfor %}
</div>

<script>
document.addEventListener('DOMContentLoaded', () => {
  const filterButtons = document.querySelectorAll('.filter-btn');
  const changeItems = document.querySelectorAll('.change-item');
  
  filterButtons.forEach(button => {
    button.addEventListener('click', () => {
      const filter = button.getAttribute('data-filter');
      
      // Update active button
      filterButtons.forEach(btn => btn.classList.remove('active'));
      button.classList.add('active');
      
      // Filter items
      changeItems.forEach(item => {
        if (filter === 'all' || item.getAttribute('data-type') === filter) {
          item.style.display = 'block';
        } else {
          item.style.display = 'none';
        }
      });
    });
  });
});
</script>

<style>
.filters {
  display: flex;
  flex-wrap: wrap;
  gap: 0.5rem;
  margin-bottom: 2rem;
}

.filter-btn {
  padding: 0.5rem 1rem;
  background: var(--light-bg);
  border: 1px solid #ddd;
  border-radius: 4px;
  cursor: pointer;
  font-size: 0.9rem;
  transition: all 0.2s;
}

.filter-btn.active {
  background: var(--primary-color);
  color: white;
  border-color: var(--primary-color);
}

.filter-btn:hover:not(.active) {
  background: #e9ecef;
}

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

.change-file, .change-source {
  background: #e9ecef;
  padding: 0.25rem 0.5rem;
  border-radius: 4px;
}

@media (max-width: 768px) {
  .filters {
    justify-content: center;
  }
}
</style> 