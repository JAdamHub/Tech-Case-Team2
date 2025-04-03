---
layout: default
title: Home
---

# LLM Code Change Tracker

Welcome to the LLM Code Change Tracker. This site provides an overview of code modifications suggested and applied by the AI.

## Recent Changes

<ul>
  {% for change in site.llm_changes reversed %}
    <li>
      <a href="{{ change.url | relative_url }}">{{ change.title }}</a> - {{ change.date | date: "%Y-%m-%d %H:%M" }}
    </li>
  {% endfor %}
</ul> 