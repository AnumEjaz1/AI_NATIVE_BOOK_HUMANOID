# Data Model: Update Docusaurus Site Logo for Physical AI Project

## Entities

### Logo File
- **name**: String ("logo.svg")
- **format**: String ("SVG")
- **path**: String ("/static/img/logo.svg")
- **dimensions**: Object (width: number, height: number)
- **color_scheme**: String ("dark/neutral base with blue/cyan/white accents")
- **elements**: Array of visual elements (humanoid silhouette, neural patterns, circuit motifs)
- **size**: Number (file size in bytes, under 100KB)
- **transparency**: Boolean (true - transparent background)

### Navigation Configuration
- **logo_path**: String (path to logo file in static directory)
- **alt_text**: String ("AI Native Book - Humanoid Robotics")
- **max_width**: Number (maximum width in navbar, typically 100px)
- **max_height**: Number (maximum height in navbar, typically 32px)
- **theme_compatibility**: Boolean (works with light/dark themes)

## Relationships
- Navigation Configuration references Logo File via logo_path

## Validation Rules
- Logo File must be in SVG format
- Logo File must have transparent background
- Logo File must scale appropriately for navbar display
- Navigation Configuration must point to existing logo file
- Logo File size must be under 100KB

## State Transitions
- Design → Review → Approved → Implemented → Tested