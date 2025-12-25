# Data Model for UI/UX Improvements

## Textbook Content Structure

### Chapter Entity
- **Fields**:
  - title: string (chapter title)
  - content: markdown text (the actual chapter content)
  - metadata: object (frontmatter with author, date, etc.)
  - navigation: object (previous/next chapter links)
  - codeBlocks: array (embedded code examples)
  - admonitions: array (tip, note, warning blocks)

### Navigation Entity
- **Fields**:
  - label: string (display name)
  - type: enum (category, link, doc)
  - items: array (nested navigation items)
  - collapsible: boolean (whether section can be collapsed)
  - collapsed: boolean (initial collapsed state)

### Styling Entity
- **Fields**:
  - typography: object (font, size, line-height, spacing)
  - colorScheme: object (light/dark theme variables)
  - layout: object (margins, padding, grid structure)
  - responsive: object (mobile/tablet/desktop adjustments)

## UI Components

### Admonition Component
- **Type**: tip, note, info, caution, danger
- **Structure**: title, content, icon, color scheme
- **Usage**: Educational emphasis within content

### Code Block Component
- **Structure**: language, code content, line numbers, copy button
- **Styling**: syntax highlighting theme, font, spacing
- **Functionality**: syntax highlighting, copy functionality

### Sidebar Component
- **Structure**: hierarchical navigation tree
- **Features**: collapsible sections, active state highlighting
- **Responsive**: mobile-friendly navigation

### Homepage Component
- **Structure**: hero section, feature highlights, call-to-action
- **Styling**: academic-focused design elements
- **Content**: book overview, module summaries