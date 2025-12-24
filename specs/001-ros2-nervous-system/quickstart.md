# Quickstart: Module 1 – The Robotic Nervous System (ROS 2)

## Setup Docusaurus Documentation Site

1. **Install Node.js and npm** (if not already installed)
   ```bash
   # Verify Node.js installation (requires Node.js 18.0 or later)
   node --version
   npm --version
   ```

2. **Initialize Docusaurus project**
   ```bash
   # Create new Docusaurus project with docs preset
   npx create-docusaurus@latest website classic

   # Navigate to project directory
   cd website
   ```

3. **Install additional dependencies**
   ```bash
   # No additional dependencies required beyond the standard Docusaurus setup
   ```

4. **Create module directory and chapter files**
   ```bash
   # Create module directory
   mkdir -p docs/module-1

   # Create the three chapter files
   touch docs/module-1/chapter-1-ros2-architecture.md
   touch docs/module-1/chapter-2-python-agents-rclpy.md
   touch docs/module-1/chapter-3-urdf-humanoids.md
   ```

5. **Update sidebar configuration**
   Edit the `sidebars.js` file to include Module 1 and its chapters:

   ```javascript
   // sidebars.js
   module.exports = {
     tutorialSidebar: [
       'intro',
       {
         type: 'category',
         label: 'Module 1 - The Robotic Nervous System (ROS 2)',
         items: [
           'module-1/chapter-1-ros2-architecture',
           'module-1/chapter-2-python-agents-rclpy',
           'module-1/chapter-3-urdf-humanoids',
         ],
       },
     ],
   };
   ```

6. **Add content to chapter files**
   Add appropriate content to each chapter file based on the module requirements:

   For chapter-1-ros2-architecture.md:
   ```markdown
   # ROS 2 Architecture Fundamentals

   This chapter covers the core concepts of ROS 2 architecture including nodes, topics, services, actions, and DDS concepts, explaining why ROS 2 is suited for real-time humanoid control.

   <!-- Add detailed content here -->
   ```

7. **Start development server**
   ```bash
   # Start the development server
   npm start

   # The site will be available at http://localhost:3000
   ```

8. **Build for production**
   ```bash
   # Build the static files for production
   npm run build
   ```

## Expected Outcomes
- Docusaurus site running locally at http://localhost:3000
- Module 1 visible in the sidebar with three chapters
- Each chapter accessible and properly formatted
- Site ready for content addition following the book standards