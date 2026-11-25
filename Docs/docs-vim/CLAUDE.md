# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Purpose

This folder holds tutorial Markdown files for terminal tools and programs. Other folders in this repository follow the same pattern (e.g., `/tmux`, `/cat`). Files are standalone reference documents — not a software project.

## File Conventions

- Each tool gets its own `.md` file named after the tool (e.g., `vim.md`, `tmux.md`)
- Structure: intro → concept overview → getting-started steps → categorized cheat sheet → learning path
- Tone: direct, practical, no hand-holding filler — the reader is technically capable
- Use fenced code blocks for all key sequences and commands
- Organize cheat sheets with clear `##` section headers so they're scannable at a glance

## Content Guidelines

- Lead with *why* something works, not just *what* to type — mental models stick better than lists
- Cross-reference related tools where relevant (e.g., vim ↔ tmux multiplexing)
- Learning trees should be concrete next steps, not vague "practice more" advice
