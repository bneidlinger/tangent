# TANGNET Project Structure

## 📁 Current Directory Layout (After Migration)

```
tangnet/
├── .github/                    # GitHub Actions workflows
│   └── workflows/
│       └── update-mesh-inventory.yml
├── archive/                    # Archived/deprecated code
│   ├── oldtanchatfiles/       # Original tanchat experiments
│   ├── tanchat/               # Legacy FastAPI chat server
│   └── tanchat-node/          # Legacy Node.js chat interface
├── assets/                     # Root-level assets
│   ├── command.jpeg           # Lab photo - command center
│   └── kb.jpeg                # Lab photo - hardware setup
├── config/                     # Configuration files
├── docs/                       # All documentation (GitHub Pages)
│   ├── api/                   # API documentation
│   ├── architecture/          # Architecture docs
│   │   └── mesh/              # Mesh network documentation
│   │       ├── mesh-inventory.md
│   │       ├── mesh-inventory.yaml
│   │       └── mesh_network.md
│   ├── assets/                # Documentation assets
│   │   └── images/
│   │       └── picluster.png  # Main architecture diagram
│   ├── guides/                # Setup and usage guides
│   │   └── llama2-7b-guide.html
│   ├── setup/                 # Setup documentation
│   │   ├── cana_setup.html
│   │   ├── modelsetup.html
│   │   ├── nextphase3080.html
│   │   ├── set-up2.html
│   │   ├── set-up3.html
│   │   └── tailscalesetup.html
│   ├── *.html                 # Various doc pages (from overview/)
│   ├── mesh-inventory-auto.md # Auto-generated inventory
│   ├── mesh-inventory-auto.yaml
│   ├── mesh-status.svg        # Live status badge
│   └── node-badges/           # Individual node status badges
├── lab_photos/                # Lab photos (duplicate of assets)
├── node 02/                   # Node-specific files
│   ├── UI/
│   │   └── console_ui.py
│   └── set-up/
│       └── *.html             # Node setup docs
├── scripts/                   # Utility scripts
├── src/                       # Source code (future)
├── tailscale/                 # Tailscale integration
│   └── update_mesh_inventory.py
├── venv/                      # Python virtual environment
├── .gitignore
├── architecture.html          # Architecture overview
├── CLAUDE.md                  # Claude Code instructions
├── index.html                 # Main landing page
├── LICENSE
├── MIGRATION_GUIDE.md         # Migration guide
├── PROJECT_STRUCTURE.md       # This file
├── README.md                  # Project README
└── requirements.txt           # Python dependencies
```

## 🔍 Key Directories

### `/docs/`
All project documentation lives here for GitHub Pages hosting:
- **architecture/**: System design and mesh network docs
- **guides/**: How-to guides and tutorials
- **setup/**: Installation and configuration docs
- **assets/**: Images, diagrams, and other media

### `/archive/`
Legacy code that's no longer actively used:
- **tanchat/**: Original FastAPI chat server (deprecated)
- **tanchat-node/**: Node.js chat interface (deprecated)
- **oldtanchatfiles/**: Early experiments

### `/src/` (Future)
Will contain the new chat system and other active code.

### `/tailscale/`
Mesh network management scripts and Tailscale integration.

## 📝 Migration Completed

✅ **Completed Steps:**
1. Moved all documentation to `/docs/` for GitHub Pages
2. Archived all tanchat-related folders to `/archive/`
3. Updated all internal links to reflect new structure
4. Consolidated assets in proper locations
5. Cleaned up root directory

## 🚧 Remaining Cleanup

1. **Consolidate duplicate assets**: `/lab_photos/` duplicates `/assets/`
2. **Move node-specific files**: "node 02" folder could be better organized
3. **Clean up root HTML files**: Some HTML files remain in root

## 🚀 Future Structure

As the project grows:
- `/src/tangnet-core/` - Core AI inference engine
- `/src/tangnet-api/` - New API server
- `/src/tangnet-ui/` - Web interface
- `/deploy/` - Deployment scripts and configs
- `/tests/` - Test suites

## 🎯 Benefits Achieved

1. **Clean root directory**: Most files organized into subdirectories
2. **GitHub Pages ready**: `/docs` folder properly structured
3. **Clear separation**: Archived code separated from active development
4. **Scalable structure**: Ready for project growth
5. **Easy navigation**: Logical organization of all components