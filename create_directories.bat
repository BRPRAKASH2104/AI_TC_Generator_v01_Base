# Create prompt management directory structure
# Run this from your Auto_Generate root directory

# Create main directories
mkdir -p prompts/templates
mkdir -p prompts/config
mkdir -p prompts/examples
mkdir -p prompts/tools
mkdir -p prompts/examples/sample_outputs

# Create placeholder files to ensure git tracking
echo "# Prompt Templates Directory" > prompts/templates/README.md
echo "# Prompt Configuration Directory" > prompts/config/README.md
echo "# Prompt Examples and Documentation" > prompts/examples/README.md
echo "# Prompt Management Tools" > prompts/tools/README.md

# Create .gitkeep files for empty subdirectories
touch prompts/examples/sample_outputs/.gitkeep

echo "✅ Directory structure created successfully!"
echo "📁 Created:"
echo "   prompts/templates/"
echo "   prompts/config/"
echo "   prompts/examples/"
echo "   prompts/tools/"
echo "   prompts/examples/sample_outputs/"