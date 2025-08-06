# Integration Instructions for Tangnet GitHub Pages

## Adding the UFO Glint Detector Banner to Your Main Page

### Quick Integration

1. Open your main `index.html` file at your GitHub pages repo
2. Add the banner HTML from `banner_section.html` to your page
3. Choose between the full animated banner or the minimalist version

### Option 1: Full Animated Banner

Copy the entire first section from `banner_section.html` (includes all styles and animations) and paste it where you want the banner to appear on your main page.

### Option 2: Minimalist Banner

Use the simpler version at the bottom of `banner_section.html` if you prefer less animation.

### File Structure

Make sure your GitHub pages repository has this structure:
```
/
├── index.html (your main page)
├── UFOglintdetector/
│   ├── enhanced_glint_detector.html
│   ├── README.md
│   └── (other project files)
```

### Customization

You can adjust these values in the banner:
- Detection count: Update the "147" value
- Uncorrelated targets: Update the "3" value
- Status: Change "PROJECT ACTIVE" if needed
- Colors: Modify the hex values (#00ff41 for green, #00e0ff for cyan, etc.)

### GitHub Pages Settings

1. Go to your repository settings
2. Navigate to Pages
3. Ensure your site is published from the correct branch
4. The banner will automatically appear once you commit the changes

### Testing Locally

```bash
# If you have Python installed
python -m http.server 8000

# Or with Node.js
npx http-server

# Then visit http://localhost:8000
```

### Live Updates

To make the statistics update automatically, you could:
1. Create a `stats.json` file that gets updated by your detection system
2. Add JavaScript to fetch and display current values
3. Use GitHub Actions to automatically update the stats

### Support

If you need help integrating the banner, feel free to open an issue in the UFOglintdetector project.