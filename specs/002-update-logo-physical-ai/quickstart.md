# Quickstart: Update Docusaurus Site Logo for Physical AI Project

## Create the Physical AI Logo

1. **Create the SVG logo file**
   ```bash
   # Create static/img directory if it doesn't exist
   mkdir -p static/img
   ```

2. **Design the logo with Physical AI/Humanoid Robotics themes**
   - Use abstract, minimal design elements
   - Include humanoid silhouette or robotic head
   - Add neural/node-link patterns symbolizing ROS 2 middleware
   - Add subtle circuit or sensor motifs
   - Use dark/neutral base with blue/cyan/white accents
   - Ensure transparent background
   - Optimize for small size readability

3. **Save the logo as SVG**
   ```bash
   # Save the logo file in the static/img directory
   # File name: logo.svg
   ```

## Update Docusaurus Configuration

1. **Update docusaurus.config.js**
   ```javascript
   // In docusaurus.config.js, update the navbar logo configuration:
   navbar: {
     logo: {
       alt: 'AI Native Book - Humanoid Robotics',
       src: '/img/logo.svg',  // Point to the new logo
     },
     // ... rest of navbar configuration
   }
   ```

2. **Verify the logo path is correct**
   - Ensure the logo file is in `/static/img/`
   - Ensure the path in `docusaurus.config.js` is `/img/logo.svg` (Docusaurus serves static files from /static/ at /)

## Test the Implementation

1. **Start the development server**
   ```bash
   npm start
   ```

2. **Verify the logo appears in the navbar**
   - Check that the logo displays correctly
   - Verify it's readable at small sizes
   - Confirm transparent background renders properly
   - Test across different themes (light/dark mode)

3. **Validate logo quality**
   - Ensure no pixelation or quality loss
   - Verify proper scaling at different sizes
   - Confirm file size is under 100KB

## Expected Outcomes
- New Physical AI/Humanoid Robotics themed logo displays in navbar
- Logo maintains quality when scaled
- Logo has transparent background
- Logo aligns with technical, research-grade aesthetic
- Site navigation continues to function properly